# Distributed under the MIT License.
# See LICENSE for details.
import numpy as np
import rasterio as rio
import geopandas as gpd
from scipy import optimize
from scipy.optimize import least_squares as least_squares

from CosmicExplorerLocationSearch import Detector, Geotiff


def pixel_data_from_rasters(raster_file_dict, detector):
    """Inputs:
         raster_file_dict: dictionary of raster file paths
         detector: output of Detector.detector()

       Returns: 
         A dictionary keyed by the keys in raster_file_dict. Under each
         key is a dictionary containing the following:
           * "coords" = x,y coords of points along detector arms
           * "values" = value at x,y from this raster
       Note: this function reads pixel data directly from files on disk,
       which reduces memory use but might strain the filesystem.
    """
    result = {}
    for raster in raster_file_dict:
        result[raster] = {
            "coords": detector["arms_xy"],
            "values": np.array([]),
        }
        with rio.open(raster_file_dict[raster]) as raster_file:
            result[raster]["values"] = np.array([
                sample[0]
                for sample in raster_file.sample(result[raster]["coords"])
            ])
    return result


def pixel_data_from_shared_memory(shm_name, transform, nodata_value, detector,
                                  shape, dtype):
    """Inputs:
         shm_name: name of the shared memory region containing raster data
         transform: rasterio affine transform for the raster
         nodata_value: value used to represent no data in the raster
         detector: output of Detector.detector()
         shape: tuple of (height, width) for the raster
         dtype: numpy data type of the raster data

       Returns: 
         A dictionary containing the following:
           * "coords" = x,y coords of points along detector arms
           * "values" = value at x,y from this raster
       Note: this function reads pixel data from shared memory,
       which allows multiple processes to access the same data efficiently.
    """
    # Get the shared memory array
    array, shm = Geotiff.get_shared_memory_array(shm_name, shape, dtype)

    # Sample the data using the coordinates from the detector
    values = Geotiff.sample_from_array(array, transform, nodata_value,
                                       detector["arms_xy"])

    # Clean up the shared memory connection
    shm.close()

    return {
        "coords": detector["arms_xy"],
        "values": np.array(values),
    }


