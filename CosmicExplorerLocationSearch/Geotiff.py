# Distributed under the MIT License.
# See LICENSE for details.

from affine import Affine
import numpy as np
import rasterio as rio
import rasterio.mask
from shapely.geometry import Polygon

from CosmicExplorerLocationSearch import Coordinates


def bilinear_interpolate_vectorized(array, coords, transform, nodata=None):
    """
    Perform vectorized bilinear interpolation on a 2D array.
    
    This function replicates the behavior of rasterio.sample() for bilinear
    interpolation, but works directly on numpy arrays without copying data.
    
    Inputs:
        array: 2D numpy array containing raster data
        coords: Nx2 array of (x, y) coordinates in the same projection as the transform
        transform: rasterio transform object that maps pixel coordinates to world coordinates
        nodata: value to return for coordinates outside the raster bounds
        
    Returns:
        N-length array of interpolated values
        
    Note:
        This function returns nodata for coordinates outside the array bounds.
    """
    nrows, ncols = array.shape

    # Use rasterio's rowcol function to get pixel coordinates (matches rasterio.sample behavior)
    rows_f, cols_f = rio.transform.rowcol(transform,
                                          [coord[0] for coord in coords],
                                          [coord[1] for coord in coords])
    rows_f = np.array(rows_f, dtype=float)
    cols_f = np.array(cols_f, dtype=float)

    # Check if coordinates are exactly at pixel centers (integer coordinates)
    is_pixel_center = (np.abs(rows_f - np.round(rows_f)) <
                       1e-10) & (np.abs(cols_f - np.round(cols_f)) < 1e-10)

    # For pixel centers, use exact integer coordinates
    rows_f = np.where(is_pixel_center, np.round(rows_f), rows_f)
    cols_f = np.where(is_pixel_center, np.round(cols_f), cols_f)

    # Get floor and ceiling indices
    row_floor = np.floor(rows_f).astype(int)
    col_floor = np.floor(cols_f).astype(int)
    row_ceil = row_floor + 1
    col_ceil = col_floor + 1

    # Calculate interpolation weights
    row_weight = rows_f - row_floor
    col_weight = cols_f - col_floor

    # Handle edge cases where weight would be NaN
    row_weight = np.where(np.isnan(row_weight), 0.0, row_weight)
    col_weight = np.where(np.isnan(col_weight), 0.0, col_weight)

    # Clamp weights to [0, 1] range for out-of-bounds coordinates
    row_weight = np.clip(row_weight, 0.0, 1.0)
    col_weight = np.clip(col_weight, 0.0, 1.0)

    # Out-of-bounds logic: allow sampling at the last pixel center
    out_of_bounds = ((row_floor < 0) | (row_floor >= nrows) | (col_floor < 0) |
                     (col_floor >= ncols) | ((row_ceil > nrows) |
                                             ((row_ceil == nrows) &
                                              (row_weight != 0))) |
                     ((col_ceil > ncols) | ((col_ceil == ncols) &
                                            (col_weight != 0))))

    # Clamp indices to valid array bounds for interpolation
    row_floor = np.clip(row_floor, 0, nrows - 1)
    col_floor = np.clip(col_floor, 0, ncols - 1)
    row_ceil = np.clip(row_ceil, 0, nrows - 1)
    col_ceil = np.clip(col_ceil, 0, ncols - 1)

    # Get the four corner values (vectorized)
    v00 = array[row_floor, col_floor]
    v01 = array[row_floor, col_ceil]
    v10 = array[row_ceil, col_floor]
    v11 = array[row_ceil, col_ceil]

    # Bilinear interpolation (vectorized)
    v0 = v00 * (1 - col_weight) + v01 * col_weight
    v1 = v10 * (1 - col_weight) + v11 * col_weight
    values = v0 * (1 - row_weight) + v1 * row_weight

    # Set out-of-bounds results to nodata
    if nodata is not None:
        values[out_of_bounds] = nodata

    return values


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
