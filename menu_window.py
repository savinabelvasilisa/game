from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MenuWindow(QWidget):
    def __init__(self, start_callback, stats_callback, exit_callback):
        super().__init__()
        self.start_callback = start_callback
        self.stats_callback = stats_callback
        self.exit_callback = exit_callback

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Fluppy Vasya 🐥")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        easy_btn = QPushButton("Легко")
        medium_btn = QPushButton("Средне")
        hard_btn = QPushButton("Сложно")
        stats_btn = QPushButton("Статистика")
        exit_btn = QPushButton("Выход")

        for btn in [easy_btn, medium_btn, hard_btn, stats_btn, exit_btn]:
            btn.setFixedHeight(40)
            btn.setFont(QFont("Arial", 14))
            layout.addWidget(btn)

        easy_btn.clicked.connect(lambda: start_callback("easy"))
        medium_btn.clicked.connect(lambda: start_callback("medium"))
        hard_btn.clicked.connect(lambda: start_callback("hard"))
        stats_btn.clicked.connect(stats_callback)
        exit_btn.clicked.connect(exit_callback)

        self.setLayout(layout)
