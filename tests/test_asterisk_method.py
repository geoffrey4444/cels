# Distributed under the MIT License.
# See LICENSE for details.
from CosmicExplorerLocationSearch import Detector
from CosmicExplorerLocationSearch import Score
from CosmicExplorerLocationSearch.TestHelpers import *
import csv
import fiona
import numpy as np
import os
from pyproj import CRS
import subprocess
import rasterio as rio
import tempfile


def test_asterisk_scoring():
    """Test that the asterisk (asterisk_number_of_rotation_angles is not None) detector method produces
    results identical to standard method. Generates random tiff, creates detector objects,
    compares structure and scores between methods using original scoring function and asterisk.
    Tests a random opening angle (60,90 and 120).
    """
    # Creating temporary test image and directory
    with tempfile.TemporaryDirectory() as temp_dir:
        elevation_path = os.path.join(temp_dir, "elevation.tif")
        landcover_path = os.path.join(temp_dir, "landcover.tif")
        land_acquisition_path = os.path.join(temp_dir, "land_acquisition.tif")
        roads_path = os.path.join(temp_dir, "roads.shp")
        rasters = {
            "elevation": elevation_path,
            "landcover": landcover_path,
            "land_acquisition": land_acquisition_path,
        }
        shapefiles_paths = {"roads": roads_path}

        width = 100  # pixels
        profile, bounds = profile_for_random_geotiff(width)
        no_data_value = profile["nodata"]

        random_geotiff(rasters["elevation"], profile)
        random_geotiff(rasters["landcover"], profile)
        random_land_acquisition_geotiff_with_width(land_acquisition_path,
                                                   width)
        random_roads_shapefile(roads_path, bounds)

        # Pick a vertex safely inside the raster
        random_arm_length = np.random.randint(5000, 40000)
        random_arm_dl = np.random.randint(
            50, 500
        )  #set to always be smaller than arm length, by at least a factor of 10
        random_opening_angle_i = np.random.randint(1, 1000)
        random_rotation_angle_j = np.random.randint(1, 1000)
        random_vertex_row = np.random.randint(1, 1000)
        random_vertex_col = np.random.randint(1, 1000)

        max_arm = 20000.0
        random_x = np.random.uniform(bounds.left + 1.1 * max_arm,
                                     bounds.right - 1.1 * max_arm)
        random_y = np.random.uniform(bounds.bottom + 1.1 * max_arm,
                                     bounds.top - 1.1 * max_arm)

        # Generate random detector parameters.

        opening_angle_degrees = float(
            np.random.choice([45, 60, 90, 120])
        )  # Selecting a random opening angle, the angle it self only need to evenly divide 360
        required_divisor = int(
            360 // opening_angle_degrees
        )  #the number of rotation angles must be a multiple of 360//opening angles
        lcm = int(np.lcm(required_divisor, 4))
        valid_ns = [n for n in range(lcm, 37, lcm)
                    ]  # Building list of valid numbers of rotation angles
        rotation_number = int(np.random.choice(valid_ns))

        vertex_x_test = random_x
        vertex_y_test = random_y
        arm_length_meters_test = random_arm_length
        dl_for_arms_meters_test = random_arm_dl

        rotation_angles_degrees = np.linspace(0,
                                              360,
                                              rotation_number,
                                              endpoint=False)
        list_of_detectors = [
            Detector.detector(arm_length_meters_test, dl_for_arms_meters_test,
                              opening_angle_degrees, angle, vertex_x_test,
                              vertex_y_test)
            for angle in rotation_angles_degrees
        ]

        # Build the asterisk detector ).
        asterisk = Detector.detector(
            arm_length_meters_test,
            dl_for_arms_meters_test,
            opening_angle_degrees=opening_angle_degrees,
            rotation_angle_degrees=
            None,  #rotation angle is not used in asterisk method, but must be provided to the detector function
            vertex_x=vertex_x_test,
            vertex_y=vertex_y_test,
            asterisk_number_of_rotation_angles=rotation_number,
        )

        paired_arms = Detector.pair_arm_coords(asterisk)
        eps = 1e-8  #the lowest tolerance for floating point comparison that reliably passed in testing

        # asterisk vs standard structure check
        assert len(paired_arms) == len(list_of_detectors)
        for i, det in enumerate(paired_arms):
            assert det["vertex_x"] == vertex_x_test
            assert det["vertex_y"] == vertex_y_test
            assert det["arm_length_meters"] == arm_length_meters_test
            assert det["dl_for_arms_meters"] == dl_for_arms_meters_test
            assert abs(det["rotation_angle_degrees"] -
                       list_of_detectors[i]["rotation_angle_degrees"]) < eps
            assert paired_arms[i]["scores"] is None
            assert np.shape(det["arms_xy"]) == np.shape(
                list_of_detectors[i]["arms_xy"])
            assert abs(
                np.sum(
                    det["distance_from_vertex_meters"] -
                    list_of_detectors[i]["distance_from_vertex_meters"])) < eps
            assert det["vertex_pixel"] == list_of_detectors[i]["vertex_pixel"]

        for det in paired_arms:
            vx, vy = det["vertex_x"], det["vertex_y"]
            x_tip = det["arms_xy"][0]
            y_tip = det["arms_xy"][-1]
            vec_x = np.array([x_tip[0] - vx, x_tip[1] - vy])
            vec_y = np.array([y_tip[0] - vx, y_tip[1] - vy])
            cos_angle = np.dot(
                vec_x, vec_y) / (np.linalg.norm(vec_x) * np.linalg.norm(vec_y))
            measured_angle = np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))
            assert abs(measured_angle - opening_angle_degrees) < eps, (
                f"Expected opening angle {opening_angle_degrees}, got {measured_angle} "
                f"(n={rotation_number})")

        # Asterisk vs Standard score check
        rotation_angles = np.linspace(0, 360, rotation_number, endpoint=False)
        scored_dets = [
            Score.score_detector_from_grid(
                rasters,
                shapefiles_paths,
                no_data_value,
                arm_length_meters_test,
                dl_for_arms_meters_test,
                opening_angle_degrees,
                angle,
                vertex_x_test,
                vertex_y_test,
                random_opening_angle_i,
                random_rotation_angle_j,
                random_vertex_row,
                random_vertex_col,
                use_shared_memory=False,
                shared_memory_info=None,
            ) for angle in rotation_angles
        ]

        # score_detector_from_grid_asterisk scores all rotation angles at once
        scored_dets_asterisk = Score.score_detector_from_grid_asterisk(
            rasters,
            shapefiles_paths,
            no_data_value,
            arm_length_meters_test,
            dl_for_arms_meters_test,
            opening_angle_degrees,
            0,
            vertex_x_test,
            vertex_y_test,
            random_opening_angle_i,
            random_rotation_angle_j,
            random_vertex_row,
            random_vertex_col,
            rotation_number,
        )

        for i in range(rotation_number):
            sd = scored_dets[i]
            sda = scored_dets_asterisk[i]

            assert sd["arm_length_meters"] == sda["arm_length_meters"]
            assert sd["dl_for_arms_meters"] == sda["dl_for_arms_meters"]
            assert sd["opening_angle_degrees"] == sda["opening_angle_degrees"]
            assert sd["rotation_angle_degrees"] == sda[
                "rotation_angle_degrees"]
            assert sd["vertex_x"] == sda["vertex_x"]
            assert sd["vertex_y"] == sda["vertex_y"]
            assert sd["opening_angle_i"] == sda["opening_angle_i"]
            assert sd["rotation_angle_j"] == sda["rotation_angle_j"]
            assert sd["vertex_row"] == sda["vertex_row"]
            assert sd["vertex_col"] == sda["vertex_col"]

            assert abs(sd["elevation_score"] - sda["elevation_score"]) < eps
            assert abs(sd["tilt_score"] - sda["tilt_score"]) < eps
            assert abs(sd["landcover_score"] - sda["landcover_score"]) < eps
            assert abs(sd["land_acquisition_score"] -
                       sda["land_acquisition_score"]) < eps
            assert abs(sd["roads_score"] - sda["roads_score"]) < eps
            assert abs(sd["total_score"] - sda["total_score"]) < eps


