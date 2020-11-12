from settings import Settings
from copy import deepcopy

class LevelController:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.settings_copy = deepcopy(self.settings)

        self.current_level = 0

    def level_up(self):
        self._clean_before_levelup()
        if self.current_level <= self.settings.level_max:
            self._level_up_alien()
            self._level_up_ship()
            self._level_up_frontline()
            self.current_level +=1
            print(f"Current level: {self.current_level}")
        else:
            self.ai_game.stats.game_stas_active = False

    def change_weapon_mode(self, mode = 'n'):
        if mode == "r": # Super weapon, kill all aliens
            self.settings.bullet_width = self.settings.screen_width
            self.settings.bullet_is_penetration = True
            print(f"is PEN FFF ")

    def _clean_before_levelup(self):
            self.settings.bullet_width = self.settings_copy.bullet_width
            self.settings.bullet_is_penetration = self.settings_copy.bullet_is_penetration
            print(f"is PEN SSS :{self.settings.bullet_is_penetration}")

    def _level_up_alien(self):
        if self.settings.alien_spacing_between_x > 10:
            self.settings.alien_spacing_between_x -=2

        if self.settings.alien_spacing_edge_x > 0:
            self.settings.alien_spacing_edge_x -=2

        self.settings.alien_spacing_between_y = 2

        if self.settings.alien_spacing_edge_y > 0:
            self.settings.alien_spacing_edge_y -=2

        self.settings.alien_speed += 0.1
        self.settings.fleet_drop_speed += 0.5

    def _level_up_ship(self):
        self.settings.ship_speed -= 0.2

    def _level_up_frontline(self):
        self.settings.alien_ship_frontline -= 1

    def _level_up_bullet(self):
        self.settings.bullet_allowed +=1
