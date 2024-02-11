import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Класс корабля игрока"""

    def __init__(self, game):
        """Иницилизация корабля и установка в начальную позицию"""
        super().__init__()
        self.icon_ship = "images/ship.bmp"
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        # Загрузка изображения корабля
        self.image = pygame.image.load(self.icon_ship)
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет позицию коробля с учетом флага moving_right"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed_factor
        self.rect.x = self.x

    def blitme(self):
        """Отображение корабля в текущей позиции"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центр внизу"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
