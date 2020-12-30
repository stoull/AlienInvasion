class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 640
        self.screen_height = 400
        self.bg_color = (230, 230, 230)

        # level
        self.level_max = 12

        # ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 2
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullet_is_penetration = False
        self.bullet_allowed = 3         # a number of bullets allowed show the same time on the screen

        # Alien settings
        self.alien_spacing_between_x = 66   # spacing between two alien, it'll change depends on the size of alien's image
        self.alien_spacing_edge_x = 32      # spacing on the screen edge
        self.alien_spacing_between_y = 2
        self.alien_spacing_edge_y = 44
        # The spaces between alien and ship in the begining of the game
        self.alien_ship_frontline = self.screen_height - self.alien_spacing_edge_y - \
                                    self.alien_spacing_between_y - 120

        self.alien_speed = 0.1
        self.fleet_drop_speed = 1
        # fleet_direction of 1 represents right, -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

