import os
import logging
import numpy as np
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

print("has density? %s" % bag.has_density())
if not bag.has_density():
    exit()

bag_density = bag.density(mask_nan=True)
print(type(bag.density(mask_nan=True)),
      bag.density(mask_nan=True).shape,
      bag.density(mask_nan=True).dtype)

print("min: %s" % np.nanmin(bag_density))
print("max: %s" % np.nanmax(bag_density))

# from hyo2.bag.density import Density2Gdal
# Density2Gdal(bag_density=bag_density, bag_meta=bag_meta, fmt="ascii")
# Density2Gdal(bag_density=bag_density, bag_meta=bag_meta, fmt="geotiff")
# Density2Gdal(bag_density=bag_density, bag_meta=bag_meta, fmt="xyz")

