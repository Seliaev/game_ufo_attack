class Settings:
    """Класс хранения настроек игры"""

    def __init__(self):
        """Инициализация настроек игры"""
        self.screen_size = 1200, 800
        self.bg_color = 230, 230, 230

        self.ship_speed_factor = 1.5