def _run_findsites_search_and_validate(elevation_path,
                                       landcover_path,
                                       land_acquisition_path,
                                       roads_path,
                                       rotation_angles,
                                       outdir,
                                       use_shared_memory=False,
                                       asterisk=True):
    """Shared driver for findsites subprocess tests.

    Builds the findsites CLI args, runs the search as a subprocess, then
    validates that all expected output files were produced and contain sane
    values.

    Both test_findsites_asterisk and test_findsites_asterisk_and_shared_memory
    do a search at the center of the landcover and elevation images in
    test_images (1km resolution), over a 10 x 10 grid of vertex locations.
    The outscore is fixed at 200.0 (million USD) to ensure Ls are returned
    with the added road crossing costs.

    Input:
      elevation_path: path to elevation raster (.tif or .bsq)
      landcover_path: path to landcover raster (.tif or .bsq)
      land_acquisition_path: path to land acquisition raster (.tif or .bsq)
      roads_path: path to roads shapefile
      rotation_angles: number of rotation angles to pass to --rotation-angles
      outdir: output directory for findsites results (must exist)
      use_shared_memory: if True, pass --use-shared-memory to findsites
      asterisk: if True, pass --asterisk to findsites (default True)

    Output:
      Nothing; raises an AssertionError if any check fails.
    """
    find_sites_path = "findsites"
    lon = -107.7
    lat = 32.3
    width = 100000.0  # width of search region is 100km = 100 pixels
    height = 40000.0  # height of search region is 40km
    vertex_spacing = 10  # grid of detectors spaced every 10 km
    arm_length = 40000.0  # meters
    dl_for_arms = 1000.0  # meters
    opening_angle = 90.0
    outscore = 200.0  # The score threshold in million USD.

    args = [
        find_sites_path,
        f"--lon={lon}",
        f"--lat={lat}",
        f"--width={width}",
        f"--height={height}",
        f"--N={vertex_spacing}",
        f"--arm_length={arm_length}",
        f"--dl={dl_for_arms}",
        f"--opening-angle={opening_angle}",
        f"--rotation-angles={rotation_angles}",
        f"--elevation={elevation_path}",
        f"--landcover={landcover_path}",
        f"--land_acquisition={land_acquisition_path}",
        f"--roads={roads_path}",
        f"--outscore={outscore}",
        f"--outdir={outdir}",
        f"--njobs=2",
    ]
    if use_shared_memory:
        args.append("--use-shared-memory")
    if asterisk:
        args.append("--asterisk")

    print(f"Starting search in path: {outdir}")
    print(" ".join(args))
    subprocess.run(args)

    # Checks that all expected output files exist in the output directory
    expected_files = [
        'elevation_score.tif', 'best_detectors.prj', 'total_score.tif',
        'best_detectors.dbf', 'scores.csv', 'landcover_score.tif',
        'best_detectors.shp', 'best_detectors.cpg', 'tilt_score.tif',
        'best_detectors.shx', 'total_score_minus_land_acq.tif'
    ]
    output_file_names = os.listdir(outdir)
    for name in expected_files:
        print(name)
        assert name in output_file_names

        # If tif file, do some sanity checks
        if name.split(".")[-1] == "tif":
            geofile = rio.open(outdir + "/" + name)
            # Searching a 100 x 40 pixel region, skipping every 10 pixels,
            # so there should be (100/10 + 1) pixels wide and (40/10 + 1)
            # pixels high in the geotiffs
            assert geofile.profile["width"] == 11
            assert geofile.profile["height"] == 5

            # Check properties the geotiff should have in common with the
            # test images
            assert geofile.profile["nodata"] == 32767.0
            assert geofile.profile["crs"] == CRS.from_epsg(5070)

            # Each geofile should have 1 float dataset in it
            assert geofile.profile["count"] == 1
            assert geofile.profile["dtype"] == 'float32'

            # Check that sane scores were written: mean should be
            # between 0, 32767
            average_score = np.average(geofile.read())
            assert average_score > 0
            assert average_score < 32767
            geofile.close()

        elif name.split(".")[-1] == "shp":
            shapefile = fiona.open(outdir + "/" + name)
            assert len(shapefile) > 0
            for i, ell in enumerate(shapefile):
                # check that the score is in the expected range
                assert ell.properties["tot_score"] > 0
                assert ell.properties["tot_score"] < outscore
                # check that the detector arm length is as expected
                assert ell.properties["arm_length"] == arm_length
            shapefile.close()

        elif name.split(".")[-1] == "csv":
            csvfile = open(outdir + "/" + name)
            reader = csv.reader(csvfile, delimiter=' ')
            rows = 0
            for row in reader:
                rows += 1
                assert len(row) == 11
            assert rows > 2  # if search succeeded, at least header + 1 row
            csvfile.close()


