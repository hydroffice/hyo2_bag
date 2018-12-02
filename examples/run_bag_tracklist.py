import subprocess
import os

from hyo2.bag.helper import Helper
from hyo2.bag import tools


tools_folder = os.path.abspath(os.path.dirname(tools.__file__))
tool_path = os.path.join(tools_folder, 'bag_tracklist.py')
print("tool: %s" % tool_path)

# help
print("\n\n# -h")
subprocess.call("python %s -h" % tool_path)

# verbose + test file
file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_02.bag")
print("\n\n# -v %s" % file_bag_0)
subprocess.call("python %s -v -hd -o test_it.csv %s" % (tool_path, file_bag_0))

# verbose + fake file
file_bag_0 = os.path.join(Helper.samples_folder(), "not_present_00.bag")
print("\n\n# -v %s" % file_bag_0)
subprocess.call("python %s -v %s" % (tool_path, file_bag_0))

# test file
file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_02.bag")
print("\n\n# %s" % file_bag_0)
subprocess.call("python %s %s" % (tool_path, file_bag_0))
