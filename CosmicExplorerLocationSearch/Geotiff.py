# Distributed under the MIT License.
# See LICENSE for details.

import numpy as np
import rasterio as rio
import rasterio.mask
from shapely.geometry import Polygon
import multiprocessing.shared_memory as shared_memory
import os
import uuid

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


def sample_from_array(pixel_data, affine_transform, nodata_value, coordinates):
    """Sample pixel values from a numpy array at given coordinates.
    
    Inputs:
        pixel_data: numpy array holding geotiff pixel data (2D array)
        affine_transform: rasterio affine transform for the geotiff
        nodata_value: value used to represent no data in the geotiff
        coordinates: list of (x, y) coordinate pairs in the same projection as the geotiff
        
    Returns:
        List of pixel values, one for each coordinate in the input list.
        For coordinates outside the raster bounds, returns the nodata_value.
        
    Note: This function uses nearest neighbor sampling, which matches the
    default behavior of rasterio's .sample() method.
    """
    if len(pixel_data.shape) != 2:
        raise ValueError("pixel_data must be a 2D numpy array")

    if len(coordinates) == 0:
        return []

    xs = [coord[0] for coord in coordinates]
    ys = [coord[1] for coord in coordinates]

    rows, cols = rio.transform.rowcol(affine_transform, xs, ys)

    values = []
    height, width = pixel_data.shape

    for row, col in zip(rows, cols):
        in_bounds = (0 <= row < height and 0 <= col < width)
        if in_bounds:
            values.append(pixel_data[row, col])
        else:
            values.append(nodata_value)
    return values


def geotiff_to_bsq(in_geotiff_path, out_bsq_path):
    """Convert a geotiff to a band sequential binary file sutiable for
    directly reading into memory.
    
    Inputs:
        in_geotiff_path: path to the input geotiff file
        out_bsq_path: path to the output BSQ binary file
    """
    with rio.open(in_geotiff_path) as geofile:
        profile = geofile.profile.copy()
        profile.update(
            driver="ENVI",
            interleave="bsq",
            count=geofile.count,
            dtype=geofile.dtypes[0],
            nodata=geofile.nodata,
            width=geofile.width,
            height=geofile.height,
            transform=geofile.transform,
        )
        with rio.open(out_bsq_path, "w", **profile) as out_geofile:
            out_geofile.write(geofile.read())


def read_bsq_array(bsq_path, shape, dtype):
    """Read a BSQ (Band Sequential) binary file directly into a numpy array.
    
    Inputs:
        bsq_path: path to the BSQ binary file
        shape: tuple of (height, width) for the raster
        dtype: numpy data type of the raster data
        
    Returns:
        numpy array with shape (height, width) containing the raster data
        
    Note: This function reads the raw binary data directly without using rasterio.
    It assumes the BSQ file contains a single band of data in band sequential format.
    Also, note that this function should not be used to read in large geotiffs;
    instead, use the function read_bsq_array_to_shared_memory.
    """
    with open(bsq_path, 'rb') as f:
        raw_data = f.read()

    # Convert read bytes to numpy array of desired shape, assuming known dtype
    array = np.frombuffer(raw_data, dtype=dtype).reshape(shape)

    return array


def read_bsq_to_shared_memory(bsq_path):
    """Read a BSQ file into shared memory and return metadata for sampling.
    
    This function reads the BSQ binary data directly into a shared memory
    region without copying the bytes, and uses rasterio to read the metadata.
    
    Inputs:
        bsq_path: path to the BSQ binary file
        
    Returns:
        Dictionary containing:
            - 'shared_data_name': name of the shared memory region
            - 'affine_transform': rasterio affine transform for the geotiff
            - 'nodata_value': value used to represent no data in the geotiff
            - 'shape': tuple of (height, width) for the raster
            - 'dtype': numpy data type of the raster data
    """
    # Read metadata using rasterio
    with rio.open(bsq_path) as geofile:
        affine_transform = geofile.transform
        nodata_value = geofile.nodata
        shape = (geofile.height, geofile.width)
        dtype = geofile.dtypes[0]

    # Generate a unique name for the shared memory region
    shared_data_name = f"bsq_{uuid.uuid4().hex[:8]}"

    # Read the raw binary data
    with open(bsq_path, 'rb') as f:
        raw_data = f.read()

    # Create shared memory region
    shm = shared_memory.SharedMemory(name=shared_data_name,
                                     create=True,
                                     size=len(raw_data))

    # Copy the data to shared memory
    shm.buf[:len(raw_data)] = raw_data

    return {
        'shared_data_name': shared_data_name,
        'affine_transform': affine_transform,
        'nodata_value': nodata_value,
        'shape': shape,
        'dtype': dtype,
        'data_size': len(raw_data)
    }


def get_shared_memory_array(shared_data_name, shape, dtype):
    """Access shared memory data as a numpy array.
    
    This function connects to an existing shared memory region and returns
    a numpy array that views the shared memory data without copying.
    
    Inputs:
        shared_data_name: name of the shared memory region
        shape: tuple of (height, width) for the raster
        dtype: numpy data type of the raster data
        
    Returns:
        numpy array that views the shared memory data
        
    Note: The shared memory region must have been created by read_bsq_to_shared_memory.
    """
    shm = shared_memory.SharedMemory(name=shared_data_name)
    array = np.ndarray(shape, dtype=dtype, buffer=shm.buf)
    return array, shm
