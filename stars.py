import pygame
from pygame.sprite import Sprite
from random import randint


class Stars(Sprite):
    """Класс представляющий звезды на фоне"""

    def __init__(self, game):
        """Инициализирует звезду и задает начальную позицию"""
        super().__init__()
        self.icon_ship = "images/star.bmp"
        self.screen = game.screen

        # Загрузка изображения звезды
        self.image = pygame.image.load(self.icon_ship)
        self.rect = self.image.get_rect()

        # Поворот изображения на рандомный угол
        self.image, self.rect = self._random_rotate(self.image, self.rect, randint(-90, 90))

        # Каждая новая звезда появляется у нижнего края экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение горизонтальной позиции звезды в float
        self.x = float(self.rect.x)

    @staticmethod
    def _random_rotate(image, rect, angle):
        """Случайный угол поворота звезды"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect
