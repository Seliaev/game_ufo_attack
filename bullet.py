import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления снарядами"""

    def __init__(self, game):
        """Создание обьектов снарядов в текущей позиции корабля"""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # Создание снаряда в позиции 0, 0 и назначение верной позиции
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = game.ship.rect.midtop

        # Позиция снаряда хранится в float
        self.y = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану"""
        # Обновление позиции снаряда вверх по экрану
        self.y -= self.settings.bullet_speed
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        """Вывод снаряда на экран"""
        pygame.draw.rect(self.screen, self.color, self.rect)
