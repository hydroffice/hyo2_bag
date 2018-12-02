import unittest
import os

from hyo2.bag.helper import Helper
from hyo2.bag.helper import BAGError


class TestBAGError(unittest.TestCase):

    def setUp(self):
        self.err = BAGError("test")

    def tearDown(self):
        pass

    def test_is_instance(self):
        self.assertTrue(isinstance(self.err, Exception))

    def test_raise(self):
        with self.assertRaises(BAGError):
            raise self.err
        try:
            raise self.err
        except BAGError as e:
            self.assertIn("test", str(e))

    def test_has_message(self):
        assert hasattr(self.err, 'message')


class TestBagHelper(unittest.TestCase):

    def test_bag_samples_folder(self):
        assert os.path.exists(Helper.samples_folder())


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBAGError))
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBagHelper))
    return s
