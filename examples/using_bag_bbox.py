import os
import logging
from PySide2 import QtWidgets  # required by matplotlib
from matplotlib import pyplot as plt

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.bag import BAGError
from hyo2.bag.helper import Helper
from hyo2.bag.bbox import Bbox2Gdal

logger = logging.getLogger(__name__)
set_logging(ns_list=['hyo2.bag'])

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0, mode='r')
logger.debug(bag_0)

logger.debug(type(bag_0.elevation(mask_nan=True)))
logger.debug(bag_0.elevation(mask_nan=True).shape)
logger.debug(bag_0.elevation(mask_nan=True).dtype)
# ax =plt.contourf(bag_0.elevation(mask_nan=True))
# plt.colorbar(ax)
# plt.show()

bag_meta = bag_0.populate_metadata()
logger.debug(bag_meta)

Bbox2Gdal(bag_meta, fmt="gjs", title=os.path.basename(file_bag_0))
Bbox2Gdal(bag_meta, fmt="gml", title=os.path.basename(file_bag_0))
Bbox2Gdal(bag_meta, fmt="kml", title=os.path.basename(file_bag_0))
Bbox2Gdal(bag_meta, fmt="shp", title=os.path.basename(file_bag_0))