def _compare_output_dirs(outdir_a,
                         outdir_b,
                         tif_relative_tolerance=1e-3,
                         csv_relative_tolerance=1e-4):
    """
    Compare two output directories and assert that their contents are similar within specified tolerances.
    inputs:
        outdir_a: path to first output directory
        outdir_b: path to second output directory
        tif_relative_tolerance: relative tolerance for comparing TIF files
        csv__relative_tolerance: relative tolerance for comparing CSV files
    """
    score_tifs = [
        'elevation_score.tif',
        'landcover_score.tif',
        'tilt_score.tif',
        'total_score_minus_land_acq.tif',
        'total_score.tif',
    ]

    # --- TIF comparison ---
    for name in score_tifs:
        with rio.open(outdir_a + "/" + name) as fa, \
             rio.open(outdir_b + "/" + name) as fb:
            data_a = fa.read(1).astype(np.float64)
            data_b = fb.read(1).astype(np.float64)
        assert np.allclose(
            data_a,
            data_b,
            rtol=tif_relative_tolerance,
            atol=0,
            equal_nan=True
        ), (f"{name}: max relative difference = "
            f"{np.nanmax(np.abs(data_a - data_b) / np.maximum(np.abs(data_b), 1e-10)):.6g}"
            )

    # --- CSV comparison ---
    def _read_csv(path):
        """
        Read a CSV file and return its header and data as a list of tuples.
        Input:
            path: path to the CSV file
        Output:
            header: list of column names
            data: list of tuples containing the data
        """
        with open(path) as f:
            reader = csv.reader(f, delimiter=' ')
            rows = list(reader)
        header = rows[0]
        data = [tuple(float(v) for v in row) for row in rows[1:]]
        return header, data

    header_a, rows_a = _read_csv(outdir_a + "/scores.csv")
    header_b, rows_b = _read_csv(outdir_b + "/scores.csv")

    assert header_a == header_b, "CSV headers differ"
    assert len(rows_a) == len(rows_b), (
        f"CSV row count differs: {len(rows_a)} vs {len(rows_b)}")

    rows_a.sort()
    rows_b.sort()

    for row_idx, (row_a, row_b) in enumerate(zip(rows_a, rows_b)):
        for col_idx, (val_a, val_b) in enumerate(zip(row_a, row_b)):
            rel_diff = abs(val_a - val_b) / max(abs(val_b), 1e-10)
            assert rel_diff <= csv_relative_tolerance, (
                f"scores.csv row {row_idx + 1} col {col_idx + 1} "
                f"({header_a[col_idx]}): {val_a} vs {val_b}, "
                f"relative diff = {rel_diff:.6g}")

    # --- Shapefile comparison ---
    with fiona.open(outdir_a + "/best_detectors.shp") as shp_a, \
         fiona.open(outdir_b + "/best_detectors.shp") as shp_b:
        records_a = sorted(shp_a, key=lambda f: f.properties["tot_score"])
        records_b = sorted(shp_b, key=lambda f: f.properties["tot_score"])

    assert len(records_a) == len(records_b), (
        f"Shapefile record count differs: {len(records_a)} vs {len(records_b)}"
    )

    for rec_a, rec_b in zip(records_a, records_b):
        score_a = rec_a.properties["tot_score"]
        score_b = rec_b.properties["tot_score"]
        rel_diff = abs(score_a - score_b) / max(abs(score_b), 1e-10)
        assert rel_diff <= tif_relative_tolerance, (
            f"Shapefile tot_score relative diff = {rel_diff:.6g}: "
            f"{score_a} vs {score_b}")


