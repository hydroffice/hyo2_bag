import os
import logging

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper
from hyo2.bag.meta import Meta

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0)
logger.debug(bag_0)

meta = Meta(bag_0.metadata())

logger.debug("vertical datum: %s (%s)" % (meta.wkt_vertical_datum, type(meta.wkt_vertical_datum)))
