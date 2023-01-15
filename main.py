import pygame
from start import *

# Initialize pygame
pygame.init()

# Class for the starting page
class Start:
    # Function for screen settings
    def __init__(self):
        self.screen = pygame.display.set_mode((672, 672))
        self.background = pygame.image.load("images/bg.png") 

    # To play bg music
    pygame.mixer.music.load("sounds/background_msc.wav")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1) 

    # Function for the start page
    def start(self):
        # Setting the start button
        start = pygame.image.load('images/start.png')
        start = pygame.transform.scale(start, (200, 110))
        # Setting the quit button
        exit = pygame.image.load('images/exit.png')
        exit = pygame.transform.scale(exit, (200, 110))
        # the looping begin
        while True:
            # For the background
            self.screen.blit(self.background, (0, 0))
            # To set the position of start and quit button.
            self.screen.blit(start, (230, 250))
            self.screen.blit(exit, (230, 385))

            # Get position of the user's mouse
            mouse = pygame.mouse.get_pos()

            # Settings for the action
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # If the user clicked:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    press = pygame.mouse.get_pressed()
                    if press[0]:
                        # Coordinate of mouse to start the game / switch into game page.
                        if 300 < mouse[0] < 500 and 250 < mouse[1] < 400:
                            start_game()
                        # Coordinate of mouse to quit / exit the game.
                        elif 300 < mouse[0] < 500 and 350 < mouse[1] < 600:
                            quit()
            # Update before looping again
            pygame.display.update()


# To start the game
if __name__ == "__main__": 
    while True:
        start = Start()
        start.start() 
