# Distributed under the MIT License.
# See LICESNSE for details.
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import rasterio as rio
from tqdm import tqdm

from CosmicExplorerSiteSearch import Coordinates, Detector, Score


def evaluate_region(x_center, y_center, width_meters, height_meters,
                    grid_downsample_factor, arm_length_meters,
                    dl_for_arms_meters, opening_angles, rotation_angles,
                    rasters, max_total_score_for_L_out, path_for_output,
                    njobs):
    """Evaluate the suitability of a 2D grid of detectors placed in a 
    rectangular region such that they are evenly spaced horizontally
    and vertically. Uses the projection of the provided elevation map for
    outputting results to geotiff and shapefiles.
    Input:
      x_center: center of the rect search region (meters)
      y_center: center of the rect search region (meters)
      width_meters: width of search region
      height_meters: height of search region
      grid_downsample_factor: integer N; vertexes are placed every N pixels on
                              those pixels within the rectangular search region.
      arm_length_meters: length of each detector's arms
      dl_for_arms_meters: spacing between sample points on the detector arms
      opening_angles: numpy array of opening angles to consider
      rotation_angles: numpy array of rotation angles to consider
      rasters: dictionary with paths to rasters to consider. Must contain
               keys required by Score.suitability_scores(), including
               "elevation." The value of each key is a string containing a
               path to the raster's geotiff file.
      max_total_score_for_L_out: output to .shp file detector L's with scores
                                 no larger than this. Only the best L with a
                                 given vertex x,y position will be output.
      path_for_output: string pointing to a directory where output will be
                       written (must exist).
      njobs: number of jobs to run in parallel
    Output:
      * One geotiff for each score returned for each detector, with pixel
        values equal to the best score at each x,y point, maximizing over
        opening angles and rotation angles. Uses the projection of the provided
        elevaiton raster.
      * One ESRI shape file containing each L with scores no larger than
        max_total_score_for_L_out.
      * One ASCII CSV file containing the detector parameters and scores
        for the best detector at each x,y location, maximizing over 
        opening angles and rotation angles.
    """
    # First, open the elevation file to get dimensions of the input rasters.
    elevation_file = rio.open(rasters["elevation"])

    # Check the desired bounds for the search
    # Start by getting the bounds of the file, and then reducing them by
    # 1.01% of the arm length, to ensure the arms never hit the edge of the
    # raster
    file_bounds = elevation_file.bounds
    bounds_safety_length_meters = arm_length_meters * 1.01
    max_bounds = rio.coords.BoundingBox(
        left=file_bounds.left + bounds_safety_length_meters,
        bottom=file_bounds.bottom + bounds_safety_length_meters,
        right=file_bounds.right - bounds_safety_length_meters,
        top=file_bounds.top - bounds_safety_length_meters)

    # Get the desired bounds, either those specified or max_bounds, whichever
    # enclose the smallest area.
    left_desired = np.max([x_center - 0.5 * width_meters, max_bounds.left])
    bottom_desired = np.max(
        [y_center - 0.5 * height_meters, max_bounds.bottom])
    right_desired = np.min([x_center + 0.5 * width_meters, max_bounds.right])
    top_desired = np.min([y_center + 0.5 * height_meters, max_bounds.top])

    # For consistency with the input rasters, reset the desired grid bounds to
    # the elevation map's pixel coordinates
    bounds_rows, bounds_cols = rio.transform.rowcol(
        elevation_file.transform, [left_desired, right_desired],
        [bottom_desired, top_desired])
    bounds_xs, bounds_ys = rio.transform.xy(elevation_file.transform,
                                            bounds_rows, bounds_cols)
    detector_xmin, detector_xmax = bounds_xs[0], bounds_xs[1]
    detector_ymin, detector_ymax = bounds_ys[0], bounds_ys[1]

    # The bounds for output geotiffs are half a pixel width different from
    # the coordinate bounds, since the coordinates come from the pixel center
    x_half_pixel_size = 0.5 * elevation_file.transform[0]
    y_half_pixel_size = -0.5 * elevation_file.transform[4]
    elevation_file.close()
    bounds = rio.coords.BoundingBox(left=detector_xmin - x_half_pixel_size,
                                    bottom=detector_ymin - y_half_pixel_size,
                                    right=detector_xmax + x_half_pixel_size,
                                    top=detector_ymax + y_half_pixel_size)

    # Generate grid of x's and y's for detector center
    detector_spacing = 2.0 * x_half_pixel_size * np.round(
        grid_downsample_factor)
    detector_xs = np.arange(detector_xmin, detector_xmax + detector_spacing,
                            detector_spacing)
    detector_ys = np.arange(detector_xmin, detector_xmax + detector_spacing,
                            detector_spacing)
    grid_cols = detector_xs.shape[0]
    grid_rows = detector_ys.shape[0]
    number_of_opening_angles = np.shape(opening_angles)[0]
    number_of_rotation_angles = np.shape(rotation_angles)[0]

    raster_files = {
        "elevation": rio.open(rasters["elevation"]),
        "landcover": rio.open(rasters["landcover"])
    }

    # Set up arrays to hold the results
    # Keys should match keys in dict returned by Score.score_detector_from_grid
    result = {
        "opening_angle_degrees":
        np.zeros((number_of_opening_angles, number_of_rotation_angles,
                  grid_rows, grid_cols)),
        "rotation_angle_degrees":
        np.zeros((number_of_opening_angles, number_of_rotation_angles,
                  grid_rows, grid_cols)),
        "vertex_x":
        np.zeros((number_of_opening_angles, number_of_rotation_angles,
                  grid_rows, grid_cols)),
        "vertex_y":
        np.zeros((number_of_opening_angles, number_of_rotation_angles,
                  grid_rows, grid_cols)),
        "elevation_score":
        np.zeros((number_of_opening_angles, number_of_rotation_angles,
                  grid_rows, grid_cols)),
        "tilt_score":
        np.zeros((number_of_opening_angles, number_of_rotation_angles,
                  grid_rows, grid_cols)),
        "landcover_score":
        np.zeros((number_of_opening_angles, number_of_rotation_angles,
                  grid_rows, grid_cols)),
        "total_score":
        np.zeros((number_of_opening_angles, number_of_rotation_angles,
                  grid_rows, grid_cols)),
    }

    # Set up a pool
    pool = ProcessPoolExecutor(njobs)
    futures = [
        pool.submit(Score.score_detector_from_grid, raster_files,
                    arm_length_meters, dl_for_arms_meters, opening_angle,
                    rotation_angle, x, y, i, j, row, col)
        for i, opening_angle in enumerate(opening_angles)
        for j, rotation_angle in enumerate(rotation_angles)
        for row, y in enumerate(detector_ys)
        for col, x in enumerate(detector_xs)
    ]
    for future in tqdm(as_completed(futures), total=len(futures)):
        score = future.result()
        i = score["opening_angle_i"]
        j = score["rotation_angle_j"]
        row = score["vertex_row"]
        col = score["vertex_col"]

        result["opening_angle_degrees"][i][j][row][col] = result[
            "opening_angle_degrees"]
        result["rotation_angle_degrees"][i][j][row][col] = result[
            "rotation_angle_degrees"]
        result["vertex_x"][i][j][row][col] = result["vertex_x"]
        result["vertex_y"][i][j][row][col] = result["vertex_y"]
        result["elevation_score"][i][j][row][col] = result["elevation_score"]
        result["tilt_score"][i][j][row][col] = result["tilt_score"]
        result["landcover_score"][i][j][row][col] = result["landcover_score"]
        result["total_score"][i][j][row][col] = result["total_score"]

    # Output geotiffs
    out_profile = raster_files["elevation"].profile
    out_transform = rio.transform.from_bounds(bounds.left, bounds.bottom,
                                              bounds.right, bounds.top,
                                              grid_cols, grid_rows)
    out_profile.update(width=grid_cols,
                       height=grid_rows,
                       transform=out_transform)
    with rio.open(path_for_output + "/elevation_score.tif", "w",
                  **out_profile) as out_geofile:
        out_geofile.write(result["elevation_score"])
    with rio.open(path_for_output + "/tilt_score.tif", "w",
                  **out_profile) as out_geofile:
        out_geofile.write(result["tilt_score"])
    with rio.open(path_for_output + "/landcover_score.tif", "w",
                  **out_profile) as out_geofile:
        out_geofile.write(result["landcover_score"])
    with rio.open(path_for_output + "/total_score.tif", "w",
                  **out_profile) as out_geofile:
        out_geofile.write(result["total_score"])

    # Output ascii
    detectors = []
    legend = "#opening_angle rotation_angle vertex_x vertex_y elevation_score"
    legend += " tilt_score landcover_score total_score\n"
    with open(path_for_output + "/scores.csv", "w") as out_ascii:
        out_ascii.write(legend)
        for i, opening_angle in enumerate(opening_angles):
            for j, rotation_angle in enumerate(rotation_angles):
                for row, y in enumerate(detector_ys):
                    for col, x in enumerate(detector_xs):
                        row_text = ""
                        row_text += str(result["opening_angle_degrees"][i][j]
                                        [row][col]) + " "
                        row_text += str(result["rotation_angle_degrees"][i][j]
                                        [row][col]) + " "
                        row_text += str(
                            result["vertex_x"][i][j][row][col]) + " "
                        row_text += str(
                            result["vertex_y"][i][j][row][col]) + " "
                        row_text += str(
                            result["elevation_score"][i][j][row][col]) + " "
                        row_text += str(
                            result["tilt_score"][i][j][row][col]) + " "
                        row_text += str(
                            result["landcover_score"][i][j][row][col]) + " "
                        row_text += str(
                            result["total_score"][i][j][row][col]) + "\n"
                        out_ascii.write(row_text)

                        if result["total_score"] <= max_total_score_for_L_out:
                            detectors.append(
                                Detector.detector(arm_length_meters,
                                                  dl_for_arms_meters,
                                                  opening_angles[i],
                                                  rotation_angles[j],
                                                  detector_xs[col],
                                                  detector_ys[row]))

    # Finally, write the shape file
    Detector.write_shapefile_of_detectors(
        detectors, path_for_output + "/best_detectors.shp")


