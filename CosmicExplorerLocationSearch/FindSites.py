# Distributed under the MIT License.
# See LICENSE for details.
import argparse
from datetime import datetime
import itertools
import numpy as np
import rasterio as rio
import sys

import concurrent
from concurrent.futures import ProcessPoolExecutor, wait, as_completed

from CosmicExplorerLocationSearch import Coordinates, Detector, Score


def evaluate_region(x_center, y_center, width_meters, height_meters,
                    grid_downsample_factor, arm_length_meters,
                    dl_for_arms_meters, opening_angles,
                    number_of_rotation_angles, max_total_score_for_L_out,
                    path_for_output, njobs, raster_info):
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
      number_of_rotation_angles: integer number of rotation angles to consider
                                 (angles will be calculated from floor division
                                  of 360 degrees by N)
      max_total_score_for_L_out: output to .shp file detector L's with scores
                                 no larger than this. Only the best L with a
                                 given vertex x,y position will be output.
      path_for_output: string pointing to a directory where output will be
                       written (must exist).
      njobs: number of jobs to run in parallel
      raster_info: dict containing information about the raster files being
                   used. Keys must include the following, mostly obtained
                   by opening a raster with rasterio (rio):
                       * "no_data_value": via open_rio_file.profile["nodata"]
                       * "wkt": via open_rio_file.crs.wkt
                       * "bounds": via open_rio_file.bounds
                       * "transform": via open_rio_file.transform
                       * "profile": via open_rio_file.profile
                       * "paths" = dict containing the following:
                         * "elevation" = path to elevation raster
                         * "landcover" = path to landcover raster
    Output:
      * One geotiff for each score returned for each detector, with pixel
        values equal to the best score at each x,y point, minimizing over
        opening angles and rotation angles. Uses the projection of the provided
        elevation raster.
      * One ESRI shape file containing each L with scores no larger than
        max_total_score_for_L_out.
      * One ASCII CSV file containing the detector parameters and scores
        for the best detector at each x,y location, maximizing over 
        opening angles and rotation angles.
    """
    # Check the desired bounds for the search
    # Start by getting the bounds of the file, and then reducing them by
    # 1.01% of the arm length, to ensure the arms never hit the edge of the
    # raster
    file_bounds = raster_info["bounds"]
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
        raster_info["transform"], [left_desired, right_desired],
        [bottom_desired, top_desired])
    bounds_xs, bounds_ys = rio.transform.xy(raster_info["transform"],
                                            bounds_rows, bounds_cols)
    detector_xmin, detector_xmax = bounds_xs[0], bounds_xs[1]
    detector_ymin, detector_ymax = bounds_ys[0], bounds_ys[1]
    print("Detector vertex xmin, xmax, ymin, ymax")
    print(detector_xmin, detector_xmax, detector_ymin, detector_ymax)

    # The bounds for output geotiffs are half a pixel width different from
    # the coordinate bounds, since the coordinates come from the pixel center
    x_half_pixel_size = 0.5 * raster_info["transform"][0]
    y_half_pixel_size = -0.5 * raster_info["transform"][4]

    # Generate grid of x's and y's for detector center
    detector_spacing = 2.0 * x_half_pixel_size * np.round(
        grid_downsample_factor)
    detector_xs = np.arange(detector_xmin, detector_xmax + detector_spacing,
                            detector_spacing)
    detector_ys = np.arange(detector_ymin, detector_ymax + detector_spacing,
                            detector_spacing)
    bounds = rio.coords.BoundingBox(left=detector_xs[0] - x_half_pixel_size,
                                    bottom=detector_ys[0] - y_half_pixel_size,
                                    right=detector_xs[-1] + x_half_pixel_size,
                                    top=detector_ys[-1] + y_half_pixel_size)
    grid_cols = detector_xs.shape[0]
    grid_rows = detector_ys.shape[0]
    number_of_opening_angles = np.shape(opening_angles)[0]
    rotation_angles = np.arange(0.0, 360.0, 360 // number_of_rotation_angles)
    if (rotation_angles.shape[0] != number_of_rotation_angles):
        print("ERROR! Shape of rotation_angles incorrect")

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
    print("Shape of total score array:")
    print(result["total_score"].shape)

    # Submitting every task in one go led to excessive memory usage that 
    # prevented a national search with ~500M tasks from completing.
    # One attempt to limit memory usage is dividing the tasks into rounds,
    # with only tasks_each_round futures in memory at a time. Memory usage
    # is better but still large with this change; a future improvement might
    # be able to further improve memory usage.
    tasks_each_round = 100000
    tasks_done = 0
    func_to_call = Score.score_detector_from_grid
    # params_for_futures is a generator expression. It only evaluates
    # when you loop over it. When you loop over it, looped over items are
    # automatically removed from the generator expression.
    params_for_futures = ((raster_info["paths"], raster_info["no_data_value"],
                           arm_length_meters, dl_for_arms_meters,
                           opening_angle, rotation_angle, x, y, i, j, row, col)
                          for i, opening_angle in enumerate(opening_angles)
                          for j, rotation_angle in enumerate(rotation_angles)
                          for row, y in enumerate(detector_ys)
                          for col, x in enumerate(detector_xs))

    # Based on https://alexwlchan.net/2019/adventures-with-concurrent-futures/
    print(str(datetime.now()) + " -- Starting process pool executor...")
    with ProcessPoolExecutor(njobs) as pool:
        # Make a dictionary of tasks_each_round futures
        # Itertools takes an iterable and loops over the first N, or all
        # if less than N. N here is tasks_each_round. After this call:
        #   * futures will have tasks_each_round tasks
        #   * params_for_futures updated, so iterating over it excludes first
        #   * N cases
        futures = {
            pool.submit(func_to_call, *params): params
            for params in itertools.islice(params_for_futures,
                                           tasks_each_round)
        }
        # Loop over futures while dictionary is not empty
        while futures:
            # Respond to figures as they complete, storing results in
            # a numpy array. Note: only the futures run on different
            # threads (and thus only the futures can run on different cores).
            # There is just one result dict, and it lives on the main thread.
            for future in as_completed(futures):
                score = future.result()
                score_i = score["opening_angle_i"]
                score_j = score["rotation_angle_j"]
                score_row = score["vertex_row"]
                score_col = score["vertex_col"]

                result["opening_angle_degrees"][score_i][score_j][score_row][
                    score_col] = score["opening_angle_degrees"]
                result["rotation_angle_degrees"][score_i][score_j][score_row][
                    score_col] = score["rotation_angle_degrees"]
                result["vertex_x"][score_i][score_j][score_row][
                    score_col] = score["vertex_x"]
                result["vertex_y"][score_i][score_j][score_row][
                    score_col] = score["vertex_y"]
                result["elevation_score"][score_i][score_j][score_row][
                    score_col] = score["elevation_score"]
                result["tilt_score"][score_i][score_j][score_row][
                    score_col] = score["tilt_score"]
                result["landcover_score"][score_i][score_j][score_row][
                    score_col] = score["landcover_score"]
                result["total_score"][score_i][score_j][score_row][
                    score_col] = score["total_score"]
                tasks_done += 1

                # Submit as many futures as done futures obtained.
                # Note: the params we already looped over are no longer in
                # params_for_futures, because generator expressions drop
                # cases after you loop over them automatically.
                # Also remove the completed future
                futures.pop(future)
                for params in itertools.islice(params_for_futures, 1):
                    # .update takes a dict and adds/overwrites key/value pairs
                    # with those in the provided dict
                    futures.update(
                        {pool.submit(func_to_call, *params): params})

            print(
                str(datetime.now()) + " -- " + str(tasks_done) +
                " tasks complete")
            sys.stdout.flush()

    # Output geotiffs, finding best (smallest) score over opening and rotation
    # angles
    print(str(datetime.now()) + " -- Outputting geotiffs")
    out_profile = raster_info["profile"]
    out_transform = rio.transform.from_bounds(bounds.left, bounds.bottom,
                                              bounds.right, bounds.top,
                                              grid_cols, grid_rows)
    out_profile.update(width=grid_cols,
                       height=grid_rows,
                       transform=out_transform,
                       nodata=raster_info["no_data_value"],
                       dtype=np.float32)
    best_elevation = np.flip(np.log10(
        np.min(np.min(result["elevation_score"], axis=0), axis=0)),
                             axis=0)
    best_tilt = np.flip(np.log10(
        np.min(np.min(result["tilt_score"], axis=0), axis=0)),
                        axis=0)
    # Add 1.e-15 for the unlikely event that arm only touches spaces
    # with zero landcover
    eps = 1e-15
    best_landcover = np.flip(
        np.log10(eps +
                 np.min(np.min(result["landcover_score"], axis=0), axis=0)),
        axis=0)
    best_total = np.flip(np.log10(
        np.min(np.min(result["total_score"], axis=0), axis=0)),
                         axis=0)

    # Undo log of nodata points, replace with actual no data value
    no_data = raster_info["no_data_value"]
    factor_to_make_no_value_large = 1000000000
    no_data_times_big_factor = factor_to_make_no_value_large * np.abs(no_data)
    log10_no_data_times_big_factor = np.log10(no_data_times_big_factor)
    eps_for_log = 1.e-6
    print("No data = " + str(no_data) + " log10(no data * big factor) = " +
          str(log10_no_data_times_big_factor))
    best_elevation[np.abs(best_elevation -
                          log10_no_data_times_big_factor) < eps_for_log] = no_data
    best_tilt[np.abs(best_tilt - log10_no_data_times_big_factor) < eps_for_log] = no_data
    best_landcover[np.abs(best_landcover -
                          log10_no_data_times_big_factor) < eps_for_log] = no_data
    best_total[np.abs(best_total - log10_no_data_times_big_factor) < eps_for_log] = no_data

    with rio.open(path_for_output + "/elevation_score.tif", "w",
                  **out_profile) as out_geofile:
        out_geofile.write(best_elevation, 1)
    with rio.open(path_for_output + "/tilt_score.tif", "w",
                  **out_profile) as out_geofile:
        out_geofile.write(best_tilt, 1)
    with rio.open(path_for_output + "/landcover_score.tif", "w",
                  **out_profile) as out_geofile:
        out_geofile.write(best_landcover, 1)
    with rio.open(path_for_output + "/total_score.tif", "w",
                  **out_profile) as out_geofile:
        out_geofile.write(best_total, 1)

    # Output csv
    print(str(datetime.now()) + " -- Outputting csv")
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
                        detector_scores = {
                            "elevation_score":
                            result["elevation_score"][i][j][row][col],
                            "tilt_score":
                            result["tilt_score"][i][j][row][col],
                            "landcover_score":
                            result["landcover_score"][i][j][row][col],
                            "total_score":
                            result["total_score"][i][j][row][col]
                        }
                        if result["total_score"][i][j][row][
                                col] <= max_total_score_for_L_out:
                            detectors.append(
                                Detector.detector(
                                    arm_length_meters, dl_for_arms_meters,
                                    opening_angles[i], rotation_angles[j],
                                    detector_xs[col], detector_ys[row],
                                    detector_scores))

    # Finally, write the shape file
    print(str(datetime.now()) + " -- Outputting shapefiles")
    Detector.write_shapefile_of_detectors(
        detectors, path_for_output + "/best_detectors.shp")
    print(str(datetime.now()) + " -- Complete!")


def evaluate_region_lon_lat(lon_center, lat_center, width_meters,
                            height_meters, grid_downsample_factor,
                            arm_length_meters, dl_for_arms_meters,
                            opening_angles, number_of_rotation_angles,
                            max_total_score_for_L_out, path_for_output, njobs,
                            raster_info):
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
    x_center, y_center = Coordinates.lonlat_to_xy(lon_center, lat_center,
                                                  raster_info["wkt"])
    return evaluate_region(x_center, y_center, width_meters, height_meters,
                           grid_downsample_factor, arm_length_meters,
                           dl_for_arms_meters, opening_angles,
                           number_of_rotation_angles,
                           max_total_score_for_L_out, path_for_output, njobs,
                           raster_info)


def main():
    # Parse arguments.
    start_time = datetime.now()
    helptext = """Evaluate the suitability of a 2D grid of detectors placed in a 
        rectangular region such that they are evenly spaced horizontally
        and vertically. Uses the projection of the provided elevation map for
        outputting results to geotiff and shapefiles.
    """
    p = argparse.ArgumentParser(prog='FindSites', description=helptext)
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
                   help="Vertex spacing = every N pixels of elevation raster")
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
    p.add_argument('--rotation-angles',
                   type=int,
                   help="Number of rotation angles")
    p.add_argument('--elevation', help="Path to elevation geotiff")
    p.add_argument('--landcover', help="Path to landcover geotiff")
    p.add_argument('--outscore',
                   type=float,
                   help="Output detector L's if total score < outscore")
    p.add_argument('--outdir', help="Path to output directory (must exist)")
    p.add_argument('--njobs',
                   type=int,
                   help="Number of jobs to run in parallel")
    args = p.parse_args()
    print(Score.__file__)
    print(args)

    # Create dictionary of raster data and transforms. This happens once on each
    # process.
    raster_info = {
        "no_data_value": None,
        "wkt": None,
        "bounds": None,
        "transform": None,
        "profile": None,
        "paths": None
    }

    # Use the elevation file to determine default raster information.
    with rio.open(args.elevation) as geofile:
        raster_info["no_data_value"] = geofile.profile["nodata"]
        raster_info["wkt"] = geofile.crs.wkt
        raster_info["bounds"] = geofile.bounds
        raster_info["transform"] = geofile.transform
        raster_info["profile"] = geofile.profile
        raster_info["paths"] = {
            "elevation": args.elevation,
            "landcover": args.landcover
        }
    print(f"Raster info: {raster_info}")

    evaluate_region_lon_lat(args.lon, args.lat, args.width, args.height,
                            args.N, args.arm_length, args.dl,
                            np.array(args.opening_angle), args.rotation_angles,
                            args.outscore, args.outdir, args.njobs,
                            raster_info)


if __name__ == '__main__':
    main()
