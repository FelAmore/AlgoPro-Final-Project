import pygame

# Class for the Icons shown inside the reels
class Icon(pygame.sprite.Sprite):
    # Function that gets the icon's name, win rate when 3 icons are aligned, win rate when 2 icons are aligned, icon's image, and winrate for special icons as the parameters.
    def __init__(self, name, win_rate_full, win_rate_two, icon_image, bonus_win_rate = 0):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load("images/" + icon_image)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.win_rate_full = win_rate_full
        self.win_rate_two = win_rate_two
        self.bonus_win_rate = bonus_win_rate