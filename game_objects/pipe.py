from PyQt5.QtGui import QPainter, QPixmap, QTransform
from PyQt5.QtCore import QRect
import random
import os

class Pipe:
    image = None  # Картинка трубы
    flipped_image = None  # Перевёрнутая труба

    def __init__(self, x, speed, gap_height):
        self.x = x
        self.width = 80  # Новая ширина под твою картинку
        self.speed = speed
        self.gap_height = gap_height
        self.top_height = random.randint(50, 400)

        # Загружаем изображение один раз
        if Pipe.image is None:
            path = os.path.join("assets", "pipe.png")
            Pipe.image = QPixmap(path)
            Pipe.flipped_image = Pipe.image.transformed(QTransform().scale(1, -1))

        # Прямоугольники для отрисовки
        self.top_rect = QRect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = QRect(self.x, self.top_height + self.gap_height, self.width, 1000)

    def update(self):
        self.x -= self.speed
        self.top_rect.moveTo(self.x, 0)
        self.bottom_rect.moveTo(self.x, self.top_height + self.gap_height)

    def draw(self, painter: QPainter):
        # Верхняя труба (перевёрнутая)
        top_src_rect = QRect(0, Pipe.image.height() - self.top_height, self.width, self.top_height)
        painter.drawPixmap(self.top_rect, Pipe.flipped_image, top_src_rect)

        # Нижняя труба (обычная)
        bottom_src_rect = QRect(0, 0, self.width, self.bottom_rect.height())
        painter.drawPixmap(self.bottom_rect, Pipe.image, bottom_src_rect)

    def is_off_screen(self):
        return self.x + self.width < 0

    def collides_with(self, bird_rect):
        return self.top_rect.intersects(bird_rect) or self.bottom_rect.intersects(bird_rect)

    def passed_by(self, bird_x):
        return self.x + self.width < bird_x
