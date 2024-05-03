import os
import logging

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.base import is_bag, File
from hyo2.bag.helper import Helper

logger = logging.getLogger(__name__)
set_logging(ns_list=['hyo2.bag'])

# Example that use bag.base to:
# - test for being a BAG file
# - open and read some metadata info from a BAG file

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_0):
    logger.info("- file_bag_0: %s is BAG? %r" % (file_bag_0, is_bag(file_bag_0)))

file_bag_1 = os.path.join(Helper.samples_folder(), "bdb_02.bag")
if os.path.exists(file_bag_1):
    logger.info("- file_bag_1: %s is BAG? %r" % (file_bag_1, is_bag(file_bag_1)))

file_fake_0 = os.path.join(Helper.samples_folder(), "fake_00.bag")
if os.path.exists(file_fake_0):
    logger.info("- file_fake_0: %s is BAG? %r" % (file_fake_0, is_bag(file_fake_0)))

bag_0 = File(file_bag_0)
logger.info("\n%s\n" % bag_0)
logger.info("filename: %s" % bag_0.filename)
logger.info("attributes for %s: %d" % (bag_0.attrs, len(bag_0.attrs)))
logger.info("driver: %s" % bag_0.driver)
bag_0.flush()
bag_0.close()
logger.info("\n%s\n" % bag_0)

bag_1 = File(file_bag_1)
bag_1.flush()
bag_1.close()

try:
    fake_0 = File(file_fake_0)
except IOError:
    logger.info("Expected exception")



