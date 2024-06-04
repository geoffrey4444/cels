# Cosmic Explorer Location Search (CELS)
This python package contains code to assist with identifying and evaluating
potential locations for [Cosmic Explorer](https://cosmicexplorer.org), a planned
next-generation gravitational-wave observatory.

## Installation
To install this code in your python environment, you can run the 
following terminal command:
```sh
pip install -e .
```

## Usage
The following is an example of a command to run a search for potential
detector locations on two threads. In the terminal, navigate to the
top level directory of the CosmicExplorerLocationSearch repository, and 
then do the following commands:
```sh
mkdir test_search
findsites \
  --lon=-107.7 --lat=32.3 --width=100000.0 --height=40000.0 \
  --N=10 --arm_length=40000.0 --dl=1000.0 --opening-angle=90.0 \
  --rotation-angles=18 \
  --elevation=./tests/test_images/SouthNM_Elevation_1km.tif \
  --landcover=./tests/test_images/SouthNM_Landcover_1km.tif \
  --outscore=70.0 --outdir=./test_search/ --njobs=2
```
This command will output the following:
* geotiff images containing the best score at each vertex location
* shapefiles with the detectors with scores below the threshold `outscore`
* a csv file with scores of all configurations tested during the search
For help on the available options, run
```sh
findsites -h
```

Individual functions can also be used directly in python through
the following modules:
```python
from CosmicExplorerLocationSearch import Coordinates, Detector, Geotiff, Score
```
* `Coordinates`: utilities for converting longitude, latitude to x,y coordinates
in different projections
* `Detector`: a function `detector()` that creates a detector configuration,
represented as an an "L" shape determined by the locations of two end stations
and a vertex
* `Score`: functions to evaluate (score) detector configurations, using e.g.
elevation and landcover data

For help on an individual function, use Python's `help()` command to show
available commands and their documentation:
```python
import CosmicExplorerLocationSearch
help(CosmicExplorerLocationSearch)
from CosmicExplorerLocationSearch import Coordinates, Detector, Geotiff, Score
help(Coordinates)
help(Detector)
help(Geotiff)
help(Score)
```

## Data
The code requires geotiffs with elevation and landcover data for the United
States. Small, public-domain test images are included in the repository. 
Sources of national data include the following:
* [100-meter elevation data (2012)](https://earthworks.stanford.edu/catalog/stanford-zz186ss2071)
* [100-meter landcover data (2001)](https://purl.stanford.edu/wv372bn9329)
* [30-meter landcover data (2021)](https://www.mrlc.gov/data/nlcd-2021-land-cover-conus)
