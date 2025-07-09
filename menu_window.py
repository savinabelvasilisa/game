# menu_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QSlider, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize



class MenuWindow(QWidget):
    def __init__(self, start_callback, stats_callback, exit_callback):
        super().__init__()
        self.start_callback = start_callback
        self.stats_callback = stats_callback
        self.exit_callback = exit_callback

        self.selected_character = "chick_1.png"

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.bg = QPixmap("assets/menu_bg.png")
        self.setAutoFillBackground(False)

        char_label = QLabel("Выбери персонажа:")
        char_label.setFont(QFont("Arial", 14))
        char_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(char_label)

        self.char_combo = QComboBox()
        self.char_combo.setIconSize(QSize(48, 48))
        self.char_options = [
            "chick_1.png", "chick_2.png", "chick_3.png", "chick_4.png", "chick_5.png"
        ]

        for name in self.char_options:
            icon = QIcon(f"assets/characters/{name}")
            self.char_combo.addItem(icon, name)

        self.char_combo.currentIndexChanged.connect(self.update_selected_character)
        layout.addWidget(self.char_combo)

        title = QLabel("Fluppy Vasya 🐥")
        title.setFont(QFont("Arial", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Выбор сложности
        self.difficulty_box = QComboBox()
        self.difficulty_box.addItems(["Легко", "Средне", "Сложно"])
        layout.addWidget(QLabel("Сложность:"))
        layout.addWidget(self.difficulty_box)

        # Выбор карты
        self.map_box = QComboBox()
        self.map_box.addItems(["Лес", "Небо", "Город"])
        layout.addWidget(QLabel("Карта:"))
        layout.addWidget(self.map_box)

        # Настройка звука
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)

        self.volume_slider.valueChanged.connect(self.update_volume)


        layout.addWidget(QLabel("Громкость:"))
        layout.addWidget(self.volume_slider)

        # Кнопки
        play_btn = QPushButton("Играть")
        stats_btn = QPushButton("Статистика")
        exit_btn = QPushButton("Выход")

        for btn in [play_btn, stats_btn, exit_btn]:
            btn.setFixedHeight(40)
            btn.setFont(QFont("Arial", 14))
            layout.addWidget(btn)

        play_btn.clicked.connect(self.on_start)
        stats_btn.clicked.connect(self.stats_callback)
        exit_btn.clicked.connect(self.exit_callback)

        self.setLayout(layout)

    def update_selected_character(self):
        self.selected_character = self.char_options[self.char_combo.currentIndex()]    

    def update_volume(self, value):
        import pygame
        pygame.mixer.music.set_volume(value / 100)

    def on_start(self):
        difficulty = self.difficulty_box.currentText()
        map_choice = self.map_box.currentText()
        volume = self.volume_slider.value()

        config = {
            "Легко": {"pipe_speed": 3,"gap_height": 200,"pipe_interval": 100},
            "Средне": {"pipe_speed": 4, "gap_height": 160, "pipe_interval": 80},
            "Сложно": {"pipe_speed": 5, "gap_height": 120, "pipe_interval": 60}
        }[difficulty]

        # Назначение фона по карте
        map_bg = {
            "Лес": "assets/bg_forest.png",
            "Небо": "assets/bg_sky.png",
            "Город": "assets/bg_city.png"
        }.get(map_choice, "")

        config["bg"] = map_bg
        config["volume"] = volume
        config["character"] = self.selected_character

        self.start_callback(config)