# The landcover "type" includes descriptions and codes follow the 
# National Land Cover DatabaseLand Cover Classification Legend, available at
# https://www.mrlc.gov/sites/default/files/NLCDclasses.pdf
# The codes for Ocean Water (0) and Non-U.S. land (101, 102, 103) conform to
# the USGS 100-Meter Resolution Land Cover of the Conterminous
# United States, 2001 geotiff, available at
# https://geodata.mit.edu/catalog/stanford-wv372bn9329.
# The "score" given here for each landcover type is a cost in units of US dollars per acre.
# These costs represent rough (one significant digit) estimates for clearing land 
# with that type of landcover to "brown field" conditions (or in the case of open water 
# or ocean, building a bridge). 
# Note that effects such costs varying by region and economies of scale 
# (clearing 100 acres is less than 100 times as expensive as clearing one acre) are not 
# currently taken into account. Note also that land acquisition costs will be costed 
# separately in a future merge request. 
# Some references for acre clearing/bridge costs include: 
# [1] https://www.fixr.com/costs/land-clearing-and-building-site-preparation
# [2] https://www.danieldean.com/how-much-does-it-cost-to-clear-land-in-2025/
# [3] https://georgehardscaping.com/commercial-snow-removal-pricing-calculator/
# [4] https://deltademolitioncontractor.com/blog/how-much-does-it-cost-to-remove-a-parking-lot/  
# [5] https://www.wsdot.wa.gov/eesc/bridge/WBES/2017/Session8/8A3-Saindon.pdf
# When these cost values are are changed, test_landcover_score_by_type() in test_score.py 
# must also change.
landcover_score_by_type = {
    0: 7e6,  # ocean; Bridge costs ([5], example 4) $150/ft^2 * 43,560 ft^2/acre=$6,534,000.
    11: 7e6,  # open water; Bridge costs ([5], example 4) $150/ft^2 * 43,560 ft^2/acre=$6,534,000.
    12: 4e2,  # perennial ice/snow; Commercial snow/ice removal up tp $400 per acre per application [3].
    21: 6e3,  # developed, open space; Sparse demolition (0.1*$1/ft^2=$4,356/acre [4]) plus clearing ($2,000/acre [2]).
    22: 2e4,  # developed, low intensity; Low demolition (0.2*$2/ft^2=$17,424/acre [4]) plus clearing ($2,000/acre [2]).
    23: 5e4,  # developed, medium intensity; Medium demolition (0.3*$3/ft^2=$43,560/acre [4]) plus clearing ($2,000/acre [2]).
    24: 2e5,  # developed, high intensity; High demolition (1.0*$4/ft^2=$174,240/acre [4]) plus clearing ($2,000/acre [2]).
    31: 1e3,  # barren land (rock/sand/clay); Clearing ($1,200/acre [1,2]). 
    41: 6e3,  # deciduous forest; Forest clearing rough average. Clearing ($6,000/acre [1,2]).
    42: 6e3,  # evergreen forest; Forest clearing rough average. Clearing ($6,000/acre [1,2]).
    43: 6e3,  # mixed forest; Forest clearing rough average. Clearing ($6,000/acre [1,2]).
    51: 2e3,  # dwarf scrub; Between barren land and forest [1,2].
    52: 3e3,  # shrub/scrub; Between barren land and forest, but more vegetation [1,2].
    71: 1e3,  # grassland/herbaceous; Clearing ($1,200/acre [1,2]).
    72: 1e3,  # sedge/herbaceous; Clearing ($1,200/acre [1,2]).
    73: 1e3,  # lichens; Clearing ($1,200/acre [1,2]).
    74: 1e3,  # moss; Clearing ($1,200/acre [1,2]).
    81: 1e3,  # pasture/hay; Clearing ($1,200/acre [1,2]).
    82: 1e3,  # cultivated crops; Clearing ($1,200/acre [1,2]).
    90: 8e3,  # woody wetlands; Higher than forest clearing costs, clearing regulations ($8,000/acre [2]).
    95: 8e3,  # emergent herbaceous wetlands; Higher than forest clearing costs, clearing regulations ($8,000/acre [2]).
    101: 1e8,  # Canada; Exclude, made up number, not considering these areas.
    102: 1e8,  # Mexico; Exclude, made up number, not considering these areas.
    103: 1e8  # Cuba; Exclude, made up number, not considering these areas.
}

# These descriptions and codes follow the National Land Cover DatabaseLand Cover
# Classification Legend, which is available at
# https://www.mrlc.gov/sites/default/files/NLCDclasses.pdf
# The codes for Ocean Water (0) and Non-U.S. land (101, 102, 103) conform to
# the USGS 100-Meter Resolution Land Cover of the Conterminous
# United States, 2001 geotiff, available at
# https://geodata.mit.edu/catalog/stanford-wv372bn9329.
landcover_labels = {
    0: "Ocean Water",
    11: "Open Water",
    12: "Perennial Ice/Snow",
    21: "Developed, Open Space",
    22: "Developed, Low Intensity",
    23: "Developed, Medium Intensity",
    24: "Developed, High Intensity",
    31: "Barren Land (Rock/Sand/Clay)",
    41: "Deciduous Forest",
    42: "Evergreen Forest",
    43: "Mixed Forest",
    51: "Dwarf Scrub",
    52: "Shrub/Scrub",
    71: "Grassland/Herbaceous",
    72: "Sedge/Herbaceous",
    73: "Lichens",
    74: "Moss",
    81: "Pasture/Hay",
    82: "Cultivated Crops",
    90: "Woody Wetlands",
    95: "Emergent Herbaceous Wetlands",
    101: "Canada",
    102: "Mexico",
    103: "Cuba",
}

