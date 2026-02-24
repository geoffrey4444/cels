# Distributed under the MIT License.
# See LICENSE for details.

import csv
import fiona
import numpy as np
import os
from pyproj import CRS
import subprocess
import rasterio as rio
import tempfile

def test_findsites():
  # Test run using sample data
  # Make a temporary directory
  temp_dir = tempfile.TemporaryDirectory()
  temp_path = temp_dir.name
  base_path = os.path.dirname(os.path.realpath(__file__))
  find_sites_path = "findsites"
  elevation_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
  landcover_path = base_path + "/test_images/SouthNM_Landcover_1km.tif"
  land_acquisition_path = base_path + "/test_images/SouthNM_LandAcquisition_1km.tif"
  roads_path = base_path + "/test_images/SouthNM_Roads_1km.shp"

  print("Running test in " + temp_path)

  # For testing purposes, do a search at the center of the landcover and
  # elevation images in test_images, which are 1km resolution.
  # Lay down a grid of 10 x 10 vertex locations.
  # The outscore is 200.0 in order to ensure Ls are returned with
  # the added road crossing costs.

  lon = -107.7
  lat = 32.3
  width = 100000.0  # width of search region is 100km = 100 pixels
  height = 40000.0  # height of search region is 40km
  vertex_spacing = 10  # grid of detectors spaced every 10 km
  arm_length = 40000.0  # meters
  dl_for_arms = 1000.0  # meters
  opening_angle = 90.0
  rotation_angles = 18 
  outscore = 200.0 #The score threshold in million USD.

  args = [
      find_sites_path, f"--lon={lon}", f"--lat={lat}", f"--width={width}",
      f"--height={height}", f"--N={vertex_spacing}",
      f"--arm_length={arm_length}", f"--dl={dl_for_arms}",
      f"--opening-angle={opening_angle}", f"--rotation-angles={rotation_angles}",
      f"--elevation={elevation_path}", f"--landcover={landcover_path}",
      f"--land_acquisition={land_acquisition_path}",
      f"--roads={roads_path}", f"--outscore={outscore}",
      f"--outdir={temp_path}", f"--njobs=2"
  ]
  print(f"Starting search in path: {temp_path}")
  print(" ".join(args))
  subprocess.run(args)

  # Checks that all expected output files exist in the temporary directory
  expected_files = [
      'elevation_score.tif', 'best_detectors.prj', 'total_score.tif',
      'best_detectors.dbf', 'scores.csv', 'landcover_score.tif',
      'best_detectors.shp', 'best_detectors.cpg', 'tilt_score.tif',
      'best_detectors.shx'
  ]
  output_file_names = os.listdir(temp_path)
  for name in expected_files:
    print(name)
    assert name in output_file_names

    # If tif file, do some sanity checks
    if name.split(".")[-1] == "tif":
      geofile = rio.open(temp_path + "/" + name)
      # Searching a 100 x 40 pixel region, skipping every 10 pixels,
      # so there should be (100/10 + 1) pixels wide and (40/10 + 1) pixels high
      # in the geotiffs
      assert geofile.profile["width"] == 11
      assert geofile.profile["height"] == 5

      # Check properties the geotiff should have in common with the test images
      assert geofile.profile["nodata"] == 32767.0
      assert geofile.profile["crs"] == CRS.from_epsg(5070)

      # Each geofile should have 1 float dataset in it
      assert geofile.profile["count"] == 1
      assert geofile.profile["dtype"] == 'float32'

      # Check that sane scores were written: mean should be between 0, 32767
      average_score = np.average(geofile.read())
      assert average_score > 0
      assert average_score < 32767
      geofile.close()

    elif name.split(".")[-1] == "shp":
      shapefile = fiona.open(temp_path + "/" + name)
      assert len(shapefile) > 0
      for i, ell in enumerate(shapefile):
        # check that the score is in the expected range
        assert ell.properties["tot_score"] > 0
        assert ell.properties["tot_score"] < outscore
        # check that the detector arm length is as expected
        assert ell.properties["arm_length"] == arm_length
      shapefile.close()

    elif name.split(".")[-1] == "csv":
      csvfile = open(temp_path + "/" + name)
      reader = csv.reader(csvfile, delimiter=' ')
      rows = 0
      for row in reader:
        rows += 1
        assert len(row) == 10
      assert rows > 2 # if search succeeded, at least header + 1 row
      csvfile.close()


