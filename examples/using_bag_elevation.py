import os
import logging
from matplotlib import pyplot as plt

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # change to WARNING to reduce verbosity, DEBUG for high verbosity
ch_formatter = logging.Formatter('%(levelname)-9s %(name)s.%(funcName)s:%(lineno)d > %(message)s')
ch.setFormatter(ch_formatter)
logger.addHandler(ch)

from hyo2.bag import BAGFile
from hyo2.bag import BAGError
from hyo2.bag.helper import Helper

bag_file = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(bag_file):
    print("- file_bag_0: %s" % bag_file)

bag = BAGFile(bag_file)

bag_meta = bag.populate_metadata()
print(bag_meta)

print("has elevation? %s" % bag.has_elevation())

bag_elevation = bag.elevation(mask_nan=False)
print(type(bag.elevation()), bag.elevation().shape, bag.elevation().dtype)

from hyo2.bag.elevation import Elevation2Gdal
Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="ascii")
Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="geotiff")
Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="xyz")


