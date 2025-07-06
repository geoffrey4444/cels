# Distributed under the MIT License.
# See LICENSE for details.
import numpy as np
import os
import rasterio as rio
from rasterio.enums import Resampling
import tempfile
import pytest
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import multiprocessing.shared_memory as shared_memory

from CosmicExplorerLocationSearch import Coordinates, Geotiff


def test_crop():
    """Test cropping geotiff image.
    The test i) checks that cropping to an original image does nothing, and
    ii) tests that a specific cropping has the correct metadata and agrees
    with a cropped sample image.
    """
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # Get path this script is in
    # via https://stackoverflow.com/questions/4934806/
    # how-can-i-find-scripts-directory
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Base image uses projection EPSG:5070
    base_image_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
    expected_crop_path = base_path
    expected_crop_path += "/test_images/SouthNM_Elevation_1km_Crop.tif"

    crop_path = temp_path + "/crop.tif"
    center_lon, center_lat = -107.7, 32.3
    center_x, center_y = Coordinates.lonlat_to_xy(center_lon, center_lat,
                                                  "EPSG:5070")
    crop_width = 4.0e4  # sample image is a square of width 2.0e5
    Geotiff.crop(base_image_path, crop_path, center_lon, center_lat,
                 crop_width)
    with rio.open(crop_path) as crop_file:
        crop_file_bounds = crop_file.bounds
        # Compare bounds, requiring cropped bounds to be as expected
        # within one pixel
        eps = (crop_file.bounds.right -
               crop_file.bounds.left) / crop_file.profile["width"]
        assert abs(crop_file_bounds.left - (center_x - 0.5 * crop_width)) < eps
        assert abs(crop_file_bounds.right -
                   (center_x + 0.5 * crop_width)) < eps
        assert abs(crop_file_bounds.bottom -
                   (center_y - 0.5 * crop_width)) < eps
        assert abs(crop_file_bounds.top - (center_y + 0.5 * crop_width)) < eps

        # Ensure profile is square
        assert crop_file.profile["height"] == crop_file.profile["width"]

        # Compare pixel values to those of a saved file, to ensure code changes
        # don't change the cropped output unexpectedly
        with rio.open(expected_crop_path) as expected:
            expected_array = expected.read()
            crop_array = crop_file.read()
            assert expected_array.shape == crop_array.shape
            eps_for_comparison = 1.e-15
            assert np.sum(np.abs(crop_array -
                                 expected_array)) < eps_for_comparison

        # Ensure that an identity cropping does not change the file
        crop_identity_path = temp_path + "/crop_identity.tif"
        Geotiff.crop(crop_path, crop_identity_path, center_lon, center_lat,
                     crop_width)
        with rio.open(crop_identity_path) as crop_file_identity:
            crop_file_bounds_identity = crop_file.bounds
            eps = 1.0e-6
            assert abs(crop_file_bounds_identity.left -
                       crop_file_bounds.left) < eps
            assert abs(crop_file_bounds_identity.right -
                       crop_file_bounds.right) < eps
            assert abs(crop_file_bounds_identity.bottom -
                       crop_file_bounds.bottom) < eps
            assert abs(crop_file_bounds.top - crop_file_bounds.top) < eps
            assert crop_file_identity.profile["width"] == crop_file.profile[
                "width"]
            assert crop_file_identity.profile["height"] == crop_file.profile[
                "width"]
            eps_for_identity = 1.e-15
            crop_array = crop_file.read()
            crop_array_identity = crop_file_identity.read()
            assert crop_array.shape == crop_array_identity.shape
            assert crop_file.profile == crop_file_identity.profile
            assert np.sum(np.abs(crop_array -
                                 crop_array_identity)) < eps_for_identity


def test_resample():
    """Test resampling geotiff image.
    The test i) checks that resampling with a factor of 1 does nothing, and
    ii) tests that a specific resampling has the correct metadata and agrees
    with a resampled sample image.
    """
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # Get path this script is in
    # via https://stackoverflow.com/questions/4934806/
    # how-can-i-find-scripts-directory
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Base image uses projection EPSG:5070
    base_image_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"

    resample_path = temp_path + "/resample.tif"
    resample_factor = 0.1
    Geotiff.resample(base_image_path, resample_path, 0.1, Resampling.average)

    resample_identity_path = temp_path + "/resample_identity.tif"
    Geotiff.resample(base_image_path, resample_identity_path, 1.0,
                     Resampling.average)

    with rio.open(resample_path) as resample_file:
        with rio.open(base_image_path) as base_file:
            assert base_file.profile["width"] == int(
                resample_file.profile["width"] / resample_factor)
            assert base_file.profile["height"] == int(
                resample_file.profile["height"] / resample_factor)

            with rio.open(resample_identity_path) as resample_identity_file:
                assert base_file.profile[
                    "width"] == resample_identity_file.profile["width"]
                assert base_file.profile[
                    "height"] == resample_identity_file.profile["height"]

            expected_resample_path = base_path + "/test_images/"
            expected_resample_path += "SouthNM_Elevation_10km.tif"
            with rio.open(expected_resample_path) as expected_resample_file:
                expected_array = expected_resample_file.read()
                resample_array = resample_file.read()
                eps = 1.e-15
                assert np.sum(np.abs(expected_array - resample_array)) < eps


