# game_window.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRect
from datetime import datetime

from game_objects.bird import Bird
from game_objects.pipe import Pipe
from game_objects.coin import Coin


import json
import os
import pygame

class GameWidget(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.config = config
        self.volume = config.get("volume", 50) / 100

        self.bird = Bird(x=150, y=300, image_path=f"assets/characters/{config.get('character', 'chick_1.png')}")
        self.pipes = []
        self.pipe_timer = 0
        self.pipes_spawned = 0

        self.pipe_speed = config["pipe_speed"]
        self.gap_height = config["gap_height"]
        self.pipe_interval = config.get("pipe_interval", 60)

        self.coins = []
        self.coin_timer = 0
        self.coins_collected = 0

        self.score = 0
        self.high_score = self.load_high_score()
        self.new_record = False
        self.new_record_timer = None
        self.new_record_shown = False

        if self.gap_height >= 200:
            self.goal_score = 10
        elif self.gap_height >= 160:
            self.goal_score = 60
        else:
            self.goal_score = 100

        self.game_over = False
        self.level_completed = False
        self.show_stats = None
        self.show_menu = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

 

        self.game_over_image = QPixmap("assets/game_over.png")
        self.win_image = QPixmap("assets/win.png")
        self.bg_image = QPixmap(config.get("bg", ""))

        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/music/game_music.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

        self.show_go_text = True
        QTimer.singleShot(1000, self.hide_go_text)

        self.coin_icon = QPixmap("assets/coin.png")
        self.score_icon = QPixmap("assets/score.png") 
        self.go_image = QPixmap("assets/go_text.png")
        self.new_record_image = QPixmap("assets/new_record.png")


    def hide_go_text(self):
        self.show_go_text = False
        self.update()

    def hide_new_record(self):
        self.new_record = False
        self.update()
    
    def set_show_stats_callback(self, callback):
        self.show_stats = callback

    def set_show_menu_callback(self, callback):
        self.show_menu = callback

    def game_loop(self):
        if self.game_over or self.level_completed:
            return

        self.bird.update()

        for pipe in self.pipes:
            pipe.update()

        self.pipes = [p for p in self.pipes if not p.is_off_screen()]

        self.pipe_timer += 1
        if self.pipe_timer >= self.pipe_interval and self.pipes_spawned < self.goal_score:
            new_pipe = Pipe(x=self.width(), speed=self.pipe_speed, gap_height=self.gap_height)
            self.pipes.append(new_pipe)
            self.pipe_timer = 0
            self.pipes_spawned += 1

            self.coin_timer += 1
            if self.coin_timer >= 2:
                coin_y = new_pipe.top_height + new_pipe.gap_height / 2
                self.coins.append(Coin(pipe=new_pipe, offset_x=40, y=coin_y))
                self.coin_timer = 0

        rectf = self.bird.get_rect()
        bird_rect = QRect(int(rectf.x()), int(rectf.y()), int(rectf.width()), int(rectf.height()))

        for pipe in self.pipes:
            if pipe.collides_with(bird_rect):
                self.end_game()
                return
            elif not hasattr(pipe, "scored") and pipe.passed_by(self.bird.x):
                self.score += 1
                pipe.scored = True
                if self.score > self.high_score:
                    self.high_score = self.score
                    if not self.new_record_shown:
                        self.new_record = True
                        self.new_record_shown = True  # ← показываем один раз
                        if self.new_record_timer:
                            self.new_record_timer.stop()
                        self.new_record_timer = QTimer(self)
                        self.new_record_timer.setSingleShot(True)
                        self.new_record_timer.timeout.connect(self.hide_new_record)
                        self.new_record_timer.start(2000)
  

        for coin in self.coins:
            coin.update(self.volume)
            if not coin.collected and coin.collides_with(bird_rect):
                coin.collected = True
                self.coins_collected += 1

        self.coins = [c for c in self.coins if not c.is_off_screen()]

        if self.bird.y > self.height():
            self.end_game()
            return

        if self.score >= self.goal_score:
            self.complete_level()
            return

        self.update()

    def end_game(self):
        if self.game_over:
            return
        self.game_over = True
        self.timer.stop()
        self.save_result()

        pygame.mixer.music.stop()
        death = pygame.mixer.Sound("assets/music/death.wav")
        death.set_volume(self.volume)
        death.play()

        QTimer.singleShot(2000, self.show_menu_callback)
        self.update()

    def complete_level(self):
        self.level_completed = True
        self.timer.stop()
        self.save_result()

        pygame.mixer.music.stop()
        win = pygame.mixer.Sound("assets/music/win.wav")
        win.set_volume(self.volume)
        win.play()

        QTimer.singleShot(2000, self.show_menu_callback)
        self.update()

    def restart_game(self):
        self.bird = Bird(x=150, y=300)
        self.pipes = []
        self.pipe_timer = 0
        self.coins = []
        self.coin_timer = 0
        self.score = 0
        self.coins_collected = 0
        self.game_over = False
        self.level_completed = False
        self.new_record = False
        self.new_record_shown = False
        self.setFocus()
        self.timer.start(16)

        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/music/game_music.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)

    def save_result(self):
        result = {
            "score": self.score,
            "coins": self.coins_collected,
            "difficulty": self.config,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ← добавим дату и время
        }

        # Обновление results.json (история игр)
        if not os.path.exists("results.json"):
            with open("results.json", "w") as f:
                json.dump([], f)

        with open("results.json", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

        data.append(result)

        with open("results.json", "w") as f:
            json.dump(data, f, indent=2)

        # Обновление progress.json (накопленные монеты)
        progress_path = "data/progress.json"
        if os.path.exists(progress_path):
            with open(progress_path, "r") as f:
                try:
                    progress = json.load(f)
                except json.JSONDecodeError:
                    progress = {"coins": 0, "unlocked": ["chick_1.png"]}
        else:
            progress = {"coins": 0, "unlocked": ["chick_1.png"]}

        progress["coins"] = progress.get("coins", 0) + self.coins_collected

        with open(progress_path, "w") as f:
            json.dump(progress, f, indent=2)

        # Обновление рекорда
        if self.score > self.high_score:
            with open("highscore.txt", "w") as f:
                f.write(str(self.score))


    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                return int(f.read())
        return 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self.bg_image.isNull():
            painter.drawPixmap(self.rect(), self.bg_image)
        else:
            painter.fillRect(self.rect(), QColor("#ccf2ff"))

        self.bird.draw(painter)

        for pipe in self.pipes:
            pipe.draw(painter)

        for coin in self.coins:
            coin.draw(painter)
        
        painter.drawPixmap(10, 10, 32, 32, self.score_icon)
        painter.setFont(QFont("Arial", 16))
        painter.setPen(Qt.black)
        painter.drawText(50, 34, f"{self.score} / {self.goal_score}")
        painter.drawPixmap(10, 45, 32, 32, self.coin_icon)
        painter.drawText(50, 70, f"{self.coins_collected}")

        # Прогресс-бар
        progress = min(self.score / self.goal_score, 1.0)
        full_width = self.width() - 100
        bar_width = full_width * progress

        painter.setBrush(QColor("#cccccc"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(50, self.height() - 40, int(full_width), 20)

        painter.setBrush(QColor("#00cc66"))
        painter.drawRect(50, self.height() - 40, int(bar_width), 20)

        painter.setPen(QColor("black"))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(50, self.height() - 40, int(full_width), 20)
    
        if self.show_go_text:
            iw = self.go_image.width()
            ih = self.go_image.height()
            x = (self.width() - iw) // 2
            y = (self.height() - ih) // 2
            painter.drawPixmap(x, y, self.go_image)

        if self.new_record:
            iw = self.new_record_image.width()
            ih = self.new_record_image.height()
            x = (self.width() - iw) // 2
            y = 60
            painter.drawPixmap(x, y, self.new_record_image)

        if self.game_over and not self.game_over_image.isNull():
            painter.drawPixmap(self.rect(), self.game_over_image)

        if self.level_completed and not self.win_image.isNull():
            painter.drawPixmap(self.rect(), self.win_image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and not self.game_over and not self.level_completed:
            self.bird.jump()
        elif event.key() == Qt.Key_Return and (self.game_over or self.level_completed):
            self.restart_game()

class GameWindow(GameWidget):
    def __init__(self, config):
        super().__init__(config)
