import unittest
import json
import os

from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)


class TestProgressLoadSave(unittest.TestCase):
    def setUp(self):
        self.path = "test_progress.json"
        self.data = {"coins": 15, "unlocked": ["chick_1.png", "chick_2.png"]}
        with open(self.path, "w") as f:
            json.dump(self.data, f)

    def test_load_progress(self):
        with open(self.path) as f:
            loaded = json.load(f)
        self.assertEqual(loaded["coins"], 15)
        self.assertIn("chick_2.png", loaded["unlocked"])

    def tearDown(self):
        os.remove(self.path)

if __name__ == "__main__":
    unittest.main()
