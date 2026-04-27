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

if vr_bag.has_attr_tracking_list_length():
    logger.debug(f"Tracking list length: {vr_bag.tracking_list().shape[0]}")
    logger.debug(f"Attribute tracking list length: {vr_bag.attr_tracking_list_length()}")

if vr_bag.has_varres_metadata():

    arr = vr_bag.varres_metadata_dim_x()
    if vr_bag.has_attr_varres_metadata_max_dim_x():
        logger.debug(f"Varres metadata max dimension x: {arr[arr != vr_bag.VR_META_DIM_NODATA].max()}")
        logger.debug(f"Attribute varres metadata max dimension x: {vr_bag.attr_varres_metadata_max_dim_x()}")
    if vr_bag.has_attr_varres_metadata_min_dim_x():
        logger.debug(f"Varres metadata min dimension x: {arr[arr != vr_bag.VR_META_DIM_NODATA].min()}")
        logger.debug(f"Attribute varres metadata min dimension x: {vr_bag.attr_varres_metadata_min_dim_x()}")

    arr = vr_bag.varres_metadata_dim_y()
    if vr_bag.has_attr_varres_metadata_max_dim_y():
        logger.debug(f"Varres metadata max dimension y: {arr[arr != vr_bag.VR_META_DIM_NODATA].max()}")
        logger.debug(f"Attribute varres metadata max dimension y: {vr_bag.attr_varres_metadata_max_dim_y()}")
    if vr_bag.has_attr_varres_metadata_min_dim_y():
        logger.debug(f"Varres metadata min dimension y: {arr[arr != vr_bag.VR_META_DIM_NODATA].min()}")
        logger.debug(f"Attribute varres metadata min dimension x: {vr_bag.attr_varres_metadata_min_dim_y()}")

    arr = vr_bag.varres_metadata_res_x()
    if vr_bag.has_attr_varres_metadata_max_res_x():
        logger.debug(f"Varres metadata max resolution x: {arr[arr != vr_bag.VR_META_RES_NODATA].max()}")
        logger.debug(f"Attribute varres metadata max resolution x: {vr_bag.attr_varres_metadata_max_res_x()}")
    if vr_bag.has_attr_varres_metadata_min_res_x():
        logger.debug(f"Varres metadata min resolution x: {arr[arr != vr_bag.VR_META_RES_NODATA].min()}")
        logger.debug(f"Attribute varres metadata min resolution x: {vr_bag.attr_varres_metadata_min_res_x()}")

    arr = vr_bag.varres_metadata_res_y()
    if vr_bag.has_attr_varres_metadata_max_res_y():
        logger.debug(f"Varres metadata max resolution y: {arr[arr != vr_bag.VR_META_RES_NODATA].max()}")
        logger.debug(f"Attribute varres metadata max resolution y: {vr_bag.attr_varres_metadata_max_res_y()}")
    if vr_bag.has_attr_varres_metadata_min_res_y():
        logger.debug(f"Varres metadata min resolution y: {arr[arr != vr_bag.VR_META_RES_NODATA].min()}")
        logger.debug(f"Attribute varres metadata min dimension x: {vr_bag.attr_varres_metadata_min_res_y()}")

if vr_bag.has_varres_refinements():

    arr = vr_bag.varres_refinements_depth()
    if vr_bag.has_attr_varres_refinements_max_depth():
        logger.debug(f"Varres refinements max depth: {arr[arr != vr_bag.BAG_NAN].max()}")
        logger.debug(f"Attribute varres refinements max depth: {vr_bag.attr_varres_refinements_max_depth()}")
    if vr_bag.has_attr_varres_refinements_min_depth():
        logger.debug(f"Varres refinements min depth: {arr[arr != vr_bag.BAG_NAN].min()}")
        logger.debug(f"Attribute varres refinements min depth: {vr_bag.attr_varres_refinements_min_depth()}")
        
    arr = vr_bag.varres_refinements_uncrt()
    if vr_bag.has_attr_varres_refinements_max_uncrt():
        logger.debug(f"Varres refinements max uncrt: {arr[arr != vr_bag.BAG_NAN].max()}")
        logger.debug(f"Attribute varres refinements max uncrt: {vr_bag.attr_varres_refinements_max_uncrt()}")
    if vr_bag.has_attr_varres_refinements_min_uncrt():
        logger.debug(f"Varres refinements min uncrt: {arr[arr != vr_bag.BAG_NAN].min()}")
        logger.debug(f"Attribute varres refinements min uncrt: {vr_bag.attr_varres_refinements_min_uncrt()}")

if vr_bag.has_varres_tracking_list():

    logger.debug(f"VR Tracking list length: {vr_bag.varres_tracking_list().shape[0]}")
    logger.debug(f"Attribute VR tracking list length: {vr_bag.attr_varres_tracking_list_length()}")
