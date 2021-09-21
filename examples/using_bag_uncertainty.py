import os
import logging
from matplotlib import pyplot as plt

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.bag import BAGError
from hyo2.bag.helper import Helper
from hyo2.bag.uncertainty import Uncertainty2Gdal

logger = logging.getLogger(__name__)
set_logging(ns_list=['hyo2.bag'])

bag_file = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(bag_file):
    logger.debug("- file_bag_0: %s" % bag_file)

bag = BAGFile(bag_file)

bag_meta = bag.populate_metadata()
logger.debug(bag_meta)

logger.debug("has uncertainty? %s" % bag.has_uncertainty())
logger.debug("has product uncertainty? %s" % bag.has_product_uncertainty())

bag_uncertainty = bag.uncertainty(mask_nan=True)
logger.debug(type(bag.elevation(mask_nan=True)))
logger.debug(bag.elevation(mask_nan=True).shape)
logger.debug(bag.elevation(mask_nan=True).dtype)

Uncertainty2Gdal(bag_uncertainty, bag_meta, fmt="ascii")
Uncertainty2Gdal(bag_uncertainty, bag_meta, fmt="geotiff")
Uncertainty2Gdal(bag_uncertainty, bag_meta, fmt="xyz")
