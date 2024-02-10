class Settings:
    """Класс хранения настроек игры"""

    def __init__(self):
        """Инициализация настроек игры"""
        # Настройки игры
        self.screen_size = 1200, 800
        self.bg_color = 230, 230, 230
        # Параметры корабля игрока
        self.ship_speed_factor = 1.5
        # Параметры снаряда
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