# Earth nominal equatorial radius via https://arxiv.org/pdf/1510.07674.pdf
# Hardcoded here instead of adding astropy as a dependency
# If this is changed (e.g. to more precision), test_earth_radius_meters
# must also be updated
earth_radius_meters = 6378100

# Width of the Cosmic Explorer site footprint (300ft, from CE-G2300054) in meters.
# Hardcoded here. 
arms_footprint_width_meters = 91.44

# Conversion of acres to meters squared, 1 acre = 4046.86 m^2. Hardcoded here. 
meters_squared_per_acre = 4046.86

def landcover_score(landcover_pixel_data, dl_for_arms_meters):
    """Input: landcover_pixel_data: 1D array of landcover pixel data, e.g. 
    output from pixel_data_from_rasters()

    Output: Total landcover cost obtained by summing result of passing the 
    value at each pixel into the Score.landcover_score_by_type dict and 
    multiplying by number of acres and multiplying by 1e-6 to get cost in $1M USD.

    Note:
    Landcover pixel data should conform to the National
    Land Cover Database Class Legend, available at
    https://www.mrlc.gov/sites/default/files/NLCDclasses.pdf
      Pix value   Description
      0           Ocean Water
      11          Open Water
      12          Perennial Ice/Snow
      21          Developed, Open Space
      22          Developed, Low Intensity
      23          Developed, Medium Intensity
      24          Developed, High Intensity
      31          Barren Land (Rock/Sand/Clay)
      41          Deciduous Forest
      42          Evergreen Forest
      43          Mixed Forest
      51          Dwarf Scrub
      52          Shrub/Scrub
      71          Grasslands/Herbaceous
      72          Sedge/Herbaceous
      73          Lichens
      74          Moss
      81          Pasture/Hay
      82          Cultivated Crops
      90          Woody Wetlands
      95          Emergent Herbaceous Wetlands
      101 - 103   Non-U.S. Land
    """
    # Sum over the landcover cost (acre clearing cost in dollars, 
    # times number of acres) for each pixel in the arm
    # and multiply the result by 1e-6 to get an answer in $1M USD. 
    return np.sum(
        np.array([
            landcover_score_by_type[v] * dl_for_arms_meters * arms_footprint_width_meters / meters_squared_per_acre
            for v in landcover_pixel_data
        ])) * 1e-6


def land_acquisition_score(land_acquisition_pixel_data, dl_for_arms_meters):
    """Input: land_acquisition_pixel_data: 1D array of land acquisition pixel data, e.g. 
    output from pixel_data_from_rasters()

    Output: Total land acquisition cost
    """
    # Sum over the land acquisition cost (cost in dollars per acre, 
    # times number of acres) for each pixel in the arm
    # and multiply the result by 1e-6 to get an answer in $1M USD. 
    return np.sum(
        np.array([
            land_acquisition_pixel_data * dl_for_arms_meters * arms_footprint_width_meters / meters_squared_per_acre
            ])) * 1e-6


