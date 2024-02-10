import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс представляющий один корабль пришельцев"""

    def __init__(self, game):
        """Инициализирует корабль пришельцев и задает начальную позицию"""
        super().__init__()
        self.icon_ship = "images/alien.bmp"
        self.screen = game.screen

        # Загрузка изображения корабля пришельцев
        self.image = pygame.image.load(self.icon_ship)
        self.rect = self.image.get_rect()

        # Каждый новый корабль пришельцев появляется у нижнего края экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение горизонтальной позиции корабля пришельцев в float
        self.x = float(self.rect.x)
