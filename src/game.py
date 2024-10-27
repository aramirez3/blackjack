from random import randrange

from deck import *
from constants import *
from player import *
from game_state import *

class Game():
    def __init__(self):
        self.deck = []
        self.dealer = None
        self.human_player = None
        self.number_of_bots = 0
        self.bot_players = []
        self.minimum_bet = 5
        self.seats = [[]] * 5
        state = Game_State()
        self.state = state
    
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
                player.cash_money = randrange(1,9) * 10 * self.minimum_bet
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
        self.state.start_game
        self.state.start_hand
    
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
        print(f"current player: {self.human_player.name}")
        print(f"Welcome to the Blackjack table!\nThis table has minimum bets of {self.minimum_bet}.")
        
        self._select_seat_number()
        self._player_cash_in()
        self._select_bot_teammates()

    def _select_seat_number(self):
        validation_message = "Please select a seat number from 1-5"
        while True:
            try:
                seat_number = int(input("Pick a seat number (1-5): "))
                if seat_number > 0 and seat_number <=5:
                    self.human_player.seat_number = seat_number - 1
                    break
                else:
                    print(validation_message)
            except ValueError:
                print(validation_message)
    
    def _player_cash_in(self):
        validation_message = f"Minimum bet is {self.minimum_bet}."
        while True:
            try:
                amount = float(input("How much would you like to cash in?: "))
                if amount > self.minimum_bet:
                    self.human_player.cash_money = amount
                    print(f"Deep pockets! You now have {amount} worth of chips.")
                    break
                else:
                    print(validation_message)
            except ValueError:
                print(f"Invalid entry. {validation_message}")
        
    def _select_bot_teammates(self):
        validation_message = "Please enter a number from 0 to 4"
        while True:
            try:
                number_of_bots = int(input("How many bot players would you like to play with?: "))
                if number_of_bots >= 0 and number_of_bots <= 4:
                    if (number_of_bots == 1):
                        print("OKAY! I see you want to 1v1. Good luck!")
                    else:
                        print("Excellent! Good luck, all!")
                    self.number_of_bots = number_of_bots
                    break
                else:
                    print(validation_message)
            except ValueError:
                print(f"Invalid entry. {validation_message}")

    def place_bets(self):
        validation_message = f"Minimum bet is {self.minimum_bet} (True count {self.state.true_count})"
        while True:
            try:
                current_bet = float(input(f"Place your bet (min: {self.minimum_bet}): "))
                if current_bet >= self.minimum_bet:
                    break
                else:
                    print(validation_message)
            except ValueError:
                print(f"Invalid input. {validation_message}")
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
                        self.draw_card(player)
            self.draw_card(self.dealer)
            print(f"Cards remaining in deck: {len(self.deck)}")
    
    def draw_card(self, player):
        card = self.deck.pop()
        if card.rank == Ranks.ACE:
            player.set_soft_status()
        self.state.count_card(card, self)
        player.update_hand(card, self)
        return card
     
    def print_player_hands(self):
        for player in self.seats:
            if player != [] and player != self.human_player:
                print(f"--{player.name} shows {player.hand_description} ({player.hand_value})")
        
        print(f"++Dealer's full hand = {self.dealer.hand_description}")
        if len(self.dealer.hand) > 2:
            print(f"++Dealer shows {self.dealer.visible_hand_description}")
        else:
            print(f"++Dealer shows {self.dealer.visible_hand_description}")
        print(f"    --dealer visible value = {self.dealer.visible_value}")
        
        print(f"Your hand: {self.human_player.hand_description} ({self.human_player.hand_value})")

    def update_game_status(self):
        if not self.state.first_hand:
            for player in self.seats:
                if player != []:
                    if player.cash_money < self.minimum_bet:
                        if player == self.human_player:
                            print(f"Game over! The house ALWAYS wins!")
                            self.state.end_game
                            return
                        print(f"{player.name} has been eliminated!")
                        player.deactivate()
    
    def decide_next_round(self):
        if not self.state.first_hand:
            if self.dealer.hand_value < 17:
                self.players_decide_next_move()
                return
            else:
                self.dealer_collects_or_pays_out()
        else:
            self.check_for_blackjacks()
            self.players_decide_next_move()
            self.state.end_first_hand()
    
    def check_for_blackjacks(self):
        print(f"check if dealer has blackjack")
        print(f"insurance?")
        print(f"Dealer collects if dealer has blackjack")
        print(f"Continue checking players for blackjack")
        for player in self.seats:
            if player != [] and player.is_active:
                if player.hand_value == 21:
                    player.has_blackjack(self)
    
    def dealer_collects_or_pays_out(self):
        print("dealer_collects_or_pays_out")
        if 17 <= self.dealer.hand_value <= 21:
            print(f"Dealer has {self.dealer.hand_value}")
            for player in self.seats:
                if player != [] and player.is_active:
                    if player.hand_value > 21:
                        player.breaks(self)
                    elif player.hand_value == self.dealer.hand_value:
                        player.pushes(self)
                    elif player.hand_value > self.dealer.hand_value:
                        player.wins(self)
                        
    def players_decide_next_move(self):
            for player in self.seats:
                if player != [] and player.is_active:
                    if player == self.human_player:
                        player.human_player_next_play(self)
                    else:
                        player.play_basic_strategy()