from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRect

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 25
        self.speed = 2
        self.collected = False

    def update(self):
        self.x -= self.speed

    def draw(self, painter: QPainter):
        if not self.collected:
            painter.setBrush(QBrush(QColor("gold")))
            painter.drawEllipse(int(self.x - self.size // 2), int(self.y - self.size // 2), int(self.size), int(self.size))

    def get_rect(self):
        return QRect(int(self.x - self.size // 2), int(self.y - self.size // 2), self.size, self.size)

    def collides_with(self, bird_rect):
        return self.get_rect().intersects(bird_rect)

    def is_off_screen(self):
        return self.x + self.size < 0
