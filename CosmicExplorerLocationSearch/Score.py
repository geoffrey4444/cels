# Distributed under the MIT License.
# See LICENSE for details.
import numpy as np
import rasterio as rio
from scipy import optimize
from scipy.optimize import leastsq as leastsq

from CosmicExplorerLocationSearch import Detector


def pixel_data_from_rasters(raster_file_dict, detector):
    """Inputs:
         raster_file_dict: dictionary of raster file paths
         detector: output of Detector.detector()

       Returns: 
         A dictionary keyed by the keys in raster_file_dict. Under each
         key is a dictionary containing the following:
           * "coords" = x,y coords of points along detector arms
           * "values" = value at x,y from this raster
       Note: this function reads pixel data directly from files on disk,
       which reduces memory use but might strain the filesystem.
    """
    result = {}
    for raster in raster_file_dict:
        result[raster] = {
            "coords": detector["arms_xy"],
            "values": np.array([]),
        }
        with rio.open(raster_file_dict[raster]) as raster_file:
            result[raster]["values"] = np.array([
                sample[0]
                for sample in raster_file.sample(result[raster]["coords"])
            ])
    return result


# These descriptions and codes follow the National Land Cover DatabaseLand Cover
# Classification Legend, which is available at
# https://www.mrlc.gov/sites/default/files/NLCDclasses.pdf
# The codes for Ocean Water (0) and Non-U.S. land (101, 102, 103) conform to
# the USGS 100-Meter Resolution Land Cover of the Conterminous
# United States, 2001 geotiff, available at
# https://geodata.mit.edu/catalog/stanford-wv372bn9329.
# The scores are not necessarily optimal choices. When these are changed,
# test_landcover_score_by_type() in test_score.py must also change.
landcover_score_by_type = {
    0: 1e4,  # ocean
    11: 1e4,  # open water
    12: 1e4,  # perennial ice/snow
    21: 100,  # developed, open space
    22: 300,  # developed, low intensity
    23: 1e4,  # developed, medium intensity
    24: 1e4,  # developed, high intensity
    31: 0,  # barren land (rock/sand/clay)
    41: 20,  # deciduous forest
    42: 20,  # evergreen forest
    43: 20,  # mixed forest
    51: 0,  # dwarf scrub
    52: 5,  # shrub/scrub
    71: 0,  # grassland/herbaceous
    72: 0,  # sedge/herbaceous
    73: 0,  # lichens
    74: 0,  # moss
    81: 20,  # pasture/hay
    82: 100,  # cultivated crops
    90: 1e4,  # woody wetlands
    95: 1e4,  # emergent herbaceous wetlands
    101: 1e4,  # Canada
    102: 1e4,  # Mexico
    103: 1e4  # Cuba
}

# These descriptions and codes follow the National Land Cover DatabaseLand Cover
# Classification Legend, which is available at
# https://www.mrlc.gov/sites/default/files/NLCDclasses.pdf
# The codes for Ocean Water (0) and Non-U.S. land (101, 102, 103) conform to
# the USGS 100-Meter Resolution Land Cover of the Conterminous
# United States, 2001 geotiff, available at
# https://geodata.mit.edu/catalog/stanford-wv372bn9329.
landcover_labels = {
    0: "Ocean Water",
    11: "Open Water",
    12: "Perennial Ice/Snow",
    21: "Developed, Open Space",
    22: "Developed, Low Intensity",
    23: "Developed, Medium Intensity",
    24: "Developed, High Intensity",
    31: "Barren Land (Rock/Sand/Clay)",
    41: "Deciduous Forest",
    42: "Evergreen Forest",
    43: "Mixed Forest",
    51: "Dwarf Scrub",
    52: "Shrub/Scrub",
    71: "Grassland/Herbaceous",
    72: "Sedge/Herbaceous",
    73: "Lichens",
    74: "Moss",
    81: "Pasture/Hay",
    82: "Cultivated Crops",
    90: "Woody Wetlands",
    95: "Emergent Herbaceous Wetlands",
    101: "Canada",
    102: "Mexico",
    103: "Cuba",
}

# Earth nominal equatorial radius via https://arxiv.org/pdf/1510.07674.pdf
# Hardcoded here instead of adding astropy as a dependency
# If this is changed (e.g. to more precision), test_earth_radius_meters
# must also be updated
earth_radius_meters = 6378100


def landcover_score(landcover_pixel_data, dl_for_arms_meters):
    """Input: landcover_pixel_data: 1D array of landcover pixel data, e.g. 
    output from pixel_data_from_rasters()

    Output: Total landcover score obtained by summing result of passing the 
    value at each pixel into the Score.landcover_score_by_type dict.

    Note:
    Landcover pixel data should conform to the National
    Land Cover Database Class Legend, available at
    https://www.mrlc.gov/sites/default/files/NLCDclasses.pdf
      Pix value   Description
      0           Ocean Water
      11          Open Water
      12          Perennial Ice/Snow
      21          Developed, Open Space
      22          Developed, Low Intensity
      23          Developed, Medium Intensity
      24          Developed, High Intensity
      31          Barren Land (Rock/Sand/Clay)
      41          Deciduous Forest
      42          Evergreen Forest
      43          Mixed Forest
      51          Dwarf Scrub
      52          Shrub/Scrub
      71          Grasslands/Herbaceous
      72          Sedge/Herbaceous
      73          Lichens
      74          Moss
      81          Pasture/Hay
      82          Cultivated Crops
      90          Woody Wetlands
      95          Emergent Herbaceous Wetlands
      101 - 103   Non-U.S. Land
    """
    # Just sum over the landcover scores set above for all pixels,
    # and multiply the result by some normalization, so this is comparable
    # to other scores (here the normalization is 1e-5)
    return np.sum(
        np.array([
            landcover_score_by_type[v] * dl_for_arms_meters
            for v in landcover_pixel_data
        ])) * 1e-5
