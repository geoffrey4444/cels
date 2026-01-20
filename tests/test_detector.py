# Distributed under the MIT License.
# See LICENSE for details.
from CosmicExplorerLocationSearch import Detector
from CosmicExplorerLocationSearch.TestHelpers import *
import fiona
import numpy as np
from pyproj import CRS, Transformer
import tempfile


def test_detector():
    random_detector_and_inputs = random_detector()
    vertex_x = random_detector_and_inputs[0]
    vertex_y = random_detector_and_inputs[1]
    arm_length_meters = random_detector_and_inputs[2]
    dl_for_arms_meters = random_detector_and_inputs[3]
    opening_angle_degrees = random_detector_and_inputs[4]
    rotation_angle_degrees = random_detector_and_inputs[5]
    detector = random_detector_and_inputs[6]

    # Check that the results that are supposed to be just the input parameters
    # actually are
    assert detector["vertex_x"] == vertex_x
    assert detector["vertex_y"] == vertex_y
    assert detector["arm_length_meters"] == arm_length_meters
    assert detector["dl_for_arms_meters"] == dl_for_arms_meters
    assert detector["opening_angle_degrees"] == opening_angle_degrees
    assert detector["rotation_angle_degrees"] == rotation_angle_degrees

    # Check that the arms have the correct number of points
    sample_points_per_arm = int(
        np.round(arm_length_meters / dl_for_arms_meters))
    number_of_sample_points = 1 + 2 * int(sample_points_per_arm)
    assert detector["arms_xy"].shape[1] == 2
    assert detector["arms_xy"].shape[0] == number_of_sample_points

    # For comparing floating point numbers, only demand agreement to some
    # epislon to account for rounding errors.
    eps = 1e-8

    # Check that the sample points on the arms are spaced as expected
    # to within eps.
    assert np.max(
        np.abs(
            np.abs(
                np.diff(
                    np.sqrt(
                        np.square(detector["arms_xy"][:, 0] - vertex_x) +
                        np.square(detector["arms_xy"][:, 1] - vertex_y)))) -
            dl_for_arms_meters)) < eps

    # Check that the points have the correct opening angle
    x_arm_points = detector["arms_xy"][:sample_points_per_arm, :]
    y_arm_points = detector["arms_xy"][sample_points_per_arm + 1:, :]
    x_arm_x_coords = x_arm_points[:, 0]
    x_arm_y_coords = x_arm_points[:, 1]
    y_arm_x_coords = y_arm_points[:, 0]
    y_arm_y_coords = y_arm_points[:, 1]
    x_arm_angle = np.arctan2(x_arm_y_coords - vertex_y,
                             x_arm_x_coords - vertex_x) * 180.0 / np.pi
    y_arm_angle = np.arctan2(y_arm_y_coords - vertex_y,
                             y_arm_x_coords - vertex_x) * 180.0 / np.pi

    # arctan2 returns angles from -180 to 180 degrees
    # Return an angle between 0 and 360 degrees instead
    x_arm_angle = x_arm_angle - 180.0 * (np.sign(x_arm_angle) - 1.0)
    y_arm_angle = y_arm_angle - 180.0 * (np.sign(y_arm_angle) - 1.0)

    if (rotation_angle_degrees + opening_angle_degrees) > 360.0:
        y_arm_angle += 360.0
    assert np.all(np.abs(x_arm_angle - rotation_angle_degrees) < eps)
    assert np.all(
        np.abs(y_arm_angle - opening_angle_degrees -
               rotation_angle_degrees) < eps)

    assert detector["scores"] == None

    # test case with scores provided
    scores = random_scores()

    # test that distance to vertex has min zero, max arm_length_meters, and
    # spacing dl_for_arms_meters. Also check distance from vertex of
    # vertex pixel is zero.
    dist_from_vertex = detector["distance_from_vertex_meters"]
    assert dist_from_vertex.shape[0] == detector["arms_xy"].shape[0]
    assert np.abs(np.min(dist_from_vertex)) < eps
    assert np.abs(np.max(dist_from_vertex) - arm_length_meters) < eps
    assert np.abs(np.min(np.diff(dist_from_vertex)) + dl_for_arms_meters) < eps
    assert np.abs(dist_from_vertex[detector["vertex_pixel"]]) < eps

    _, _, _, _, _, _, scores, detector_with_scores = random_detector(
        random_scores())
    assert detector_with_scores["scores"] == scores