def ideal_beamtube_depth_meters(detector):
    """Input: detector (output from Detector.detector()).
       Output: depth (- cut, + fill) of straight beamtube in meters for the
       idealized situation of a perfectly spherical Earth.
       Imagine balancing the midpoint of each arm of the detector on a sphere
       of radius earth_radius_meters. This function calculates the height each
       point on the arm is above the spherical earth's surface:
       h = r_earth * (1 - cos(phi)), where phi (using the small angle
       approximation) is (d - d_average) / earth_radius_meters, where
       d = distance from vertex and d_average = average distance from vertex.
       Then, it returns h - h_average; subtract the average height for each
       point so that instead of just building a giant berm, you cut some
       places and fill others, reducing the volume of required or excess earth
       that must be brought to or taken from the location.
    """
    arm_length_meters = detector["arm_length_meters"]
    dl_for_arms_meters = detector["dl_for_arms_meters"]

    ## Get distance from vertex in a way that always has same
    ## size as detector
    dist_from_vertex = detector["distance_from_vertex_meters"]

    # The average distance from vertex will be half the arm length, and since
    # the arm lengths are equal, this distance applies to both arms.
    dist_from_vertex_average = np.average(
        dist_from_vertex[:detector["vertex_pixel"] + 1])

    # If arm is balanced in the middle on the sphere of earth radius,
    # find the angle (using sin theta ~ theta approx.) phi between
    #  i) line from center of earth to center of arm, and
    # ii) line from center of earth to point on arm some distance from
    #     the vertex
    phi = (dist_from_vertex - dist_from_vertex_average) / earth_radius_meters

    # Using phi, find the height each point on the arms is above ground,
    # if Earth were perfect sphere of radius earth_radius_meters
    height = earth_radius_meters * (1.0 - np.cos(phi))

    # Remove the average height from the height, so in the middle,
    # the arm is below ground, and near the edges, arm is above ground.
    # This is the depth.
    # Note: averaging over the x arm means averaging from pixel 0 through
    # the pixel closest to the vertex, which is pixel ivertex. The + 1 is
    # because y[:n] returns 0 <= i < n.
    depth = height - np.average(height[:detector["vertex_pixel"] + 1])

    return depth


def func_to_minimize_by_tilting_detector_plane(
        params, detector, elevation_pixel_data_average_removed):
    """
    Input:
      params: tuple of 3 floats:
        x_tilt: tilt of x arm (dimensionless, meters / meter)
        y_tilt: tilt of y arm (dimensionless, meters / meter)
        vertex_height_meters: vertex height
      detector: output of Detector.detector()
      elevation_pixel_data_average_removed: 1D array of elevation pixel data,
                                            e.g. the output of
                                            pixel_data_from_rasters() except
                                            with the average of that output
                                            subtracted out. Do that subtraction
                                            first because this function gets
                                            called many times.

    Output:
      func_to_minimize: a function to minimize by adjusting the tilt of each
                        arm and the height of the vertex
    Minimizing this function fits the detector tilt and vertex height to
    the provided elevation data.
    """
    x_tilt, y_tilt, vertex_height_meters = params

    ## Get distance from vertex
    dist_from_vertex = detector["distance_from_vertex_meters"]

    # Func to minimize = x_tilt * dist_from_vertex_x_arm
    #                  + y_tilt * dist_from_vertex_y_arm
    #                  + vertex_height - (elevation - elevation_average)
    # Start with a copy of dist_from_vertex
    func_to_minimize = np.array(dist_from_vertex)
    func_to_minimize[:detector["vertex_pixel"] + 1] *= x_tilt
    func_to_minimize[detector["vertex_pixel"] + 1:] *= y_tilt
    func_to_minimize += vertex_height_meters
    func_to_minimize -= elevation_pixel_data_average_removed
    return func_to_minimize


def depth_and_tilt(detector, elevation_pixel_data):
    """
    Input:
      detector: output of Detector.detector()
      elevation_pixel_data: 1D array of elevation pixel data, e.g. the output of
                            pixel_data_from_rasters()

    Output:
      Dict containing the following:
        "depth": pixel data for depth (- for cut, + for fill) along arms
        "x_tilt": tilt of x arm (dimensionless)
        "y_tilt": tilt of y arm (dimensionless)
        "vertex_height_meters": vertex height in meters
    """
    elevation_pixel_data_average_removed = elevation_pixel_data - np.average(
        elevation_pixel_data)
    # TODO: investigate if the fit can be improved, e.g. by changing settings
    # or using a linear least squares fit instead
    tilt_fit_results = least_squares(
        func_to_minimize_by_tilting_detector_plane, [0, 0, 0],
        method='trf',
        verbose=0,
        args=(detector, elevation_pixel_data_average_removed))
    tilt_params_solution = tilt_fit_results.x

    depth = func_to_minimize_by_tilting_detector_plane(
        tilt_params_solution, detector, elevation_pixel_data_average_removed)
    depth += ideal_beamtube_depth_meters(detector)
    result = {}
    result["depth"] = depth
    result["x_tilt"] = tilt_params_solution[0]
    result["y_tilt"] = tilt_params_solution[1]
    result["vertex_height"] = tilt_params_solution[2]
    return result


