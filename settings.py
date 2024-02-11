class Settings:
    """Класс хранения настроек игры"""

    def __init__(self):
        """Инициализация настроек игры"""
        # Настройки игры
        self.screen_size = 1200, 800
        self.bg_color = 230, 230, 230
        # Параметры корабля игрока
        self.ship_limit = 3
        # Параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        # Параметры кораблей пришельцев
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.2
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализация настроек, меняющиеся по ходу игры"""
        # Параметры корабля игрока
        self.ship_speed_factor = 1.5
        # Параметры снаряда
        self.bullet_speed_factor = 1.5
        # Параметры кораблей пришельцев
        self.alien_speed_factor = 0.4
        self.fleet_direction = 1  # 1 - движение вправо; -1 - движение влево
        self.reward_point_for_hit = 10

    def increase_speed(self):
        """Увеличение настроек скорости и получения очков"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.reward_point_for_hit = int(self.reward_point_for_hit * self.score_scale)



