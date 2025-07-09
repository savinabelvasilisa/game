from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import QRect
import os

class Bird:
    def __init__(self, x, y, image_path=None):
        self.x = x
        self.y = y
        self.radius = 32  # половина размера 64x64
        self.velocity = 0
        self.gravity = 0.6
        self.lift = -10

        # Загрузка картинки птицы
        self.image = QPixmap("assets/bird.png")
        
        if image_path:
            self.image = QPixmap(image_path)
        else:
            self.image = None

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.lift

  
    def draw(self, painter):
        if self.image:
            size = 70
            painter.drawPixmap(QRect(int(self.x - size//2), int(self.y - size//2), int(size), int(size)), self.image)
        
    
    def get_rect(self):
        if self.image:
            size = self.image.width()
            padding = size * 0.4  # уменьшим рамку на 50%
            return QRect(int(self.x - size // 2 + padding // 2), int(self.y - size // 2 + padding // 2), int(size - padding), int(size - padding))

        else:
            return QRect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
    