def elevation_and_tilt_score(detector, elevation_pixel_data):
    """
      Input:
        detector: output of Detector.detector()
        elevation_pixel_data: 1D array of elevation pixel data, e.g. the 
                              output of pixel_data_from_rasters()

      Output: Dict containing 2 floats, "elevation_score" and "tilt_score".
              Computes the elevation and tilt scores using Eqs. (4) and (3) of
              CE-T2000016-v2.
      Note: because both scores rely on the output of Score.depth_and_tilt(),
            this function computes both scores together
    """
    depth_tilt = depth_and_tilt(detector, elevation_pixel_data)
    depth = depth_tilt["depth"]

    # Compute the elevation score
    # Estimated width of 18 m for trench/berm for the beamtube and two roads, 
    # based on the width for LHO and LLO (beamtube and one road) which is 15 m
    width_meters = 18.0

    # The angle of repose is hard-coded here as 45 degrees, following
    # CE-T2000016-v2, which explains that this is a conservative estimate.
    # The angle of repose is the slope of the sides of a trench or berm.
    # This turns out to mean cot_angle_of_repose == 1.0, because
    # tan(45 degrees) = 1.
    # As long as this is numerically 1, do not calculate it...
    # but if, in the future, other angles of repose are used, uncomment the
    # next two lines and comment the line after that

    # cot_angle_of_repose = 1.0 / np.tan(45 * np.pi / 180.0)
    # dirt_area = depth * (np.abs(depth) * cot_angle_of_repose + width_meters)
    dirt_area = depth * (np.abs(depth) + width_meters)

    # Eq. (2) of CE-T2000016-v2: A=V/l = h*(w + h*cot(theta_repose))
    # Note that we take abs(h) in the cot term, because we don't want the
    # sign in the overall factor of h to cancel for that term. The sign
    # of height h tells you if this volume is cut or fill.
    # Derive this formula by calculating the area of the central rectangle and
    # then the area of the two triangular side parts.

    # The detector is represented as a set of evenly spaced locations; the
    # spacing is provided in the detector dictionary.
    dl_for_arms_meters = detector["dl_for_arms_meters"]

    # To turn the cross-sectional area into a volume, multiply each detector
    # point's cross-sectional area by the spacing between points. This
    # will effectively add one extra spacing, e.g. one extra meter of digging
    # over 40km or 20km, so this should not significantly affect the
    # suitability score based on the dirt volume.
    dirt_volume = dirt_area * dl_for_arms_meters

    # CE-T2000016-v2 caps the amount of dirt cut, supposing that the cost
    # would switch to tunneling once the digging cost reaches the cost
    # to tunnel. The cap in CE-T2000016-v2 is 5e5 m^3 / km = 500 m^3 / m.
    # The negative sign is because this is a limit on excavation depth, not on
    # the height of a berm. Note that the area of the berm/trench is
    # depth * (|depth| + width), so a cap of 500.0 m^3/m corresponds to
    # a depth of d^2 + d w == 500, => d ~ 20 meters.
    max_dirt_meters_cubed_per_meter = -500.0
    dirt_volume[
        dirt_volume < max_dirt_meters_cubed_per_meter *
        dl_for_arms_meters] = max_dirt_meters_cubed_per_meter * dl_for_arms_meters

    # The elevation score is based on CE-T2000016-v2 Eq. (3), which
    # (with a suitable normalization) is (cut + fill) + abs(cut - fill)
    # The first term can be found by summing abs(dirt_volume), since
    # dirt_volume has a + sign for cut and - sign for fill; the abs makes
    # both signs +. This term penalizes moving dirt around, since that is
    # will cost money. The term abs(cut - fill) is just the abs of the sum of
    # dirt_volume and penalizes having either too much cut (that must be
    # hauled away) or fill (that must be hauled in).
    cut_fill_excess = np.abs(np.sum(dirt_volume))
    cut_fill_total = np.sum(np.abs(dirt_volume))

    # CE-T2000016-v2 sets the normalization by dividing the volume by
    # 10^5 m^3. This primarily affects the relative importance of elevation
    # score to other scores. The idea is to estimate the cost of moving
    # 1 m^3 of earth at $10, and then expressing the cost in units of $1M.
    # So the nominal dollar cost is (cut_fill_total + cut_fill_excess) / $10,
    # which in units of $1M is (cut_fill_total + cut_fill_excess) * 10 / 1e6
    # == (cut_fill_total + cut_fill_excess) * 1e-5.
    elevation_score = (cut_fill_total + cut_fill_excess) * 1.0e-5

    # Compute the tilt score
    x_tilt = depth_tilt["x_tilt"]
    y_tilt = depth_tilt["y_tilt"]

    # CE-T2000016-v2 has a tilt score penalizing tilt because it lowers
    # detector sensitivity. The score is
    #   10 * ((tilt_x/tilt_0)^2 + (tilt_y/tilt_0)^2)
    # I don't know where the 10 comes from; it sets the importance of this
    # score over other scores. The normalization
    # tilt_0 = 0.5 * arm_length_meters / earth_radius_meters
    # is meant to capture the minimum arm tilt because of Earth's curvature.
    tilt_0 = 0.5 * detector["arm_length_meters"] / earth_radius_meters
    tilt_score = 10.0 * (np.square(x_tilt / tilt_0) +
                         np.square(y_tilt / tilt_0))

    result = {}
    result["elevation"] = elevation_score
    result["tilt"] = tilt_score

    # For testing, also include the minimum dirt volume in the returned result,
    # i.e., the maximum cut volume in a pixel
    result["max_cut_vol_meters^3"] = np.min(dirt_volume)
    result["expected_max_cut_vol_meters^3"] = max_dirt_meters_cubed_per_meter
    return result



