# Distributed under the MIT License.
# See LICENSE for details.
import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
import rasterio.mask
from shapely import LineString

from CosmicExplorerSiteSearch import Coordinates


def detector_coordinates(
    arm_length_meters,
    opening_angle_degrees,
    rotation_angle_degrees,
    vertex_x,
    vertex_y,
):
    """
    Inputs:
      arm_length: detector arm length (meters)
      opening_angle_degrees: detector opening angle (degrees)
      rotation_angle_degrees: rotation (degrees) of detector vs. proj x-y axes
      vertex_x: vertex x coordinate (in units of x-y projection, assumed meters)
      vertex_y: vertex y coordinate (in units of x-y projection, assumed meters)

    Returns: dictionary containing
      vertex_x
      vertex_y
      arm_length_meters
      opening_angle_degrees
      rotation_angle_degrees
      arms_xy: x,y coordinates (meters) of arm, order (xend ... vertex ... yend)
    """
    opening_angle_rad = opening_angle_degrees * np.pi / 180.0
    rotation_angle_rad = rotation_angle_degrees * np.pi / 180.0

    # Set up detector (no rotation about vertex yet)
    dl_for_arms = 1.0  # meters
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
        "opening_angle_degrees": opening_angle_degrees,
        "rotation_angle_degrees": rotation_angle_degrees,
        "arms_xy": arms_xy,
    }


def detector(
    arm_length,
    opening_angle_degrees,
    rotation_angle_degrees,
    vertex_x,
    vertex_y,
):
    """
    Inputs:
      arm_length: detector arm length (meters)
      opening_angle_degrees: detector opening angle (degrees)
      rotation_angle_degrees: rotation (degrees) of detector vs. proj x-y axes
      vertex_x: vertex x coordinate (in units of x-y projection, usually meters)
      vertex_y: vertex y coordinate (in units of x-y projection, usually meters)

    Returns:
      A dictionary containing the following:
        * "x_arm": LineString representing detector x arm
        * "y_arm": LineString representing detector y arm 
        * "xy_arm": dict containing sae output as detector_arm_coordinates()
    """
    arm_coords = detector_coordinates(arm_length, opening_angle_degrees,
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
    }


def pixel_data(raster_file_dict, detector):
    """Inputs:
         raster_file_dict: dictionary of open raster files; 
                           open the files with rasterio.open() before calling
                           this function
         detector: output of Detector.detector()

       Returns: 
         A dictionary keyed by the keys in raster_file_dict. Under each
         key is a dictionary containing the following:
           * "coords" = x,y coords of points along detector arms
           * "values" = value at x,y from this raster
    """
    result = {}
    for raster in raster_file_dict:
        result[raster] = {
            "coords": np.array([]),
            "value": np.array([]),
        }
        raster_file = raster_file_dict[raster]
        nodata_value = raster_file.nodata

        result[raster]["coords"] = detector["arms"]["arms_xy"]
        result[raster]["value"] = np.array([
            sample[0]
            for sample in raster_file.sample(result[raster]["coords"])
        ])
    return result
