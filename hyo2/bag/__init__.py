"""
Hydro-Package
BAG
"""
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .helper import BAGError
from .base import is_bag
from .bag import BAGFile


name = 'BAG'
__version__ = '1.1.0'
__author__ = 'gmasetti@ccom.unh.edu'
__license__ = 'LGPLv3 license'
__copyright__ = 'Copyright (c) 2021, University of New Hampshire, Center for Coastal and Ocean Mapping'
