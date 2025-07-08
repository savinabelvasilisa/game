from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRect

import random

class Pipe:
    def __init__(self, x, speed, gap_height):
        self.x = x
        self.width = 60
        self.speed = speed
        self.gap_height = gap_height

        self.top_height = random.randint(50, 400)

        self.top_rect = QRect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = QRect(
            self.x, self.top_height + self.gap_height, self.width, 1000
        )

    def update(self):
        self.x -= self.speed
        self.top_rect.moveTo(self.x, 0)
        self.bottom_rect.moveTo(self.x, self.top_height + self.gap_height)

    def draw(self, painter: QPainter):
        painter.setBrush(QBrush(QColor("green")))
        painter.drawRect(self.top_rect)
        painter.drawRect(self.bottom_rect)

    def is_off_screen(self):
        return self.x + self.width < 0

    def collides_with(self, bird_rect):
        return self.top_rect.intersects(bird_rect) or self.bottom_rect.intersects(bird_rect)

    def passed_by(self, bird_x):
        return self.x + self.width < bird_x
