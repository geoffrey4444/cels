# Distributed under the MIT License.
# See LICENSE for details.
import numpy as np
import rasterio as rio
from rasterio.enums import Resampling
import rasterio.mask
from shapely import LineString

from CosmicExplorerSiteSearch import Coordinates


def detector_coordinates(
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
      vertex_x
      vertex_y
      x_arm_end_x
      x_arm_end_y
      y_arm_end_x
      y_arm_end_y
    """
    opening_angle_rad = opening_angle_degrees * np.pi / 180.0
    rotation_angle_rad = rotation_angle_degrees * np.pi / 180.0

    # Set up detector (no rotation about vertex yet)
    x_arm_end_x_norot = arm_length
    x_arm_end_y_norot = 0
    y_arm_end_x_norot = arm_length * np.sin(opening_angle_rad)
    y_arm_end_y_norot = arm_length * np.cos(opening_angle_rad)

    # Rotate about vertex
    x_arm_end_x = x_arm_end_x_norot * np.cos(
        rotation_angle_rad) - x_arm_end_y_norot * np.sin(rotation_angle_rad)
    x_arm_end_y = x_arm_end_x_norot * np.sin(
        rotation_angle_rad) + x_arm_end_y_norot * np.cos(rotation_angle_rad)
    y_arm_end_x = y_arm_end_x_norot * np.cos(
        rotation_angle_rad) - y_arm_end_y_norot * np.sin(rotation_angle_rad)
    y_arm_end_y = y_arm_end_x_norot * np.sin(
        rotation_angle_rad) + y_arm_end_y_norot * np.cos(rotation_angle_rad)

    return (
        vertex_x,
        vertex_y,
        vertex_x + x_arm_end_x,
        vertex_y + x_arm_end_y,
        vertex_x + y_arm_end_x,
        vertex_y + y_arm_end_y,
    )


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
        * "vertex_x": x coordinate of the detector vertex
        * "vertex_y": y coordinate of the detector vertex
    """
    vert_x, vert_y, xend_x, xend_y, yend_x, yend_y = detector_coordinates(
        arm_length, opening_angle_degrees, rotation_angle_degrees, vertex_x,
        vertex_y)
    xarm_line = LineString([[vert_x, vert_y], [xend_x, xend_y]])
    yarm_line = LineString([[vert_x, vert_y], [yend_x, yend_y]])
    return {
        "x_arm": xarm_line,
        "y_arm": yarm_line,
        "arm_length": arm_length,
        "opening_angle_degrees": opening_angle_degrees,
        "rotation_angle_degrees": rotation_angle_degrees,
        "vertex_x": vert_x,
        "vertex_y": vert_y,
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
           * "x" = x coordinates of each pixel
           * "y" = y coordinates of each pixel
           * "value" = dict containing values for each key in raster_file_dict
           * "distance" = distance from vertex (- for x arm, + for y arm)
    """
    result = {}
    for raster in raster_file_dict:
        result[raster] = {
            "x": np.array([]),
            "y": np.array([]),
            "value": np.array([]),
            "distance": np.array([])
        }
        raster_file = raster_file_dict[raster]
        nodata_value = raster_file.nodata
        vertex_x = detector["vertex_x"]
        vertex_y = detector["vertex_y"]

        for arm in ["x_arm", "y_arm"]:
            # Mask pixels touching the arm. Crop to a minimal rectangular image
            # that contains these pixels.
            masked_image, masked_transform = rio.mask.mask(raster_file,
                                                           [detector[arm]],
                                                           all_touched=True,
                                                           crop=True)

            # Get row and col at each pixel for the cropped image
            image_number_of_rows, image_number_of_cols = masked_image[0].shape
            col_at_pixels, row_at_pixels = np.meshgrid(
                np.arange(image_number_of_cols),
                np.arange(image_number_of_rows))

            # From rows and cols of the cropped image, get coords at each pixel
            x_coords_list, y_coords_list = rio.transform.xy(
                masked_transform, row_at_pixels, col_at_pixels)
            x_coords_at_pixels = np.array(x_coords_list)
            y_coords_at_pixels = np.array(y_coords_list)

            # Get which pixels touch the arm
            matching_pixel_indices = np.nonzero(
                masked_image[0] != nodata_value)

            # Get the x,y coordinates of the touching pixels
            x_coords_at_matching_pixels = x_coords_at_pixels[
                matching_pixel_indices]
            y_coords_at_matching_pixels = y_coords_at_pixels[
                matching_pixel_indices]

            # Get each matching pixel's raster value and distance from vertex
            value_at_matching_pixels = masked_image[0][
                masked_image[0] != nodata_value]
            dist_from_vertex = np.sqrt(
                np.square(x_coords_at_matching_pixels - vertex_x) +
                np.square(y_coords_at_matching_pixels - vertex_y))

            # Sort the pixel data
            sorted_pixel_indices = np.argsort(dist_from_vertex)
            if arm == "x_arm":
                # Reverse the x arm elements
                sorted_pixel_indices = sorted_pixel_indices[::-1]
            else:
                # Remove vertex point for the y arm
                sorted_pixel_indices = sorted_pixel_indices[1:]

            x_coords_matching_sorted = x_coords_at_matching_pixels[
                sorted_pixel_indices]
            y_coords_matching_sorted = y_coords_at_matching_pixels[
                sorted_pixel_indices]
            value_matching_sorted = value_at_matching_pixels[
                sorted_pixel_indices]
            dist_from_vertex_sorted = dist_from_vertex[sorted_pixel_indices]

            if arm == "x_arm":
                result[raster]["x"] = x_coords_matching_sorted
                result[raster]["y"] = y_coords_matching_sorted
                result[raster]["value"] = value_matching_sorted
                result[raster]["distance"] = -dist_from_vertex_sorted
            else:
                result[raster]["x"] = np.concatenate(
                    (result[raster]["x"], x_coords_matching_sorted))
                result[raster]["y"] = np.concatenate(
                    (result[raster]["y"], y_coords_matching_sorted))
                result[raster]["value"] = np.concatenate(
                    (result[raster]["value"], value_matching_sorted))
                result[raster]["distance"] = np.concatenate(
                    (result[raster]["distance"], dist_from_vertex_sorted))

    return result
