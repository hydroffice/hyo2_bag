import os
import logging

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper
from hyo2.bag.meta import Meta

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

# file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
file_bag_0 = r"C:\Users\gmasetti\Desktop\H13405S_MB_8m_MLLW_1of2_edited.bag"
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0, mode="r")
logger.debug(bag_0)

meta = Meta(bag_0.metadata())

output_xml = "original_metadata.xml"
bag_0.extract_metadata(output_xml)
# os.remove(output_xml)
