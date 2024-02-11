class GameStats:
    """Отслеживание статистики для игры"""
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def pause(self):
        """Установка игры на паузу"""
        if self.game_active:
            self.game_active = False
        else:
            self.game_active = True
