# Distributed under the MIT License.
# See LICESNSE for details.
import argparse
from datetime import datetime
from multiprocessing import shared_memory
import numpy as np
import rasterio as rio
import time
from tqdm import tqdm

from CosmicExplorerSiteSearch import Coordinates, Detector, Score

# Parse arguments. Note: every process parses the arguments, so they
# can determine what kind of parallelism is being used
global_start_time = datetime.now()
helptext = """Evaluate the suitability of a 2D grid of detectors placed in a 
    rectangular region such that they are evenly spaced horizontally
    and vertically. Uses the projection of the provided elevation map for
    outputting results to geotiff and shapefiles.
"""
p = argparse.ArgumentParser(prog='FindSites', description=helptext)
p.add_argument('--lon',
               type=float,
               help="Longitude of center of search region (decimal degrees)")
p.add_argument('--lat',
               type=float,
               help="Latitude of center of search region (decimal degrees)")
p.add_argument('--width', type=float, help="Width of search region (meters)")
p.add_argument('--height', type=float, help="Height of search region (meters)")
p.add_argument('--N',
               type=int,
               help="vertex spacing = every N pixels of elevation raster")
p.add_argument('--arm_length', type=float, help="Detector arm length (meters)")
p.add_argument('--dl',
               type=float,
               help="Spacing between sample points on arms")
p.add_argument('--opening-angle',
               type=float,
               nargs='+',
               help="One or more opening angles")
p.add_argument('--rotation-angles', type=int, help="Number of rotation angles")
p.add_argument('--elevation', help="Path to elevation geotiff")
p.add_argument('--landcover', help="Path to landcover geotiff")
p.add_argument('--outscore',
               type=float,
               help="Output detector L's if total score < max_score")
p.add_argument('--outdir', help="Path to output directory (must exist)")
p.add_argument('--njobs', type=int, help="Number of jobs to run in parallel")
p.add_argument('--mpi',
               action='store_true',
               help="Use mpi for parallelization")
args = p.parse_args()

# Determine which parallelism is being used
# ProcessPoolExecutor is good for running on a single machine
# MPIPoolExecutor is good for running on multiple compute nodes
if args.mpi:
    import mpi4py
    from mpi4py import MPI
    from mpi4py.futures import MPIPoolExecutor, as_completed
    mpi_comm = MPI.COMM_WORLD
    mpi_rank = mpi_comm.Get_rank()
    mpi_size = mpi_comm.Get_size()
else:
    from concurrent.futures import ProcessPoolExecutor, as_completed

# Create dictionary of raster data and transforms. This happens once on each
# process.
Score.init_global_data({
    "elevation": args.elevation,
    "landcover": args.landcover
})


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
      rotation_angles: numpy array of rotation angles to consider
      max_total_score_for_L_out: output to .shp file detector L's with scores
                                 no larger than this. Only the best L with a
                                 given vertex x,y position will be output.
      path_for_output: string pointing to a directory where output will be
                       written (must exist).
      njobs: number of jobs to run in parallel
      raster_info: dict with keys for each raster stored in memory. Each key
                   stores a dict containing array shape, dtype, nbytes
                   (get eachw ith the corresponding numpy array methods)
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
    # Check the desired bounds for the search
    # Start by getting the bounds of the file, and then reducing them by
    # 1.01% of the arm length, to ensure the arms never hit the edge of the
    # raster
    file_bounds = Score.global_raster_bounds
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
        Score.global_raster_transform, [left_desired, right_desired],
        [bottom_desired, top_desired])
    bounds_xs, bounds_ys = rio.transform.xy(Score.global_raster_transform,
                                            bounds_rows, bounds_cols)
    detector_xmin, detector_xmax = bounds_xs[0], bounds_xs[1]
    detector_ymin, detector_ymax = bounds_ys[0], bounds_ys[1]
    print("Detector vertex xmin, xmax, ymin, ymax")
    print(detector_xmin, detector_xmax, detector_ymin, detector_ymax)

    # The bounds for output geotiffs are half a pixel width different from
    # the coordinate bounds, since the coordinates come from the pixel center
    x_half_pixel_size = 0.5 * Score.global_raster_transform[0]
    y_half_pixel_size = -0.5 * Score.global_raster_transform[4]

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

    total_tasks = number_of_opening_angles * number_of_rotation_angles
    total_tasks *= grid_rows * grid_cols
    tasks_each_round = 1000000
    tasks_to_submit = total_tasks
    tasks_for_this_round = 0
    params_for_futures = []
    for i, opening_angle in enumerate(opening_angles):
        for j, rotation_angle in enumerate(rotation_angles):
            for row, y in enumerate(detector_ys):
                for col, x in enumerate(detector_xs):
                    params_for_futures.append(
                        (Score.score_detector_from_grid, arm_length_meters,
                         dl_for_arms_meters, opening_angle, rotation_angle, x,
                         y, i, j, row, col, raster_info))
                    tasks_for_this_round += 1
                    tasks_to_submit -= 1
                    if (tasks_for_this_round
                            >= tasks_each_round) or tasks_to_submit <= 0:
                        print(
                            str(datetime.now()) + " -- Submitting " +
                            str(tasks_for_this_round) + " tasks")
                        with ProcessPoolExecutor(njobs) as pool:
                            futures = [
                                pool.submit(*params)
                                for params in params_for_futures
                            ]
                            for future in as_completed(futures):
                                score = future.result()
                                score_i = score["opening_angle_i"]
                                score_j = score["rotation_angle_j"]
                                score_row = score["vertex_row"]
                                score_col = score["vertex_col"]

                                result["opening_angle_degrees"][score_i][
                                    score_j][score_row][score_col] = score[
                                        "opening_angle_degrees"]
                                result["rotation_angle_degrees"][score_i][
                                    score_j][score_row][score_col] = score[
                                        "rotation_angle_degrees"]
                                result["vertex_x"][score_i][score_j][
                                    score_row][score_col] = score["vertex_x"]
                                result["vertex_y"][score_i][score_j][
                                    score_row][score_col] = score["vertex_y"]
                                result["elevation_score"][score_i][score_j][
                                    score_row][score_col] = score[
                                        "elevation_score"]
                                result["tilt_score"][score_i][score_j][
                                    score_row][score_col] = score["tilt_score"]
                                result["landcover_score"][score_i][score_j][
                                    score_row][score_col] = score[
                                        "landcover_score"]
                                result["total_score"][score_i][score_j][
                                    score_row][score_col] = score[
                                        "total_score"]
                        print(
                            str(datetime.now()) + " -- Completed " +
                            str(tasks_for_this_round) + " tasks (" +
                            str(tasks_to_submit) + " remaining)")
                        params_for_futures = []
                        tasks_for_this_round = 0
                        time.sleep(30)

    # Output geotiffs, finding best (smallest) score over opening and rotation
    # angles
    print(str(datetime.now()) + " -- Outputting geotiffs")
    out_profile = Score.global_raster_profile
    out_transform = rio.transform.from_bounds(bounds.left, bounds.bottom,
                                              bounds.right, bounds.top,
                                              grid_cols, grid_rows)
    out_profile.update(width=grid_cols,
                       height=grid_rows,
                       transform=out_transform,
                       nodata=Score.global_no_data,
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
    no_data = Score.global_no_data
    log10_no_data = np.log10(no_data)
    eps_for_log = 1.e-6
    print("No data = " + str(no_data) + " log10(no data) = " +
          str(log10_no_data))
    best_elevation[np.abs(best_elevation -
                          log10_no_data) < eps_for_log] = no_data
    best_tilt[np.abs(best_tilt - log10_no_data) < eps_for_log] = no_data
    best_landcover[np.abs(best_landcover -
                          log10_no_data) < eps_for_log] = no_data
    best_total[np.abs(best_total - log10_no_data) < eps_for_log] = no_data

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
                                                  Score.global_raster_wkt)
    return evaluate_region(x_center, y_center, width_meters, height_meters,
                           grid_downsample_factor, arm_length_meters,
                           dl_for_arms_meters, opening_angles,
                           number_of_rotation_angles,
                           max_total_score_for_L_out, path_for_output, njobs,
                           raster_info)


