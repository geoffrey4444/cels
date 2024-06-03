# Distributed under the MIT License.
# See LICENSE for details.
from CosmicExplorerLocationSearch import Detector
from CosmicExplorerLocationSearch import Score
import random
import numpy as np
from pyproj import CRS, Transformer
import rasterio as rio

# Here are some helper functions for use with the unit tests


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


def random_detector(scores=None, length_bounds=None, center=None):
    """Create a random detector for use with unit tests. Optionally 
    return provided scores. Optionally make arms with length_bounds, a
    pair of bounds in the order (min, max) or with vertex at
    (x,y) == center[0], center[1]), or both."""
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
    if center is None:
        vertex_x = random.uniform(xmin * bounds_factor, xmax * bounds_factor)
        vertex_y = random.uniform(ymin * bounds_factor, ymax * bounds_factor)
    else:
        vertex_x = center[0]
        vertex_y = center[1]
    # Choose other detector parameters randomly
    arm_length_meters = None
    if (length_bounds is not None):
        arm_length_meters = random.uniform(length_bounds[0], length_bounds[1])
    else:
        arm_length_meters = random.uniform(10000.0, 50000.0)
    # Ensure that sample point spacing evenly divides arm lengths
    dl_for_arms_meters = arm_length_meters / np.random.randint(100.0, 501.0)
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


def profile_for_random_geotiff(width):
    # Make a 40km x 40km raster empty raster file, with latitude and
    # longitude located in the United States (New Mexico),
    # with 1km pixels (so 40x40 pixels), that can be populated with random
    # data for testing.
    bounds = rio.coords.BoundingBox(left=-1113460.0,
                                    bottom=1071639.0,
                                    right=-1073460.0,
                                    top=1111639.0)
    height = width
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
    return profile, bounds


def random_geotiff(path, profile, data=np.array([])):
    """Output a random geotiff for use with unit tests, returning the 
    randomly generated data as a numpy array, given a profile and path."""
    width = profile["width"]
    height = profile["height"]
    profile.update(dtype=np.float64)
    if data.size == 0:
        data = np.random.rand(height, width)
    with rio.open(path, "w", **profile) as out_geofile:
        out_geofile.write(data, 1)
    return data


def random_elevation_geotiff_with_width(path, width):
    """Output a random geotiff for use with unit tests, returning the 
    randomly generated data as a numpy array, given a path. Uses
    profile_for_random_geotiff()."""
    profile, _ = profile_for_random_geotiff(width)
    data = np.random.uniform(-100.0, 1000.0, (width, width))
    return random_geotiff(path, profile, data=data)


def random_landcover_geotiff_with_width(path, width, omit_bad_values=True):
    """Output a random geotiff for use with unit tests, returning the 
    randomly generated data as a numpy array, given a path. Uses
    profile_for_random_geotiff(). Omits excluded landcover values
    unless omit_bad_values is false, in which case all landcover
    values are drawn from the omitted values"""
    profile, _ = profile_for_random_geotiff(width)
    landcover_choices_all = Score.landcover_labels.keys()
    landcover_choices_no_nodata = [
        key for key in landcover_choices_all if key not in [0, 101, 102, 103]
    ]
    landcover_bad_values_only = [key for key in [0, 101, 102, 103]]
    data = None
    if omit_bad_values == True:
        data = np.random.choice(landcover_choices_no_nodata, (width, width))
    else:
        data = np.random.choice(landcover_bad_values_only, (width, width))
    return random_geotiff(path, profile, data=data)
