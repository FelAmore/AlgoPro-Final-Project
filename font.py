import pygame

# Class to show a text label using digital font ttf
class DigitalFont(pygame.sprite.Sprite):
    def __init__(self, method, pos, color = (196,65,46)):
        pygame.sprite.Sprite.__init__(self)
        self.digital_font = pygame.font.Font("fonts/DS-DIGIT.TTF", 22)
        self.font_color = color
        self.meth = method
        self.pos = pos

    # Function to return the rendered text
    def get_rendered_surface(self):
        return self.digital_font.render(str(self.meth()), 1, self.font_color)

    # Function to render the text by update
    def update(self):
        self.digital_font.render(str(self.meth()), 1, self.font_color)