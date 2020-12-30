import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from level_control import LevelController
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.stats = GameStats(self)
        self.stats.game_stas_active = False
        self.scoreBoard = Scoreboard(self)

        self.level_ctr = LevelController(self)

        # storing Bullets in a Group
        self.bullets = pygame.sprite.Group()
        # storing Alien ships
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Create the Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.stats.game_stas_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screeen()

    def _check_events(self):
        for event in pygame.event.get():
            event_type = event.type
            if event_type == pygame.QUIT:
                sys.exit()
            elif event_type == pygame.KEYDOWN:  # press the keyboard down
                self._check_keydown_events(event)
            elif event_type == pygame.KEYUP:    # left finger form keyboard
                self._check_keyup_events(event)
            elif event_type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        key = event.key
        if key == pygame.K_RIGHT:
            self.ship.is_moving_right = True
        elif key == pygame.K_LEFT:
            self.ship.is_moving_left = True
        elif key == pygame.K_q:
            sys.exit()
        elif key == pygame.K_r:
            self.level_ctr.change_weapon_mode('boost')
        elif key == pygame.K_SPACE:
            self._fire_bullet()
        elif key == pygame.K_l:
            self.level_ctr.change_weapon_mode('super')
        else:
            pass
            print(f"key down {key}")

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
        availbe_height_y = self.settings.screen_height - (2 * spacing_edge_y)\
                           - self.ship.rect.height - self.settings.alien_ship_frontline
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

    def _check_fleet_edge(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's dicrection"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """Check if the fleet is at an edge,
            then update the positions of all aliens in the fleet
        """
        self._check_fleet_edge()


        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # look for if aliens hit the screen bottom
        self._check_aliens_bottom()

        self.aliens.update()

    def _update_screeen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the socre information
        self.scoreBoard.show_score()

        #Draw the play button if the game is inactive
        if not self.stats.game_stas_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        is_penetration = self.settings.bullet_is_penetration
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, not is_penetration, True
        )

        if collisions:
            for alines in collisions.values():
                self.stats.score += self.settings.alien_points
            self.scoreBoard.prep_score()

        if not self.aliens:
            # Destory existing bullets and create new fleet
            self.bullets.empty()
            # level up
            if self.level_ctr.level_up():
                self._create_fleet()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(1)
        else:
            self.stats.game_stas_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this same if the ship got hit
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        buttton_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if buttton_clicked and not self.stats.game_stas_active:
            self.stats.reset_stats()
            self.stats.game_stas_active = True
            self.scoreBoard.prep_score()

            #Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
