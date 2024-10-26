from random import randrange

from deck import *

class Game():
    def __init__(self):
        self.deck = []
        self.dealer = None
        self.human_player = None
        self.number_of_bots = 0
        self.bot_players = []
        self.minimum_bet = 5
        self.seats = [[]] * 5
        self.is_active = False
    
    def _create_human_player(self):
        player = Player()
        player.name = "Player 1"
        self.human_player = player
        return player
        
    def _create_bot_players(self, bots):
        if 0 < bots < 5:
            self.number_of_bots = bots
            bots_list = []
            for i in range(bots):
                player = Player()
                player.name = f"Bot {i}"
                bots_list.append(player)
            self.bot_players.extend(bots_list)
        
    def _create_dealer(self):
        dealer = Player()
        dealer.name = "Dealer"
        self.dealer = dealer
        
    def _assign_seating(self):
        reserved_seat = self.human_player.seat_number
        self.seats[reserved_seat] = self.human_player
        bots_remaining = len(self.bot_players)
        while bots_remaining:
            seat_number = randrange(0, 5)
            if seat_number != reserved_seat and self.seats[seat_number] == []:
                self.seats[seat_number] = self.bot_players[bots_remaining - 1]
                bots_remaining -= 1
    
    def start_new_game(self):
        self._create_human_player()
        self._create_dealer()
        self.game_start_greeting()
        self._create_bot_players(self.number_of_bots)
        self._assign_seating()
        self.shuffle_deck()
        self.is_active = True
    
    def shuffle_deck(self):
        deck = Deck()
        for _ in range(0, len(deck.game_deck)):
            cards_remaining = len(deck.game_deck)
            card_index = randrange(0, cards_remaining)
            card = deck.game_deck[card_index]
            self.deck.append(card)
            del deck.game_deck[card_index]
            
    def game_start_greeting(self):
        print(f"current player: {self.human_player}")
        print(f"Welcome to the Blackjack table!\nThis table has minimum bets of {self.minimum_bet}.")
        
        self._select_seat_number()
        self._player_cash_in()
        self._select_bot_teammates()

    def _select_seat_number(self):
        while True:
            try:
                seat_number = int(input("Pick a seat number (1-5): "))
                if seat_number > 0 and seat_number <=5:
                    self.human_player.seat_number = seat_number
                    break
            except ValueError:
                print("Please select a seat number from 1-5")
    
    def _player_cash_in(self):
         while True:
            try:
                amount = float(input("How much would you like to cash in?: "))
                if amount > self.minimum_bet:
                    self.human_player.cash_money = amount
                    print(f"Deep pockets! You now have {amount} worth of chips.")
                    break
            except ValueError:
                print(f"Invalid entry. Minimum bet is {self.minimum_bet}.")
        
    def _select_bot_teammates(self):
        while True:
            try:
                number_of_bots = int(input("How many bot players would you like to play with?: "))
                if number_of_bots >= 0 and number_of_bots < 4:
                    if (number_of_bots == 1):
                        print("OKAY! I see you want to 1v1. Good luck!")
                    else:
                        print("Excellent! Good luck, all!")
                    self.number_of_bots = number_of_bots
                    break
            except ValueError:
                print("Invalid entry. Please enter 0-4: ")

    def place_bets(self):
        while True:
            try:
                current_bet = float(input(f"Place your bet (min: {self.minimum_bet}): "))
                if current_bet > self.minimum_bet:
                    break
                else:
                    print(f"Minimum bet is {self.minimum_bet}")
            except ValueError:
                print(f"Invalid input. Minimum bet is {self.minimum_bet}")
        print(f"Your bet is {current_bet} ({self.human_player.hand_value} remaining)")
        self.human_player.update_money(current_bet)
        for player in self.bot_players:
            if player.is_active:
                player.update_money(self.minimum_bet)
    
    def deal_cards(self):
        print("Dealing cards...")
        for _ in range(0, 2):
            for player in self.seats:
                if player != []:
                    player.activate(self)
                    if player.is_active:
                        player.update_hand(self.deck.pop())
                        player.update_hand_description()
            self.dealer.update_hand(self.deck.pop())
            print(f"Cards remaining in deck: {len(self.deck)}")
     
    def print_player_hands(self):
        if len(self.dealer.hand) > 2:
            print(f"++Dealer shows {', '.join(map(lambda x: x.value, self.dealer.hand[1:]))} ({self.dealer.hand_value - self.dealer.hand[0].value})")
        else:
            print(f"++Dealer shows {self.dealer.hand[1].value} ({self.dealer.hand_value})")
        
        for player in self.seats:
            if player != [] and player != self.human_player:
                print(f"--{player.name} shows {player.hand_description} ({player.hand_value})")
        
        print(f"Your hand: {self.human_player.hand_description} ({self.human_player.hand_value})")

    def update_game_status(self):
        for player in self.seats:
            if player != []:
                if player.hand_value < self.minimum_bet:
                    if player == self.human_player:
                        print(f"Game over! The house ALWAYS wins!")
                        self.is_active = False
                        return
                    print(f"{player.name} has been eliminated!")
                    player.deactivate()
        pass

class Player():
    def __init__(self, seat_number = 0):
        self.name = ""
        self.hand = []
        self.hand_value = 0
        self.cash_money = 0
        self.seat_number = seat_number
        self.hand_description = ""
        self.is_active = True
        
    def update_hand_description(self):
        self.hand_description = ", ".join(map(lambda x: x.name, self.hand))
    
    def update_hand(self, card):
        self.hand.append(card)
        self.hand_value += card.value
        
    def update_money(self, bet):
        self.cash_money -= bet
        
    def activate(self, game):
        if self.cash_money > game.minimum_bet:
            self.is_active = True
    
    def deactivate(self):
        self.is_active = False