def test_findsites_asterisk():
    # Test run using asterisk method, without shared memory
    base_path = os.path.dirname(os.path.realpath(__file__))
    elevation_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
    landcover_path = base_path + "/test_images/SouthNM_Landcover_1km.tif"
    land_acquisition_path = base_path + "/test_images/SouthNM_LandAcquisition_1km.tif"
    roads_path = base_path + "/test_images/SouthNM_Roads_1km.shp"

    with tempfile.TemporaryDirectory() as temp_path:
        print("Running test in " + temp_path)
        _run_findsites_search_and_validate(
            elevation_path,
            landcover_path,
            land_acquisition_path,
            roads_path,
            rotation_angles=36,
            outdir=temp_path,
            use_shared_memory=False,
            asterisk=True,
        )


def test_findsites_asterisk_and_shared_memory():
    # Test run using sample data with shared memory
    base_path = os.path.dirname(os.path.realpath(__file__))
    elevation_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
    landcover_path = base_path + "/test_images/SouthNM_Landcover_1km.tif"
    land_acquisition_path = base_path + "/test_images/SouthNM_LandAcquisition_1km.tif"
    roads_path = base_path + "/test_images/SouthNM_Roads_1km.shp"

    with tempfile.TemporaryDirectory() as temp_path:
        print("Running shared memory test in " + temp_path)

        # Convert geotiffs to BSQ files for shared memory test
        elevation_bsq_path = temp_path + "/elevation.bsq"
        landcover_bsq_path = temp_path + "/landcover.bsq"
        land_acquisition_bsq_path = temp_path + "/land_acquisition.bsq"

        import CosmicExplorerLocationSearch.Geotiff as Geotiff
        Geotiff.geotiff_to_bsq(elevation_path, elevation_bsq_path)
        Geotiff.geotiff_to_bsq(landcover_path, landcover_bsq_path)
        Geotiff.geotiff_to_bsq(land_acquisition_path,
                               land_acquisition_bsq_path)

        _run_findsites_search_and_validate(
            elevation_bsq_path,
            landcover_bsq_path,
            land_acquisition_bsq_path,
            roads_path,
            rotation_angles=36,
            outdir=temp_path,
            use_shared_memory=True,
            asterisk=True,
        )