def test_detector_from_points_xy():
    detector = random_plausible_detector(
        arm_length_meters=np.random.uniform(0.0, 1.0) * 1000.0 + 40000.0,
        vertex_x0=-704330 + np.random.uniform(-100.0, 100.0),
        vertex_y0=1188917 + np.random.uniform(-100.0, 100.0))
    # Check that detector_from_points_xy works no matter whether the X or Y
    # end station's (x,y) coordinates are given first. 50% chance of 
    # testing either choice each time this test is run.
    if np.random.rand() < 0.5:
        end1_x_meters = detector[
            "vertex_x"] + detector["arm_length_meters"] * np.cos(
                detector["rotation_angle_degrees"] * np.pi / 180.0)
        end1_y_meters = detector[
            "vertex_y"] + detector["arm_length_meters"] * np.sin(
                detector["rotation_angle_degrees"] * np.pi / 180.0)
        end2_x_meters = detector[
            "vertex_x"] + detector["arm_length_meters"] * np.cos(
                (detector["rotation_angle_degrees"] +
                 detector["opening_angle_degrees"]) * np.pi / 180.0)
        end2_y_meters = detector[
            "vertex_y"] + detector["arm_length_meters"] * np.sin(
                (detector["rotation_angle_degrees"] +
                 detector["opening_angle_degrees"]) * np.pi / 180.0)
    else:
        end2_x_meters = detector[
            "vertex_x"] + detector["arm_length_meters"] * np.cos(
                detector["rotation_angle_degrees"] * np.pi / 180.0)
        end2_y_meters = detector[
            "vertex_y"] + detector["arm_length_meters"] * np.sin(
                detector["rotation_angle_degrees"] * np.pi / 180.0)
        end1_x_meters = detector[
            "vertex_x"] + detector["arm_length_meters"] * np.cos(
                (detector["rotation_angle_degrees"] +
                 detector["opening_angle_degrees"]) * np.pi / 180.0)
        end1_y_meters = detector[
            "vertex_y"] + detector["arm_length_meters"] * np.sin(
                (detector["rotation_angle_degrees"] +
                 detector["opening_angle_degrees"]) * np.pi / 180.0)
    detector_from_points_xy = Detector.detector_from_points_xy(
        detector["vertex_x"], detector["vertex_y"], end1_x_meters,
        end1_y_meters, end2_x_meters, end2_y_meters,
        detector["arm_length_meters"], detector["dl_for_arms_meters"])
    assert detector_from_points_xy["vertex_x"] == detector["vertex_x"]
    assert detector_from_points_xy["vertex_y"] == detector["vertex_y"]
    assert detector_from_points_xy["arm_length_meters"] == detector[
        "arm_length_meters"]
    assert detector_from_points_xy["dl_for_arms_meters"] == detector[
        "dl_for_arms_meters"]
    eps = 1.e-6  # arctan2 for angles introduces some roundoff error
    assert np.abs(detector_from_points_xy["opening_angle_degrees"] -
                  detector["opening_angle_degrees"]) < eps
    assert np.abs(detector_from_points_xy["rotation_angle_degrees"] -
                  detector["rotation_angle_degrees"]) < eps
    assert np.all(
        np.abs(detector_from_points_xy["arms_xy"] - detector["arms_xy"]) < eps)

    detector_from_points_xy_no_arm_length = Detector.detector_from_points_xy(
        detector["vertex_x"], detector["vertex_y"], end1_x_meters,
        end1_y_meters, end2_x_meters, end2_y_meters, None,
        detector["dl_for_arms_meters"])

    assert np.abs(detector_from_points_xy_no_arm_length["arm_length_meters"] -
                  detector["arm_length_meters"]) < eps
    assert detector_from_points_xy_no_arm_length[
        "dl_for_arms_meters"] == detector["dl_for_arms_meters"]
    assert np.abs(
        detector_from_points_xy_no_arm_length["opening_angle_degrees"] -
        detector["opening_angle_degrees"]) < eps
    assert np.abs(
        detector_from_points_xy_no_arm_length["rotation_angle_degrees"] -
        detector["rotation_angle_degrees"]) < eps
    assert detector_from_points_xy_no_arm_length["vertex_x"] == detector[
        "vertex_x"]
    assert detector_from_points_xy_no_arm_length["vertex_y"] == detector[
        "vertex_y"]
    assert detector_from_points_xy_no_arm_length["scores"] == detector[
        "scores"]
    assert np.all(
        np.abs(detector_from_points_xy_no_arm_length["arms_xy"] -
               detector["arms_xy"]) < eps)


