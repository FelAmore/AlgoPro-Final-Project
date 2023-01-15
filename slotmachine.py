import pygame
import random
from icon import Icon


# Class for all the methods required when playing the slot machine
class SlotMachine:
    MAIN_MSG = "Fel's Slot Machine"
    YOU_WIN = "You just won $"
    YOU_WIN_JACKPOT = "Jackpot won $"
    YOU_LOST = "You just lost $"
    YOU_BET = "You bet $"
    NO_CASH_LEFT = "Cannot bet to that amount. Cash not enough."
    CANNOT_SPIN = "Cannot spin. Cash not enough."
    STARTING_BET = 10
    JACKPOT_INCREASE_RATE = .15


    # Function that gets the starting jackpot price and the starting cash amount as the parameters.
    def __init__(self, starting_jackpot, starting_cash):
        # To set all sounds
        pygame.mixer.init()
        self.bet_snd = pygame.mixer.Sound("sounds/bet_snd.wav")
        self.bet_no_cash_snd = pygame.mixer.Sound("sounds/bet_no_cash_snd.wav")
        self.spin_snd = pygame.mixer.Sound("sounds/spin_snd.ogg")
        self.spinning_snd = pygame.mixer.Sound("sounds/spinning_snd.ogg")
        self.reset_snd = pygame.mixer.Sound("sounds/reset_snd.ogg")

        # Setting the starting values
        self.starting_jackpot = starting_jackpot
        self.starting_cash = starting_cash

        # Setting the icons/images that would be in the reels
        self.icons = []
        self.__create_icons()

        # To call the method used to set the initial values
        self.set_resettable_values()

    
    # Function to set values of slot machine which are resettable
    def set_resettable_values(self):
        self.current_message = SlotMachine.MAIN_MSG
        self.current_jackpot = self.starting_jackpot
        self.current_cash = self.starting_cash
        self.results = 3*["Seven"]
        self.bet = SlotMachine.STARTING_BET

   
    # Function to create and set icons in an array
    def __create_icons(self):
    # The bonus win rate is for when no sad face appeared on the reel
        self.icons.append(Icon("Sad Face", 0, 0, "sadface.png", bonus_win_rate = 1))
        self.icons.append(Icon("Bell", 10, 1, "bell.png"))
        self.icons.append(Icon("Cherry", 20, 2, "cherry.png"))
        self.icons.append(Icon("Melon", 30, 2, "melon.png"))
        self.icons.append(Icon("Orange", 100, 2, "orange.png"))
        self.icons.append(Icon("Grape", 200, 2, "grape.png"))
        self.icons.append(Icon("Diamond", 300, 5, "diamond.png"))
        self.icons.append(Icon("Seven", 1000, 10, "seven.png", bonus_win_rate = 5))

    
    # Function to set a bet
    def set_bet(self, bet):
        # When valid, users are allow to bet. 
        if self.current_cash - bet >= 0:
            self.bet = bet
            self.current_message = SlotMachine.YOU_BET + str(self.bet)
            self.bet_snd.play()
        # Otherwise, it'll tell users that they're out of cash.
        else:
            self.current_message = SlotMachine.NO_CASH_LEFT
            self.bet_no_cash_snd.play()


    # Functions to get attributes
    def get_bet(self):
        return self.bet

    def get_current_cash(self):
        return self.current_cash

    def get_current_jackpot(self):
        return self.current_jackpot

    def get_current_message(self):
        return self.current_message

   
    # Function to spin the reels. Spinning is only allowed when there is enough money to do so.
    def spin(self):
        if self.current_cash - self.bet >= 0:
            self.spin_snd.play()
            # pay the bet and increase the jackpot
            self.__pay()
            self.__increase_jackpot()

            # For each reel,
            for spin in range(3):
                # Save the wildcard number as spinned_result
                spinned_result = random.randint(0, 100)

                if spinned_result in range(0, 40):     # 40% Chance
                    self.results[spin] = self.icons[0].name
                elif spinned_result in range(40, 56):  # 16% Chance
                    self.results[spin] = self.icons[1].name
                elif spinned_result in range(56, 70):  # 14% Chance
                    self.results[spin] = self.icons[2].name
                elif spinned_result in range(70, 82):  # 12% Chance
                    self.results[spin] = self.icons[3].name
                elif spinned_result in range(82, 89):  # 7% Chance
                    self.results[spin] = self.icons[4].name
                elif spinned_result in range(89, 95):  # 6% Chance
                    self.results[spin] = self.icons[5].name
                elif spinned_result in range(95, 99):  # 4% Chance
                    self.results[spin] = self.icons[6].name
                elif spinned_result in range(99, 100):  # 1% Chance
                    self.results[spin] = self.icons[7].name

            # To check the result of the calculation rewards.
            self.__check_results()
        else:
            # Show the reason why the slot machine cannot be spinned
            self.current_message = SlotMachine.CANNOT_SPIN

   
    # Function to reduce cash by the bet amount everytime the user spin the slot machine.
    def __pay(self):
        self.current_cash -= self.bet

  
    # Function to increase the jackpot prize to be winned
    def __increase_jackpot(self):
        self.current_jackpot += (int(self.bet * SlotMachine.JACKPOT_INCREASE_RATE))

  
    # Function to check how much the player won or lost
    def __check_results(self):
        winnings = 0
        jackpot_won = 0
        # Go through each icon and check how many of the said icon is present. Base on that, check how much the player have won.
        for icon in self.icons:
            # Check how many of this icon is on the reel. Then multiply the win rate to the bet and add it to winnings.
            if self.results.count(icon.name) == 3:
                winnings += self.bet * icon.win_rate_full
                # Play jackpot when 3 of a kind and not sadface is the result
                if winnings > 0:
                    jackpot_won = self.jackpot_win()
            if self.results.count(icon.name) == 2:
                winnings += self.bet * icon.win_rate_two
        # If there is 1 Seven, it is considered a win
        if self.results.count(self.icons[7].name) == 1:
            winnings += self.bet * self.icons[7].bonus_win_rate
        # If there is no sad face, it is considered a bet return win
        if self.results.count(self.icons[0].name) == 0:
            winnings += self.bet * self.icons[0].bonus_win_rate

    
        # Set the appropriate message for:
        # If the user won the jackpot
        if jackpot_won > 0:
            self.current_message = SlotMachine.YOU_WIN_JACKPOT + str(jackpot_won) + " With Cash $" + str(winnings)
        # Or if the user won something
        elif winnings > 0:
            self.current_cash += winnings
            self.current_message = SlotMachine.YOU_WIN + str(winnings)
        # Or if the user lost
        elif winnings <= 0:
            self.current_message = SlotMachine.YOU_LOST + str(self.bet)
        else:
            self.current_message = "Somethings wrong"

    
    # Function to return the value of the user's jackpot winnings
    def jackpot_win(self):
        # Set the wildcard jackpot number
        JACKPOT_WILDCARD = 7
        # Generate a random number from 1 to 100
        jackpot_try = random.randint(1, 100)
        winnings = 0

        # Compare the wildcard to the random number
        if jackpot_try == JACKPOT_WILDCARD:
            # If they match, then the user wins
            self.current_cash += self.current_jackpot
            # Set the current jackpot as the winnings. 
            winnings = self.current_jackpot
            # Reset the jackpot
            self.current_jackpot = self.starting_jackpot
        return winnings

   
    # Function to reset the slot machine when started
    def reset(self):
        self.set_resettable_values()