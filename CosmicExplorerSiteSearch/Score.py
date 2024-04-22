# Distributed under the MIT License.
# See LICENSE for details.
import numpy as np
import rasterio as rio
from scipy import optimize
from scipy.optimize import leastsq as leastsq

from CosmicExplorerSiteSearch import Detector

global_raster_paths = {}
global_raster_data = {}
global_raster_transform = None
global_raster_profile = None
global_raster_bounds = None
global_raster_wkt = None
global_no_sample = False
global_no_data = None


def init_global_data(raster_paths, no_sample):
    """
    Inputs:
        raster_file_dict: dictionary of raster file paths
    Outputs: None
    Note: stores raster data in Score.global_raster_paths, 
    Score.global_raster_data, Score.global_raster_transforms,
    Score.global_raster_profiles, and Score.global_raster_bounds.
    """
    global global_raster_paths
    global global_raster_data
    global global_raster_transform
    global global_raster_profile
    global global_raster_bounds
    global global_raster_wkt
    global global_no_sample
    global global_no_data
    global_raster_paths = raster_paths
    global_no_sample = no_sample
    with rio.open(global_raster_paths["elevation"]) as geofile:
        global_no_data = geofile.profile["nodata"]
        global_raster_wkt = geofile.crs.wkt
        global_raster_bounds = geofile.bounds
        global_raster_transform = geofile.transform
        global_raster_profile = geofile.profile
    if global_no_sample == True:
        for key in global_raster_paths.keys():
            with rio.open(global_raster_paths[key]) as raster_file:
                global_raster_data[key] = raster_file.read()


def pixel_data_from_raster_files(raster_file_dict, detector):
    """Inputs:
         raster_file_dict: dictionary of raster file paths
         detector: output of Detector.detector()

       Returns: 
         A dictionary keyed by the keys in raster_file_dict. Under each
         key is a dictionary containing the following:
           * "coords" = x,y coords of points along detector arms
           * "values" = value at x,y from this raster
       Note: this function reads pixel data directly from files on disk.
       To create pixel data for many detectors, using pixel_data() instead
       could lead to better performance.
    """
    result = {}
    for raster in raster_file_dict:
        result[raster] = {
            "coords": detector["arms"]["arms_xy"],
            "values": np.array([]),
        }
        with rio.open(raster_file_dict[raster]) as raster_file:
            result[raster]["values"] = np.array([
                sample[0]
                for sample in raster_file.sample(result[raster]["coords"])
            ])
    return result


def pixel_data(detector):
    """Inputs:         
         detector: output of Detector.detector()

       Returns: 
         A dictionary keyed by the keys in raster_file_dict. Under each
         key is a dictionary containing the following:
           * "coords" = x,y coords of points along detector arms
           * "values" = value at x,y from this raster
       Note: This file computes pixel data for a detector from raster data
       stored in memory. This approach is suitable for getting pixel data
       repeatedly for many detectors. To just get pixel data for one or 
       a few detectors, use pixel_data_from_raster_files().
       Before calling this function, call init_global_data().
    """
    global global_raster_data
    global global_raster_transforms
    result = {}
    for raster in global_raster_paths.keys():
        result[raster] = {
            "coords": detector["arms"]["arms_xy"],
            "values": np.array([]),
        }
        rows_and_cols = rio.transform.rowcol(global_raster_transforms[raster],
                                             detector["arms"]["arms_x"],
                                             detector["arms"]["arms_y"])
        result[raster]["values"] = global_raster_data[raster][0][rows_and_cols]
    return result


landcover_score_by_type = {
    0: 1e4,  # ocean
    11: 1e4,  # open water
    12: 1e4,  # perennial ice/snow
    21: 100,  # developed, open space
    22: 300,  # developed, low intensity
    23: 1e4,  # developed, medium intensity
    24: 1e4,  # developed, high intensity
    31: 0,  # barren land (rock/sand/clay)
    41: 20,  # deciduous forest
    42: 20,  # evergreen forest
    43: 20,  # mixed forest
    51: 0,  # swarf scrub
    52: 5,  # shrub/scrub
    71: 0,  # grassland/herbaceous
    72: 0,  # sedge/herbaceous
    73: 0,  # lichens
    74: 0,  # moss
    81: 20,  # pasture/hay
    82: 100,  # cultivated crops
    90: 1e4,  # woody wetlands
    95: 1e4,  # emergent herbaceous wetlands
    101: 1e4,  # Canada
    102: 1e4,  # Mexico
    103: 1e4  # Cuba
}

