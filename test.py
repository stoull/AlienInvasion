import sys
import pygame

class AlienInv:
	"""docstring for AlienInv"""
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((640, 400))
		pygame.display.set_caption("Alien Invision")

		self.image_ship = pygame.image.load('images/rocket.png')
		self.rect_ship = self.image_ship.get_rect()
		self.rect_ship.midbottom = self.screen.get_rect().midbottom

	def run_game(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			self.screen.fill((140, 207, 247))
			self.screen.blit(self.image_ship, self.rect_ship)
			pygame.display.flip()

if __name__ == '__main__':
	ai = AlienInv()
	ai.run_game()