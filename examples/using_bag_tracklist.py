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
from hyo2.bag.tracklist import TrackList2Csv

bag_file = os.path.join(Helper.samples_folder(), "bdb_01.bag")
bag = BAGFile(bag_file)
tl = bag.tracking_list()
tl2csv = TrackList2Csv(tl)

bag_file = os.path.join(Helper.samples_folder(), "bdb_02.bag")
bag = BAGFile(bag_file)
tl = bag.tracking_list()
tl_fields = bag.tracking_list_fields()
tl_types = bag.tracking_list_types()
print(tl_fields)
print(tl_types)
print(tl)
tl2csv = TrackList2Csv(track_list=tl, header=tl_fields)