def test_findsites_asterisk_matches_standard():
    """Test that asterisk and standard findsites produce identical output files.

    Runs findsites twice over the same search region with the same rotation
    angles — once with --asterisk and once without — then compares all score
    TIF files pixel-by-pixel and all CSV rows value-by-value within tolerance.
    """
    base_path = os.path.dirname(os.path.realpath(__file__))
    elevation_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
    landcover_path = base_path + "/test_images/SouthNM_Landcover_1km.tif"
    land_acquisition_path = base_path + "/test_images/SouthNM_LandAcquisition_1km.tif"
    roads_path = base_path + "/test_images/SouthNM_Roads_1km.shp"

    # 36 rotation angles: divisible by 360/90=4, so valid for 90° opening angle.
    rotation_angles = 36

    with tempfile.TemporaryDirectory() as outdir_standard, \
         tempfile.TemporaryDirectory() as outdir_asterisk:

        _run_findsites_search_and_validate(
            elevation_path,
            landcover_path,
            land_acquisition_path,
            roads_path,
            rotation_angles=rotation_angles,
            outdir=outdir_standard,
            use_shared_memory=False,
            asterisk=False,
        )

        _run_findsites_search_and_validate(
            elevation_path,
            landcover_path,
            land_acquisition_path,
            roads_path,
            rotation_angles=rotation_angles,
            outdir=outdir_asterisk,
            use_shared_memory=False,
            asterisk=True,
        )

        _compare_output_dirs(outdir_standard,
                             outdir_asterisk,
                             tif_relative_tolerance=1e-3,
                             csv_relative_tolerance=1e-5)


