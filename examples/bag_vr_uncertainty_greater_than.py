import os
import logging

from hyo2.abc2.lib.logging import set_logging
from hyo2.abc2.lib.testing import Testing
from hyo2.abc2.lib.gdal_aux import GdalAux
from hyo2.bag.bag import BAGFile
from hyo2.bag.meta import Meta
from hyo2.qc4.lib.common.writers.s57_writer import S57Writer
from hyo2.qc4.lib.common.writers.kml_writer import KmlWriter
from hyo2.qc4.lib.common.writers.shp_writer import ShpWriter

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

# file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
file_bag_0 = r"D:\google_drive\_ccom\QC Tools\data\survey\BAG Checks\H13275_MB_VR_MLLW.bag"
th = 2.0

root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
testing = Testing(root_folder=root_folder)

if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

bag_0 = BAGFile(file_bag_0, mode="r")
logger.debug(bag_0)

GdalAux.push_gdal_error_handler()
GdalAux.check_gdal_data(verbose=True)

meta = Meta(bag_0.metadata())

ret = bag_0.vr_uncertainty_greater_than(th=th)
logger.debug(ret)

s57_bn_path = os.path.join(testing.output_data_folder(), "%s.blue_notes.000" % os.path.basename(file_bag_0))
s57_ss_path = os.path.join(testing.output_data_folder(), "%s.soundings.000" % os.path.basename(file_bag_0))

flags_for_blue_notes = list()
for entry in ret:
    flags_for_blue_notes.append([entry[0], entry[1], "%.2f" % entry[2]])
S57Writer.write_bluenotes(feature_list=flags_for_blue_notes, path=s57_bn_path, list_of_list=False)
S57Writer.write_soundings(feature_list=ret, path=s57_ss_path, list_of_list=False)
KmlWriter().write_bluenotes(feature_list=ret, path=s57_ss_path[:-4], list_of_list=False)
ShpWriter().write_bluenotes(feature_list=ret, path=s57_ss_path[:-4], list_of_list=False)
