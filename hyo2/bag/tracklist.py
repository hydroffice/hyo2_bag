import os
import logging

log = logging.getLogger(__name__)

import numpy as np
from .meta import Meta
from .helper import BAGError, Helper
from . import __version__


class TrackList2Csv(object):

    default_csv_name = "BAG.tracklist.csv"

    def __init__(self, track_list, csv_file=None, header=None, comment=None):
        assert isinstance(track_list, np.ndarray)
        log.debug("track list shape: %s" % track_list.shape)
        log.debug("track list size: %s" % track_list.size)

        self.track_list = track_list
        if self.track_list.size == 0:
            log.warning("nothing to export since the tracking list is empty")
            return

        self.csv_file = csv_file
        if csv_file is None:
            self.csv_file = self.default_csv_name
        self.csv_file = os.path.abspath(self.csv_file)
        log.debug("output: %s" % self.csv_file)

        self.header = header
        if self.header is None:
            self.header = str()
        if type(self.header) is tuple:
            self.header = ",".join(fld for fld in self.header)
            self.header += "\n"
        log.debug("header: %s" % self.header)

        self.comment = comment
        if self.comment is None:
            self.comment = "# Exported using BAG tools r%s\n" % __version__
        log.debug("comment: %s" % self.comment)

        with open(self.csv_file, 'w') as f:
            f.write(self.comment)
            f.write(self.header)
            for row in track_list:
                f.write("%s, %s, %s, %s, %s, %s\n" % (row[0], row[1], row[2], row[3], row[4], row[5]))
