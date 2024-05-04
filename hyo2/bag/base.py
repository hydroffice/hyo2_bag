import os
import logging

import h5py
from h5py._hl.base import with_phil

logger = logging.getLogger(__name__)


def is_bag(file_name):
    """ Determine if a file is valid BAG (False if it doesn't exist). """

    # we first check if the file is a valid hdf5 (it also checks if the file exists)
    if not h5py.is_hdf5(file_name):
        return False

    fid = h5py.File(file_name, 'r')

    try:
        fid["BAG_root"]

    except KeyError:
        return False

    return True


class File(h5py.File):
    """ Represents a BAG file (at low-level, thin wrapper around h5py). """

    def __init__(self, name, mode: str = "r", driver=None,
                 libver=None, userblock_size=None, swmr=False, **kwds):
        """
        Create a new file object.

        See the h5py user guide for a detailed explanation of the options.

        name
            Name of the file on disk.  Note: for files created with the 'core'
            driver, HDF5 still requires this be non-empty.
        driver
            Name of the driver to use.  Legal values are None (default,
            recommended), 'core', 'sec2', 'stdio', 'mpio'.
        libver
            Library version bounds.  Currently only the strings 'earliest'
            and 'latest' are defined.
        userblock
            Desired size of user block.  Only allowed when creating a new
            file (mode w, w- or x).
        swmr
            Open the file in SWMR read mode. Only used when mode = 'r'.
        Additional keywords
            Passed on to the selected file driver.
        """
        super(File, self).__init__(name=name, mode=mode, driver=driver,
                                   libver=libver, userblock_size=userblock_size, swmr=swmr, **kwds)

    def close(self):
        """ Close the file.  All open objects become invalid """
        logger.debug("closing")
        super(File, self).close()

    def flush(self):
        """ Tell the BAG library to flush its buffers. """
        logger.debug("flushing")
        super(File, self).flush()

    @with_phil
    def __repr__(self):
        if not self.id:
            logger.info("closed file")
            r = '<BAG file>\n'
            r += "  <status: closed>"
        else:
            # Filename has to be forced to Unicode if it comes back bytes
            # Mode is always a "native" string
            filename = self.filename
            if isinstance(filename, bytes):  # Can't decode fname
                filename = filename.decode('utf8', 'replace')
            r = '<BAG file "%s" (mode %s)>' % (os.path.basename(filename), self.mode)
            r += "  <status: open>\n"
            r += "  <id: %s>\n" % self.id
            r += "  <name: %s>\n" % self.name
            r += "  <driver: %s>\n" % self.driver
            r += "  <user block size: %s>\n" % self.userblock_size

        return r
