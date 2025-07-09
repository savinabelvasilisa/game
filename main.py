# main.py
from PyQt5.QtWidgets import QApplication, QStackedWidget
from menu_window import MenuWindow
from game_window import GameWindow
from stats_window import StatsWindow
from game_objects.coin import Coin

import sys
import pygame

pygame.mixer.init()

app = QApplication(sys.argv)
Coin.load_frames()
stack = QStackedWidget()


def start_game(config):
    pygame.mixer.music.stop()
    game_window = GameWindow(config=config)
    game_window.set_show_stats_callback(show_stats)
    stack.addWidget(game_window)
    stack.setCurrentWidget(game_window)


def show_menu():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/menu_music.wav")
    pygame.mixer.music.set_volume(menu.volume_slider.value() / 100)
    pygame.mixer.music.play(-1)
    stack.setCurrentWidget(menu)


def show_stats():
    stats_window = StatsWindow()
    stats_window.set_back_callback(show_menu)
    stack.addWidget(stats_window)
    stack.setCurrentWidget(stats_window)


menu = MenuWindow(start_callback=start_game, stats_callback=show_stats, exit_callback=app.quit)
stack.addWidget(menu)

stack.setFixedSize(600, 800)
stack.show()

# Воспроизводим музыку меню при запуске
pygame.mixer.music.load("assets/menu_music.wav")
pygame.mixer.music.set_volume(menu.volume_slider.value() / 100)
pygame.mixer.music.play(-1)

sys.exit(app.exec_())