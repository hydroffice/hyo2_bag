import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # change to WARNING to reduce verbosity, DEBUG for high verbosity
ch_formatter = logging.Formatter('%(levelname)-9s %(name)s.%(funcName)s:%(lineno)d > %(message)s')
ch.setFormatter(ch_formatter)
logger.addHandler(ch)

from hyo2.bag import BAGFile
from hyo2.bag import BAGError
from hyo2.bag.helper import Helper

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
# file_bag_0 = "D:\\test_data\\radar_bag\\Sample_Beaufort_2\\Sample_Beaufort_2.bag"
if os.path.exists(file_bag_0):
    print("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0)
print(bag_0)

output_xml = "fixed_metadata.xml"
if not os.path.exists(output_xml):
    raise RuntimeError("unable to find metadata file: %s" % output_xml)
bag_0.substitute_metadata(output_xml)
os.remove(output_xml)
