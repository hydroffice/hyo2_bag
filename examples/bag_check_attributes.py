import logging

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.bag import BAGFile

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

vr_bag_path = r"G:\My Drive\_ccom\QC Tools\data\survey\QC Tools 4\BAG_Checks\VR_resolution_is_zero\H11694_MB_VR_MLLW_1of2.bag"

vr_bag = BAGFile(vr_bag_path, mode="r")

logger.debug(f"Version {vr_bag.bag_version()} is official: {vr_bag.has_official_bag_version()}")

