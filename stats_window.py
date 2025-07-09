# stats_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StatsWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Статистика игр")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.filter_box = QComboBox()
        self.filter_box.addItems(["Все", "Легко", "Средне", "Сложно"])
        self.filter_box.currentTextChanged.connect(self.load_stats)

        self.list_widget = QListWidget()
        self.figure = plt.figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(250)

        self.back_button = QPushButton("Назад в меню")
        self.back_button.setFixedHeight(40)

        layout.addWidget(title)
        layout.addWidget(QLabel("Фильтр по сложности:"))
        layout.addWidget(self.filter_box)
        layout.addWidget(self.list_widget)
        layout.addWidget(QLabel("График очков:"))
        layout.addWidget(self.canvas)
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.load_stats()

    def load_stats(self):
        self.list_widget.clear()
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        filter_text = self.filter_box.currentText()
        scores = []

        if os.path.exists("results.json"):
            with open("results.json", "r") as f:
                data = json.load(f)
                filtered = []
                for result in data:
                    diff_str = self.format_difficulty(result.get("difficulty", {}))
                    if filter_text == "Все" or filter_text == diff_str:
                        filtered.append(result)

                for i, result in enumerate(filtered[-10:]):
                    score = result.get("score", 0)
                    coins = result.get("coins", 0)
                    diff = self.format_difficulty(result.get("difficulty", {}))
                    item = f"Очки: {score} | Монеты: {coins} | Сложность: {diff}"
                    self.list_widget.addItem(item)
                    scores.append(score)

        if scores:
            ax.plot(range(1, len(scores)+1), scores, marker='o')
            ax.set_title("Очки за последние игры")
            ax.set_xlabel("Игра")
            ax.set_ylabel("Очки")
            self.figure.tight_layout()
        else:
            ax.text(0.5, 0.5, "Нет данных", ha='center', va='center')

        self.canvas.draw()

    def format_difficulty(self, config):
        if config.get("gap_height", 0) >= 200:
            return "Легко"
        elif config.get("gap_height", 0) >= 160:
            return "Средне"
        else:
            return "Сложно"

    def set_back_callback(self, callback):
        self.back_button.clicked.connect(callback)
