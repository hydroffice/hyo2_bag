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

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_0):
    print("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0)
print(bag_0)

print(type(bag_0.elevation(mask_nan=True)), bag_0.elevation(mask_nan=True).shape, bag_0.elevation(mask_nan=True).dtype)
# ax =plt.contourf(bag_0.elevation(mask_nan=True))
# plt.colorbar(ax)
# plt.show()

bag_meta = bag_0.populate_metadata()
print(bag_meta)

from hyo2.bag.bbox import Bbox2Gdal
Bbox2Gdal(bag_meta, fmt="gjs", title=os.path.basename(file_bag_0))
Bbox2Gdal(bag_meta, fmt="gml", title=os.path.basename(file_bag_0))
Bbox2Gdal(bag_meta, fmt="kml", title=os.path.basename(file_bag_0))
Bbox2Gdal(bag_meta, fmt="shp", title=os.path.basename(file_bag_0))
