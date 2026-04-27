import os
import unittest

# noinspection PyUnresolvedReferences
from hyo2.bag.bag import BAGFile
# noinspection PyUnresolvedReferences
from hyo2.bag.bag_error import BAGError
# noinspection PyUnresolvedReferences
from hyo2.bag.helper import Helper


class TestBagBase(unittest.TestCase):

    def setUp(self):
        self.file_bag_0 = os.path.join(Helper.samples_folder(), "bdb_01.bag")
        self.file_bag_1 = os.path.join(Helper.samples_folder(), "bdb_02.bag")
        self.file_fake_0 = os.path.join(Helper.samples_folder(), "fake_00.bag")

    def tearDown(self):
        pass

    def test_is_bag(self):
        self.assertTrue(BAGFile.is_bag(self.file_bag_0, advanced=True))
        self.assertTrue(BAGFile.is_bag(self.file_bag_1, advanced=True))
        self.assertFalse(BAGFile.is_bag(self.file_fake_0, advanced=True))

    def test_bag_file_raise(self):
        with self.assertRaises(BAGError):
            BAGFile(self.file_fake_0)

    def test_bag_file_open(self):
        self.assertIsNotNone(BAGFile(self.file_bag_0))
        self.assertIsNotNone(BAGFile(self.file_bag_1))

    def test_bag_file_filename(self):
        bag_0 = BAGFile(self.file_bag_0)
        self.assertEqual(os.path.abspath(self.file_bag_0), bag_0.filename)
        bag_1 = BAGFile(self.file_bag_1)
        self.assertEqual(os.path.abspath(self.file_bag_1), bag_1.filename)


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBagBase))
    return s