def test_sample_from_array():
    """Test that sample_from_array produces the same results as rasterio's .sample() method."""
    base_path = os.path.dirname(os.path.realpath(__file__))
    test_image_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"

    with rio.open(test_image_path) as raster_file:
        pixel_data = raster_file.read(1)  # Read first band
        affine_transform = raster_file.transform
        nodata_value = raster_file.nodata

        bounds = raster_file.bounds
        test_coordinates = [
            (bounds.left + 1000, bounds.bottom + 1000),  # Near bottom-left
            (bounds.right - 1000, bounds.top - 1000),  # Near top-right
            (bounds.left + (bounds.right - bounds.left) / 2,
             bounds.bottom + (bounds.top - bounds.bottom) / 2),  # Center
            (bounds.left + 5000, bounds.bottom + 5000),
        ]

        outside_coordinates = [
            (bounds.left - 1000, bounds.bottom - 1000),  # Outside bottom-left
            (bounds.right + 1000, bounds.top + 1000),  # Outside top-right
        ]

        # Get samples using Geotiff.sample_from_array()
        geotiff_samples = Geotiff.sample_from_array(
            pixel_data, affine_transform, nodata_value,
            test_coordinates + outside_coordinates)

        # Get expected results using rasterio's .sample() method
        rasterio_results = []
        for sample in raster_file.sample(test_coordinates +
                                         outside_coordinates):
            rasterio_results.append(sample[0])

        # Compare results
        assert len(geotiff_samples) == len(rasterio_results)
        for i, (geotiff_sample_value, rasterio_sample_value) in enumerate(
                zip(geotiff_samples, rasterio_results)):
            assert geotiff_sample_value == rasterio_sample_value, f"Mismatch at index {i}: sample_from_array_value={geotiff_sample_value}, rasterio_sample_value={rasterio_sample_value}"

        # Test with empty coordinates list
        empty_results = Geotiff.sample_from_array(pixel_data, affine_transform,
                                                  nodata_value, [])
        assert empty_results == []

        # Test with single coordinate
        single_coord = [(bounds.left + 1000, bounds.bottom + 1000)]
        single_result = Geotiff.sample_from_array(pixel_data, affine_transform,
                                                  nodata_value, single_coord)
        assert len(single_result) == 1

        # Verify the single result matches rasterio
        single_rasterio_result = list(raster_file.sample(single_coord))[0][0]
        assert single_result[0] == single_rasterio_result


def test_geotiff_to_bsq():
    """Test that geotiff_to_bsq converts a geotiff to a band sequential binary file."""
    temp_dir = tempfile.TemporaryDirectory()
    bsq_path = temp_dir.name + "/SouthNM_Elevation_1km.bsq"
    test_image_path = os.path.dirname(
        os.path.realpath(__file__)) + "/test_images/SouthNM_Elevation_1km.tif"
    with rio.open(test_image_path) as source_geotiff:
        geotiff_metadata = {
            "crs": source_geotiff.crs,
            "transform": source_geotiff.transform,
            "shape": source_geotiff.shape,
            "dtype": source_geotiff.dtypes[0],
            "nodata": source_geotiff.nodata,
        }
        source_data = source_geotiff.read()

    Geotiff.geotiff_to_bsq(test_image_path, bsq_path)

    # Read the bsq file and compare to the original geotiff
    with rio.open(bsq_path) as bsq_file:
        bsq_data = bsq_file.read()
        bsq_metadata = {
            "crs": bsq_file.crs,
            "transform": bsq_file.transform,
            "shape": bsq_file.shape,
            "dtype": bsq_file.dtypes[0],
            "nodata": bsq_file.nodata,
        }
        assert bsq_metadata["crs"] == geotiff_metadata["crs"]
        assert bsq_metadata["shape"] == geotiff_metadata["shape"]
        assert bsq_metadata["dtype"] == geotiff_metadata["dtype"]
        assert bsq_metadata["nodata"] == geotiff_metadata["nodata"]

        transform_tolerance = 1.e-10
        assert np.allclose(bsq_metadata["transform"],
                           geotiff_metadata["transform"],
                           atol=transform_tolerance)

        # Compare data read from bsq via the source geotiff data
        assert np.array_equal(bsq_data, source_data)

    # Test direct reading of BSQ file without rasterio still gives same
    # data as the original geotiff
    bsq_array = Geotiff.read_bsq_array(bsq_path, geotiff_metadata["shape"],
                                       geotiff_metadata["dtype"])
    assert np.array_equal(bsq_array, source_data[0])


