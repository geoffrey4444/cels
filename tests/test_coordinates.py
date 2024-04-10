# Distributed under the MIT License.
# See LICENSE for details.

from CosmicExplorerSiteSearch import Coordinates
import random
from pyproj import CRS, Transformer


def test_xy_to_lonlat():
    """Test conversion of EPSG:5070 to EPSG:4326.
    Note: EPSG:5070 is NAD83 / Conus Albers, a conic, equal-area projection
    that is good to use (minimizes distortion) for the United States.
    EPSG:5070 is commonly used for national atlas maps, for instance.
    EPSG:4326 is the WSG 84 projection, whose coordinates are latitude and
    longitude. Converting to/from EPSG:4326 amounts to converting from the
    x,y coorddinates of the input projection to latitude/longitude, and vice
    versa.
    """
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
    x = random.uniform(xmin * bounds_factor, xmax * bounds_factor)
    y = random.uniform(ymin * bounds_factor, ymax * bounds_factor)
    lon, lat = Coordinates.xy_to_lonlat(x, y, xy_wkt)
    print(lon, lat)
    x_check, y_check = Coordinates.lonlat_to_xy(lon, lat, xy_wkt)

    eps = 1.e-6
    assert abs(x_check - x) < eps
    assert abs(y_check - y) < eps

    # Verify transformation for a single, known point
    # Cal State Fullerton lies at lon,lat =
    # -117.885278, 33.880556 (via wikipedia). This should convert to
    # x,y = -1992101.6635348154, 1432029.2332942358 according to
    # https://epsg.io/transform
    csuf_x, csuf_y = -1992101.6635348154, 1432029.2332942358
    csuf_lon, csuf_lat = -117.885278, 33.880556
    csuf_lon_check, csuf_lat_check = Coordinates.xy_to_lonlat(
        csuf_x, csuf_y, xy_wkt)
    assert abs(csuf_lon_check - csuf_lon) < eps
    assert abs(csuf_lat_check - csuf_lat) < eps


def test_lonlat_to_xy():
    """Test conversion of EPSG:5070 to EPSG:4326
    Note: EPSG:5070 is NAD83 / Conus Albers, a conic, equal-area projection
    that is good to use (minimizes distortion) for the United States.
    EPSG:5070 is commonly used for national atlas maps, for instance.
    EPSG:4326 is the WSG 84 projection, whose coordinates are latitude and
    longitude. Converting to/from EPSG:4326 amounts to converting from the
    x,y coorddinates of the input projection to latitude/longitude, and vice
    versa.
    """
    # Get lon,lat possible values
    lonlat_crs = CRS("EPSG:4326")
    lonmin, latmin, lonmax, latmax = lonlat_crs.area_of_use.bounds

    xy_wkt = "EPSG:5070"
    # I want to test on random points, but if the points are too close to
    # the boundary, the transform can fail. So only try points within eps of
    # bounds, where eps is however small to avoid failing transforms
    bounds_factor = 0.1
    lon = random.uniform(lonmin * bounds_factor, lonmax * bounds_factor)
    lat = random.uniform(latmin * bounds_factor, latmax * bounds_factor)
    x, y = Coordinates.lonlat_to_xy(lon, lat, xy_wkt)
    lon_check, lat_check = Coordinates.xy_to_lonlat(x, y, xy_wkt)

    eps = 1.e-6
    assert abs(lon_check - lon) < eps
    assert abs(lat_check - lat) < eps

    # Verify transformation for a single, known point
    # Cal State Fullerton lies at lon,lat =
    # -117.885278, 33.880556 (via wikipedia). This should convert to
    # x,y = -1992101.6635348154, 1432029.2332942358 according to
    # https://epsg.io/transform
    csuf_x, csuf_y = -1992101.6635348154, 1432029.2332942358
    csuf_lon, csuf_lat = -117.885278, 33.880556
    csuf_x_check, csuf_y_check = Coordinates.lonlat_to_xy(
        csuf_lon, csuf_lat, xy_wkt)
    eps_xy = 0.1  # 0.1 meter accuracy
    assert abs(csuf_x_check - csuf_x) < eps_xy
    assert abs(csuf_y_check - csuf_y) < eps_xy
