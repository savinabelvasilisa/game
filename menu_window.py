# menu_window.py
import json
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QComboBox, QSlider, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter
from PyQt5.QtCore import Qt, QSize


class MenuWindow(QWidget):
    def __init__(self, start_callback, stats_callback, exit_callback):
        super().__init__()
        self.start_callback = start_callback
        self.stats_callback = stats_callback
        self.exit_callback = exit_callback

        self.progress_path = "data/progress.json"
        self.total_coins = 0
        self.unlocked = ["chick_1.png"]
        self.load_progress()
        self.selected_character = "chick_1.png"
        self.bg = QPixmap("assets/menu_bg.png")

     

        self.char_combo = QComboBox()
        self.char_combo.setIconSize(QSize(48, 48))
        self.char_options = [
            ("chick_1.png", 0),
            ("chick_2.png", 10),
            ("chick_3.png", 15),
            ("chick_4.png", 20),
            ("chick_5.png", 25)
        ]

        for name, cost in self.char_options:
            icon = QIcon(f"assets/characters/{name}")
            label = "" if name in self.unlocked else f" 🔒 {cost} монет"
            self.char_combo.addItem(icon, label, userData=name)

        self.char_combo.currentIndexChanged.connect(self.update_selected_character)


                # === Главные кнопки ===
        self.play_btn = self.create_image_button("assets/buttons/play.png", 220, 430, self.on_start, 160, 72)
        self.stats_btn = self.create_image_button("assets/buttons/stats.png", 40, 430, self.stats_callback, 160, 72)
        self.exit_btn = self.create_image_button("assets/buttons/exit.png", 400, 430, self.exit_callback, 160, 72)
        
                # === Выбор сложности ===
        self.difficulties = ["easy", "medium", "hard"]
        self.difficulty_index = 0

        self.left_diff_btn = self.create_image_button("assets/buttons/arrow_left.png", 160, 696, lambda: self.change_difficulty(-1), 40, 45)
        self.right_diff_btn = self.create_image_button("assets/buttons/arrow_right.png", 400, 696, lambda: self.change_difficulty(1), 40, 45)

        self.difficulty_label = QLabel(self)
        self.difficulty_label.setPixmap(QPixmap(f"assets/buttons/difficulty_{self.difficulties[self.difficulty_index]}.png"))
        self.difficulty_label.setFixedSize(194, 45)  # подгоняешь под размер png
        self.difficulty_label.move(203, 696)
        self.difficulty_label.setScaledContents(True)

        # === Выбор карты ===
        self.maps = ["forest", "sky", "city"]
        self.map_index = 0

        self.left_map_btn = self.create_image_button("assets/buttons/arrow_left.png", 160, 635, lambda: self.change_map(-1), 40, 45)
        self.right_map_btn = self.create_image_button("assets/buttons/arrow_right.png", 400, 635, lambda: self.change_map(1), 40, 45)

        self.map_label = QLabel(self)
        self.map_label.setPixmap(QPixmap(f"assets/buttons/map_{self.maps[self.map_index]}.png"))
        self.map_label.setFixedSize(194, 45)
        self.map_label.move(203, 635)
        self.map_label.setScaledContents(True)



        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.update_volume)
        

        
        # Монеты
        # ===== Монеты =====
        self.coin_icon = QLabel(self)
        self.coin_icon.setPixmap(QPixmap("assets/coin.png"))
        self.coin_icon.setFixedSize(35, 35)
        self.coin_icon.setScaledContents(True)
        self.coin_icon.move(20, 20)
        
        self.coins_label = QLabel(str(self.total_coins), self)
        self.coins_label.setFont(QFont("Arial", 15))
        self.coins_label.setStyleSheet("color: white;")
        self.coins_label.setFixedHeight(45)
        self.coins_label.move(60, 15)
         
        
        # Персонажи
        
        self.char_combo.setParent(self)
        self.char_combo.move(420, 20)
        
        # Громкость
        self.volume_icon = QLabel(self)
        self.volume_icon.setPixmap(QPixmap("assets/volume.png"))
        self.volume_icon.setFixedSize(32, 32)  # или другой размер, например 45x45
        self.volume_icon.setScaledContents(True)
        self.volume_icon.move(190, 25)  # подгони под своё расположение
        
        
        self.volume_slider.setParent(self)
        self.volume_slider.setFixedWidth(200)
        self.volume_slider.move(200, 30)
        self.volume_slider.setStyleSheet("""
        QSlider::groove:horizontal {
            border: none;
            height: 14px;
            background: transparent;
            image: url(assets/slider_bg.png);
        }
        QSlider::handle:horizontal {
            image: url(assets/slider_knob.png);
            width: 30px;
            height: 40px;
            margin: -26px 0;                             
        }
        """)        


        


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.bg)

    def create_image_button(self, path, x, y, callback, w=None, h=None):
        pixmap = QPixmap(path)
        # если размеры не заданы вручную — берем из картинки
        if w is None or h is None:
            w = pixmap.width()
            h = pixmap.height()
        btn = QPushButton(self)
        btn.setIcon(QIcon(path))
        btn.setIconSize(QSize(w, h))
        btn.setFixedSize(w, h)
        btn.setFlat(True)
        btn.setStyleSheet("background-color: transparent; border: none;")
        btn.move(x, y)
        btn.clicked.connect(callback)
        return btn

    def change_difficulty(self, direction):
        self.difficulty_index = (self.difficulty_index + direction) % len(self.difficulties)
        new_img = QPixmap(f"assets/buttons/difficulty_{self.difficulties[self.difficulty_index]}.png")
        self.difficulty_label.setPixmap(new_img)

    def change_map(self, direction):
        self.map_index = (self.map_index + direction) % len(self.maps)
        new_img = QPixmap(f"assets/buttons/map_{self.maps[self.map_index]}.png")
        self.map_label.setPixmap(new_img)

    def load_progress(self):
        if os.path.exists(self.progress_path):
            with open(self.progress_path, "r") as f:
                data = json.load(f)
                self.total_coins = data.get("coins", 0)
                self.unlocked = data.get("unlocked", ["chick_1.png"])

    def save_progress(self):
        with open(self.progress_path, "w") as f:
            json.dump({
                "coins": self.total_coins,
                "unlocked": self.unlocked
            }, f, indent=2)

    def update_selected_character(self):
        index = self.char_combo.currentIndex()
        name, cost = self.char_options[index]

        if name not in self.unlocked:
            if self.total_coins >= cost:
                reply = QMessageBox.question(self, "Разблокировка", f"Разблокировать {name} за {cost} монет?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.total_coins -= cost
                    self.unlocked.append(name)
                    self.save_progress()
                    self.refresh_ui()
            else:
                QMessageBox.warning(self, "Недостаточно монет", "У вас недостаточно монет для разблокировки")
                self.char_combo.setCurrentIndex(0)
                return

        self.selected_character = name

    def refresh_ui(self):
        self.coins_label.setText(str(self.total_coins))
        self.char_combo.blockSignals(True)
        self.char_combo.clear()
        for name, cost in self.char_options:
            icon = QIcon(f"assets/characters/{name}")
            label = name if name in self.unlocked else f"{name} (🔒 {cost} монет)"
            self.char_combo.addItem(icon, label, userData=name)
        self.char_combo.blockSignals(False)

    def update_volume(self, value):
        import pygame
        pygame.mixer.music.set_volume(value / 100)

    def on_start(self):
        difficulty = self.difficulties[self.difficulty_index]
        map_choice = self.maps[self.map_index]
        volume = self.volume_slider.value()

        config = {
            "easy": {"pipe_speed": 3,"gap_height": 200,"pipe_interval": 100},
            "medium": {"pipe_speed": 4, "gap_height": 160, "pipe_interval": 80},
            "hard": {"pipe_speed": 5, "gap_height": 120, "pipe_interval": 60}
        }[difficulty]

        map_bg = {
            "forest": "assets/map/bg_forest.png",
            "sky": "assets/map/bg_sky.png",
            "city": "assets/map/bg_city.png"
        }.get(map_choice, "")

        config["bg"] = map_bg
        config["volume"] = volume
        config["character"] = self.selected_character

        self.start_callback(config)
        self.refresh_ui()
