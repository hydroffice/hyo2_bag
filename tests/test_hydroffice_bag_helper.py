import os
import unittest

# noinspection PyUnresolvedReferences
from hyo2.bag.helper import Helper


class TestBagHelper(unittest.TestCase):

    def test_bag_samples_folder(self):
        assert os.path.exists(Helper.samples_folder())


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBagHelper))
    return s
