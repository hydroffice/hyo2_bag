import os
import logging
from osgeo import osr

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper
from hyo2.bag.meta import Meta

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

# file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
file_bag_0 = r"C:\Users\gmasetti\Downloads\H13745_MB_4m_MLLW_1of1 (1).bag"
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0, mode='r')
logger.debug(bag_0)

meta = Meta(bag_0.metadata())

logger.debug("vertical datum: %s (%s)" % (meta.wkt_vertical_datum, type(meta.wkt_vertical_datum)))

vrs = osr.SpatialReference()
ret = vrs.ImportFromWkt(meta.wkt_vertical_datum)
logger.debug("wkt import: %s" % ret)

is_vertical = vrs.IsVertical() == 1
logger.debug('wkt is vertical: %s' % is_vertical)

is_epsg = vrs.GetAttrValue("AUTHORITY", 0).lower() == 'epsg'
if is_epsg:
    epsg = vrs.GetAttrValue("AUTHORITY", 1)
    logger.debug("EPSG:%s" % epsg)

is_depth = vrs.GetAttrValue("AXIS", 0).lower() == 'depth'
if is_depth:
    direction = vrs.GetAttrValue("AXIS", 1)
    logger.debug("depth is %s" % direction)
