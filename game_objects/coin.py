# coin.py
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QRect, QTimer
import pygame
import os

# coin.py
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QRect
import pygame
import os

class Coin:
    frames = []

    @classmethod
    def load_frames(cls):
        if not cls.frames:
            for i in range(6):
                path = os.path.join("assets", "coin_frames", f"coin_{i}.png")
                pixmap = QPixmap(path)
                cls.frames.append(pixmap)

    def __init__(self, pipe, offset_x, y):
        Coin.load_frames()
        self.pipe = pipe          # Привязка к трубе
        self.offset_x = offset_x  # Смещение от трубы
        self.y = y
        self.radius = 32
        self.collected = False
        self.frame_index = 0
        self.frame_delay = 5
        self.frame_counter = 0
        self.sound = pygame.mixer.Sound("assets/music/coin.wav")

    def update(self, volume):
        if self.collected:
            return
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(Coin.frames)
        self.sound.set_volume(volume)

    def draw(self, painter: QPainter):
        if not self.collected and Coin.frames:
            x = self.pipe.x + self.offset_x
            frame = Coin.frames[self.frame_index]
            w, h = frame.width(), frame.height()
            painter.drawPixmap(QRect(int(x - w / 2), int(self.y - h / 2), w, h), frame)

    def collides_with(self, bird_rect):
        if self.collected:
            return False
        x = self.pipe.x + self.offset_x
        coin_rect = QRect(int(x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
        if coin_rect.intersects(bird_rect):
            self.collected = True
            self.sound.play()
            return True
        return False    

    def is_off_screen(self):
        return self.pipe.x + self.offset_x + self.radius < 0
