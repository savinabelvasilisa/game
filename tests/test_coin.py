import unittest
from unittest.mock import MagicMock, patch
from game_objects.coin import Coin

class TestCoin(unittest.TestCase):
    @patch("pygame.mixer.Sound")  # отключаем звук в тестах
    def setUp(self, mock_sound):
        self.mock_pipe = MagicMock()
        self.mock_pipe.x = 300
        self.coin = Coin(pipe=self.mock_pipe, offset_x=40, y=100)

    @patch("pygame.mixer.Sound")
    def test_initial_position(self, mock_sound):
        self.assertEqual(self.coin.x, 340)
        self.assertEqual(self.coin.y, 100)

    @patch("pygame.mixer.Sound")
    def test_update_position(self, mock_sound):
        self.mock_pipe.x = 250
        self.coin.update(volume=1.0)
        self.assertEqual(self.coin.x, 290)

    @patch("pygame.mixer.Sound")
    def test_is_off_screen(self, mock_sound):
        self.mock_pipe.x = -200
        self.assertTrue(self.coin.is_off_screen())
