import pygame


class GameStats:
    """Отслеживание статистики для игры"""
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def pause(self):
        """Установка игры на паузу"""
        if self.game_active:
            pygame.mouse.set_visible(True)
            self.game_active = False
        else:
            pygame.mouse.set_visible(False)
            self.game_active = True
