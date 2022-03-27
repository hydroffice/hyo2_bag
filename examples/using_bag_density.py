import os
import logging
import numpy as np
from PySide2 import QtWidgets  # required by matplotlib
from matplotlib import pyplot as plt

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.bag import BAGError
from hyo2.bag.helper import Helper
# from hyo2.bag.density import Density2Gdal

logger = logging.getLogger(__name__)
set_logging(ns_list=['hyo2.bag'])

bag_file = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(bag_file):
    logger.debug("- file_bag_0: %s" % bag_file)

bag = BAGFile(bag_file, mode='r')

bag_meta = bag.populate_metadata()
logger.debug(bag_meta)

logger.debug("has density? %s" % bag.has_density())
if not bag.has_density():
    exit()

bag_density = bag.density(mask_nan=True)
logger.debug(type(bag.density(mask_nan=True)))
logger.debug(bag.density(mask_nan=True).shape)
logger.debug(bag.density(mask_nan=True).dtype)

logger.debug("min: %s" % np.nanmin(bag_density))
logger.debug("max: %s" % np.nanmax(bag_density))

# Density2Gdal(bag_density=bag_density, bag_meta=bag_meta, fmt="ascii")
# Density2Gdal(bag_density=bag_density, bag_meta=bag_meta, fmt="geotiff")
# Density2Gdal(bag_density=bag_density, bag_meta=bag_meta, fmt="xyz")