landcover_labels = {
    0: "ocean",
    11: "open water",
    12: "perennial ice/snow",
    21: "developed, open space",
    22: "developed, low intensity",
    23: "developed, medium intensity",
    24: "developed, high intensity",
    31: "barren land (rock/sand/clay)",
    41: "deciduous forest",
    42: "evergreen forest",
    43: "mixed forest",
    51: "swarf scrub",
    52: "shrub/scrub",
    71: "grassland/herbaceous",
    72: "sedge/herbaceous",
    73: "lichens",
    74: "moss",
    81: "pasture/hay",
    82: "cultivated crops",
    90: "woody wetlands",
    95: "emergent herbaceous wetlands",
    101: "Canada",
    102: "Mexico",
    103: "Cuba",
}

# Earth nominal equatorial radius via https://arxiv.org/pdf/1510.07674.pdf
# Hardcoded here instead of adding astropy as a dependency
earth_radius_meters = 6378100


def landcover_score(landcover_pixel_data, dl_for_arms_meters):
    """Input: landcover_pixel_data: 1D array of landcover pixel data, e.g. 
    output from pixel_data()

    Output: Total landcover score obtained by summing result of passing the 
    value at each pixel into the Score.landcover_score_by_type dict.
    """
    # Just sum over the landcover scores set above for all pixels,
    # and multiply the result by some normalization, so this is comparable
    # to other scores (here the normalization is 1e-5)
    return np.sum(
        np.array([
            landcover_score_by_type[v] * dl_for_arms_meters
            for v in landcover_pixel_data
        ])) * 1e-5


