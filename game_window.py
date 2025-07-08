from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QTimer

from game_objects.bird import Bird
from game_objects.pipe import Pipe
from game_objects.coin import Coin

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

import json
import os

class GameWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.config = config
        self.bird = Bird(x=150, y=300)

        self.pipes = []
        self.pipe_timer = 0
        self.pipe_speed = config["pipe_speed"]
        self.gap_height = config["gap_height"]

        self.coins = []
        self.coin_timer = 0
        self.coins_collected = 0

        self.score = 0
        self.game_over = False
        self.show_stats = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)



    def set_show_stats_callback(self, callback):
        self.show_stats = callback

    def game_loop(self):
        if self.game_over:
            return

        self.bird.update()

        for pipe in self.pipes:
            pipe.update()

        self.pipes = [p for p in self.pipes if not p.is_off_screen()]

        self.pipe_timer += 1
        if self.pipe_timer >= 90:
            self.pipes.append(Pipe(x=self.width(), speed=self.pipe_speed, gap_height=self.gap_height))
            self.pipe_timer = 0
            self.coin_timer += 1
            if self.coin_timer >= 2:
                last_pipe = self.pipes[-1]
                coin_y = last_pipe.top_height + last_pipe.gap_height / 2
                self.coins.append(Coin(x=self.width() + 30, y=coin_y))
                self.coin_timer = 0

        # Столкновения
        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            if pipe.collides_with(bird_rect):
                self.end_game()
                return
            elif not hasattr(pipe, "scored") and pipe.passed_by(self.bird.x):
                self.score += 1
                pipe.scored = True

        for coin in self.coins:
            coin.update()
            if not coin.collected and coin.collides_with(bird_rect):
                coin.collected = True
                self.coins_collected += 1

        self.coins = [c for c in self.coins if not c.is_off_screen()]

        if self.bird.y > self.height():
            self.end_game()
            return

        self.update()

    def end_game(self):
        if self.game_over:
            return
        self.game_over = True
        self.timer.stop()
        self.save_result()

        self.game_over_image = QPixmap("assets/game_over.png")
        print("Картинка загружена?", not self.game_over_image.isNull())
        self.update()
        QTimer.singleShot(2000, self.show_stats)

    def restart_game(self):
        self.bird = Bird(x=150, y=300)
        self.pipes = []
        self.pipe_timer = 0
        self.coins = []
        self.coin_timer = 0
        self.score = 0
        self.coins_collected = 0
        self.game_over = False
        self.setFocus()
        self.timer.start(16)

    def save_result(self):
        result = {
            "score": self.score,
            "coins": self.coins_collected,
            "difficulty": self.config
        }
        if not os.path.exists("results.json"):
            with open("results.json", "w") as f:
                json.dump([], f)

        with open("results.json", "r") as f:
            data = json.load(f)

        data.append(result)

        with open("results.json", "w") as f:
            json.dump(data, f, indent=2)

        if self.show_stats:
            self.show_stats()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Фон
        painter.fillRect(self.rect(), QColor("#ccf2ff"))

        # Птица
        self.bird.draw(painter)

        # Трубы
        for pipe in self.pipes:
            pipe.draw(painter)

        # Монеты
        for coin in self.coins:
            coin.draw(painter)

        # Очки
        painter.setFont(QFont("Arial", 18))
        painter.setPen(Qt.black)
        painter.drawText(10, 30, f"Очки: {self.score}")
        painter.drawText(10, 55, f"Монеты: {self.coins_collected}")

        # Game Over
        if self.game_over and hasattr(self, "game_over_image"):
            print("Рисуем Game Over изображение")
            painter.drawPixmap(self.rect(), self.game_over_image)
        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and not self.game_over:
            self.bird.jump()
        elif event.key() == Qt.Key_Return and self.game_over:
            self.restart_game()


class GameWindow(GameWidget):
    def __init__(self, config):
        super().__init__(config)
