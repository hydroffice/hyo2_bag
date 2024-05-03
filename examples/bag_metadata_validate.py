import os
import logging

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper
from hyo2.bag.meta import Meta

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0, mode='r')
ret = bag_0.validate_metadata()
logger.debug("valid: %s" % ret)

if not ret:
    for bag_error in bag_0.meta_errors:
        logger.debug(" - %s" % bag_error)