# These descriptions follow the RTTYP (Route Type Code) classification scheme,
# as defined by https://www.census.gov/library/reference/code-lists/route-type-codes.html


road_labels = {
    "C": "County",
    "I": "Interstate",
    "M": "Common Name",
    "O": "Other",
    "S": "State",
    "U": "US",
}


# Associated cost of roads per road type. These are uncalibrated for now,
# associating the highest cost to interstate highways. US highways are
# given the second highest cost. Other and Common Name roads
# can vary in size and usage and are given a score of 50. County and "other"
# roads are assigned a cost of 10. 

road_score_by_type = {
    "C": 10.0,
    "I": 100.0,
    "M":50.0,
    "O":10.0,
    "S":50.0,
    "U":75.0,
}


def roads_scores(roads_shapefile_path, detector):
    """
    Input:
        detector: output of Detector.detector()
        roads_shapefile_path: path to a shapefile containing roads information
    Output:
        result:
            *"crossings": A GeoDataFrame containing all crossing points with major
            US roads, the RTTYP road type, the full road name
            *"score_roads": A "roads" suitability score for this detector
    """
    roads = gpd.read_file(roads_shapefile_path).to_crs(5070)
    detector_df = gpd.GeoDataFrame(geometry=[Detector.detector_to_multiline_string(detector)], crs='EPSG:5070')
    crossings = gpd.overlay(roads, detector_df, how='intersection', keep_geom_type=False)
    score_roads = 0
    for c in crossings.itertuples():
        score_roads += road_score_by_type[c.RTTYP]
    result = {}
    result["crossings"] = crossings
    result["score_roads"] = score_roads
    return result




