from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
import os

class StatsWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Статистика игр")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.list_widget = QListWidget()
        self.load_stats()

        self.back_button = QPushButton("Назад в меню")
        self.back_button.setFixedHeight(40)

        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def load_stats(self):
        self.list_widget.clear()
        if os.path.exists("results.json"):
            with open("results.json", "r") as f:
                data = json.load(f)
                for result in data[-10:][::-1]:  # последние 10 игр
                    score = result.get("score", 0)
                    coins = result.get("coins", 0)
                    diff = result.get("difficulty", {})
                    diff_str = self.format_difficulty(diff)
                    item = f"Очки: {score} | Монеты: {coins} | Сложность: {diff_str}"
                    self.list_widget.addItem(item)
        else:
            self.list_widget.addItem("Нет сохранённых данных.")

    def format_difficulty(self, config):
        if config["gap_height"] >= 200:
            return "Легко"
        elif config["gap_height"] >= 160:
            return "Средне"
        else:
            return "Сложно"

    def set_back_callback(self, callback):
        self.back_button.clicked.connect(callback)
