import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс представляющий один корабль пришельцев"""

    def __init__(self, game):
        """Инициализирует корабль пришельцев и задает начальную позицию"""
        super().__init__()
        self.icon_ship = "images/alien.bmp"
        self.screen = game.screen
        self.settings = game.settings

        # Загрузка изображения корабля пришельцев
        self.image = pygame.image.load(self.icon_ship)
        self.rect = self.image.get_rect()

        # Каждый новый корабль пришельцев появляется у нижнего края экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение горизонтальной позиции корабля пришельцев в float
        self.x = float(self.rect.x)

    def update(self):
        """Перемещает пришельца вправо и влево"""
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x


    def check_edge(self):
        """Возвращает True если пришелец у края"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True