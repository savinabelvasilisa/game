from PyQt5.QtWidgets import QMainWindow, QPushButton
from game_window import GameWindow

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Меню")
        self.setGeometry(100, 100, 400, 300)

        # Кнопка "Начать игру"
        self.start_button = QPushButton("Начать игру", self)
        self.start_button.setGeometry(130, 100, 140, 40)
        self.start_button.clicked.connect(self.start_game)

        # Кнопка "Выход"
        self.quit_button = QPushButton("Выход", self)
        self.quit_button.setGeometry(130, 160, 140, 40)
        self.quit_button.clicked.connect(self.close)

    def start_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.hide()  # Скрываем меню