def suitability_scores(
        raster_paths,
        shapefiles_paths,
        no_data_value,
        detector,
        include_pixel_data,
        use_shared_memory=False,
        shared_memory_info=None):
    """
    Input:
      detector: output of Detector.detector()
      include_pixel_data: if true, add a key to the returned scores
                          dictionary holding the pixel_data (e.g. for plotting)
      use_shared_memory: if true, use shared memory for raster data
      shared_memory_info: dict containing shared memory metadata (required if use_shared_memory=True)
    Output:
      scores: dictionary of suitability scores, including "total" which is the 
              sum of the other scores in the dictionary
    Note: This file uses pixel data for a detector from raster data
       stored in memory. This approach is suitable for getting pixel data
       repeatedly for many detectors. To just get pixel data for one or 
       a few detectors, use pixel_data_from_raster_files().
    """
    if use_shared_memory:
        if shared_memory_info is None:
            raise ValueError("shared_memory_info must be provided when use_shared_memory=True")
        pix_data = {}
        for raster_type in ["elevation", "landcover", "land_acquisition"]:
            shm_info = shared_memory_info[raster_type]
            pix_data[raster_type] = pixel_data_from_shared_memory(
                shm_info["shared_data_name"],
                shm_info["affine_transform"],
                shm_info["nodata_value"],
                detector,
                shm_info["shape"],
                shm_info["dtype"]
            )
    else:
        pix_data = pixel_data_from_rasters(raster_paths, detector)
    # If L contains pixels in ocean (0) or other country (101-103), assign
    # nodata to scores and return
    if ((0 in pix_data["landcover"]["values"])
            # or (11 in pix_data["landcover"]["values"])
            or (101 in pix_data["landcover"]["values"]) or
        (102 in pix_data["landcover"]["values"]) or
        (103 in pix_data["landcover"]["values"]) or
        (no_data_value in pix_data["landcover"]["values"]) or
        (no_data_value in pix_data["elevation"]["values"]) or
        (no_data_value in pix_data["land_acquisition"]["values"])):
        factor_to_make_no_value_large = 1000000000
        return {
            # Take abs of no_data_value in case that value is negative
            "elevation_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "tilt_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "landcover_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "land_acquisition_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "roads_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "total_score_m_lacq": factor_to_make_no_value_large * np.abs(no_data_value),
            "total_score": factor_to_make_no_value_large * np.abs(no_data_value)
        }

    elevation_tilt_scores = elevation_and_tilt_score(
        detector, pix_data["elevation"]["values"])
    elevation_score = elevation_tilt_scores["elevation"]
    tilt_score = elevation_tilt_scores["tilt"]
    roads_path = shapefiles_paths["roads"]
    roads = roads_scores(roads_path, detector)
    roads_score = roads["score_roads"]
    roads_crossings_df = roads["crossings"]
    landcover = landcover_score(pix_data["landcover"]["values"],
                                detector["dl_for_arms_meters"])
    land_acquisition = land_acquisition_score(pix_data["land_acquisition"]["values"], 
                                              detector["dl_for_arms_meters"])
    total_score_m_lacq = elevation_score + tilt_score + landcover + roads_score
    total_score = elevation_score + tilt_score + landcover + land_acquisition + roads_score
    if include_pixel_data:
        return {
            "elevation_score": elevation_score,
            "tilt_score": tilt_score,
            "landcover_score": landcover,
            "land_acquisition_score": land_acquisition,
            "roads_score": roads_score,
            "total_score_m_lacq": total_score_m_lacq,
            "total_score": total_score,
            "pixel_data": pix_data,
            "crossings_data": roads_crossings_df
        }
    else:
        return {
            "elevation_score": elevation_score,
            "tilt_score": tilt_score,
            "landcover_score": landcover,
            "land_acquisition_score": land_acquisition,
            "roads_score": roads_score,
            "total_score_m_lacq": total_score_m_lacq,
            "total_score": total_score
        }