def ideal_beamtube_depth(detector):
    """Input: detectort (output from Detector.detector())
       Output: depth (+ cut, - fill) of elevation of straight beamtube
    """
    arm_length_meters = detector["arms"]["arm_length_meters"]
    dl_for_arms_meters = detector["arms"]["dl_for_arms_meters"]
    dist_from_vertex_x = np.arange(arm_length_meters, -dl_for_arms_meters,
                                   -dl_for_arms_meters)
    dist_from_vertex_y = np.arange(dl_for_arms_meters,
                                   arm_length_meters + dl_for_arms_meters,
                                   dl_for_arms_meters)
    dist_from_vertex = np.concatenate((dist_from_vertex_x, dist_from_vertex_y))
    dist_from_vertex_average = np.average(dist_from_vertex_x)

    # If arm is balanced in the middle on the sphere of earth radius,
    # find the angle (using sin theta ~ theta approx.) phi between
    #  i) line from center of earth to center of arm, and
    # ii) line from center of earth to point on arm some distance from
    #     the vertex
    phi = (dist_from_vertex - dist_from_vertex_average) / earth_radius_meters

    # Using phi, find the height each point on the arms is above ground,
    # if Earth were perfect sphere of radius Earth radius
    height = earth_radius_meters * (1.0 - np.cos(phi))

    # Remove the average height from the height, so in the middle,
    # the arm is below ground, and near the edges, arm is above ground.
    # This is the depth.
    depth = height - np.average(height[:dist_from_vertex_x.shape[0] + 1])
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
                                            pixel_data() except with
                                            the average of that output
                                            subtracted out. Do that subtraction
                                            first because this function gets
                                            called many times.

    Output:
      func_to_minimize: a function to minimize by adjusting the tilt of each
                        arm and the height of the vertex
                        
    """
    x_tilt, y_tilt, vertex_height_meters = params

    arm_length_meters = detector["arms"]["arm_length_meters"]
    dl_for_arms_meters = detector["arms"]["dl_for_arms_meters"]

    # Set up array in order xend, ..., vertex, ... yend with distances
    # from vertex
    dist_from_vertex_x = np.arange(arm_length_meters, -dl_for_arms_meters,
                                   -dl_for_arms_meters)
    dist_from_vertex_y = np.arange(dl_for_arms_meters,
                                   arm_length_meters + dl_for_arms_meters,
                                   dl_for_arms_meters)

    # Func to minimize = x_tilt * dist_from_vertex_x_arm
    #                  + y_tilt + dist_from_vertex_y_arm
    #                  + vertex_height - (elevation - elevation_average)
    func_to_minimize = np.concatenate((dist_from_vertex_x, dist_from_vertex_y))
    func_to_minimize[:dist_from_vertex_x.shape[0]] *= x_tilt
    func_to_minimize[dist_from_vertex_x.shape[0]:] *= y_tilt
    func_to_minimize += vertex_height_meters
    func_to_minimize -= elevation_pixel_data_average_removed
    return func_to_minimize


def depth_and_tilt(detector, elevation_pixel_data):
    """
    Input:
      detector: output of Detector.detector()
      elevation_pixel_data: 1D array of elevation pixel data, e.g. the output of
                            pixel_data()

    Output:
      Dict containing the following:
        "depth": pixel data for depth (+ for cut, - for fill) along arms
        "x_tilt": tilt of x arm (dimensionless)
        "y_tilt": tilt of y arm (dimensionless)
        "vertex_height_meters": vertex height in meters
    """
    elevation_pixel_data_average_removed = elevation_pixel_data - np.average(
        elevation_pixel_data)
    tilt_fit_results = leastsq(
        func_to_minimize_by_tilting_detector_plane, [0, 0, 0],
        (detector, elevation_pixel_data_average_removed))
    tilt_params_solution = (tilt_fit_results[0][0], tilt_fit_results[0][1],
                            tilt_fit_results[0][2])
    depth = func_to_minimize_by_tilting_detector_plane(
        tilt_params_solution, detector, elevation_pixel_data_average_removed)
    depth += ideal_beamtube_depth(detector)
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
                              output of pixel_data()

      Output: Dict containing 2 floats, "elevation_score" and "tilt_score".
              Computes the elevation and tilt scores using Eqs. (4) and (3) of
              CE-T2000016-v2.
      Note: because both scores rely on the output of Score.depth_and_tilt(),
            this function computes both scores together
    """
    depth_tilt = depth_and_tilt(detector, elevation_pixel_data)
    depth = depth_tilt["depth"]

    # Compute the elevation score

    # The angle of repose is hard-coded here as 45 degrees, following
    # CE-T2000016-v2, which explains that this is a conservative estimate.
    # The angle of repose is the slope of the sides of a trench or berm.
    cot_angle_of_repose = 1.0 / np.tan(45 * np.pi / 180.0)
    width_meters = 4.0

    # Eq. (2) of CE-T2000016-v2: A=V/l = h*(w + h*cot(theta_repose))
    # Note that we take abs(h) in the cot term, because we don't want the
    # sign in the overall factor of h to cancel for that term. The sign
    # of height h tells you if this volume is cut or fill.
    # Derive this formula by calculating the area of the central rectangle and
    # then the area of the two triangular side parts.
    dirt_area = depth * (np.abs(depth) * cot_angle_of_repose + width_meters)

    # The detector is represented as a set of evenly spaced locations; the
    # spacing is provided in the detector dictionary.
    dl_for_arms_meters = detector["arms"]["dl_for_arms_meters"]

    # To turn the cross-sectional area into a volume, multiply each detector
    # point's cross-sectional area by the spacing between points. This
    # will effectively add one extra spacing, e.g. one extra meter of digging
    # over 40km or 20km, so this should not significantly affect the
    # suitability score based on the dirt volume.
    dirt_volume = dirt_area * dl_for_arms_meters

    # Following CE-T2000016-v2, cap the amount of dirt cut because we will
    # then switch to tunnelling. But until we have a tunneling score
    # included here, maybe this cap should be removed? For the best sites,
    # this shouldn't matter, because if elevation score is maxed out too often,
    # then this is probably not an area of interest?
    # The cap is 5e5 m^3 / km = 500 m^3 / m, assuming dl_for_arms_meters = 1.0.
    # The negative sign is because this is a limit on excavation, not on
    # the size of a berm.
    max_dirt_meters_cubed_per_meter = -500.0
    dirt_volume[
        dirt_volume <
        max_dirt_meters_cubed_per_meter] = max_dirt_meters_cubed_per_meter

    # The elevation score is based on CE-T2000016-v2 Eq. (3), which
    # (with a suitable normalization) is (cut + fill) + abs(cut - fill)
    # The first term can be found by summing abs(dir_volume), since
    # dirt_volume has a + sign for cut and - sign for fill; the abs makes
    # both signs +. This term penalizes moving dirt around, since that is
    # will cost money. The term abs(cut - fill) is just the abs of the sum of
    # dirt_volume and penalizes having either too much cut (that must be
    # hauled away) or fill (that must be hauled in).
    cut_fill_excess = np.abs(np.sum(dirt_volume))
    cut_fill_total = np.sum(np.abs(dirt_volume))

    # CE-T2000016-v2 sets the normalization by dividing the volume by
    # 10^5 m^3. It's unclear where this normalization comes from. It primarily
    # affects the relative importance of elevation score to other scores.
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
    tilt_0 = 0.5 * detector["arms"]["arm_length_meters"] / earth_radius_meters
    tilt_score = 10.0 * (np.square(x_tilt / tilt_0) +
                         np.square(y_tilt / tilt_0))

    result = {}
    result["elevation"] = elevation_score
    result["tilt"] = tilt_score
    return result