def test_read_bsq_array_errors():
    """Test error handling in read_bsq_array function."""
    temp_dir = tempfile.TemporaryDirectory()

    # Test that a non-existent file triggers the expected error
    with pytest.raises(FileNotFoundError):
        Geotiff.read_bsq_array("nonexistent.bsq", (100, 100), np.int16)

    # Test that incorrect shape (file too small) triggers an error
    small_bsq = temp_dir.name + "/small.bsq"
    with open(small_bsq, 'wb') as f:
        f.write(np.array([1, 2, 3], dtype=np.int16).tobytes())

    with pytest.raises(ValueError):
        Geotiff.read_bsq_array(small_bsq, (100, 100), np.int16)


def worker_process_for_test_shared_memory_multiprocessing(
        worker_id, shared_data_name, shape, dtype, original_data,
        affine_transform, nodata_value):
    """Worker function that runs in each subprocess."""
    try:
        # Access shared memory data
        shared_array, shm = Geotiff.get_shared_memory_array(
            shared_data_name, shape, dtype)

        # Compare shared data with original data
        assert np.array_equal(shared_array, original_data), \
            f"Worker {worker_id}: Shared memory data doesn't match original data"

        # Test sampling from shared memory data
        bounds = (shared_array.shape[1], shared_array.shape[0]
                  )  # width, height
        test_coordinates = [
            (1000, 1000),  # Near top-left
            (bounds[0] - 1000, bounds[1] - 1000),  # Near bottom-right
            (bounds[0] // 2, bounds[1] // 2),  # Center
        ]

        # Sample from shared memory data
        shared_samples = Geotiff.sample_from_array(shared_array,
                                                   affine_transform,
                                                   nodata_value,
                                                   test_coordinates)

        # Sample from original data for comparison
        original_samples = Geotiff.sample_from_array(original_data,
                                                     affine_transform,
                                                     nodata_value,
                                                     test_coordinates)

        # Compare samples
        assert shared_samples == original_samples, \
            f"Worker {worker_id}: Sampling results don't match"

        # Clean up shared memory connection
        shm.close()

        return f"Worker {worker_id}: Success"

    except Exception as e:
        return f"Worker {worker_id}: Error - {str(e)}"


def test_shared_memory_multiprocessing():
    """Test that shared memory data can be accessed by multiple processes.
    
    This test:
    1. Converts a test geotiff to BSQ format
    2. Reads the BSQ file into shared memory
    3. Reads the original geotiff using rasterio
    4. Starts a process pool with 4 subprocesses
    5. Each subprocess accesses the shared data and compares it to the original
    """
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # Get path to test image
    base_path = os.path.dirname(os.path.realpath(__file__))
    test_image_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
    bsq_path = temp_path + "/test_elevation.bsq"

    # Convert geotiff to BSQ
    Geotiff.geotiff_to_bsq(test_image_path, bsq_path)

    # Read BSQ into shared memory
    shared_info = Geotiff.read_bsq_to_shared_memory(bsq_path)

    # Read original geotiff for comparison
    with rio.open(test_image_path) as geofile:
        original_data = geofile.read(1)  # Read first band

    # Start process pool with 4 workers
    with ProcessPoolExecutor(max_workers=4) as executor:
        # Submit tasks to all workers
        futures = []
        for i in range(4):
            future = executor.submit(
                worker_process_for_test_shared_memory_multiprocessing, i,
                shared_info['shared_data_name'], shared_info['shape'],
                shared_info['dtype'], original_data,
                shared_info['affine_transform'], shared_info['nodata_value'])
            futures.append(future)

        # Collect results
        results = [future.result() for future in futures]

    # Check that all workers succeeded
    for result in results:
        assert "Success" in result, f"Worker failed: {result}"

    # Clean up shared memory
    try:
        shm = shared_memory.SharedMemory(name=shared_info['shared_data_name'])
        shm.close()
        shm.unlink()
    except:
        pass  # Shared memory might already be cleaned up by workers
