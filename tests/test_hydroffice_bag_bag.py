import unittest
import os

from hyo2.bag.bag import BAGFile


class TestBAGFile(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_instance(self):
        self.assertTrue(True)


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBAGFile))
    return s
