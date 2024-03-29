import sys
import pygame

from random import randint
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from stars import Stars
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_size)  # pygame.FULLSCREEN
        # self.settings.screen_size = (self.screen.get_rect().width,
        #                              self.screen.get_rect().height)
        pygame.display.set_caption("Alien Invision")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self._create_stars_sky()
        x_play_button, y_play_button = self.screen.get_rect().center
        y_play_button -= Button.height_y_spaces
        self.play_button = Button(self, "Play", x_play_button, y_play_button)
        x_settings_button, y_settings_button = self.play_button.rect.center
        y_settings_button += Button.height_y_spaces
        self.settings_button = Button(self, "Settings", x_settings_button, y_settings_button)

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Отслеживание клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_events_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_events_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запуск новой игры при нажатии Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """Запуск игры при нажатии клавиши P или кнопки Play"""
        pygame.mouse.set_visible(False)
        self.stats.game_active = True
        self._restart()

    def _restart(self):
        """Перезапуск игры"""
        self.stats.reset_stats()
        self._restart_window()

    def _restart_window(self):
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ship()
        self.settings.initialize_dynamic_settings()
        self.aliens.empty()
        self.bullets.empty()
        self.stars.empty()
        self._create_stars_sky()
        self._create_fleet()
        self.ship.center_ship()

    def _check_events_keydown(self, event):
        """Реагирует на нажатие клавишь"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_r:
            self._restart()
        elif event.key == pygame.K_ESCAPE:
            self.stats.pause()

    def _check_events_keyup(self, event):
        """Реагирует на отпускание клавишь"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу self.bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Проверка попадания в корабль пришельца. При попадании удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:
            """Уничтожение снарядов и создание нового флота"""
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.reward_point_for_hit * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()



    def _create_alien(self, alien_num, row_num):
        """Создание корабля пришельцев и его размещение"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_num
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
        self.aliens.add(alien)

    def _create_fleet(self):
        """Создание флота вторжения"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_size[0] - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Определение кол-ва рядов на экране
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_size[1] - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_num in range(number_rows):
            for alien_num in range(number_aliens_x):
                self._create_alien(alien_num, row_num)

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец-корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверка соприкосновения кораблей пришельцев с нижним краем экрана
        self._check_aliens_buttom()

    def _check_fleet_edges(self):
        """Реакция на достижение кораблем пришельцев края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обработка столкновений корабля с пришельцами"""
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self._restart_window()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_buttom(self):
        """Проверяет соприкосновение кораблей пришельцев с нижней частью экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Те же действия, что при столкновении с кораблем игрока
                self._ship_hit()
                break

    def _create_star(self, star_num, row_num):
        """Создание звезды и ее размещение"""
        star = Stars(self)
        star_width, star_height = star.rect.size
        random_num = randint(-70, 70)
        star.x = (star_width + 4 * star_width * star_num) + random_num
        star.rect.x = star.x
        star.rect.y = (star.rect.height + 4 * star.rect.height * row_num) + random_num
        self.stars.add(star)

    def _create_stars_sky(self):
        """Создание звездного неба"""
        star = Stars(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_size[0] - (4 * star_width)
        number_stars_x = available_space_x // (4 * star_width)
        # Определение кол-ва рядов на экране
        number_rows = self.settings.screen_size[1] // (3 * star_height)
        for row_num in range(number_rows):
            for star_num in range(number_stars_x):
                self._create_star(star_num, row_num)

    def _update_screen(self):
        """Обновляет изображение и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.sb.show_score()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Отображение кнопки Play в случае если игра не активна
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.settings_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
