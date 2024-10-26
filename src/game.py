from random import randrange

from deck import *
from constants import *

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
                player.name = f"Bot {i + 1}"
                bots_list.append(player)
            self.bot_players.extend(bots_list)
        
    def _create_dealer(self):
        dealer = Dealer()
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
        print("----------------\nShuffling the deck")
        deck = Deck()
        for _ in range(0, len(deck.game_deck)):
            cards_remaining = len(deck.game_deck)
            card_index = randrange(0, cards_remaining)
            card = deck.game_deck[card_index]
            self.deck.append(card)
            del deck.game_deck[card_index]
        print("Deck is shuffled\n----------------")
            
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
                    self.human_player.seat_number = seat_number - 1
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
                if current_bet >= self.minimum_bet:
                    break
                else:
                    print(f"Minimum bet is {self.minimum_bet}")
            except ValueError:
                print(f"Invalid input. Minimum bet is {self.minimum_bet}")
        self.human_player.update_money(current_bet)
        print(f"Your bet is {current_bet} ({self.human_player.cash_money} remaining)")
        for player in self.bot_players:
            if player.is_active:
                player.update_money(self.minimum_bet)
        print("All bets have been placed")
    
    def deal_cards(self, quantity = 1):
        print("Dealing cards...")
        for _ in range(0, quantity):
            for player in self.seats:
                if player != []:
                    player.activate(self)
                    if player.is_active:
                        player.update_hand(self.deck.pop(), self)
            card = self.deck.pop()
            self.dealer.update_hand(card, self)
            print(f"Cards remaining in deck: {len(self.deck)}")
     
    def print_player_hands(self):
        print(f"++Dealer's full hand = {self.dealer.hand_description}")
        if len(self.dealer.hand) > 2:
            print(f"++Dealer shows {self.dealer.visible_hand_description}")
        else:
            print(f"++Dealer shows {self.dealer.visible_hand_description}")
        print(f"    --dealer visible value = {self.dealer.visible_value}")
        
        for player in self.seats:
            if player != [] and player != self.human_player:
                print(f"--{player.name} shows {player.hand_description} ({player.hand_value})")
        
        print(f"Your hand: {self.human_player.hand_description} ({self.human_player.hand_value})")

    def update_game_status(self, first_round=True):
        for player in self.seats:
            if player != []:
                if player.cash_money < self.minimum_bet:
                    if player == self.human_player:
                        print(f"Game over! The house ALWAYS wins!")
                        self.is_active = False
                        return
                    print(f"{player.name} has been eliminated!")
                    player.deactivate()
    
    def decide_next_round(self):
        if self.dealer.hand_value < 17:
            self.players_decide_next_move()
            return
        else:
            self.dealer_collects_or_pays_out()
    
    def dealer_collects_or_pays_out(self):
        print("dealer_collects_or_pays_out")
            
    def players_decide_next_move(self):
            for player in self.seats:
                if player != [] and player.is_active:
                    if player == self.human_player:
                        player.human_player_next_play(self)
                    else:
                        player.play_basic_strategy()

class Player():
    def __init__(self, seat_number = 0):
        self.name = ""
        self.hand = []
        self.hand_value = 0
        self.cash_money = 0
        self.seat_number = seat_number
        self.hand_description = ""
        self.is_active = True
        
    def update_hand_description(self, game):
        self.hand_description = ", ".join(map(lambda x: x.name, self.hand))
        if self == game.dealer:
            self.visible_hand_description = ", ".join(map(lambda x: x.name, self.hand[1:]))
    
    def update_hand(self, card, game):
        self.hand.append(card)
        self.hand_value += card.value
        if self == game.dealer:
            self.visible_value = self.hand_value - self.hand[0].value
        self.update_hand_description(game)
        
    def update_money(self, bet):
        self.cash_money -= bet
        
    def activate(self, game):
        if self.cash_money > game.minimum_bet:
            self.is_active = True
    
    def deactivate(self):
        self.is_active = False
        
    def play_basic_strategy(self):
        print(f"basic strategy moves for {self.name}")
        
    def human_player_next_play(self, game):
        available_moves = [
            PlayerMoves.HIT,
            PlayerMoves.STAY,
            PlayerMoves.DOUBLE_DOWN
        ]
        if len(self.hand) == 2:
            if self.hand[0].rank == self.hand[1].rank:
                available_moves.append(PlayerMoves.SPLIT)
        while True:
            dealer_shows = f"{game.dealer.visible_hand_description} ({game.dealer.dealer_visible_value})"
            print(f"Dealer shows {dealer_shows}. Your hand is {self.hand_description} ({self.hand_value}).")
            move = input(f"Next move? {', '.join(map(lambda x: x.value, available_moves))}: ")

class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.visible_value = 0
        self.visible_hand_description = ""
        