def score_detector_from_grid(
    raster_paths,
    shapefiles_paths,
    no_data_value,
    arm_length_meters,
    dl_for_arms_meters,
    opening_angle_degrees,
    rotation_angle_degrees,
    vertex_x,
    vertex_y,
    opening_angle_i,
    rotation_angle_j,
    vertex_row,
    vertex_col,
    use_shared_memory=False,
    shared_memory_info=None,
):
    """
    Score one detector from a 2D array of detector vertex locations. Note: 
    this function is meant to be called asynchronously.
    Input:
      raster_paths: dict containing paths to rasters keyed by "elevation",
                    "landcover" and "land_acquisition"
      shapefiles_paths: dict containing paths to vector files keyed by
                    "roads"
      no_data_value: integer used to represent no data in output rasters
      arm_length_meters: detector arm length (meters)
      dl_for_arms_meters: distance between sample points (meters)
      opening_angle_degrees: detector opening angle (degrees)
      rotation_angle_degrees: rotation (degrees) of detector vs. proj x-y axes
      vertex_x: vertex x coordinate (in units of x-y projection, assumed meters)
      vertex_y: vertex y coordinate (in units of x-y projection, assumed meters)
      opening_angle_i: which angle corresponds to opening_angle_degrees
      rotation_angle_j: which angle corresponds to rotation_angle_j
      vertex_row: row of a grid of vertex positions corresponding to vertex_y
      vertex_col: column of a grid of vertex positions corresponding to vertex_x      
    Note: opening_angle_i, rotation_angle_j, vertex_row, vertex_col are provided 
    only so they can be returned, so results can be assembled in to an array 
    asynchronously.

    Output:
      scores: dict containing all input parameters except raster_file_dict,
              as well as the scores returned by 
              suitability_scores(include_pixel_data=False).
    """
    detector = Detector.detector(arm_length_meters, dl_for_arms_meters,
                                 opening_angle_degrees, rotation_angle_degrees,
                                 vertex_x, vertex_y)
    try:
        scores = suitability_scores(raster_paths, shapefiles_paths, no_data_value, detector,
                                    False, use_shared_memory, shared_memory_info)
    except Exception as error:
        print("\nUnexpected error scoring detector:")
        print(error)

        # Return no data for this detector
        factor_to_make_no_value_large = 1000000000
        result = {
            "arm_length_meters": arm_length_meters,
            "dl_for_arms_meters": dl_for_arms_meters,
            "opening_angle_degrees": opening_angle_degrees,
            "rotation_angle_degrees": rotation_angle_degrees,
            "vertex_x": vertex_x,
            "vertex_y": vertex_y,
            "opening_angle_i": opening_angle_i,
            "rotation_angle_j": rotation_angle_j,
            "vertex_row": vertex_row,
            "vertex_col": vertex_col,
            "elevation_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "tilt_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "landcover_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "land_acquisition_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "roads_score": factor_to_make_no_value_large * np.abs(no_data_value),
            "total_score_m_lacq": factor_to_make_no_value_large * np.abs(no_data_value),
            "total_score": factor_to_make_no_value_large * np.abs(no_data_value)
        }
        print("Detector that failed:")
        print(result)
        print("continuing, reporting no data for this detector\n\n")
        return result

    result = {
        "arm_length_meters": arm_length_meters,
        "dl_for_arms_meters": dl_for_arms_meters,
        "opening_angle_degrees": opening_angle_degrees,
        "rotation_angle_degrees": rotation_angle_degrees,
        "vertex_x": vertex_x,
        "vertex_y": vertex_y,
        "opening_angle_i": opening_angle_i,
        "rotation_angle_j": rotation_angle_j,
        "vertex_row": vertex_row,
        "vertex_col": vertex_col,
        "elevation_score": scores["elevation_score"],
        "tilt_score": scores["tilt_score"],
        "landcover_score": scores["landcover_score"],
        "land_acquisition_score": scores["land_acquisition_score"],
        "roads_score": scores["roads_score"],
        "total_score_m_lacq": scores["total_score_m_lacq"],
        "total_score": scores["total_score"]
    }
    return result