if __name__ == '__main__':
    # First, look for leftover shared memory and delete if it already exists
    try:
        shm_elevation = shared_memory.SharedMemory("shm_elevation",
                                                   create=False)
        shm_elevation.unlink()
        print("Cleaned up existing shared memory for elevation")
    except:
        print("No existing shared memory for elevation to clean up")
    try:
        shm_landcover = shared_memory.SharedMemory("shm_landcover",
                                                   create=False)
        shm_landcover.unlink()
        print("Cleaned up existing shared memory for landcover")
    except:
        print("No existing shared memory for landcover to clean up")
    raster_info = {"elevation": {}, "landcover": {}}
    print(str(datetime.now()) + " -- Reading elevation data")
    elev_file = rio.open(args.elevation)
    elev = elev_file.read()
    raster_info["elevation"] = {
        "shape": elev.shape,
        "dtype": elev.dtype,
        "nbytes": elev.nbytes
    }

    elev_shm = shared_memory.SharedMemory(
        create=True,
        name="shm_elevation",
        size=raster_info["elevation"]["nbytes"])

    print(
        str(datetime.now()) + " -- Copying elevation data into shared memory")
    elev_shared = np.ndarray(raster_info["elevation"]["shape"],
                             dtype=raster_info["elevation"]["dtype"],
                             buffer=elev_shm.buf)
    elev_shared[:] = elev[:]
    elev_file.close()

    print(str(datetime.now()) + " -- Reading landcover data")
    lc_file = rio.open(args.landcover)
    lc = lc_file.read()
    raster_info["landcover"] = {
        "shape": lc.shape,
        "dtype": lc.dtype,
        "nbytes": lc.nbytes
    }

    lc_shm = shared_memory.SharedMemory(
        create=True,
        name="shm_landcover",
        size=raster_info["landcover"]["nbytes"])

    print(
        str(datetime.now()) + " -- Copying landcover data into shared memory")
    lc_shared = np.ndarray(raster_info["landcover"]["shape"],
                           dtype=raster_info["landcover"]["dtype"],
                           buffer=lc_shm.buf)
    lc_shared[:] = lc[:]
    lc_file.close()

    print(str(datetime.now()) + " -- Starting evaluation")
    evaluate_region_lon_lat(args.lon, args.lat, args.width, args.height,
                            args.N, args.arm_length, args.dl,
                            np.array(args.opening_angle),
                            np.array(args.rotation_angles), args.outscore,
                            args.outdir, args.njobs, raster_info)
    elev_shm.close()
    elev_shm.unlink()
    lc_shm.close()
    lc_shm.unlink()
