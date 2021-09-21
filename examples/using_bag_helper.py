import os
import logging

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.helper import BAGError, Helper

logger = logging.getLogger(__name__)
set_logging(ns_list=['hyo2.bag'])

try:
    raise BAGError("test")
except BAGError as e:
    logger.debug(e)

data_folder = Helper.samples_folder()
if os.path.exists(data_folder):
    logger.debug("data folder: %s" % data_folder)

iso_folder = Helper.iso19139_folder()
if os.path.exists(iso_folder):
    logger.debug("iso folder: %s" % iso_folder)

iso_folder = Helper.iso19757_3_folder()
if os.path.exists(iso_folder):
    logger.debug("iso folder: %s" % iso_folder)
