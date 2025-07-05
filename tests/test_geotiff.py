# Distributed under the MIT License.
# See LICENSE for details.
from affine import Affine
import numpy as np
import os
import rasterio as rio
from rasterio.enums import Resampling
import tempfile

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
            assert np.sum(
                np.abs(crop_array - expected_array)) < eps_for_comparison

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
            assert np.sum(
                np.abs(crop_array - crop_array_identity)) < eps_for_identity


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


def test_bilinear_interpolation_matches_rasterio_sample():
    """Test that our bilinear interpolation function matches rasterio.sample() behavior."""
    # Make a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_path = temp_dir.name

    # Get path this script is in
    base_path = os.path.dirname(os.path.realpath(__file__))

    # Use the existing test image
    base_image_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"

    with rio.open(base_image_path) as geofile:
        # Read the raster data into memory
        array = geofile.read(1)  # Read first band
        transform = geofile.transform
        nodata = geofile.nodata

        # Create test coordinates - mix of pixel centers and fractional positions
        # to test interpolation behavior
        bounds = geofile.bounds

        # Test coordinates: some at pixel centers, some at fractional positions
        test_coords = np.array([
            # Pixel center coordinates (should give exact pixel values)
            [bounds.left + 1000, bounds.bottom + 1000],  # Near bottom-left
            [bounds.right - 1000, bounds.top - 1000],  # Near top-right

            # Fractional coordinates (should interpolate)
            [bounds.left + 1500, bounds.bottom + 1500],  # Between pixels
            [bounds.right - 1500, bounds.top - 1500],  # Between pixels

            # Edge cases
            [bounds.left, bounds.bottom],  # Exact edge
            [bounds.right, bounds.top],  # Exact edge
        ])

        # Get values using rasterio.sample()
        rasterio_values = np.array(
            [sample[0] for sample in geofile.sample(test_coords)])

        # Get values using our bilinear interpolation function        
        inv_transform = ~transform
        pixel_coords = np.array(
            [inv_transform * (x, y) for x, y in test_coords])
        cols_f = pixel_coords[:, 0]
        rows_f = pixel_coords[:, 1]
        row_floor = np.floor(rows_f).astype(int)
        col_floor = np.floor(cols_f).astype(int)
        row_ceil = row_floor + 1
        col_ceil = col_floor + 1
        row_weight = rows_f - row_floor
        col_weight = cols_f - col_floor

        our_values = Geotiff.bilinear_interpolate_vectorized(array,
                                                             test_coords,
                                                             transform,
                                                             nodata=nodata)

        # Compare results
        eps = 1e-10  # Small tolerance for floating point differences
        assert np.allclose(rasterio_values, our_values, rtol=eps, atol=eps), \
            f"Interpolation mismatch: rasterio={rasterio_values}, ours={our_values}"

        # Test with a larger set of random coordinates
        np.random.seed(42)  # For reproducible results
        num_random_points = 100
        random_coords = np.column_stack([
            np.random.uniform(bounds.left, bounds.right, num_random_points),
            np.random.uniform(bounds.bottom, bounds.top, num_random_points)
        ])

        # Get values using rasterio.sample()
        rasterio_random_values = np.array(
            [sample[0] for sample in geofile.sample(random_coords)])

        # Get values using our bilinear interpolation function
        our_random_values = Geotiff.bilinear_interpolate_vectorized(
            array, random_coords, transform, nodata=nodata)

        # Compare random results
        assert np.allclose(rasterio_random_values, our_random_values, rtol=eps, atol=eps), \
            f"Random interpolation mismatch: max diff = {np.max(np.abs(rasterio_random_values - our_random_values))}"