def test_findsites_with_shared_memory():
  # Test run using sample data with shared memory
  # Make a temporary directory
  temp_dir = tempfile.TemporaryDirectory()
  temp_path = temp_dir.name
  base_path = os.path.dirname(os.path.realpath(__file__))
  find_sites_path = "findsites"
  elevation_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
  landcover_path = base_path + "/test_images/SouthNM_Landcover_1km.tif"
  land_acquisition_path = base_path + "/test_images/SouthNM_LandAcquisition_1km.tif"
  roads_path = base_path + "/test_images/SouthNM_Roads_1km.shp"


  print("Running shared memory test in " + temp_path)

  # Convert geotiffs to BSQ files for shared memory test
  elevation_bsq_path = temp_path + "/elevation.bsq"
  landcover_bsq_path = temp_path + "/landcover.bsq"
  land_acquisition_bsq_path = temp_path + "/land_acquisition.bsq"
  
  import CosmicExplorerLocationSearch.Geotiff as Geotiff
  Geotiff.geotiff_to_bsq(elevation_path, elevation_bsq_path)
  Geotiff.geotiff_to_bsq(landcover_path, landcover_bsq_path)
  Geotiff.geotiff_to_bsq(land_acquisition_path, land_acquisition_bsq_path)

  # For testing purposes, do a search at the center of the landcover and
  # elevation images in test_images, which are 1km resolution.
  # Lay down a grid of 10 x 10 vertex locations
  lon = -107.7
  lat = 32.3
  width = 100000.0  # width of search region is 100km = 100 pixels
  height = 40000.0  # height of search region is 40km
  vertex_spacing = 10  # grid of detectors spaced every 10 km
  arm_length = 40000.0  # meters
  dl_for_arms = 1000.0  # meters
  opening_angle = 90.0
  rotation_angles = 36
  outscore = 200.0

  args = [
      find_sites_path, f"--lon={lon}", f"--lat={lat}", f"--width={width}",
      f"--height={height}", f"--N={vertex_spacing}",
      f"--arm_length={arm_length}", f"--dl={dl_for_arms}",
      f"--opening-angle={opening_angle}", f"--rotation-angles=18",
      f"--elevation={elevation_bsq_path}", f"--landcover={landcover_bsq_path}",
      f"--land_acquisition={land_acquisition_bsq_path}",
      f"--outscore={outscore}", f"--outdir={temp_path}", f"--njobs=2",
      f"--roads={roads_path}", "--use-shared-memory"
  ]
  print(f"Starting shared memory search in path: {temp_path}")
  print(" ".join(args))
  subprocess.run(args)

  # Checks that all expected output files exist in the temporary directory
  expected_files = [
      'elevation_score.tif', 'best_detectors.prj', 'total_score.tif',
      'best_detectors.dbf', 'scores.csv', 'landcover_score.tif',
      'best_detectors.shp', 'best_detectors.cpg', 'tilt_score.tif',
      'best_detectors.shx'
  ]
  output_file_names = os.listdir(temp_path)
  for name in expected_files:
    print(name)
    assert name in output_file_names

    # If tif file, do some sanity checks
    if name.split(".")[-1] == "tif":
      geofile = rio.open(temp_path + "/" + name)
      # Searching a 100 x 40 pixel region, skipping every 10 pixels,
      # so there should be (100/10 + 1) pixels wide and (40/10 + 1) pixels high
      # in the geotiffs
      assert geofile.profile["width"] == 11
      assert geofile.profile["height"] == 5

      # Check properties the geotiff should have in common with the test images
      assert geofile.profile["nodata"] == 32767.0
      assert geofile.profile["crs"] == CRS.from_epsg(5070)

      # Each geofile should have 1 float dataset in it
      assert geofile.profile["count"] == 1
      assert geofile.profile["dtype"] == 'float32'

      # Check that sane scores were written: mean should be between 0, 32767
      average_score = np.average(geofile.read())
      assert average_score > 0
      assert average_score < 32767
      geofile.close()

    elif name.split(".")[-1] == "shp":
      shapefile = fiona.open(temp_path + "/" + name)
      assert len(shapefile) > 0
      for i, ell in enumerate(shapefile):
        # check that the score is in the expected range
        assert ell.properties["tot_score"] > 0
        assert ell.properties["tot_score"] < outscore
        # check that the detector arm length is as expected
        assert ell.properties["arm_length"] == arm_length
      shapefile.close()

    elif name.split(".")[-1] == "csv":
      csvfile = open(temp_path + "/" + name)
      reader = csv.reader(csvfile, delimiter=' ')
      rows = 0
      for row in reader:
        rows += 1
        assert len(row) == 10
      assert rows > 2 # if search succeeded, at least header + 1 row
      csvfile.close()
