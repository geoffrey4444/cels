import argparse
from CosmicExplorerLocationSearch import Detector
from CosmicExplorerLocationSearch.Coordinates import xy_to_lonlat
import csv
import geopandas as gpd
from shapely import Point

def get_more_Ls(score_threshold, csvpath, outdir_path, arm_length, dl_arms, blob, state_name, shapefile):

    if blob:
        assert state_name == None, "State name and blob shouldn't both be specified"
        area_name = blob
        area = gpd.read_file(shapefile)
        detectors = []
    
        with open (csvpath) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=' ')
            for row in reader:
                if float(row["total_score"]) > score_threshold:
                    break
                lon,lat = float(row["vertex_x"]), float(row["vertex_y"])
                point_lonlat = Point(lon,lat) 
                if area.contains(point_lonlat).any():
                    scores = {"elevation_score": float(row["elevation_score"]),
                          "tilt_score": float(row["tilt_score"]),
                          "landcover_score": float(row["landcover_score"]),
                          "total_score": float(row["total_score"])}
                    detectors.append(Detector.detector(arm_length, dl_arms, 
                                 float(row["#opening_angle"]),
                                 float(row["rotation_angle"]),
                                 float(row["vertex_x"]), 
                                 float(row["vertex_y"]),
                                 scores=scores))
                continue

    elif state_name:
        states = gpd.read_file(shapefile)
        area_name = state_name
        state = states[states['NAME']==state_name]
        detectors = []
    
        with open (csvpath) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=' ')
            for row in reader:
                if float(row["total_score"]) > score_threshold:
                    break
                lon,lat = xy_to_lonlat(float(row["vertex_x"]), float(row["vertex_y"]), 5070)
                point_lonlat = Point(lon,lat)
                if state.contains(point_lonlat).any():
                    scores = {"elevation_score": float(row["elevation_score"]),
                          "tilt_score": float(row["tilt_score"]),
                          "landcover_score": float(row["landcover_score"]),
                          "total_score": float(row["total_score"])}
                    detectors.append(Detector.detector(arm_length, dl_arms, 
                                 float(row["#opening_angle"]),
                                 float(row["rotation_angle"]),
                                 float(row["vertex_x"]), 
                                 float(row["vertex_y"]),
                                 scores=scores))

                continue
    else:
        area_name = 'national'
        detectors = []
        with open (csvpath) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=' ')
            for row in reader:
                if float(row["total_score"]) > score_threshold:
                    break
                scores = {"elevation_score": float(row["elevation_score"]),
                          "tilt_score": float(row["tilt_score"]),
                          "landcover_score": float(row["landcover_score"]),
                          "total_score": float(row["total_score"])}
                detectors.append(Detector.detector(arm_length, dl_arms, 
                                 float(row["#opening_angle"]),
                                 float(row["rotation_angle"]),
                                 float(row["vertex_x"]), 
                                 float(row["vertex_y"]),
                                 scores=scores))
                continue
             
    Detector.write_shapefile_of_detectors(detectors, f"{outdir_path}/detectors_leq_{score_threshold}_{area_name}.shp")


def main():
    helptext = """Outputs a shapefile with detectors with a total score better than a user-provided threshold for a given search area
    """
    
    p = argparse.ArgumentParser(prog = 'GetMoreLs', description = helptext)
    p.add_argument(
        '--state', 
        type = str, 
        help = "Name of the state",
        default = None)
    p.add_argument(
        '--threshold',
        type = float,
        help = "Detector threshold. The shapefile will include all detectors from the scores csv file with total score less than or equal to the score threshold.")
    p.add_argument(
        '--scores_csv',
        type = str,
        help = "Path to ordered output scores.csv file from FindSites")
    p.add_argument(
        '--blob',
        type = str,
        help = "Name of area appended to output file when reading in an arbitrary shapefile instead of a shapefile containing US state boundaries",
        default = None)
    p.add_argument(
        '--shapefile',
        type = str,
        help = "Path to shapefile for state or blob boundaries",
        default = None)
    p.add_argument(
        '--outdir_path',
        type = str,
        help = "Output directory")
    p.add_argument(
        '--arm_length_meters',
        type = float,
        help = "Length of interferometer arms in meters",
        default = 40000.0)
    p.add_argument(
        '--dl_arms_meters',
        type = float,
        help = "dL of interferometer arms in meters",
        default = 100.0)
    args = p.parse_args()
    print(args)
    
    get_more_Ls(args.threshold, args.scores_csv, args.outdir_path, args.arm_length_meters, args.dl_arms_meters, args.blob, args.state, args.shapefile)

if __name__ == '__main__':
    main()
