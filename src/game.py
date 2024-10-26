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
        self.human_player = player
        return player
        
    def _create_bot_players(self, bots):
        if 0 < bots < 5:
            self.number_of_bots = bots
            bots_list = []
            for _ in range(bots):
                player = Player()
                bots_list.append(player)
            self.bot_players.extend(bots_list)
        
    def _create_dealer(self):
        dealer = Player()
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
    
    def start_new_game(self, bots = 0):
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
        print(f"Welcome to the Blackjack table!\nThis table has minimum bets of {self.minimum_bet}.\nHow much would you like to cash in?")
        amount = float(input())
        self.human_player.cash_money = amount
        print(f"Deep pockets! You now have {amount} worth of chips.")
        print("Would you like to 1v1 the house or have some company? How many bot players would you like to play with?")
        number_of_bots = int(input())
        while (0 > number_of_bots or number_of_bots > 4):
            print("Please select a number from 0 to 4:")
            number_of_bots = int(input())
        if (number_of_bots == 1):
            print("OKAY! I see you want to 1v1. Good luck!")
        else:
            print("Excellent! Good luck, all!")
        self.number_of_bots = number_of_bots
        
    def place_bets(self):
        print("Place your bets!")
        current_bet = float(input())
    

class Player():
    def __init__(self, seat_number = 0):
        self.hand = []
        self.cash_money = 0
        self.seat_number = seat_number
        