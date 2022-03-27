import os
import logging
from shutil import copyfile

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper
from hyo2.bag.meta import Meta

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

file_bag_copy = os.path.join(os.path.dirname(__file__), "tmp_copy.bag")
bag_copy = copyfile(file_bag_0, file_bag_copy)

bag_0 = BAGFile(file_bag_copy, mode="r+")
logger.debug(bag_0)

output_xml = "fixed_metadata.xml"
if not os.path.exists(output_xml):
    raise RuntimeError("unable to find metadata file: %s" % output_xml)
bag_0.substitute_metadata(output_xml)
os.remove(output_xml)

bag_0.close()
os.remove(file_bag_copy)
