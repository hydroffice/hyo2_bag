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
from hyo2.bag.meta import Meta

# file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
# file_bag_0 = os.path.join(os.path.dirname(__file__), "tmp_copy.bag")
file_bag_0 = R"C:\Users\gmasetti\Desktop\cube.bag"
if os.path.exists(file_bag_0):
    print("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0)
ret = bag_0.validate_metadata()
print("valid: %s" % ret)

if not ret:
    for bag_error in bag_0.meta_errors:
        print(" - %s" % bag_error)