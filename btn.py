import pygame

# Class for the slot machine's button. It only have an image positioned in the screen.
class SlotMachineButton(pygame.sprite.Sprite):
    def __init__(self, image_file_name, pos):
        pygame.sprite.Sprite.__init__(self)
        # Load the png image with transparency
        self.image = pygame.image.load("images/" + image_file_name)
        self.image = self.image.convert_alpha()
        # Move the rect to make sure it follows the image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        self.pos = pos


# Derived class from SlotMachineButton
# Class for the bet value
class SlotMachineBetButton(SlotMachineButton):
    def __init__(self, image_file_name, bet_value, pos):
        SlotMachineButton.__init__(self, image_file_name, pos)
        self.bet_value = bet_value
        

# Derived class from SlotMachineButton
# Class for button that can call a function
class SlotMachineActionButton(SlotMachineButton):
    def __init__(self, image_file_name, function_callable, pos):
        SlotMachineButton.__init__(self, image_file_name, pos)
        self.function_callable = function_callable
    # To execute the function callable
    def execute_func(self):
        self.function_callable()