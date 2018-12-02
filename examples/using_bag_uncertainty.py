import os
import logging
from matplotlib import pyplot as plt

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

bag_file = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(bag_file):
    print("- file_bag_0: %s" % bag_file)

bag = BAGFile(bag_file)

bag_meta = bag.populate_metadata()
print(bag_meta)

print("has uncertainty? %s" % bag.has_uncertainty())
print("has product uncertainty? %s" % bag.has_product_uncertainty())

bag_uncertainty = bag.uncertainty(mask_nan=True)
print(type(bag.elevation(mask_nan=True)), bag.elevation(mask_nan=True).shape, bag.elevation(mask_nan=True).dtype)

from hyo2.bag.uncertainty import Uncertainty2Gdal
Uncertainty2Gdal(bag_uncertainty, bag_meta, fmt="ascii")
Uncertainty2Gdal(bag_uncertainty, bag_meta, fmt="geotiff")
Uncertainty2Gdal(bag_uncertainty, bag_meta, fmt="xyz")



