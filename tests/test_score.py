# Distributed under the MIT License.
# See LICENSE for details.
import numpy as np
import random
import rasterio as rio
import tempfile
from pyproj import CRS

from CosmicExplorerLocationSearch import Detector, Geotiff, Score
from CosmicExplorerLocationSearch.TestHelpers import *


def test_pixel_data_from_rasters():
    # Make a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # Make temporary geotiffs
    rasters = {
        "elevation": temp_path + "/elevation.tif",
        "landcover": temp_path + "/landcover.tif",
        "land_acquisition": temp_path + "/land_acquisition.tif"
    }
    shapefiles = {"roads": temp_path + "/roads.shp"}
    profile = None
    bounds = None

    # Make a 40km x 40km raster in New Mexico, with 1km pixels (so 40x40 pixels)
    width = 40
    profile, bounds = profile_for_random_geotiff(width)
    random_raster_data = {
        "elevation": random_geotiff(rasters["elevation"], profile),
        "landcover": random_geotiff(rasters["landcover"], profile),
        "land_acquisition": random_geotiff(rasters["land_acquisition"], profile)
    }
    # Random shapefile for a 40km x 40km area in New Mexico
    random_shapefile_data = {
        "roads": random_roads_shapefile(shapefiles["roads"], bounds)
    }

    # Place a detector in a corner of the raster, aligned with the pixels,
    # and make sure the detector pixel data agrees
    x_pixel_size = profile["transform"][0]
    y_pixel_size = -1.0 * profile["transform"][4]
    detector_width = 18
    arm_length = x_pixel_size * detector_width
    dl_for_arm_length = x_pixel_size
    # The following vertex coordinates place the detector overlapping the
    # pixels in the bottom-left corner. Adding half a pixel width places
    # the detector in the pixel centers. Note: if the L is on a pixel
    # boundary, the pixel to the right or below is used.
    vertex_x = bounds.left + 0.5 * x_pixel_size
    vertex_y = bounds.bottom + 0.5 * y_pixel_size
    bottom_left_detector = Detector.detector(arm_length, dl_for_arm_length,
                                             90.0, 0.0, vertex_x, vertex_y)
    bottom_left_pix_data = Score.pixel_data_from_rasters(
        rasters, bottom_left_detector)
    for raster in rasters:
        # Check that pixel data has expected shape
        assert bottom_left_pix_data[raster]["coords"].shape == (
            2 * detector_width + 1, 2)
        assert bottom_left_pix_data[raster]["values"].shape == (
            2 * detector_width + 1, )
        # Check that the pixel data agrees with the bottom-left corner
        # raster data
        expected_pix_data = np.concatenate(
            (random_raster_data[raster][-1][:detector_width + 1][::-1],
             random_raster_data[raster][:, 0][::-1][1:detector_width + 1]))

        eps = 1.e-11
        assert np.all(
            np.abs(bottom_left_detector["arms_xy"] -
                   bottom_left_pix_data[raster]["coords"]) < eps)
        assert np.all(
            np.abs(expected_pix_data -
                   bottom_left_pix_data[raster]["values"]) < eps)

    # Verify that the same answer is obtained with an L just near
    # the boundary
    arm_almost_next_pixel_factor = 1. - 1.e-8
    vertex_x = bounds.left + arm_almost_next_pixel_factor * x_pixel_size
    vertex_y = bounds.bottom + arm_almost_next_pixel_factor * y_pixel_size
    detector_nearxy = Detector.detector(arm_length, dl_for_arm_length, 90.0,
                                        0.0, vertex_x, vertex_y)
    near_xy_pix_data = Score.pixel_data_from_rasters(rasters, detector_nearxy)
    for raster in rasters:
        assert np.all(
            np.abs(bottom_left_pix_data[raster]["values"] -
                   near_xy_pix_data[raster]["values"]) < eps)

    # Verify that the same answer is NOT obtained with an L just near
    # the boundary
    arm_next_pixel_factor = 1. + 1.e-8
    vertex_x = bounds.left + arm_next_pixel_factor * x_pixel_size
    detector_offset_x = Detector.detector(arm_length, dl_for_arm_length, 90.0,
                                          0.0, vertex_x, vertex_y)
    offset_x_pix_data = Score.pixel_data_from_rasters(rasters,
                                                      detector_offset_x)
    for raster in rasters:
        assert np.all(
            np.abs(bottom_left_pix_data[raster]["values"] -
                   offset_x_pix_data[raster]["values"]) > eps)
    arm_next_pixel_factor = 1. + 1.e-8
    vertex_x = bounds.left + arm_almost_next_pixel_factor * x_pixel_size
    vertex_y = bounds.bottom + arm_next_pixel_factor * y_pixel_size
    detector_offset_y = Detector.detector(arm_length, dl_for_arm_length, 90.0,
                                          0.0, vertex_x, vertex_y)
    offset_y_pix_data = Score.pixel_data_from_rasters(rasters,
                                                      detector_offset_y)
    for raster in rasters:
        assert np.all(
            np.abs(bottom_left_pix_data[raster]["values"] -
                   offset_x_pix_data[raster]["values"]) > eps)