def suitability_scores(detector, include_pixel_data):
    """
    Input:
      detector: output of Detector.detector()
      include_pixel_data: if true, add a key to the returned scores
                          dictionary holding the pixel_data (e.g. for plotting)
    Output:
      scores: dictionary of suitability scores, including "total" which is the 
              sum of the other scores in the dictionary
    Note: This file uses pixel data for a detector from raster data
       stored in memory. This approach is suitable for getting pixel data
       repeatedly for many detectors. To just get pixel data for one or 
       a few detectors, use pixel_data_from_raster_files().
       Before calling this function, call init_global_data().
    """
    global global_no_data
    global global_no_sample
    global global_raster_profiles
    pix_data = None
    if (global_no_sample == True):
        pix_data = pixel_data(detector)
    else:
        pix_data = pixel_data_from_raster_files(global_raster_paths, detector)
    # If L contains pixels in ocean (0) or other country (101-103), assign
    # nodata to scores and return
    if ((0 in pix_data["landcover"]["values"])
            # or (11 in pix_data["landcover"]["values"])
            or (101 in pix_data["landcover"]["values"])
            or (102 in pix_data["landcover"]["values"])
            or (103 in pix_data["landcover"]["values"])):
        return {
            "elevation_score": global_no_data,
            "tilt_score": global_no_data,
            "landcover_score": global_no_data,
            "total_score": global_no_data
        }

    elevation_tilt_scores = elevation_and_tilt_score(
        detector, pix_data["elevation"]["values"])
    elevation_score = elevation_tilt_scores["elevation"]
    tilt_score = elevation_tilt_scores["tilt"]
    landcover = landcover_score(pix_data["landcover"]["values"],
                                detector["arms"]["dl_for_arms_meters"])
    total_score = elevation_score + tilt_score + landcover
    if include_pixel_data:
        return {
            "elevation_score": elevation_score,
            "tilt_score": tilt_score,
            "landcover_score": landcover,
            "total_score": total_score,
            "pixel_data": pix_data
        }
    else:
        return {
            "elevation_score": elevation_score,
            "tilt_score": tilt_score,
            "landcover_score": landcover,
            "total_score": total_score
        }


def score_detector_from_grid(
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
):
    """
    Score one detector from a 2D array of detector vertex locations. Note: 
    this function is meant to be called asynchronously.
    Input:
      arm_length_meters: detector arm length (meters)
      dl_for_arms_meters: distance between sample points (meters)
      opening_angle_degrees: detector opening angle (degrees)
      rotation_angle_degrees: rotation (degrees) of detector vs. proj x-y axes
      vertex_
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
    scores = suitability_scores(detector, False)
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
        "total_score": scores["total_score"]
    }
    return result


def score_detector_from_grid_row(arm_length_meters, dl_for_arms_meters,
                                 opening_angle_degrees, rotation_angle_degrees,
                                 vertex_y, opening_angle_i, rotation_angle_j,
                                 vertex_row, number_of_cols, detector_xmin,
                                 detector_xmax, detector_spacing):
    """For details, see score_detector_from_grid(). Loop over colums in
    a row of the detector grid, evaluating the row in serial.
    Note: list of vertex_x values stored globally, to avoid serializing/sending
    large amounts of data.
    """
    detector_xs = np.arange(detector_xmin, detector_xmax + detector_spacing,
                            detector_spacing)
    scores_this_row = [{}] * number_of_cols
    for col in range(0, number_of_cols, 1):
        scores_this_row[col] = score_detector_from_grid(
            arm_length_meters, dl_for_arms_meters, opening_angle_degrees,
            rotation_angle_degrees, detector_xs[col], vertex_y,
            opening_angle_i, rotation_angle_j, vertex_row, col)
    return scores_this_row