def test_write_shapefile_of_detectors():
    # Make a list of 3 random detectors to output
    detectors_and_inputs = [
        random_detector(random_scores()) for i in range(0, 3)
    ]
    detectors = [detector[-1] for detector in detectors_and_inputs]

    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name
    output_path = temp_path + "/detectors.shp"

    Detector.write_shapefile_of_detectors(detectors, output_path)

    with fiona.open(output_path) as output:
        assert len(output) == 6
        assert output.crs == CRS.from_epsg(5070)
        assert output.driver == "ESRI Shapefile"
        eps = 1.e-8
        for i, detector in enumerate(detectors):
            # Check coordinates of x and y arms
            coords_x_arm = output[2 * i]["geometry"]["coordinates"]
            coords_y_arm = output[2 * i + 1]["geometry"]["coordinates"]
            assert len(coords_x_arm) == 2
            assert len(coords_y_arm) == 2
            assert np.abs(detector["vertex_x"] - coords_x_arm[0][0]) < eps
            assert np.abs(detector["vertex_y"] - coords_x_arm[0][1]) < eps
            assert np.abs(detector["arms_xy"][0][0] - coords_x_arm[1][0]) < eps
            assert np.abs(detector["arms_xy"][0][1] - coords_x_arm[1][1]) < eps
            assert np.abs(detector["vertex_x"] - coords_y_arm[0][0]) < eps
            assert np.abs(detector["vertex_y"] - coords_y_arm[0][1]) < eps
            assert np.abs(detector["arms_xy"][-1][0] -
                          coords_y_arm[1][0]) < eps
            assert np.abs(detector["arms_xy"][-1][1] -
                          coords_y_arm[1][1]) < eps

            # Check x arm metadata
            assert output[2 * i].geometry.type == "LineString"
            assert output[2 * i].properties["name"] == "x arm"
            assert np.abs(output[2 * i].properties["vert_x"] -
                          detectors_and_inputs[i][0] < eps)
            assert np.abs(output[2 * i].properties["vert_y"] -
                          detectors_and_inputs[i][1] < eps)
            assert np.abs(output[2 * i].properties["arm_length"] -
                          detectors_and_inputs[i][2] < eps)
            assert np.abs(output[2 * i].properties["open_angle"] -
                          detectors_and_inputs[i][4] < eps)
            assert np.abs(output[2 * i].properties["rot_angle"] -
                          detectors_and_inputs[i][5] < eps)
            assert np.abs(output[2 * i].properties["elev_score"] -
                          detectors_and_inputs[i][6]["elevation_score"] < eps)
            assert np.abs(output[2 * i].properties["tilt_score"] -
                          detectors_and_inputs[i][6]["tilt_score"] < eps)
            assert np.abs(output[2 * i].properties["lc_score"] -
                          detectors_and_inputs[i][6]["landcover_score"] < eps)
            assert np.abs(output[2 * i].properties["tot_score"] -
                          detectors_and_inputs[i][6]["total_score"] < eps)

            # Check y arm metadata
            assert output[2 * i + 1].geometry.type == "LineString"
            assert output[2 * i + 1].properties["name"] == "y arm"
            assert np.abs(output[2 * i + 1].properties["vert_x"] -
                          detectors_and_inputs[i][0]) < eps
            assert np.abs(output[2 * i + 1].properties["vert_y"] -
                          detectors_and_inputs[i][1]) < eps
            assert np.abs(output[2 * i + 1].properties["arm_length"] -
                          detectors_and_inputs[i][2]) < eps
            assert np.abs(output[2 * i + 1].properties["open_angle"] -
                          detectors_and_inputs[i][4]) < eps
            assert np.abs(output[2 * i + 1].properties["rot_angle"] -
                          detectors_and_inputs[i][5]) < eps
            assert np.abs(output[2 * i + 1].properties["elev_score"] -
                          detectors_and_inputs[i][6]["elevation_score"]) < eps
            assert np.abs(output[2 * i + 1].properties["tilt_score"] -
                          detectors_and_inputs[i][6]["tilt_score"]) < eps
            assert np.abs(output[2 * i + 1].properties["lc_score"] -
                          detectors_and_inputs[i][6]["landcover_score"]) < eps
            assert np.abs(output[2 * i + 1].properties["tot_score"] -
                          detectors_and_inputs[i][6]["total_score"]) < eps
