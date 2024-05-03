# Distributed under the MIT License.
# See LICENSE for details.

import rasterio as rio
import rasterio.mask
from shapely.geometry import Polygon

from CosmicExplorerLocationSearch import Coordinates


def crop(in_geotiff_path, out_geotiff_path, lon_center, lat_center,
         width_meters):
    """Crop a geotiff to a square region.

    Crop a geotiff using a box constructed from a lon/lat center
    and a width in units of the geotiff's x,y coordinates
    (assumed here to be meters, as they are in EPSG:5070). Then write
    the result to a new geotiff file.

    Based on rasterio documentation example at
    https://rasterio.readthedocs.io/en/latest/topics/masking-by-shapefile.html
    """
    with rio.open(in_geotiff_path) as geofile:
        # Get the half width and height in meters
        half_width_meters = width_meters / 2.0

        # Convert the center point to x,y coordinates
        x_center, y_center = Coordinates.lonlat_to_xy(lon_center, lat_center,
                                                      geofile.crs.wkt)

        # Use rio.mask.mask to crop
        # via https://rasterio.readthedocs.io/en/stable/topics/
        # masking-by-shapefile.html
        # but here just use a single polygon constructed from coordinates
        coordinates = [
            (x_center - half_width_meters, y_center - half_width_meters),
            (x_center + half_width_meters, y_center - half_width_meters),
            (x_center + half_width_meters, y_center + half_width_meters),
            (x_center - half_width_meters, y_center + half_width_meters),
        ]
        clipping_box = Polygon(coordinates)
        out_image, out_transform = rio.mask.mask(geofile, [clipping_box],
                                                 crop=True)
        out_profile = geofile.profile
        out_profile.update(
            width=out_image.shape[1],
            height=out_image.shape[2],
            transform=out_transform,
        )
        with rio.open(out_geotiff_path, "w", **out_profile) as out_geofile:
            out_geofile.write(out_image)


def resample(in_geotiff_path, out_geotiff_path, upscale_factor,
             resampling_method):
    """
    Resample a geotiff by a given factor.

    Upsample (if upscale_factor > 1) or downsamples (if upscale_factor < 1) a 
    geotiff, then write the result to a new geotiff. Note that 
    resampling_method should be one of the rasterio.enums.Resampling,
    such as Resampling.mode (e.g. for landcover) or Resampling.average
    (e.g. for elevation).

    Based on example in rasterio help text at
    https://rasterio.readthedocs.io/en/stable/topics/resampling.html
    """
    with rio.open(in_geotiff_path) as geofile:
        # resample data to target shape
        out_image = geofile.read(
            out_shape=(geofile.count, int(geofile.height * upscale_factor),
                       int(geofile.width * upscale_factor)),
            resampling=resampling_method)

        # scale image transform
        out_transform = geofile.transform * geofile.transform.scale(
            (geofile.width / out_image.shape[-1]),
            (geofile.height / out_image.shape[-2]))
        out_profile = geofile.profile
        out_profile.update(
            width=out_image.shape[1],
            height=out_image.shape[2],
            transform=out_transform,
        )

        with rio.open(out_geotiff_path, "w", **out_profile) as out_geofile:
            out_geofile.write(out_image)
