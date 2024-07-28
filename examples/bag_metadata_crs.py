import os
import logging

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper
from hyo2.bag.meta import Meta

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

# file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
file_bag_0 = r"D:\google_drive\_ccom\QC Tools\data\survey\BAG Checks\QC3_error\F00834_MB_VR_MLLW_2of2.bag"
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0, mode='r')
logger.debug(bag_0)

meta = Meta(bag_0.metadata())

logger.debug("crs: %s (%s)" % (meta.wkt_srs, type(meta.wkt_srs)))
