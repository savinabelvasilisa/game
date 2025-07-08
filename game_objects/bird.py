from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import QRect

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.jump_strength

    def draw(self, painter: QPainter):
        painter.setBrush(QBrush(QColor("yellow")))
        painter.drawEllipse(int(self.x - self.radius), int(self.y - self.radius), int(self.radius * 2), int(self.radius * 2))

    def get_rect(self):
        return QRect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

