from PyQt5.QtWidgets import QMainWindow, QPushButton

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игровое окно")
        self.setGeometry(100, 100, 500, 400)

        # Кнопка "Назад в меню"
        self.back_button = QPushButton("Назад", self)
        self.back_button.setGeometry(200, 300, 100, 40)
        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        self.close()  # Закрываем игровое окно
