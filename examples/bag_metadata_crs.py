import os
import logging

from osgeo import osr

from hyo2.abc2.lib.logging import set_logging
from hyo2.abc2.lib.gdal_aux import GdalAux
from hyo2.bag.bag import BAGFile
from hyo2.bag.helper import Helper
from hyo2.bag.meta import Meta

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
# file_bag_0 = r""
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

GdalAux.push_gdal_error_handler()
GdalAux.check_gdal_data()

bag_0 = BAGFile(file_bag_0, mode='r')
logger.debug(bag_0)

meta = Meta(bag_0.metadata())

logger.debug("crs: %s (%s)" % (meta.wkt_srs, type(meta.wkt_srs)))

# Try to create a transformation from BAG CRS to WGS84

osr_bag = osr.SpatialReference()
osr_bag.ImportFromWkt(meta.wkt_srs)
osr_bag.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
if osr_bag.IsCompound():
    osr_bag.StripVertical()
osr_geo = osr.SpatialReference()
osr_geo.ImportFromEPSG(4326)  # geographic WGS84
osr_geo.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
loc2geo = osr.CoordinateTransformation(osr_bag, osr_geo)

logger.debug(osr_bag.ExportToWkt())
