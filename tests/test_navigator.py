import os
import sys
import unittest

# Allow importing from parent directory
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src.parsereparsepoint import Navigator

FILENAME = "..\\test_navigator.py"
IMAGES = current + "/images/"

# Allow tests to be run from parent directory
os.chdir(current)

class TestNavigator(unittest.TestCase):
    def __init__(self, methodName="runTest"):  # noqa
        super().__init__(methodName)
        self.fractional_score = {}

    def test_parse_ntfs_header(self):
        nav = Navigator.Navigator(IMAGES + "test_image.img")
        self.assertEqual(nav.bytes_per_cluster, 4096)
        self.assertEqual(nav.mft_byte_offset, 3221225472)
        self.assertEqual(len(nav.mft_clusters), 69888)

if __name__ == "__main__":
    unittest.main()
        

    