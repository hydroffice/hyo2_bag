import unittest
import os

from hyo2.bag.helper import Helper
from hyo2.bag.base import is_bag, File


class TestBagBase(unittest.TestCase):

    def setUp(self):
        self.file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
        self.file_bag_1 = os.path.join(Helper.samples_folder(), "bdb_02.bag")
        self.file_fake_0 = os.path.join(Helper.samples_folder(), "fake_00.bag")

    def tearDown(self):
        pass

    def test_is_bag(self):
        self.assertTrue(is_bag(self.file_bag_0))
        self.assertTrue(is_bag(self.file_bag_1))
        self.assertFalse(is_bag(self.file_fake_0))

    def test_bag_File_raise(self):
        with self.assertRaises(IOError):
            File(self.file_fake_0)

    def test_bag_File_open(self):
        self.assertIsNotNone(File(self.file_bag_0))
        self.assertIsNotNone(File(self.file_bag_1))

    def test_bag_File_filename(self):
        bag_0 = File(self.file_bag_0)
        self.assertEqual(os.path.abspath(self.file_bag_0), bag_0.filename)
        bag_1 = File(self.file_bag_1)
        self.assertEqual(os.path.abspath(self.file_bag_1), bag_1.filename)


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBagBase))
    return s