def test_landcover_score_by_type():
    # This test is just meant to pass unless landcover_score_by_type dict is
    # changed. This is just to ensure than any changes are intended and not
    # accidental.
    expected_landcover_score_by_type = {
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
    for key in expected_landcover_score_by_type:
        assert Score.landcover_score_by_type[
            key] == expected_landcover_score_by_type[key]


def test_landcover_labels():
    # This test is just meant to pass unless landcover_score_by_type dict is
    # changed. This is just to ensure than any changes are intended and not
    # accidental.
    expected_landcover_labels = {
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
    for key in expected_landcover_labels:
        assert Score.landcover_labels[key] == expected_landcover_labels[key]


def test_earth_radius_meters():
    # This test just ensures that the correct value is not changed
    # accidentally
    assert Score.earth_radius_meters == 6378100


def test_landcover_score():
    # First, generate random landcover pixel data
    arm_pixel_length = np.random.randint(
        len(Score.landcover_labels) * 10,
        len(Score.landcover_labels) * 20)
    number_of_pixels = 2 * arm_pixel_length + 1
    # Possible pixel values
    possible_landcover_scores = []
    for score in Score.landcover_score_by_type.keys():
        possible_landcover_scores.append(score)
    random_number_generator = np.random.default_rng()
    landcover_pix_data = random_number_generator.choice(
        np.array(possible_landcover_scores), number_of_pixels)
    dl_for_arm_meters = np.random.random() * 150.0 + 50.0
    score = Score.landcover_score(landcover_pix_data, dl_for_arm_meters)
    # Check that the score (factoring out dl_for_arms_meters, a
    # constant 1e-6 that converts from dollars to millions of dollars, 
    # arms_footprint_width_meters and dividing by meters_squared_per_acre)
    # is the is just the sum of the scores for each type.
    
    # Width of the Cosmic Explorer site footprint (300ft, from CE-G2300054) in meters.
    # Hardcoded here. 
    arms_footprint_width_meters = 91.44

    # Conversion of acres to meters squared, 1 acre = 4046.86 m^2. Hardcoded here. 
    meters_squared_per_acre = 4046.86

    # Score scale factor (to go from cost in $1M USD to landcover cost value)
    landcover_score_scale = 1.e-6 * dl_for_arm_meters * arms_footprint_width_meters / meters_squared_per_acre
    
    # via https://stackoverflow.com/questions/16992713
    # /translate-every-element-in-numpy-array-according-to-key
    # map each landcover code into a score. Here compute the sum
    # differently.
    # score is output of Score.landcover_score with units of $1M USD. 
    # expected_score starts out in units of $1 USD/acre and we rescale it by landcover_score_scale 
    # which takes dollars/acre and multiplies by 1e-6 * m^2 / (m^2 / acre) to get millions of dollars. 
    # So score and expected score have the same units (millions of dollars), which means eps is in units 
    # of millions of dollars. an eps of 1e-6 million dollars = $1.
    expected_score = np.sum(
        np.vectorize(Score.landcover_score_by_type.get)(landcover_pix_data))
    expected_score *= landcover_score_scale
    eps = 1.e-4 # check score == expected to within $100
    assert np.abs(score - expected_score) < eps

    # If the scores are all one type, then verify that such scores
    # are related by the same constant
    for landcover_score in Score.landcover_score_by_type.keys():
        uniform_pix = np.ones(number_of_pixels) * landcover_score
        uniform_score = Score.landcover_score(uniform_pix, dl_for_arm_meters)
        assert np.abs(uniform_score / landcover_score_scale -
                      number_of_pixels *
                      Score.landcover_score_by_type[landcover_score]) < eps



def test_land_acquisition_score():
    arm_pixel_length = np.random.randint(200, 400)
    number_of_pixels = 2 * arm_pixel_length + 1
    dl_for_arm_meters = np.random.random() * 150.0 + 50.0
    land_acquisition_pix_data = np.random.uniform(0, 1e6, number_of_pixels)
    land_acquisition_score = Score.land_acquisition_score(land_acquisition_pix_data, dl_for_arm_meters)
    # Check that the score (factoring out dl_for_arms_meters, a
    # constant 1e-6 that converts from dollars to millions of dollars, 
    # arms_footprint_width_meters and dividing by meters_squared_per_acre)
    # is the is just the sum of the scores for each type.
    
    # Width of the Cosmic Explorer site footprint (300ft, from CE-G2300054) in meters.
    # Hardcoded here. 
    arms_footprint_width_meters = 91.44

    # Conversion of acres to meters squared, 1 acre = 4046.86 m^2. Hardcoded here. 
    meters_squared_per_acre = 4046.86

    # Score scale factor (to go from cost in $1M USD to landcover cost value)
    land_acquisition_score_scale = 1.e-6 * dl_for_arm_meters * arms_footprint_width_meters / meters_squared_per_acre
    
    # via https://stackoverflow.com/questions/16992713
    # /translate-every-element-in-numpy-array-according-to-key
    # map each landcover code into a score. Here compute the sum
    # differently.
    # score is output of Score.land_acquisition_score with units of $1M USD. 
    # expected_score starts out in units of $1 USD/acre and we rescale it by land_acquisition_score_scale 
    # which takes dollars/acre and multiplies by 1e-6 * m^2 / (m^2 / acre) to get millions of dollars. 
    # So score and expected score have the same units (millions of dollars), which means eps is in units 
    # of millions of dollars. an eps of 1e-6 million dollars = $1.
    expected_score = np.sum(land_acquisition_pix_data)
    expected_score *= land_acquisition_score_scale
    eps = 1.e-4 # check score == expected to within $100
    assert np.abs(land_acquisition_score - expected_score) < eps


def test_ideal_beamtube_depth_meters():
    random_detector_properties = random_detector()
    detector = random_detector_properties[-1]
    arm_length_meters = random_detector_properties[2]
    dl_for_arms = random_detector_properties[3]

    ideal_depth = Score.ideal_beamtube_depth_meters(detector)
    eps = 1.e-10
    # Average value along x arm should vanish
    assert np.abs(np.average(ideal_depth[:detector["vertex_pixel"] + 1])) < eps

    # Average value along y arm should also nearly vanish
    assert np.abs(np.average(ideal_depth[detector["vertex_pixel"]:])) < eps

    # Minimum depth would be zero if the average were not removed, so add the
    # minimum to recover the height from the average-removed depth
    height = ideal_depth - np.min(ideal_depth)

    # Check that we recover the cos part of the formula
    # Make sure roundoff error doesn't cause an extra term in dist_from_vertex
    # by adding or subtracting a small value from the stop values
    eps_limits = 1.e-10
    dist_from_vertex = detector["distance_from_vertex_meters"]
    vertex_pixel = detector["vertex_pixel"]
    phi_expected = dist_from_vertex - np.average(
        dist_from_vertex[:vertex_pixel + 1])
    phi_expected /= Score.earth_radius_meters

    # Angles should be small, so Taylor approx should work well for 1-cos(phi)
    one_minus_cos_phi_expected = 0.5 * np.square(phi_expected)

    one_minus_cos_phi = height / Score.earth_radius_meters
    # Check that 1-cos(phi) agrees with the expected value within 0.01%
    eps_cos_check = np.max(np.abs(one_minus_cos_phi)) * 1.e-4
    assert np.max(np.abs(one_minus_cos_phi -
                         one_minus_cos_phi_expected)) < eps_cos_check


def test_func_to_minimize_by_tilting_detector_plane():
    random_detector_properties = random_detector()
    detector = random_detector_properties[-1]

    elevation = np.random.uniform(100.0,
                                  1000.0,
                                  size=(detector["arms_xy"].shape[0], ))
    elevation_average_removed = elevation - np.average(elevation)

    eps = 1.e-10

    # Check that putting in zero for the three parameters gives
    # -elevation_average_removed
    func_given_zeros = Score.func_to_minimize_by_tilting_detector_plane(
        (0.0, 0.0, 0.0), detector, elevation_average_removed)
    assert np.max(np.abs(func_given_zeros + elevation_average_removed)) < eps

    # Check that vertex height simply offsets the elevation term
    tilt_x = np.random.uniform(-1.0, 1.0)
    tilt_y = np.random.uniform(-1.0, 1.0)
    vertex_height = np.random.uniform(0.0, 100.0)
    func_given_height_tiltxy = Score.func_to_minimize_by_tilting_detector_plane(
        (tilt_x, tilt_y, vertex_height), detector, elevation_average_removed)
    func_given_tiltxy = Score.func_to_minimize_by_tilting_detector_plane(
        (tilt_x, tilt_y, 0.0), detector, elevation_average_removed)
    assert np.max(
        np.abs(func_given_height_tiltxy - func_given_tiltxy -
               vertex_height)) < eps

    # Check tilt terms are proportional to the tilt along each arm.
    # To only check tilt terms, pass in zero vertex_height and zero elevation
    test_tilts = Score.func_to_minimize_by_tilting_detector_plane(
        (tilt_x, tilt_y, 0.0), detector,
        np.zeros_like(elevation_average_removed))
    assert np.max(
        np.abs(
            np.concatenate((test_tilts[:detector["vertex_pixel"] + 1] / tilt_x,
                            test_tilts[detector["vertex_pixel"] + 1:] /
                            tilt_y)) -
            detector["distance_from_vertex_meters"])) < eps


def test_depth_and_tilt():
    # Make a detector with one arm in the x direction and one arm in the y
    # direction
    random_detector_properties = random_detector()
    detector = Detector.detector(random_detector_properties[2],
                                 random_detector_properties[3], 90.0, 0.0,
                                 random_detector_properties[0],
                                 random_detector_properties[1])

    # Check that ideal elevation gives zero tilt
    eps_ideal_depth_meters = 1.0
    eps_ideal_tilt = 1.e-3
    depth_and_tilt_ideal = Score.depth_and_tilt(
        detector, Score.ideal_beamtube_depth_meters(detector))
    assert np.abs(depth_and_tilt_ideal["x_tilt"]) < eps_ideal_tilt
    assert np.abs(depth_and_tilt_ideal["y_tilt"]) < eps_ideal_tilt
    assert np.abs(
        depth_and_tilt_ideal["vertex_height"]) < eps_ideal_depth_meters
    # Check if depth never exceeds 1 meter when elevation is ideal
    assert np.max(np.abs(
        depth_and_tilt_ideal["depth"])) < eps_ideal_depth_meters

    # Make elevation with constant slopes in x and y direction,
    # on top of the ideal elevation,
    # and check that the the tilts recovered are correct
    tilt_x_expected = np.random.uniform(-1.0, 1.0)
    tilt_y_expected = np.random.uniform(-1.0, 1.0)
    elevation_x_arm = np.array(
        np.flip([
            tilt_x_expected * random_detector_properties[3] * i
            for i, _ in enumerate(detector["distance_from_vertex_meters"]
                                  [:detector["vertex_pixel"] + 1])
        ]))
    elevation_y_arm = np.array(
        np.array([
            tilt_y_expected * random_detector_properties[3] * i
            for i, _ in enumerate(detector["distance_from_vertex_meters"]
                                  [detector["vertex_pixel"] + 1:])
        ]))
    elevation = np.concatenate((elevation_x_arm, elevation_y_arm))
    elevation_shift = np.random.uniform(-100.0, 100.0)
    elevation += elevation_shift
    elevation += Score.ideal_beamtube_depth_meters(detector)
    vertex_height_expected = elevation[detector["vertex_pixel"]] - np.average(
        elevation)
    depth_and_tilt = Score.depth_and_tilt(detector, elevation)
    eps_recovered_tilt = 1.e-2
    assert np.abs(depth_and_tilt["x_tilt"] -
                  tilt_x_expected) < eps_recovered_tilt
    assert np.abs(depth_and_tilt["y_tilt"] -
                  tilt_y_expected) < eps_recovered_tilt

    # Check also that, within 10%, the fit recovered the average-removed
    # vertex height, unless the expected vertex height is smaller than 2km; in
    # that case, just require the vertex height to be recovered within 300.0 m.
    # This tolerance could likely be tightened with a better fit.
    eps_vertex_height = 0.1
    if vertex_height_expected > 2000.0:  #meters
        assert np.abs(
            (vertex_height_expected - depth_and_tilt["vertex_height"]) /
            vertex_height_expected) < eps_vertex_height
    else:
        assert np.abs(vertex_height_expected -
                      depth_and_tilt["vertex_height"]) < 300.0


def test_elevation_and_tilt_score():
    random_detector_properties = random_detector()
    detector = random_detector_properties[-1]

    # Test that digging cost for ideal elevation is small
    ideal_elevation = Score.ideal_beamtube_depth_meters(detector)
    ideal_scores = Score.elevation_and_tilt_score(
        detector, Score.ideal_beamtube_depth_meters(detector))
    # CE-T2000016-v2 explains the elevation score has nominal units of $1M USD
    # Here, check that for an ideal elevation, the elevation score is
    # less than 5 (nominal cost < $5M USD). In v4, with a berm/trench
    # width of 4 m, this nominal cost was taken to be $2M USD; here we have
    # increased the threshold to reflect the increase in volume from changing
    # the width to w = 18 m. In practice, the best sites found in a national 
    # search for 40-km, 90-degree-opening-angle detectors had scores O(10). 
    # The score could likely be smaller here with a better fit; this threshold is
    # chosen empirically based on how well the current fit can recover zero cost.
    assert np.abs(ideal_scores["elevation"]) < 5
    # Check for ideal elevation that the tilt score is negligible
    assert np.abs(ideal_scores["tilt"]) < 1.e-2

    # Here just test that the formulas for elevation and tilt scores
    # have not changed, using random elevation data that starts with
    # ideal elevation and then adds random noise and significant tilt
    tilt_x_expected = np.random.uniform(-0.1, -1.0)
    tilt_y_expected = np.random.uniform(0.1, 1.0)
    tilt_elevation_x_arm = np.array(
        np.flip([
            tilt_x_expected * random_detector_properties[3] * i
            for i, _ in enumerate(detector["distance_from_vertex_meters"]
                                  [:detector["vertex_pixel"] + 1])
        ]))
    tilt_elevation_y_arm = np.array(
        np.array([
            tilt_y_expected * random_detector_properties[3] * i
            for i, _ in enumerate(detector["distance_from_vertex_meters"]
                                  [detector["vertex_pixel"] + 1:])
        ]))
    tilt_elevation = np.concatenate(
        (tilt_elevation_x_arm, tilt_elevation_y_arm))
    const_height_offset = np.random.uniform(low=-100.0, high=100.0)
    elevation = ideal_elevation + tilt_elevation + np.random.uniform(
        low=-30.0, high=30.0, size=ideal_elevation.shape) + const_height_offset

    scores = Score.elevation_and_tilt_score(detector, elevation)
    depth_and_tilt = Score.depth_and_tilt(detector, elevation)
    tilt_0 = 0.5 * detector["arm_length_meters"] / Score.earth_radius_meters
    tilt_score_expected = (depth_and_tilt["x_tilt"]**2 +
                           depth_and_tilt["y_tilt"]**2) * 10.0 / (tilt_0**2)

    cut_fill_volume = depth_and_tilt["depth"] * (
        np.abs(depth_and_tilt["depth"]) + 18.0) * detector["dl_for_arms_meters"]
    cut_fill_volume[cut_fill_volume < -500.0 *
                    detector["dl_for_arms_meters"]] = -500.0 * detector[
                        "dl_for_arms_meters"]
    elevation_score_expected = (np.abs(np.sum(cut_fill_volume)) +
                                np.sum(np.abs(cut_fill_volume))) * 1.0e-5

    eps_depth_tilt_score = 1.e-8
    assert np.abs(scores["tilt"] - tilt_score_expected) < eps_depth_tilt_score
    assert np.abs(scores["elevation"] -
                  elevation_score_expected) < eps_depth_tilt_score

    # Also check that these scores are actually much worse than the ideal case
    assert np.abs(scores["elevation"] > 10.0)
    assert np.abs(scores["tilt"] > 10)

    # Verify that the minimum volume (i.e., max cut volume)
    eps_for_max_cut = 1.e-10  # to allow for some roundoff error
    assert scores["max_cut_vol_meters^3"] >= scores[
        "expected_max_cut_vol_meters^3"] * detector[
            "dl_for_arms_meters"] - eps_for_max_cut


def test_suitability_scores():
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # generate random geotiffs for elevation, landcover
    rasters = {
        "elevation": temp_path + "/elevation.tif",
        "landcover": temp_path + "/landcover.tif",
        "land_acquisition": temp_path + "/land_acquisition.tif"
    }
    shapefiles = {
        "roads": temp_path + "/roads.shp"
    }
    
    width = 40  # pixels
    profile, bounds = profile_for_random_geotiff(width)
    no_data_value = profile["nodata"]
    random_raster_data = {
        "elevation":
        random_elevation_geotiff_with_width(rasters["elevation"], width),
        "landcover":
        random_landcover_geotiff_with_width(rasters["landcover"], width),
        "land_acquisition":
        random_land_acquisition_geotiff_with_width(rasters["land_acquisition"], width)
    }
    random_shapefile_data = {
        "roads": random_roads_shapefile(shapefiles["roads"], bounds)
    }

    # generate random detector inside sample image
    min_length = 1000.0
    max_length = 2000.0
    random_center = [
        np.random.uniform(bounds.left + 1.1 * max_length,
                          bounds.right - 1.1 * max_length),
        np.random.uniform(bounds.bottom + 1.1 * max_length,
                          bounds.top - 1.1 * max_length)
    ]
    random_detector_properties = random_detector(length_bounds=(min_length,
                                                                max_length),
                                                 center=random_center)
    detector = random_detector_properties[-1]
    pix_data = Score.pixel_data_from_rasters(rasters, detector)

    scores = Score.suitability_scores(rasters, shapefiles, no_data_value, detector, True)

    eps_pix_data = 1.e-12
    assert scores['total_score_m_lacq'] == scores["elevation_score"] + scores[
        "tilt_score"] + scores["landcover_score"] + scores["roads_score"]
    assert scores['total_score'] == scores["elevation_score"] + scores[
        "tilt_score"] + scores["landcover_score"] + scores[
        "land_acquisition_score"] + scores["roads_score"]
    for key in scores["pixel_data"]:
        assert np.max(
            np.abs(scores["pixel_data"][key]["values"] -
                   pix_data[key]["values"])) < eps_pix_data
        assert np.max(
            np.abs(scores["pixel_data"][key]["coords"] -
                   pix_data[key]["coords"])) < eps_pix_data

    # Check that no pixel data returned when not requested
    scores_no_pix = Score.suitability_scores(rasters, shapefiles, no_data_value, detector,
                                             False)
    assert "pixel_data" not in scores_no_pix.keys()

    # Check that individual scores are computed from the correct functions
    assert scores_no_pix["elevation_score"] == Score.elevation_and_tilt_score(
        detector, pix_data["elevation"]["values"])["elevation"]
    assert scores_no_pix["tilt_score"] == Score.elevation_and_tilt_score(
        detector, pix_data["elevation"]["values"])["tilt"]
    assert scores_no_pix["landcover_score"] == Score.landcover_score(
        pix_data["landcover"]["values"], detector["dl_for_arms_meters"])
    assert scores_no_pix["land_acquisition_score"] == Score.land_acquisition_score(
        pix_data["land_acquisition"]["values"], detector["dl_for_arms_meters"])

    # Check that no_data_value is returned if a landcover pixel data
    # has a value to be omitted
    # generate random geotiffs for elevation, landcover where all
    # landcover pixels are drawn from values to be omitted.
    rasters_check_omitted_values = {
        "elevation": temp_path + "/elevation.tif",
        "landcover": temp_path + "/landcover_only_values_to_omit.tif",
        "land_acquisition": temp_path + "/land_acquisition.tif"
    }

    width = 40  # pixels
    profile, bounds = profile_for_random_geotiff(width)
    no_data_value = profile["nodata"]
    random_landcover_geotiff_with_width(
        rasters_check_omitted_values["landcover"], width, False)
    scores_check_omitted_values = Score.suitability_scores(
        rasters_check_omitted_values, shapefiles, no_data_value, detector, False)
    for key in scores_check_omitted_values:
        # Scores return no_data * a big number (1e9), so that these scores
        # are never best for a given corner station location unless
        # no rotation tried for a corner station location have well-defined
        # scores (as would happen e.g. if the vertex was in a no-data region)
        assert scores_check_omitted_values[key] == no_data_value * 1000000000

    # Finally, check that score_detector_from_grid() is just a wrapper
    # for suitability_scores() that also returns inputs
    arm_length_meters = random_detector_properties[2]
    dl_for_arms_meters = random_detector_properties[3]
    opening_angle_degrees = random_detector_properties[4]
    rotation_angle_degrees = random_detector_properties[5]
    vertex_x = random_detector_properties[0]
    vertex_y = random_detector_properties[1]
    opening_angle_i = np.random.randint(100, 500)
    rotation_angle_j = np.random.randint(100, 500)
    vertex_row = np.random.randint(100, 500)
    vertex_col = np.random.randint(100, 500)

    result = Score.score_detector_from_grid(
        rasters,
        shapefiles,
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
    )

    assert result["arm_length_meters"] == arm_length_meters
    assert result["dl_for_arms_meters"] == dl_for_arms_meters
    assert result["opening_angle_degrees"] == opening_angle_degrees
    assert result["rotation_angle_degrees"] == rotation_angle_degrees
    assert result["vertex_x"] == vertex_x
    assert result["vertex_y"] == vertex_y
    assert result["opening_angle_i"] == opening_angle_i
    assert result["rotation_angle_j"] == rotation_angle_j
    assert result["vertex_row"] == vertex_row
    assert result["vertex_col"] == vertex_col
    for key in scores.keys():
        if key == "pixel_data":
            continue  # score_detector_from_grid() does not return pixel data
        if key == "crossings_data":
            continue  # score_detector_from_grid() does not roads crossings data
        assert result[key] == scores[key]


def worker_process_shared_memory(shm_name, transform, nodata_value, detector,
                                 shape, dtype):
    """Worker function for testing shared memory access."""
    try:
        from CosmicExplorerLocationSearch import Score
        result = Score.pixel_data_from_shared_memory(shm_name, transform,
                                                     nodata_value, detector,
                                                     shape, dtype)
        return result
    except Exception as e:
        return {"error": str(e)}


def test_pixel_data_from_shared_memory():
    """Test pixel_data_from_shared_memory function with multiprocessing."""
    import tempfile
    import os
    from concurrent.futures import ProcessPoolExecutor
    from CosmicExplorerLocationSearch import Geotiff, Detector

    # Create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # Convert test images to BSQ files
    elevation_bsq = os.path.join(temp_path, "elevation.bsq")
    landcover_bsq = os.path.join(temp_path, "landcover.bsq")
    land_acquisition_bsq = os.path.join(temp_path, "land_acquisition.bsq")

    elevation_tif = "tests/test_images/SouthNM_Elevation_1km.tif"
    landcover_tif = "tests/test_images/SouthNM_Landcover_1km.tif"
    land_acquisition_tif = "tests/test_images/SouthNM_LandAcquisition_1km.tif"

    # Convert geotiffs to BSQ format
    Geotiff.geotiff_to_bsq(elevation_tif, elevation_bsq)
    Geotiff.geotiff_to_bsq(landcover_tif, landcover_bsq)
    Geotiff.geotiff_to_bsq(land_acquisition_tif, land_acquisition_bsq)

    # Get expected results using pixel_data_from_rasters
    raster_file_dict = {"elevation": elevation_tif, "landcover": landcover_tif,
                        "land_acquisition": land_acquisition_tif}

    # Get raster bounds for landcover
    with rio.open(landcover_tif) as src:
        bounds = src.bounds
        center_x = (bounds.left + bounds.right) / 2.0
        center_y = (bounds.bottom + bounds.top) / 2.0

    # Create a detector for testing
    detector = Detector.detector(arm_length_meters=1000.0,
                                 dl_for_arms_meters=100.0,
                                 opening_angle_degrees=90.0,
                                 rotation_angle_degrees=0.0,
                                 vertex_x=center_x,
                                 vertex_y=center_y)

    expected_results = Score.pixel_data_from_rasters(raster_file_dict,
                                                     detector)

    # Read BSQ files into shared memory
    elevation_shm_info = Geotiff.read_bsq_to_shared_memory(elevation_bsq)
    landcover_shm_info = Geotiff.read_bsq_to_shared_memory(landcover_bsq)
    land_acquisition_shm_info = Geotiff.read_bsq_to_shared_memory(land_acquisition_bsq)

    # Test with 4 processes accessing shared memory
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Submit tasks for elevation data
        elevation_futures = []
        for i in range(4):
            future = executor.submit(worker_process_shared_memory,
                                     elevation_shm_info['shared_data_name'],
                                     elevation_shm_info['affine_transform'],
                                     elevation_shm_info['nodata_value'],
                                     detector, elevation_shm_info['shape'],
                                     elevation_shm_info['dtype'])
            elevation_futures.append(future)

        # Submit tasks for landcover data
        landcover_futures = []
        for i in range(4):
            future = executor.submit(worker_process_shared_memory,
                                     landcover_shm_info['shared_data_name'],
                                     landcover_shm_info['affine_transform'],
                                     landcover_shm_info['nodata_value'],
                                     detector, landcover_shm_info['shape'],
                                     landcover_shm_info['dtype'])
            landcover_futures.append(future)
        
        # Submit tasks for land acquisition data
        land_acquisition_futures = []
        for i in range(4):
            future = executor.submit(worker_process_shared_memory,
                                     land_acquisition_shm_info['shared_data_name'],
                                     land_acquisition_shm_info['affine_transform'],
                                     land_acquisition_shm_info['nodata_value'],
                                     detector, land_acquisition_shm_info['shape'],
                                     land_acquisition_shm_info['dtype'])
            land_acquisition_futures.append(future)

        # Collect results
        elevation_results = [future.result() for future in elevation_futures]
        landcover_results = [future.result() for future in landcover_futures]
        land_acquisition_results = [future.result() for future in land_acquisition_futures]

    # Verify that all processes returned the same results as expected
    eps = 1e-12

    for i, result in enumerate(elevation_results):
        if "error" in result:
            raise AssertionError(f"Process {i} failed: {result['error']}")

        # Get the pixel indices that the shared memory method actually used
        xs = detector['arms_xy'][:, 0]
        ys = detector['arms_xy'][:, 1]
        rows, cols = rio.transform.rowcol(
            elevation_shm_info['affine_transform'], xs, ys)

        # Read the elevation raster and get the values at those exact pixel indices
        with rio.open(elevation_tif) as src:
            array = src.read(1)
            expected_values = []
            for row, col in zip(rows, cols):
                if 0 <= row < array.shape[0] and 0 <= col < array.shape[1]:
                    expected_values.append(array[row, col])
                else:
                    expected_values.append(src.nodata)

        # Compare the shared memory values with the expected values at the same pixel indices
        assert np.array_equal(
            result["values"], expected_values
        ), f"Elevation values don't match expected values at the same pixel indices"
        assert np.allclose(result["coords"],
                           expected_results["elevation"]["coords"],
                           rtol=eps)

    for i, result in enumerate(landcover_results):
        if "error" in result:
            raise AssertionError(f"Process {i} failed: {result['error']}")

        # Get the pixel indices that the shared memory method actually used
        xs = detector['arms_xy'][:, 0]
        ys = detector['arms_xy'][:, 1]
        rows, cols = rio.transform.rowcol(
            landcover_shm_info['affine_transform'], xs, ys)

        # Read the landcover raster and get the values at those exact pixel indices
        with rio.open(landcover_tif) as src:
            array = src.read(1)
            expected_values = []
            for row, col in zip(rows, cols):
                if 0 <= row < array.shape[0] and 0 <= col < array.shape[1]:
                    expected_values.append(array[row, col])
                else:
                    expected_values.append(src.nodata)

        # Compare the shared memory values with the expected values at the same pixel indices
        assert np.array_equal(
            result["values"], expected_values
        ), f"Landcover values don't match expected values at the same pixel indices"
        assert np.allclose(result["coords"],
                           expected_results["landcover"]["coords"],
                           rtol=eps)

    for i, result in enumerate(land_acquisition_results):
        if "error" in result:
            raise AssertionError(f"Process {i} failed: {result['error']}")

        # Get the pixel indices that the shared memory method actually used
        xs = detector['arms_xy'][:, 0]
        ys = detector['arms_xy'][:, 1]
        rows, cols = rio.transform.rowcol(
            land_acquisition_shm_info['affine_transform'], xs, ys)

        # Read the land acquisition raster and get the values at those exact pixel indices
        with rio.open(land_acquisition_tif) as src:
            array = src.read(1)
            expected_values = []
            for row, col in zip(rows, cols):
                if 0 <= row < array.shape[0] and 0 <= col < array.shape[1]:
                    expected_values.append(array[row, col])
                else:
                    expected_values.append(src.nodata)

        # Compare the shared memory values with the expected values at the same pixel indices
        assert np.array_equal(
            result["values"], expected_values
        ), f"Land acquisition values don't match expected values at the same pixel indices"
        assert np.allclose(result["coords"],
                           expected_results["land_acquisition"]["coords"],
                           rtol=eps)

    # Clean up shared memory
    try:
        import multiprocessing.shared_memory as shared_memory
        shm_elevation = shared_memory.SharedMemory(
            name=elevation_shm_info['shared_data_name'])
        shm_elevation.close()
        shm_elevation.unlink()

        shm_landcover = shared_memory.SharedMemory(
            name=landcover_shm_info['shared_data_name'])
        shm_landcover.close()
        shm_landcover.unlink()

        shm_land_acquisition = shared_memory.SharedMemory(
            name=land_acquisition_shm_info['shared_data_name'])
        shm_land_acquisition.close()
        shm_land_acquisition.unlink()
    except Exception as e:
        print(f"Warning: Could not clean up shared memory: {e}")

    # Clean up temporary directory
    temp_dir.cleanup()
