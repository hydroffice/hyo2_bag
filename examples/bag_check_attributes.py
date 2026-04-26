import logging

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.bag import BAGFile

set_logging(ns_list=['hyo2.bag'])
logger = logging.getLogger(__name__)

vr_bag_path = r"G:\My Drive\_ccom\QC Tools\data\survey\QC Tools 4\BAG_Checks\VR_resolution_is_zero\H11694_MB_VR_MLLW_1of2.bag"
# vr_bag_path = r"G:\My Drive\_ccom\QC Tools\data\survey\QC Tools 4\BAG_Checks\CRS error missing bracket\H13873_MB_VR_MLLW_1of1.bag"

vr_bag = BAGFile(vr_bag_path, mode="r")

if vr_bag.has_bag_version():
    logger.debug(f"Version {vr_bag.bag_version()} is official: {vr_bag.has_official_bag_version()}")

if vr_bag.has_attr_elevation_min_value() and vr_bag.has_attr_elevation_max_value():
    logger.debug(f"Elevation min/max: {vr_bag.elevation_min_max()}")
    logger.debug(f"Attribute elevation max value: {vr_bag.attr_elevation_max_value()}")
    logger.debug(f"Attribute elevation min value: {vr_bag.attr_elevation_min_value()}")

if vr_bag.has_attr_uncertainty_min_value() and vr_bag.has_attr_uncertainty_max_value():
    logger.debug(f"Uncertainty min/max: {vr_bag.uncertainty_min_max()}")
    logger.debug(f"Attribute uncertainty max value: {vr_bag.attr_uncertainty_max_value()}")
    logger.debug(f"Attribute uncertainty min value: {vr_bag.attr_uncertainty_min_value()}")

