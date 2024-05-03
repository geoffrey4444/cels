# Distributed under the MIT License.
# See LICENSE for details.

from pyproj import Transformer


def xy_to_lonlat(x, y, projection_wkt_for_xy):
    """Convert (x,y) coordinates in some projection to (lon, lat)

    Convert x,y coordinates in a projection given by well-known-text (wkt)
    projection_wkt to (longitude, latitude) coordinates in the WSG84
    projection (wkt EPSG:4326).

    Inputs:
      x: input x coordinate
      y: input y coordinate
      projection: well-known text of projection used for x,y

    Returns:
      lon: longitude
      lat: latitude
    """
    transformer = Transformer.from_crs(projection_wkt_for_xy, "EPSG:4326")
    lat, lon = transformer.transform(x, y)
    return lon, lat


def lonlat_to_xy(lon, lat, projection_wkt_for_xy):
    """Convert (x,y) coordinates in some projection to (lon, lat)

    Convert x,y coordinates in a projection given by well-known-text (wkt)
    projection_wkt to (longitude, latitude) coordinates in the WSG84
    projection (wkt EPSG:4326).

    Inputs:
      lon: longitude
      lat: latitude
      projection_wkt_for_xy: well-known text of projection used for x,y

    Returns:
      x: x coordinate
      y: y coordinate
    """
    transformer = Transformer.from_crs("EPSG:4326", projection_wkt_for_xy)
    return transformer.transform(lat, lon)
