import numpy as np
import geopandas as gpd
import os
import subprocess
from CosmicExplorerLocationSearch.TestHelpers import random_detector, random_scores
import tempfile
import shapely
from shapely.geometry import Point, Polygon, mapping
import fiona

def test_getmoreLs():
  random_detectors = []
  random_detectors_scores = []
  temp_dir = tempfile.TemporaryDirectory()
  temp_path = temp_dir.name
  path_getmoreLs = "getmoreLs"
  scores_path = temp_path + "/scores.csv"
  ordered_scores_path = temp_path + "/ordered_scores.csv"

  print("Running test in " + temp_path)

  #Generating a polygon
  polygon_coords = ((250000,250000),(250000,750000),(750000,750000),(750000,250000),(250000,250000))
  polygon = shapely.Polygon(polygon_coords)
  metadata_schema = {
    'geometry': 'Polygon', 
    'properties': {'name': 'str'},
  }
  area_shp_path = temp_path + '/TestArea.shp'

  #Write the polygon to a Shapefile:
  with fiona.open(area_shp_path, 
                'w', 'ESRI Shapefile', metadata_schema) as f:
      f.write({'geometry': mapping(polygon),
             'properties': {'name': 'TestArea'},})

  coords = np.random.rand(500,2)*1e6

  for c in coords:
      detector_score = random_scores()
      random_detectors_scores.append(detector_score['total_score'])
      random_detectors.append(random_detector(scores=detector_score,center=c))
  with open(scores_path, "w") as out_ascii:
      legend = "#opening_angle rotation_angle vertex_x vertex_y elevation_score"
      legend += " tilt_score landcover_score roads_score total_score\n"
      out_ascii.write(legend)
      for result in random_detectors:
          row_text = ""
          row_text += str(result[-1]["opening_angle_degrees"]) + " "
          row_text += str(result[-1]["rotation_angle_degrees"]) + " "
          row_text += str(
              result[-1]["vertex_x"]) + " "
          row_text += str(
              result[-1]["vertex_y"]) + " "
          row_text += str(
              result[-1]["scores"]["elevation_score"]) + " "
          row_text += str(
              result[-1]["scores"]["tilt_score"]) + " "
          row_text += str(
              result[-1]["scores"]["landcover_score"]) + " "
          row_text += str(
              result[-1]["scores"]["roads_score"]) + " "
          row_text += str(
              result[-1]["scores"]["total_score"]) + "\n"
          out_ascii.write(row_text)
  os.system(f"sort -t ' ' -k9n {scores_path} > {ordered_scores_path}")

  expected_scores_files = [
     "scores.csv",
     "ordered_scores.csv"
  ]

  #Check that the ordered csv exists
  scores_output_names = os.listdir(temp_path)
  for name in expected_scores_files:
    assert name in scores_output_names

  score_threshold = 1000.0
  minimum_score = 0.0
  maximum_score = 10000.0

  if np.all(np.array(random_detectors_scores)>score_threshold):
      print("Warning: no Ls below score threshold")

  #random_scores() returns a score between 0 and 3000 so a threshold of 1000
  #will normally return some but not all Ls. Minimum and maximum scores are 
  #edge test cases that should return none (0.0) or all (10000.0) generated Ls.
  area_name = "TestArea"

  args = [
      path_getmoreLs, f"--threshold={score_threshold}",
      f"--blob={area_name}", 
      f"--scores_csv={ordered_scores_path}",
      f"--outdir_path={temp_path}",
      f"--shapefile={area_shp_path}",
    ]

  print(f"Starting search in path: {temp_path}")
  print(" ".join(args))
  subprocess.run(args)

  # Checks that all expected output files exist in the temporary directory
  expected_files = [
      f"detectors_leq_{score_threshold}_{area_name}.cpg",
      f"detectors_leq_{score_threshold}_{area_name}.dbf",
      f"detectors_leq_{score_threshold}_{area_name}.prj",
      f"detectors_leq_{score_threshold}_{area_name}.shp",
      f"detectors_leq_{score_threshold}_{area_name}.shx"
    ]
  
  output_file_names = os.listdir(temp_path)
  for name in expected_files:
    assert name in output_file_names

  #Checking that all detectors in shapefile are within boundaries
  #of polygon and are below the chosen score threshold
  area = gpd.read_file(area_shp_path)
  shapefile = fiona.open(temp_path + f"/detectors_leq_{score_threshold}_{area_name}.shp")
  assert len(shapefile) > 0
  for i, ell in enumerate(shapefile):
        # check that the score is in the expected range
        assert ell.properties["tot_score"] > 0
        assert ell.properties["tot_score"] < score_threshold
        # check that the detector vertex is within polygon
        assert area.contains(Point(ell.properties["vert_x"],
                            ell.properties["vert_y"])).any()
  shapefile.close()

  #Edge cases with minimum and maximum scores 
  args_min = [
      path_getmoreLs, f"--threshold={minimum_score}",
      f"--blob={area_name}", 
      f"--scores_csv={ordered_scores_path}",
      f"--outdir_path={temp_path}",
      f"--shapefile={area_shp_path}",
    ]
  
  args_max = [
        path_getmoreLs, f"--threshold={maximum_score}",
        f"--scores_csv={ordered_scores_path}",
        f"--outdir_path={temp_path}",
    ]
  
  print(f"Starting minimum score search in path: {temp_path}")
  print(" ".join(args_min))
  subprocess.run(args_min)

  # Checks that all expected output files exist in the temporary directory
  expected_files = [
      f"detectors_leq_{minimum_score}_{area_name}.cpg",
      f"detectors_leq_{minimum_score}_{area_name}.dbf",
      f"detectors_leq_{minimum_score}_{area_name}.prj",
      f"detectors_leq_{minimum_score}_{area_name}.shp",
      f"detectors_leq_{minimum_score}_{area_name}.shx"
    ]
  
  output_file_names = os.listdir(temp_path)
  for name in expected_files:
    assert name in output_file_names

  #Checking that no detectors are returned in the shapefile
  shapefile = fiona.open(temp_path + f"/detectors_leq_{minimum_score}_{area_name}.shp")
  assert len(shapefile) == 0
  shapefile.close()
  
  
  print(f"Starting maximum score search in path: {temp_path}")
  print(" ".join(args_max))
  subprocess.run(args_max)

  # Checks that all expected output files exist in the temporary directory
  expected_files = [
      f"detectors_leq_{maximum_score}_national.cpg",
      f"detectors_leq_{maximum_score}_national.dbf",
      f"detectors_leq_{maximum_score}_national.prj",
      f"detectors_leq_{maximum_score}_national.shp",
      f"detectors_leq_{maximum_score}_national.shx"
    ]

  output_file_names = os.listdir(temp_path)
  for name in expected_files:
    assert name in output_file_names

  #Checking that all detectors are returned in the shapefile
  shapefile = fiona.open(temp_path + f"/detectors_leq_{maximum_score}_national.shp")
  assert len(shapefile)/2 == len(random_detectors_scores)
  #Divided by 2 as shapefile divides Ls into x and y arms
  shapefile.close()