def evaluate_region_lon_lat(lon_center, lat_center, width_meters,
                            height_meters, grid_downsample_factor,
                            arm_length_meters, dl_for_arms_meters,
                            opening_angles, rotation_angles, rasters,
                            max_total_score_for_L_out, path_for_output, njobs):
    """Wrapper for evaluate_region() that takes lon, lat instead of x,y for the
    center of the rectangular search region.
    Input:
      lon_center: longitude of center of the search region in decimal degrees
      lat_center: latitude of center of the search region in decimal degrees
      See help text of evaluate_region() for other parameters
    Output:
      Same as output of evaluate_region().
    """
    # First, open the elevation raster to get the projection to xy
    elevation_file = rio.open(rasters["elevation"])
    x_center, y_center = Coordinates.lonlat_to_xy(lon_center, lat_center,
                                                  elevation_file.crs.wkt)
    return evaluate_region(x_center, y_center, width_meters, height_meters,
                           grid_downsample_factor, arm_length_meters,
                           dl_for_arms_meters, opening_angles, rotation_angles,
                           rasters, max_total_score_for_L_out, path_for_output,
                           njobs)


helptext = """Evaluate the suitability of a 2D grid of detectors placed in a 
    rectangular region such that they are evenly spaced horizontally
    and vertically. Uses the projection of the provided elevation map for
    outputting results to geotiff and shapefiles.
"""

