import os
import logging

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper
from hyo2.bag.meta import Meta

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

# file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
# file_bag_0 = r"D:\google_drive\_ccom\QC Tools\data\survey\BAG Checks\ResolutionCheck\F00799_MB_2m_MLLW_1of2.bag"
file_bag_0 = r"C:\code\cpp\bag\examples\sample-data\NAVO_data\JD211_public_Release_1-4_UTM.bag"
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0, mode="r")
bag_0.populate_metadata()
logger.debug(bag_0)

