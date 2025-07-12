import unittest
from unittest.mock import patch, MagicMock
from game_window import GameWidget
from PyQt5.QtWidgets import QApplication
import sys
import pygame
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

@patch("pygame.mixer.Sound")
@patch("pygame.mixer.music")
class TestGameWidget(unittest.TestCase):
    def setUp(self):
        pygame.mixer.init()

        config = {
            "pipe_speed": 3,
            "gap_height": 200,
            "pipe_interval": 60,
            "difficulty": "easy",
            "bg": "assets/bg_forest.png",
            "volume": 50,
            "character": "chick_1.png"
        }
        self.widget = GameWidget(config=config)
        self.widget.set_show_menu_callback(lambda: None)
        self.widget.set_show_stats_callback(lambda: None)



    def test_initial_score_and_coins(self, mock_music, mock_sound):
        self.assertEqual(self.widget.score, 0)
        self.assertEqual(self.widget.coins_collected, 0)

    def test_game_loop_spawns_pipe(self, mock_music, mock_sound):
        self.widget.pipe_timer = 60
        self.widget.pipes_spawned = 0
        self.widget.game_loop()
        self.assertEqual(len(self.widget.pipes), 1)

    def test_end_game_does_not_crash(self, mock_music, mock_sound):
        self.widget.end_game()
        self.assertTrue(self.widget.game_over)

    def test_complete_level_does_not_crash(self, mock_music, mock_sound):
        self.widget.complete_level()
        self.assertTrue(self.widget.level_completed)