def _run_findsites(elevation_path,
                   landcover_path,
                   land_acquisition_path,
                   roads_path,
                   lon,
                   lat,
                   width,
                   height,
                   vertex_spacing,
                   arm_length,
                   dl_for_arms,
                   opening_angle,
                   rotation_angles,
                   outscore,
                   outdir,
                   njobs=8,
                   use_shared_memory=False,
                   asterisk=False):
    """Run findsites as a subprocess with the given parameters 

    Input:
      elevation_path, landcover_path, land_acquisition_path, roads_path:
        paths to the input rasters/shapefile
      lon, lat: center of the search region
      width, height: size of the search region (meters)
      vertex_spacing: grid spacing in pixels (--N)
      arm_length: detector arm length (meters)
      dl_for_arms: spacing between sample points on the arms (meters)
      opening_angle: detector opening angle (degrees)
      rotation_angles: number of rotation angles
      outscore: total score threshold for outputting detectors to .shp
      outdir: output directory (must exist)
      njobs: number of parallel jobs
      use_shared_memory: if True, pass --use-shared-memory
      asterisk: if True, pass --asterisk

    Output:
      subprocess.CompletedProcess for the findsites run (stdout/stderr are
      captured as text).
    """
    args = [
        "findsites",
        f"--lon={lon}",
        f"--lat={lat}",
        f"--width={width}",
        f"--height={height}",
        f"--N={vertex_spacing}",
        f"--arm_length={arm_length}",
        f"--dl={dl_for_arms}",
        f"--opening-angle={opening_angle}",
        f"--rotation-angles={rotation_angles}",
        f"--elevation={elevation_path}",
        f"--landcover={landcover_path}",
        f"--land_acquisition={land_acquisition_path}",
        f"--roads={roads_path}",
        f"--outscore={outscore}",
        f"--outdir={outdir}",
        f"--njobs={njobs}",
    ]
    if use_shared_memory:
        args.append("--use-shared-memory")
    if asterisk:
        args.append("--asterisk")

    print(f"Starting search in path: {outdir}")
    print(" ".join(args))
    return subprocess.run(args, capture_output=True, text=True)


def _compare_csv_outputs(csv_path_a, csv_path_b, relative_tolerance=1e-4):
    """Compare two findsites scores.csv files row-by-row within tolerance.

    Rows are sorted before comparing.

    Input:
      csv_path_a, csv_path_b: paths to the two scores.csv files to compare
      relative_tolerance: max allowed relative difference between matching
                          values

    Output:
      Raises an AssertionError if the files don't match.
    """

    def _read_csv(path):
        with open(path) as f:
            reader = csv.reader(f, delimiter=' ')
            rows = list(reader)
        header = rows[0]
        data = [tuple(float(v) for v in row) for row in rows[1:]]
        return header, data

    header_a, rows_a = _read_csv(csv_path_a)
    header_b, rows_b = _read_csv(csv_path_b)

    assert header_a == header_b, "CSV headers differ"
    assert len(rows_a) == len(rows_b), (
        f"CSV row count differs: {len(rows_a)} vs {len(rows_b)}")

    rows_a.sort()
    rows_b.sort()

    for row_idx, (row_a, row_b) in enumerate(zip(rows_a, rows_b)):
        for col_idx, (val_a, val_b) in enumerate(zip(row_a, row_b)):
            rel_diff = abs(val_a - val_b) / max(abs(val_b), 1e-10)
            assert rel_diff <= relative_tolerance, (
                f"scores.csv row {row_idx + 1} col {col_idx + 1} "
                f"({header_a[col_idx]}): {val_a} vs {val_b}, "
                f"relative diff = {rel_diff:.6g}")


def test_asterisk_csv():
    """Run findsites with the standard and asterisk methods over the same
    search region and check that scores.csv is the same (within tolerance)
    between the two methods.

    Centers on test images for known results.
    """
    base_path = os.path.dirname(os.path.realpath(__file__))
    elevation_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
    landcover_path = base_path + "/test_images/SouthNM_Landcover_1km.tif"
    land_acquisition_path = base_path + "/test_images/SouthNM_LandAcquisition_1km.tif"
    roads_path = base_path + "/test_images/SouthNM_Roads_1km.shp"

    lon = -107.7
    lat = 32.3
    width = 100000.0  # width of search region is 100km = 100 pixels
    height = 40000.0  # height of search region is 40km = 40 pixels
    vertex_spacing = 10  # grid of detectors spaced every 10 pixels
    arm_length = 40000.0  # meters
    dl_for_arms = 1000.0  # meters
    opening_angle = 90.0
    rotation_angles = 16
    outscore = 5000.0  # score threshold in million USD

    with tempfile.TemporaryDirectory() as outdir_standard, \
         tempfile.TemporaryDirectory() as outdir_asterisk:

        result_standard = _run_findsites(elevation_path,
                                         landcover_path,
                                         land_acquisition_path,
                                         roads_path,
                                         lon,
                                         lat,
                                         width,
                                         height,
                                         vertex_spacing,
                                         arm_length,
                                         dl_for_arms,
                                         opening_angle,
                                         rotation_angles,
                                         outscore,
                                         outdir_standard,
                                         njobs=8,
                                         asterisk=False)
        assert result_standard.returncode == 0, (
            f"Standard method failed:\n{result_standard.stderr}")

        result_asterisk = _run_findsites(elevation_path,
                                         landcover_path,
                                         land_acquisition_path,
                                         roads_path,
                                         lon,
                                         lat,
                                         width,
                                         height,
                                         vertex_spacing,
                                         arm_length,
                                         dl_for_arms,
                                         opening_angle,
                                         rotation_angles,
                                         outscore,
                                         outdir_asterisk,
                                         njobs=8,
                                         asterisk=True)
        assert result_asterisk.returncode == 0, (
            f"Asterisk method failed:\n{result_asterisk.stderr}")

        assert "scores.csv" in os.listdir(outdir_standard)
        assert "scores.csv" in os.listdir(outdir_asterisk)

        _compare_csv_outputs(outdir_standard + "/scores.csv",
                             outdir_asterisk + "/scores.csv",
                             relative_tolerance=1e-4)


