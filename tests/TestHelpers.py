# Distributed under the MIT License.
# See LICENSE for details.
from CosmicExplorerLocationSearch import Detector
import random
import numpy as np
from pyproj import CRS, Transformer
import rasterio as rio


def random_scores():
    """Return a dict with random scores for unit tests"""
    elevation_score = random.uniform(0.0, 1000.0)
    tilt_score = random.uniform(0.0, 1000.0)
    landcover_score = random.uniform(0.0, 1000.0)
    total_score = elevation_score + tilt_score + landcover_score
    scores = {
        "elevation_score": elevation_score,
        "tilt_score": tilt_score,
        "landcover_score": landcover_score,
        "total_score": total_score,
    }
    return scores


def random_detector(scores=None):
    """Create a random detector for use with unit tests"""
    # Get x,y possible values
    xy_wkt = "EPSG:5070"
    xy_crs = CRS(xy_wkt)
    lonlat_to_xy = Transformer.from_crs("EPSG:4326", xy_wkt)
    xmin, ymin, xmax, ymax = lonlat_to_xy.transform_bounds(
        *xy_crs.area_of_use.bounds)

    # I want to test on random points, but if the points are too close to
    # the boundary, the transform can fail. So only try points within eps of
    # bounds, where eps is however small to avoid failing transforms
    bounds_factor = 0.1

    # Choose a random vertex x,y
    vertex_x = random.uniform(xmin * bounds_factor, xmax * bounds_factor)
    vertex_y = random.uniform(ymin * bounds_factor, ymax * bounds_factor)

    # Choose other detector parameters randomly
    arm_length_meters = random.uniform(10000.0, 50000.0)
    dl_for_arms_meters = arm_length_meters / random.uniform(10.0, 5000.0)
    opening_angle_degrees = random.uniform(70.0, 110.0)
    rotation_angle_degrees = random.uniform(0.0, 360.0)

    # Make a detector from the random parameters
    detector = Detector.detector(arm_length_meters, dl_for_arms_meters,
                                 opening_angle_degrees, rotation_angle_degrees,
                                 vertex_x, vertex_y, scores)
    if scores == None:
        return (vertex_x, vertex_y, arm_length_meters, dl_for_arms_meters) + (
            opening_angle_degrees, rotation_angle_degrees, detector)
    else:
        return (vertex_x, vertex_y, arm_length_meters, dl_for_arms_meters) + (
            opening_angle_degrees, rotation_angle_degrees, scores, detector)


def random_geotiff(path, profile):
    """Output a random geotiff for use with unit tests, returning the 
    randomly generated data as a numpy array"""
    width = profile["width"]
    height = profile["height"]
    profile.update(dtype=np.float64)
    data = np.random.rand(height, width)
    with rio.open(path, "w", **profile) as out_geofile:
        out_geofile.write(data, 1)
    return data
