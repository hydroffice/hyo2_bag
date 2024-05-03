import os
import logging
from shutil import copyfile
from PySide2 import QtWidgets  # required by matplotib
from matplotlib import pyplot as plt

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if not os.path.exists(file_bag_0):
    raise RuntimeError("the file does not exist: %s" % file_bag_0)
logger.debug("- file_bag_0: %s" % file_bag_0)

file_bag_copy = os.path.join(os.path.dirname(__file__), "tmp_copy.bag")
bag_copy = copyfile(file_bag_0, file_bag_copy)

bag_0 = BAGFile(file_bag_copy, mode='r+')
logger.debug(bag_0)

logger.debug(type(bag_0.elevation(mask_nan=True)))
logger.debug(bag_0.elevation(mask_nan=True).shape)
logger.debug(bag_0.elevation(mask_nan=True).dtype)

ax = plt.contourf(bag_0.elevation(mask_nan=True))
plt.colorbar(ax)
plt.show()

wkt_prj_hor = """
    PROJCS["UTM Zone 19, Northern Hemisphere",
      GEOGCS["WGS 84",
        DATUM["WGS_1984",
          SPHEROID["WGS 84",6378137,298.257223563,
            AUTHORITY["EPSG","7030"]],
            TOWGS84[0,0,0,0,0,0,0],
          AUTHORITY["EPSG","6326"]],
          PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
          UNIT["degree",0.0174532925199433,
            AUTHORITY["EPSG","9108"]],
          AUTHORITY["EPSG","4326"]],
          PROJECTION["Transverse_Mercator"],
          PARAMETER["latitude_of_origin",0],
          PARAMETER["central_meridian",-69],
          PARAMETER["scale_factor",0.9996],
          PARAMETER["false_easting",500000],
          PARAMETER["false_northing",0],
          UNIT["Meter",1]]
"""

wkt_prj_ver = """
    VERT_CS["Mean lower low water",
      VERT_DATUM["Mean lower low water",2000]]
"""

bag_0.modify_wkt_prj(wkt_prj_hor, wkt_prj_ver)
bag_0.modify_bbox(west=-70.68079657129087, east=-70.65526106943501, south=41.506684, north=41.52777)

bag_meta = bag_0.populate_metadata()
logger.debug(bag_meta)

bag_0.close()
os.remove(file_bag_copy)
