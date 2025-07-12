import unittest
from stats_window import StatsWindow

class TestStatsWindow(unittest.TestCase):
    def test_format_difficulty_easy(self):
        w = StatsWindow()
        diff = {"gap_height": 200}
        self.assertEqual(w.format_difficulty(diff), "Легко")

    def test_format_difficulty_hard(self):
        w = StatsWindow()
        diff = {"gap_height": 100}
        self.assertEqual(w.format_difficulty(diff), "Сложно")

if __name__ == "__main__":
    unittest.main()
