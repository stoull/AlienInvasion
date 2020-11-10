import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        # storing Bullets in a Group
        self.bullets = pygame.sprite.Group()
        # storing Alien ships
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def _check_events(self):
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                sys.exit()
            elif event_type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event_type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        key = event.key
        if key == pygame.K_RIGHT:
            self.ship.is_moving_right = True
        elif key == pygame.K_LEFT:
            self.ship.is_moving_left = True
        elif key == pygame.K_q:
            sys.exit()
        elif key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        key = event.key
        if key == pygame.K_RIGHT:
            self.ship.is_moving_right = False
        elif key == pygame.K_LEFT:
            self.ship.is_moving_left = False

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """create the fleet of aliens"""
        alien = Alien(self)

        alien_width = alien.rect.width
        alien_height = alien.rect.height

        spacing_between_x = self.settings.alien_spacing_between_x   # spacing between two alien
        spacing_edge_x = self.settings.alien_spacing_edge_x      # spacing on the screen edge
        availbe_width_x = self.settings.screen_width - (2 * spacing_edge_x)
        number_aliens_x = int(availbe_width_x // (alien_width + spacing_between_x))

        spacing_between_y = self.settings.alien_spacing_between_y   # spacing between two alien
        spacing_edge_y = self.settings.alien_spacing_edge_y      # spacing on the screen edge
        availbe_height_y = self.settings.screen_height - (2 * spacing_edge_y) - self.ship.rect.height
        number_aliens_y = int(availbe_height_y // (alien_height + spacing_between_y))

        for num_y in range(number_aliens_y):
            rect_y = spacing_edge_y + (num_y * (alien_height + spacing_between_y))
            for num_x in range(number_aliens_x):
                alien = Alien(self)
                rect_x = spacing_edge_x + (num_x * (alien_width + spacing_between_x))
                alien.x = rect_x
                alien.y = rect_y
                alien.rect.x = rect_x
                alien.rect.y = rect_y
                self.aliens.add(alien)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screeen()

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screeen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
