import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load the image and set the rect attribute
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()

        self.settings.alien_spacing_between_x = self.rect.width
        self.settings.alien_spacing_between_y = self.rect.height

        # the alien start the top left of the screen
        self.rect.x = self.settings.alien_spacing_between_x
        self.rect.y = self.settings.alien_spacing_between_y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)