import unittest

# noinspection PyUnresolvedReferences
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


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBAGError))
    return s
