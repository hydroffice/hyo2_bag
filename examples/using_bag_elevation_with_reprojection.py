import os
import logging

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

bag = BAGFile(bag_file, mode='r')

bag_meta = bag.populate_metadata()
logger.debug(bag_meta)

bag_elevation = bag.elevation(mask_nan=False)
logger.debug(type(bag.elevation()))
logger.debug(bag.elevation().shape)
logger.debug(bag.elevation().dtype)

Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="ascii", epsg=4326)
Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="geotiff", epsg=4326)
Elevation2Gdal(bag_elevation=bag_elevation, bag_meta=bag_meta, fmt="xyz", epsg=4326)
