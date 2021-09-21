import os
import logging
from PySide2 import QtWidgets  # required by matplotlib
from matplotlib import pyplot as plt

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.bag import BAGError
from hyo2.bag.helper import Helper
from hyo2.bag.elevation import Elevation2Gdal

logger = logging.getLogger(__name__)
set_logging(ns_list=['hyo2.bag'])

bag_file = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(bag_file):
    logger.debug("- file_bag_0: %s" % bag_file)

bag = BAGFile(bag_file)

bag_meta = bag.populate_metadata()
logger.debug(bag_meta)

logger.debug("has elevation? %s" % bag.has_elevation())

bag_elevation = bag.elevation(mask_nan=False)
logger.debug(type(bag.elevation()), bag.elevation().shape, bag.elevation().dtype)

Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="ascii")
Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="geotiff")
Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="xyz")
