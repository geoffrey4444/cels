# Distributed under the MIT License.
# See LICENSE for details.
from CosmicExplorerLocationSearch import Detector
from CosmicExplorerLocationSearch import Score
from CosmicExplorerLocationSearch.TestHelpers import *
import numpy as np
from pyproj import CRS
import random
import rasterio as rio
import tempfile


def test_pixel_data_from_rasters():
    # Make a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # Make temporary geotiffs
    rasters = {
        "elevation": temp_path + "/elevation.tif",
        "landcover": temp_path + "/landcover.tif"
    }
    profile = None
    bounds = None

    # Make a 40km x 40km raster in New Mexico, with 1km pixels (so 40x40 pixels)
    bounds = rio.coords.BoundingBox(left=-1113460.0,
                                    bottom=1071639.0,
                                    right=-1073460.0,
                                    top=1111639.0)
    width = 40
    height = 40
    profile = {
        "driver":
        "GTiff",
        "dtype":
        np.float64,
        "nodata":
        32767.0,
        "width":
        width,
        "height":
        height,
        "count":
        1,
        "crs":
        CRS.from_epsg(5070),
        "transform":
        rio.transform.from_bounds(bounds.left, bounds.bottom, bounds.right,
                                  bounds.top, width, height)
    }
    random_raster_data = {
        "elevation": random_geotiff(rasters["elevation"], profile),
        "landcover": random_geotiff(rasters["landcover"], profile)
    }

    # Place a detector in a corner of the raster, aligned with the pixels,
    # and make sure the detector pixel data agrees
    x_pixel_size = profile["transform"][0]
    y_pixel_size = -1.0 * profile["transform"][4]
    detector_width = 4
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

    # Verify that the same answer is NOT obtained with an L just over
    # the boundary (because each sample point crossed into a different pixel)
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
        51: 0,  # dwarf scrub
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
    # Check that the score, factoring out dl_for_arms_meters and a
    # constant 1e-5, is just the sum of the scores for each type

    # via https://stackoverflow.com/questions/16992713
    # /translate-every-element-in-numpy-array-according-to-key
    # map each landcover code into a score. Here compute the sum
    # differently.
    expected_score = np.sum(
        np.vectorize(Score.landcover_score_by_type.get)(landcover_pix_data))
    expected_score *= 1.e-5 * dl_for_arm_meters
    eps = 1.e-7
    assert np.abs(score - expected_score) < eps

    # If the scores are all one type, then verify that they such scores
    # are related by the same constant
    for landcover_score in Score.landcover_score_by_type.keys():
        uniform_pix = np.ones(number_of_pixels) * landcover_score
        uniform_score = Score.landcover_score(uniform_pix, dl_for_arm_meters)
        assert np.abs(uniform_score * 1e5 / dl_for_arm_meters -
                      number_of_pixels *
                      Score.landcover_score_by_type[landcover_score]) < eps
