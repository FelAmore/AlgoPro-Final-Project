import pygame, time, random
from slotmachine import SlotMachine
from font import DigitalFont
from btn import SlotMachineBetButton, SlotMachineActionButton

# Initialize game constants
FRAME_RATE = 30
GAME_TITLE = "Final Project Slot Machine"
BACKGROUND_IMAGE_NAME = "images/background.png"

# Function to start the game
def start_game():
  # Assigning the Display Variables
  background = pygame.image.load(BACKGROUND_IMAGE_NAME)
  screen = pygame.display.set_mode(background.get_size())
  pygame.display.set_caption(GAME_TITLE)

  # Create the slot machine object and hashes to be used by the game
  slot_machine = SlotMachine(1000, 500)
  spin_results = slot_machine.results

  # The current icon images or spin result icons
  icon_images = [] 

  # Create the text labels
  digital_fonts_hash = [
    {"method": slot_machine.get_bet, "pos": (245, 424)},
    {"method": slot_machine.get_current_cash, "pos": (80, 424)},
    {"method": slot_machine.get_current_jackpot, "pos": (445, 424)},
  ]
  digital_fonts = pygame.sprite.Group()

  current_message_digifont = DigitalFont(slot_machine.get_current_message, (100, 140), (0, 0, 0))

  for digital_font in digital_fonts_hash:
    digital_fonts.add(DigitalFont(digital_font["method"], digital_font["pos"]))

  # Set the constants
  BUTTON_BOTTOM_POS = background.get_height() - 165

  # Create the bet buttons
  bet_buttons_hash = [
    {"image_file_name": "ten_button.png", "bet_value": 10, "pos": (70, BUTTON_BOTTOM_POS)},
    {"image_file_name": "twenty_button.png", "bet_value": 20, "pos": (140, BUTTON_BOTTOM_POS)},
    {"image_file_name": "fifty_button.png", "bet_value": 50, "pos": (490, BUTTON_BOTTOM_POS)},
    {"image_file_name": "hundred_button.png", "bet_value": 100, "pos": (560, BUTTON_BOTTOM_POS)}
  ]
  bet_buttons = pygame.sprite.Group()

  for bet_button in bet_buttons_hash:
    bet_buttons.add(SlotMachineBetButton(bet_button["image_file_name"], bet_button["bet_value"], bet_button["pos"]))

  # Create the action buttons
  spin_button = SlotMachineActionButton("spin_button.png" , slot_machine.spin, (270, BUTTON_BOTTOM_POS))
  reset_button = SlotMachineActionButton("reset_button.png" , slot_machine.reset, (210, BUTTON_BOTTOM_POS + 30))
  quit_button = SlotMachineActionButton("quit_button.png" , slot_machine.reset, (422, BUTTON_BOTTOM_POS + 30))
  action_buttons = pygame.sprite.Group(spin_button, reset_button, quit_button)

  # Create all the symbols/icons to be shown in the reels
  all_symbols = pygame.sprite.Group()
  icons = slot_machine.icons
  for icon in icons:
    all_symbols.add(icon)

  # Set the game clock
  clock = pygame.time.Clock()

  # The reel positions is saved as an array with tuples
  reel_positions = [(75, 258), (265, 258), (445, 258)]

  # Add the spin result symbols to icon images
  for symbol in all_symbols:
    for symbol_name in spin_results:
      if (symbol.name == symbol_name):
        icon_images.append(symbol)

  # Set the variables to be used by the game loop
  start_time = 0
  spinning = False

  # Set the previous spin results
  prev_results = slot_machine.results

  # Set the current slot machine values as previous values
  prev_bet, prev_jackpot, prev_current_msg, prev_cash = slot_machine.bet, slot_machine.current_jackpot, slot_machine.current_message, slot_machine.current_cash

  # Create functions to get the previous slot machine values
  def prev_get_bet():
    return prev_bet
  def prev_get_current_cash():
    return prev_cash
  def prev_get_current_jackpot():
    return prev_jackpot
  def prev_get_current_msg():
    return prev_current_msg

  # Set the text values as the previous values
  # The reason is to not let the users see how much they won until the spin animation is done
  prev_bet_digifont = DigitalFont(prev_get_bet, (245, 424))
  prev_cash_digifont = DigitalFont(prev_get_current_cash, (80, 424))
  prev_jackpot_digifont = DigitalFont(prev_get_current_jackpot, (445, 424))
  prev_message_digifont = DigitalFont(prev_get_current_msg, (100, 140), (0, 0, 0))

  # Create the sprite group digifonts
  # The prev digifonts are the ones to be shown to the users while the spin animation is running.
  prev_digifonts = pygame.sprite.Group(prev_bet_digifont, prev_jackpot_digifont, prev_cash_digifont, prev_message_digifont)

  # Continue looping while the player hasn't ended the game
  continue_playing = True
  while (continue_playing):
    clock.tick(FRAME_RATE)

    # Check for events
    for event in pygame.event.get():
      # Stop the loop when the user chooses to quit the game
      if (event.type == pygame.QUIT):
        continue_playing = False
      # To check which sprite is involved when the user click the mouse btn
      elif (event.type == pygame.MOUSEBUTTONDOWN):
        # To check if the bet button is clicked then set the bet value to the value of that button
        for bet_button in bet_buttons:
          if(bet_button.rect.collidepoint(event.pos)):
            slot_machine.set_bet(bet_button.bet_value)
        # To check if the spin button is clicked
        if(spin_button.rect.collidepoint(event.pos)):
          # To make sure user can't click the spin button while the reels are spinning
          if not spinning:
            spin_button.execute_func()
            # If the message in the slot machine says the user cannot spin the reels, the nothing will happen. 
            if slot_machine.current_message != SlotMachine.CANNOT_SPIN:
              spin_results = slot_machine.results

              # To set the result's icon into icon_images
              icon_images = []
              for symbol in all_symbols:
                for symbol_name in spin_results:
                  if (symbol.name == symbol_name):
                    icon_images.append(symbol)

              # Set the start time to current time. Making the spin animation run
              start_time = time.time()

              # Set spinning to true to make sure the user can't click spin again while spinning
              spinning = True
            else:
              slot_machine.bet_no_cash_snd.play()
        # If the reset button is clicked, call the function associated with the button and play the reset sound
        elif(reset_button.rect.collidepoint(event.pos)):
          slot_machine.reset_snd.play()
          reset_button.execute_func()
        # If the quit button is clicked, stop the loop
        elif(quit_button.rect.collidepoint(event.pos)):
          continue_playing = False

    # To display the background image
    screen.blit(background, background.get_rect())

    # Update the action buttons and position them on the screen
    action_buttons.update()
    for action_button in action_buttons:
      screen.blit(action_button.image, action_button.pos)

    # To update the texts
    digital_fonts.update()

    # To update the bet buttons and position them on the screen
    bet_buttons.update()
    for bet_button in bet_buttons:
      screen.blit(bet_button.image, bet_button.pos)

    # Section for the reel animation
    # While the current time - the time the spin button is clicked is less than one
    # Change the images in the reel and show the previous/current texts
    if time.time() - start_time < 1 and spinning:
      # To display the current icons in the reel so it does not change until the pulling the lever sound is finished
      for i in range(3):
        screen.blit(prev_results[i].image, reel_positions[i])
      # To display the current texts
      for digital_font in prev_digifonts:
        screen.blit(digital_font.get_rendered_surface(), digital_font.pos)
    elif time.time() - start_time < 2 and spinning:
      # To display a random icon in each reel and play the spinning sound
      for i in range(3):
        screen.blit(icons[random.randint(0, len(icons) - 1)].image, reel_positions[i])
      slot_machine.spinning_snd.play()
      # To display the current texts
      for digital_font in prev_digifonts:
        screen.blit(digital_font.get_rendered_surface(), digital_font.pos)
    else:
      # The animation is done and display the resulted values
      for i in range(3):
        screen.blit(icon_images[i].image, reel_positions[i])
      screen.blit(current_message_digifont.get_rendered_surface(), current_message_digifont.pos)
      # Spinning is now false, so the user can hit spin again
      spinning = False
      # Set the prev results to the current images to be used again on animation
      prev_results = icon_images
      # Stop the spinning sound if the game is playing
      slot_machine.spinning_snd.stop()
      # Render the current texts in the screen
      for digital_font in digital_fonts:
        screen.blit(digital_font.get_rendered_surface(), digital_font.pos)

      # Reset the prev values
      prev_bet, prev_jackpot, prev_current_msg, prev_cash = slot_machine.bet, slot_machine.current_jackpot, slot_machine.current_message, slot_machine.current_cash

    # Refresh the display
    pygame.display.flip()