def test_findsites_fail_case():
    """Check that the standard and asterisk methods agree when every
    detector is expected to fail because it sits entirely over "ocean"
    landcover (landcover value 0).
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        elevation_path = os.path.join(temp_dir, "elevation.tif")
        landcover_path = os.path.join(temp_dir, "landcover.tif")
        land_acquisition_path = os.path.join(temp_dir, "land_acquisition.tif")
        roads_path = os.path.join(temp_dir, "roads.shp")

        # 1km pixels over a fixed 40km x 40km tile centered near
        # lon=-107.7, lat=32.3
        raster_width_pixels = 40
        profile, bounds = profile_for_random_geotiff(raster_width_pixels)

        random_elevation_geotiff_with_width(elevation_path,
                                            raster_width_pixels)

        # All-ocean landcover: every pixel is landcover code 0, representing cost of building on water
        landcover_profile, _ = profile_for_random_geotiff(raster_width_pixels)
        all_ocean = np.zeros((raster_width_pixels, raster_width_pixels))
        random_geotiff(landcover_path, landcover_profile, data=all_ocean)

        random_land_acquisition_geotiff_with_width(land_acquisition_path,
                                                   raster_width_pixels)
        random_roads_shapefile(roads_path, bounds)

        lon = -107.7
        lat = 32.3
        width = 20000.0  # 20km search region, well inside the 40km tile
        height = 20000.0
        vertex_spacing = 5  # grid of detectors spaced every 5 pixels (5km)
        arm_length = 8000.0  # meters
        dl_for_arms = 200.0  # meters
        opening_angle = 90.0
        rotation_angles = 16
        outscore = 0.0001

        with tempfile.TemporaryDirectory() as outdir_standard, \
             tempfile.TemporaryDirectory() as outdir_asterisk:

            result_standard = _run_findsites(elevation_path,
                                             landcover_path,
                                             land_acquisition_path,
                                             roads_path,
                                             lon,
                                             lat,
                                             width,
                                             height,
                                             vertex_spacing,
                                             arm_length,
                                             dl_for_arms,
                                             opening_angle,
                                             rotation_angles,
                                             outscore,
                                             outdir_standard,
                                             njobs=2,
                                             asterisk=False)
            assert result_standard.returncode == 0, (
                f"Standard method failed:\n{result_standard.stderr}")

            result_asterisk = _run_findsites(elevation_path,
                                             landcover_path,
                                             land_acquisition_path,
                                             roads_path,
                                             lon,
                                             lat,
                                             width,
                                             height,
                                             vertex_spacing,
                                             arm_length,
                                             dl_for_arms,
                                             opening_angle,
                                             rotation_angles,
                                             outscore,
                                             outdir_asterisk,
                                             njobs=2,
                                             asterisk=True)
            assert result_asterisk.returncode == 0, (
                f"Asterisk method failed:\n{result_asterisk.stderr}")

            for outdir in (outdir_standard, outdir_asterisk):
                assert "scores.csv" in os.listdir(outdir)
                assert "best_detectors.shp" in os.listdir(outdir)

                # Every detector should fail the outscore
                # threshold because of the ocean landcover cost.
                with fiona.open(outdir + "/best_detectors.shp") as shapefile:
                    assert len(shapefile) == 0, (
                        f"{outdir}: expected no detectors to pass the "
                        f"threshold with all-ocean landcover")

                with open(outdir + "/scores.csv") as f:
                    reader = csv.reader(f, delimiter=' ')
                    rows = list(reader)[1:]
                assert len(rows) > 0
                for row in rows:
                    total_score = float(row[-1])
                    assert total_score > outscore, (
                        f"{outdir}: expected total_score above {outscore} "
                        f"for an all-ocean detector, got {total_score}")

            _compare_csv_outputs(outdir_standard + "/scores.csv",
                                 outdir_asterisk + "/scores.csv",
                                 relative_tolerance=1e-4)


def test_asterisk_input_angle_validation():
    """Test checking opening-angle validation and scores.
 
    Detector.pair_arm_coords determines arm pairing in asterisk method and uses
    the opening angle, and number of rotation angles to determine which arms to pair.
 
    Using 72 rotation angles (5 degree between rotations),
    and opening angle of 100 since it is a multiple of 5.
    
    Compares scores between method, and ensures that CLI gate permits 
    valid angle combinations, and rejects invalid ones.
    """
    opening_angle_degrees = 100.0  # multiple of 5, not a divisor of 360
    rotation_number = 72  # 5 degree arm spacing

    exact_next_arm = opening_angle_degrees * rotation_number / 360.0
    assert exact_next_arm == int(exact_next_arm), (
        f"Test setup error: opening_angle={opening_angle_degrees} is not "
        f"an exact multiple of the {360.0 / rotation_number} degree arm "
        f"spacing for rotation_angles={rotation_number}")

    base_path = os.path.dirname(os.path.realpath(__file__))
    real_elevation_path = base_path + "/test_images/SouthNM_Elevation_1km.tif"
    real_landcover_path = base_path + "/test_images/SouthNM_Landcover_1km.tif"
    real_land_acquisition_path = base_path + "/test_images/SouthNM_LandAcquisition_1km.tif"
    real_roads_path = base_path + "/test_images/SouthNM_Roads_1km.shp"

    lon = -107.7
    lat = 32.3
    width = 100000.0
    height = 40000.0
    vertex_spacing = 10
    arm_length = 40000.0
    dl_for_arms = 1000.0
    outscore = 5000.0

    with tempfile.TemporaryDirectory() as outdir:
        result = _run_findsites(real_elevation_path,
                                real_landcover_path,
                                real_land_acquisition_path,
                                real_roads_path,
                                lon,
                                lat,
                                width,
                                height,
                                vertex_spacing,
                                arm_length,
                                dl_for_arms,
                                opening_angle_degrees,
                                rotation_number,
                                outscore,
                                outdir,
                                njobs=8,
                                asterisk=True)

        assert result.returncode == 0

        assert "scores.csv" in os.listdir(outdir)

    # Findsites angle combination gate check: invalid combination is rejected
    # 91 degrees is not a multiple of 360/36 = 10 degrees, so
    # the arm coords will not overlap, triggering rejection gate
    invalid_opening_angle_degrees = 91.0
    invalid_rotation_number = 36

    exact_next_arm_invalid = (invalid_opening_angle_degrees *
                              invalid_rotation_number / 360.0)
    assert abs(exact_next_arm_invalid - round(exact_next_arm_invalid)) > 1e-9

    with tempfile.TemporaryDirectory() as outdir_invalid:
        result_invalid = _run_findsites(real_elevation_path,
                                        real_landcover_path,
                                        real_land_acquisition_path,
                                        real_roads_path,
                                        lon,
                                        lat,
                                        width,
                                        height,
                                        vertex_spacing,
                                        arm_length,
                                        dl_for_arms,
                                        invalid_opening_angle_degrees,
                                        invalid_rotation_number,
                                        outscore,
                                        outdir_invalid,
                                        njobs=8,
                                        asterisk=True)

        # Checking that Findsites asterisk gate triggers with invalid
        # with invalid angle combinations.
        assert result_invalid.returncode != 0
    
        # Checking that there are no files written
        assert os.listdir(outdir_invalid) == []
