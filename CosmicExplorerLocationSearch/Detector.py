# Distributed under the MIT License.
# See LICENSE for details.
from concurrent.futures import ThreadPoolExecutor, as_completed
import fiona
import numpy as np
from pyproj import CRS
import rasterio as rio
from rasterio.enums import Resampling
import rasterio.mask
from shapely import LineString

from CosmicExplorerLocationSearch import Coordinates


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
      dl_for_arms_meters: distance between sample points (meters)
      opening_angle_degrees: detector opening angle (degrees)
      rotation_angle_degrees: rotation (degrees) of detector vs. proj x-y axes
      vertex_x: vertex x coordinate (in units of x-y projection, assumed meters)
      vertex_y: vertex y coordinate (in units of x-y projection, assumed meters)
      scores: (optional) scores to store with a detector, for *.shp output

    Returns: dictionary containing
      vertex_x
      vertex_y
      arm_length_meters = length of each arm in meters
      dl_for_arms_meters = distance between sample points
      opening_angle_degrees
      rotation_angle_degrees
      arms_xy: x,y coordinates (meters) of arm, order (xend ... vertex ... yend)
      dist_from_vertex: distance from vertex, order (xend ... vertex ... yend)
      vertex_pixel: value of n such that nth element in arms_xy is the vertex
      scores: the scores provided (or None if no scores provided)
    """
    opening_angle_rad = opening_angle_degrees * np.pi / 180.0
    rotation_angle_rad = rotation_angle_degrees * np.pi / 180.0

    # Set up detector (no rotation about vertex yet)
    dl_for_arms = dl_for_arms_meters
    # final pixel should be arm_length_meters away from detector; allow
    # some roundoff error to avoid sometimes getting an extra pixel
    # Note: a previous version of this code used dl_for_arms as epislon, but
    # this is large enough that sometimes, because of roundoff, the
    # detector gets an extra pixel
    eps = 1.e-10
    arm_distance_from_vertex = np.arange(0, arm_length_meters + eps,
                                         dl_for_arms)
    x_arm_x_norot = arm_distance_from_vertex
    x_arm_y_norot = np.zeros(x_arm_x_norot.shape)
    y_arm_x_norot = arm_distance_from_vertex * np.cos(opening_angle_rad)
    y_arm_y_norot = arm_distance_from_vertex * np.sin(opening_angle_rad)

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
    # Note: returning this is redundant information, joining the array here
    arms_xy = np.concatenate((x_arm[::-1], y_arm[1:]))

    dist_from_vertex = np.sqrt(
        np.square(arms_xy[:, 0] - vertex_x) +
        np.square(arms_xy[:, 1] - vertex_y))
    vertex_pixel = len(x_arm_x_norot) - 1

    return {
        "vertex_x": vertex_x,
        "vertex_y": vertex_y,
        "arm_length_meters": arm_length_meters,
        "dl_for_arms_meters": dl_for_arms,
        "opening_angle_degrees": opening_angle_degrees,
        "rotation_angle_degrees": rotation_angle_degrees,
        "arms_xy": arms_xy,
        "distance_from_vertex_meters": dist_from_vertex,
        "vertex_pixel": vertex_pixel,
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
      Other files will be output next to the .shp file; QGIS and ArcGIS
      need them all. ArcGIS wants all the files as a zip file; QGIS
      just wants them all in the same directory.      
    """
    # shape file names have 10-character limit, so the shapefile keys
    # are abbreviated
    metadata_schema = {
        "geometry": "LineString",
        "properties": {
            "name": "str",
            "arm_length": "float",
            "open_angle": "float",
            "rot_angle": "float",
            "vert_x": "float",
            "vert_y": "float",
            "elev_score": "float",
            "tilt_score": "float",
            "lc_score": "float",
            "tot_score": "float",
        }
    }
    shp_driver = "ESRI Shapefile"
    element_to_write = {}
    with fiona.open(
            output_file_path,
            "w",
            driver="ESRI Shapefile",
            schema=metadata_schema,
            # 5070 = NAD83 / Conus Albers
            # Hard code output projection for now;
            # this could be made an option
            crs=CRS.from_epsg(5070)) as outfile:
        for detector in detectors:
            detector_properties = {
                "name": "x arm",
                "arm_length": detector["arm_length_meters"],
                "open_angle": detector["opening_angle_degrees"],
                "rot_angle": detector["rotation_angle_degrees"],
                "vert_x": detector["vertex_x"],
                "vert_y": detector["vertex_y"],
                "elev_score": -9999.0,
                "tilt_score": -9999.0,
                "lc_score": -9999.0,
                "tot_score": -9999.0,
            }
            if detector["scores"] != None:
                detector_properties["elev_score"] = detector["scores"][
                    "elevation_score"]
                detector_properties["tilt_score"] = detector["scores"][
                    "tilt_score"]
                detector_properties["lc_score"] = detector["scores"][
                    "landcover_score"]
                detector_properties["tot_score"] = detector["scores"][
                    "total_score"]

            vert_x = detector["vertex_x"]
            vert_y = detector["vertex_y"]
            xend_x = detector["arms_xy"][0][0]
            xend_y = detector["arms_xy"][0][1]
            yend_x = detector["arms_xy"][-1][0]
            yend_y = detector["arms_xy"][-1][1]
            xarm_line = LineString([[vert_x, vert_y], [xend_x, xend_y]])
            yarm_line = LineString([[vert_x, vert_y], [yend_x, yend_y]])

            element_to_write["geometry"] = xarm_line
            element_to_write["properties"] = detector_properties
            outfile.write(element_to_write)
            element_to_write["geometry"] = yarm_line
            element_to_write["properties"]["name"] = "y arm"
            outfile.write(element_to_write)
