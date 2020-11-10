import pygame

class Ship:
    """A class to manage the ship"""
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # load the ship image and get its rect.
        self.image = pygame.image.load('images/rocket.png')
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # status
        self.is_moving_right = False
        self.is_moving_left = False

        # position values
        self.x = float(self.rect.x)
        self._rect_x_min = 0
        self._rect_x_max = self.screen_rect.width - self.rect.width

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """update the ship's position"""
        if self.is_moving_right:
            if self.rect.x < self._rect_x_max:
                self.x += self.settings.ship_speed
        elif self.is_moving_left:
            if self.rect.x > self._rect_x_min:
                self.x -= self.settings.ship_speed

        self.rect.x = self.x
