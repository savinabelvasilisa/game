from PyQt5.QtWidgets import QApplication, QStackedWidget
from menu_window import MenuWindow
from game_window import GameWindow
from stats_window import StatsWindow
import sys

# Настройки уровней сложности
difficulties = {
    "easy": {
        "pipe_speed": 2,
        "gap_height": 200
    },
    "medium": {
        "pipe_speed": 3,
        "gap_height": 160
    },
    "hard": {
        "pipe_speed": 4,
        "gap_height": 130
    }
}

app = QApplication(sys.argv)

stack = QStackedWidget()

def start_game(difficulty):
    config = difficulties[difficulty]
    game_window = GameWindow(config=config)
    game_window.set_show_stats_callback(show_stats)
    stack.addWidget(game_window)
    stack.setCurrentWidget(game_window)

def show_menu():
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

sys.exit(app.exec_())
