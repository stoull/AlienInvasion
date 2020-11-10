class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 640
        self.screen_height = 400
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 2
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3         # a number of bullets allowed show the same time on the screen

        # Alien settings
        self.alien_spacing_between_x = 32   # spacing between two alien, it'll change depends on the size of alien's image
        self.alien_spacing_edge_x = 32      # spacing on the screen edge
        self.alien_spacing_between_y = 32
        self.alien_spacing_edge_y = 32

        self.alien_speed = 0.04
        self.fleet_drop_speed = 2
        # fleet_direction of 1 represents right, -1 represents left
        self.fleet_direction = 1
