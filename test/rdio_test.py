import unittest
import sys
sys.path += ["../rdio"]
from rdio import Api, validate_email


class RdioTest(unittest.TestCase):

    def setUp(self):
        self.api = Api()

    def test_validate_email(self):
        self.assertEqual(validate_email('ben@kree.gr'), 1)
        self.assertEqual(validate_email('ben@kree.info'), 1)


if __name__ == 'main':
    unittest.main()
