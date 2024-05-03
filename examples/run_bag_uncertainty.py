import logging
import subprocess
import os

from hyo2.abc2.lib.logging import set_logging
from hyo2.bag.helper import Helper
from hyo2.bag import tools

logger = logging.getLogger(__name__)
set_logging(ns_list=['hyo2.bag'])

tools_folder = os.path.abspath(os.path.dirname(tools.__file__))
tool_path = os.path.join(tools_folder, 'bag_uncertainty.py')
logger.debug("tool: %s" % tool_path)

# help
logger.debug("# -h")
subprocess.call("python %s -h" % tool_path)

# verbose + test file
file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
logger.debug("# -v %s" % file_bag_0)
subprocess.call("python %s -v -o test_unc.tiff %s" % (tool_path, file_bag_0))
subprocess.call("python %s -v -o test_unc.ascii -f ascii %s" % (tool_path, file_bag_0))

# verbose + fake file
file_bag_0 = os.path.join(Helper.samples_folder(), "not_present_00.bag")
logger.debug("# -v %s" % file_bag_0)
subprocess.call("python %s -v %s" % (tool_path, file_bag_0))

# test file
file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
logger.debug("# %s" % file_bag_0)
subprocess.call("python %s %s" % (tool_path, file_bag_0))
