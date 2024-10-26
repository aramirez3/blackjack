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
        self.human_player.hand_value -= current_bet
        print(f"Your bet is {current_bet} ({self.human_player.hand_value} remaining)")
        for player in self.bot_players:
            player.hand_value -= self.minimum_bet
    
    def deal_cards(self):
        print("Dealing cards...")
        for i in range(0, 2):
            for player in self.seats:
                if player != []:
                    card1 = self.deck.pop()
                    card2 = self.deck.pop()
                    player.hand.append(card1)
                    player.hand.append(card2)
                    player.hand_value += card1.value
                    player.hand_value += card2.value
                    print(f"Cards remaining in deck: {len(self.deck)}")
                    print(f"Player hand: {player.hand_value}")
            self.dealer.hand.append(self.deck.pop)
     
    def print_player_hands(self):
        if len(self.dealer.hand) > 2:
            print(f"Dealer shows {', '.join(self.dealer.hand[1:])} ({self.dealer.hand_value})")
        else:
            print(f"Dealer shows {self.dealer.hand[1]} ({self.dealer.hand_value})")
        for player in self.seats:
            if player != []:
                print(f"{player.name} shows {', '.join(player.hand)} ({player.hand_value})")

    def update_game_status(self):
        for i in range(0, len(self.seats)):
            player = self.seats[i]
            if player != []:
                if player.hand_value < self.minimum_bet:
                    if player == self.human_player:
                        print(f"Game over! Better luck next time!")
                        self.is_active = False
                        return
                    print(f"{player.name} has been eliminated!")
                    self.seats[i] = []
        pass

class Player():
    def __init__(self, seat_number = 0):
        self.name = ""
        self.hand = []
        self.hand_value = 0
        self.cash_money = 0
        self.seat_number = seat_number
        self.hand_description = ""
        