# Distributed under the MIT License.
# See LICENSE for details.
from concurrent.futures import ThreadPoolExecutor, as_completed
import fiona
from fiona import crs
import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
import rasterio.mask
from shapely import LineString

from CosmicExplorerSiteSearch import Coordinates


def detector_coordinates(
    arm_length_meters,
    dl_for_arms_meters,
    opening_angle_degrees,
    rotation_angle_degrees,
    vertex_x,
    vertex_y,
):
    """
    Inputs:
      arm_length: detector arm length (meters)
      dl_for_arms_meters: distance between sample points (meters)
      opening_angle_degrees: detector opening angle (degrees)
      rotation_angle_degrees: rotation (degrees) of detector vs. proj x-y axes
      vertex_x: vertex x coordinate (in units of x-y projection, assumed meters)
      vertex_y: vertex y coordinate (in units of x-y projection, assumed meters)

    Returns: dictionary containing
      vertex_x
      vertex_y
      arm_length_meters = length of each arm in meters
      dl_for_arms_meters = distance between sample points
      opening_angle_degrees
      rotation_angle_degrees
      arms_xy: x,y coordinates (meters) of arm, order (xend ... vertex ... yend)
      arms_x: x coordinates (meters) of arm, order (xend ... vertex ... yend)
      arms_y: y coordinates (meters) of arm, order (xend ... vertex ... yend)
    """
    opening_angle_rad = opening_angle_degrees * np.pi / 180.0
    rotation_angle_rad = rotation_angle_degrees * np.pi / 180.0

    # Set up detector (no rotation about vertex yet)
    dl_for_arms = dl_for_arms_meters
    x_arm_x_norot = np.arange(0, arm_length_meters + dl_for_arms, dl_for_arms)
    x_arm_y_norot = np.zeros(x_arm_x_norot.shape)
    y_arm_x_norot = np.arange(0, arm_length_meters + dl_for_arms,
                              dl_for_arms) * np.cos(opening_angle_rad)
    y_arm_y_norot = np.arange(0, arm_length_meters + dl_for_arms,
                              dl_for_arms) * np.sin(opening_angle_rad)

    # Rotate about vertex
    x_arm_x = x_arm_x_norot * np.cos(
        rotation_angle_rad) - x_arm_y_norot * np.sin(rotation_angle_rad)
    x_arm_y = x_arm_x_norot * np.sin(
        rotation_angle_rad) + x_arm_y_norot * np.cos(rotation_angle_rad)
    y_arm_x = y_arm_x_norot * np.cos(
        rotation_angle_rad) - y_arm_y_norot * np.sin(rotation_angle_rad)
    y_arm_y = y_arm_x_norot * np.sin(
        rotation_angle_rad) + y_arm_y_norot * np.cos(rotation_angle_rad)

    # Create pairs of x,y coordinates for each arm
    x_arm = np.vstack((x_arm_x + vertex_x, x_arm_y + vertex_y)).T
    y_arm = np.vstack((y_arm_x + vertex_x, y_arm_y + vertex_y)).T

    # Create a 1D list of x,y coordinates, (xend, ..., vertex, ... yend)
    # y_arm[1:] removes the vertex (so we don't get a duplicate vertex point)
    # when joining; x_arm[::-1] reverses the array order
    arms_xy = np.concatenate((x_arm[::-1], y_arm[1:]))

    return {
        "vertex_x": vertex_x,
        "vertex_y": vertex_y,
        "arm_length_meters": arm_length_meters,
        "dl_for_arms_meters": dl_for_arms,
        "opening_angle_degrees": opening_angle_degrees,
        "rotation_angle_degrees": rotation_angle_degrees,
        "arms_xy": arms_xy,
        "arms_x": arms_xy[:, 0],
        "arms_y": arms_xy[:, 1],
    }


