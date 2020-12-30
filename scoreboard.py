import pygame.font
class Scoreboard:
    """A class to report scoring information"""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.highest_score = 0

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 26)

        self.prep_score()
        self._prep_highest_score()

    def prep_score(self):
        """ Turn the socre into a rendered image."""
        self._save_higest_socre()
        round_socre = round(self.stats.score)
        score_str = "{:,}".format(round_socre)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Dispaly the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 8

        self._prep_highest_score()


    def _prep_highest_score(self):
        """Turn the highest score into a rendered image"""
        highest_score = str(self.highest_score)
        self.highest_score_image = self.font.render(highest_score, True, self.text_color, self.settings.bg_color)

        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.center = self.screen_rect.center
        self.highest_score_rect.top = 8

    def show_score(self):
        """Darw socre to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highest_score_image, self.highest_score_rect)

    def _save_higest_socre(self):
        if self.stats.score > self.highest_score:
            self.highest_score = self.stats.score