if __name__ == '__main__':
    p = argparse.ArgumentParser(prog='cess-find-sites', description=helptext)
    p.add_argument(
        '--lon',
        type=float,
        help="Longitude of center of search region (decimal degrees)")
    p.add_argument(
        '--lat',
        type=float,
        help="Latitude of center of search region (decimal degrees)")
    p.add_argument('--width',
                   type=float,
                   help="Width of search region (meters)")
    p.add_argument('--height',
                   type=float,
                   help="Height of search region (meters)")
    p.add_argument('--N',
                   type=int,
                   help="vertex spacing = every N pixels of elevation raster")
    p.add_argument('--arm_length',
                   type=float,
                   help="Detector arm length (meters)")
    p.add_argument('--dl',
                   type=float,
                   help="Spacing between sample points on arms")
    p.add_argument('--opening-angle',
                   type=float,
                   nargs='+',
                   help="One or more opening angles")
    p.add_argument('--rotation-angle',
                   type=float,
                   nargs='+',
                   help="One or more rotation angles")
    p.add_argument('--elevation', help="Path to elevation geotiff")
    p.add_argument('--landcover', help="Path to landcover geotiff")
    p.add_argument('--outscore',
                   type=float,
                   help="Output detector L's if total score < max_score")
    p.add_argument('--outdir', help="Path to output directory (must exist)")
    p.add_argument('--njobs',
                   type=int,
                   help="Number of jobs to run in parallel")
    args = p.parse_args()

    rasters = {"elevation": args.elevation, "landcover": args.landcover}
    evaluate_region_lon_lat(args.lon, args.lat, args.width, args.height,
                            args.N, args.arm_length, args.dl,
                            np.array(args.opening_angle),
                            np.array(args.rotation_angle), rasters,
                            args.outscore, args.outdir, args.njobs)
