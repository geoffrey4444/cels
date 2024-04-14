# Distributed under the MIT License.
# See LICENSE for details.
landcover_cost = {
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
    51: 0,  # swarf scrub
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

landcover_labels = {
    0: "ocean",
    11: "open water",
    12: "perennial ice/snow",
    21: "developed, open space",
    22: "developed, low intensity",
    23: "developed, medium intensity",
    24: "developed, high intensity",
    31: "barren land (rock/sand/clay)",
    41: "deciduous forest",
    42: "evergreen forest",
    43: "mixed forest",
    51: "swarf scrub",
    52: "shrub/scrub",
    71: "grassland/herbaceous",
    72: "sedge/herbaceous",
    73: "lichens",
    74: "moss",
    81: "pasture/hay",
    82: "cultivated crops",
    90: "woody wetlands",
    95: "emergent herbaceous wetlands",
    101: "Canada",
    102: "Mexico",
    103: "Cuba",
}

# Earth nominal equatorial radius via https://arxiv.org/pdf/1510.07674.pdf
# Hardcoded here instead of adding astropy as a dependency
earth_radius_meters = 6378100
