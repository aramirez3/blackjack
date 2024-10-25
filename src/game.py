from random import randrange

from deck import *

class Game():
    def __init__(self, human_player, bots = 0):
        self.deck = []
        self.dealer = None
        self.human_player = human_player
        self.number_of_bots = bots
        self.bot_players = []
        self.minimum_bet = 5
        self.seats = [[]] * 5
        self._create_bot_players()
        self._create_dealer()
        self._assign_seating()
        
    def _create_bot_players(self):
        if 0 < self.number_of_bots < 5:
            bots = []
            for _ in range(self.number_of_bots):
                player = Player()
                bots.append(player)
            self.bot_players.extend(bots)
        
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
                self.seats[seat_number] = self.bot_players.pop()
                bots_remaining -= 1
        print(self.seats)
        
    def start_new_game(self):
        self.shuffle_deck()
    
    def shuffle_deck(self):
        deck = Deck()
        for _ in range(0, len(deck.game_deck)):
            cards_remaining = len(deck.game_deck)
            card_index = randrange(0, cards_remaining)
            card = deck.game_deck[card_index]
            self.deck.append(card)
            del deck.game_deck[card_index]
    

class Player():
    def __init__(self, seat_number = 0):
        self.hand = []
        self.cash_money = 0
        self.seat_number = seat_number
        