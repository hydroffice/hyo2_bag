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

# Example that use bag.BAGFile to:
# - open a BAG file
# - read the whole elevation and uncertainty layers
# - read a selected range of rows for the elevation and uncertainty layers

file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_02.bag")
if os.path.exists(file_bag_0):
    logger.debug("- file_bag_0: %s" % file_bag_0)

# - open a file
bag_0 = BAGFile(file_bag_0)
logger.debug("\n%s\n" % bag_0)

# - get elevation shape
logger.info("elevation shape: %s" % (bag_0.elevation_shape(), ))
# - read the full elevation
full_elevation = bag_0.elevation(mask_nan=True)
logger.info("elevation array:\n  type: %s\n  shape: %s\n  dtype: %s"
            % (type(full_elevation), full_elevation.shape, full_elevation.dtype))
ax = plt.contourf(full_elevation)
plt.colorbar(ax)
plt.show()
# - read the first 10 rows of the elevation layers
selection_slice = slice(0, 10)
sliced_elevation = bag_0.elevation(mask_nan=True, row_range=selection_slice)
logger.info("sliced elevation array:\n  type: %s\n  shape: %s\n  dtype: %s"
            % (type(sliced_elevation), sliced_elevation.shape, sliced_elevation.dtype))
ax = plt.contourf(sliced_elevation)
plt.colorbar(ax)
plt.show()

# - get uncertainty shape
logger.info("uncertainty shape: %s" % (bag_0.uncertainty_shape(), ))
# - read the full uncertainty
full_uncertainty = bag_0.uncertainty(mask_nan=True)
logger.info("uncertainty array:\n  type: %s\n  shape: %s\n  dtype: %s"
            % (type(full_uncertainty), full_uncertainty.shape, full_uncertainty.dtype))
ax = plt.contourf(full_uncertainty)
plt.colorbar(ax)
plt.show()
# - read the first 10 rows of the uncertainty layers
selection_slice = slice(0, 10)
sliced_uncertainty = bag_0.uncertainty(mask_nan=True, row_range=selection_slice)
logger.info("sliced uncertainty array:\n  type: %s\n  shape: %s\n  dtype: %s"
            % (type(sliced_uncertainty), sliced_uncertainty.shape, sliced_uncertainty.dtype))
ax = plt.contourf(sliced_uncertainty)
plt.colorbar(ax)
plt.show()

# - tracking list
logger.debug("\ntracking list:\n  type: %s\n  shape: %s\n  dtype: %s"
             % (type(bag_0.tracking_list()), bag_0.tracking_list().shape, bag_0.tracking_list().dtype))

# - metadata
logger.debug("\nmetadata: %s %s\n" % (type(bag_0.metadata()), len(bag_0.metadata())))
file_bag_0_xml = os.path.join("bdb_00.bag.xml")
bag_0.extract_metadata(name=file_bag_0_xml)

bag_0.populate_metadata()
logger.debug("rows, cols: %d, %d" % (bag_0.meta.rows, bag_0.meta.cols))
logger.debug("res x, y: %f, %f" % (bag_0.meta.res_x, bag_0.meta.res_y))
logger.debug("corner SW, NE: %s, %s" % (bag_0.meta.sw, bag_0.meta.ne))
logger.debug("coord sys: %s" % bag_0.meta.wkt_srs)

logger.debug(bag_0)

file_bag_1 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
if os.path.exists(file_bag_1):
    logger.debug("file_bag_1: %s" % file_bag_1)

file_bag_2 = os.path.abspath(os.path.join("test_00.bag"))
logger.debug("file_bag_2: %s" % file_bag_2)

bag_2 = BAGFile.create_template(file_bag_2)
bag_2.close()

if os.path.exists(file_bag_2):
    os.remove(file_bag_2)
