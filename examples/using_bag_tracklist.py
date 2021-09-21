import os
import logging
from matplotlib import pyplot as plt

from hyo2.abc.lib.logging import set_logging
from hyo2.bag.bag import BAGFile
from hyo2.bag.bag import BAGError
from hyo2.bag.helper import Helper
from hyo2.bag.tracklist import TrackList2Csv

logger = logging.getLogger(__name__)
set_logging(ns_list=['hyo2.bag'])

bag_file = os.path.join(Helper.samples_folder(), "bdb_01.bag")
bag = BAGFile(bag_file)
tl = bag.tracking_list()
tl2csv = TrackList2Csv(tl)

bag_file = os.path.join(Helper.samples_folder(), "bdb_02.bag")
bag = BAGFile(bag_file)
tl = bag.tracking_list()
tl_fields = bag.tracking_list_fields()
tl_types = bag.tracking_list_types()
logger.debug(tl_fields)
logger.debug(tl_types)
logger.debug(tl)
_ = TrackList2Csv(track_list=tl, header=tl_fields)