def detector(arm_length_meters,
             dl_for_arms_meters,
             opening_angle_degrees,
             rotation_angle_degrees,
             vertex_x,
             vertex_y,
             scores=None):
    """
    Inputs:
      arm_length: detector arm length (meters)
      dl_for_arms_meters: spacing between sample points on arms (meters)
      opening_angle_degrees: detector opening angle (degrees)
      rotation_angle_degrees: rotation (degrees) of detector vs. proj x-y axes
      vertex_x: vertex x coordinate (in units of x-y projection, usually meters)
      vertex_y: vertex y coordinate (in units of x-y projection, usually meters)

    Returns:
      A dictionary containing the following:
        * "x_arm": LineString representing detector x arm
        * "y_arm": LineString representing detector y arm 
        * "arms": dict containing same output as detector_coordinates()
    """
    arm_coords = detector_coordinates(arm_length_meters, dl_for_arms_meters,
                                      opening_angle_degrees,
                                      rotation_angle_degrees, vertex_x,
                                      vertex_y)
    vert_x = arm_coords["vertex_x"]
    vert_y = arm_coords["vertex_y"]
    xend_x = arm_coords["arms_xy"][0][0]
    xend_y = arm_coords["arms_xy"][0][1]
    yend_x = arm_coords["arms_xy"][-1][0]
    yend_y = arm_coords["arms_xy"][-1][1]
    xarm_line = LineString([[vert_x, vert_y], [xend_x, xend_y]])
    yarm_line = LineString([[vert_x, vert_y], [yend_x, yend_y]])
    return {
        "x_arm": xarm_line,
        "y_arm": yarm_line,
        "arms": arm_coords,
        "scores": scores
    }


def write_shapefile_of_detectors(detectors, output_file_path):
    """
    Write a shapefile containing one or more detectors for visualization in GIS.
    Inputs:
      detectors: list of detectors, each an output of Detector.detector()
      output_file_path: path to write output .shp file (include .shp extension)
    Returns:
      Nothing
    Note:
      other files will be output next to the .shp file
    """
    metadata_schema = {
        "geometry": "LineString",
        "properties": {
            "name": "str",
            "arm_length_meters": "float",
            "opening_angle_degrees": "float",
            "rotation_angle_degrees": "float",
            "vertex_x": "float",
            "vertex_y": "float",
            "elevation_score": "float",
            "tilt_score": "float",
            "landcover_score": "float",
            "total_score": "float",
        }
    }
    shp_driver = "ESRI Shapefile"
    element_to_write = {}
    with fiona.open(output_file_path,
                    "w",
                    driver="ESRI Shapefile",
                    schema=metadata_schema,
                    crs=fiona.crs.from_epsg(5070)) as outfile:
        for detector in detectors:
            detector_properties = {
                "name":
                "x arm",
                "arm_length_meters":
                detector["arms"]["arm_length_meters"],
                "opening_angle_degrees":
                detector["arms"]["opening_angle_degrees"],
                "rotation_angle_degrees":
                detector["arms"]["rotation_angle_degrees"],
                "vertex_x":
                detector["arms"]["vertex_x"],
                "vertex_y":
                detector["arms"]["vertex_y"],
                "elevation_score":
                -9999.0,
                "tilt_score":
                -9999.0,
                "landcover_score":
                -9999.0,
                "total_score":
                -9999.0,
            }
            if detector["scores"] != None:
                detector_properties["elevation_score"] = detector["scores"][
                    "elevation_score"]
                detector_properties["tilt_score"] = detector["scores"][
                    "tilt_score"]
                detector_properties["landcover_score"] = detector["scores"][
                    "landcover_score"]
                detector_properties["total_score"] = detector["scores"][
                    "total_score"]
            element_to_write["geometry"] = detector["x_arm"]
            element_to_write["properties"] = detector_properties
            outfile.write(element_to_write)
            element_to_write["geometry"] = detector["y_arm"]
            outfile.write(element_to_write)
