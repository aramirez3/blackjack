from random import randrange

from deck import *
from constants import *
from player import Player, Dealer
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
        
    def _create_bot_players(self, bots = None):
        if bots is None:
            bots = randrange(0,4)
        if bots > 0:
            self.number_of_bots = bots
            bots_list = []
            for i in range(bots):
                player = Player()
                player.name = f"Bot {i + 1}"
                player.cash_money = randrange(1,9) * 10 * self.minimum_bet
                bots_list.append(player)
                self.bot_players.extend(bots_list)
            print(f"{', '.join(map(lambda x: x.name, bots_list))} have joined your game")
        
    def _create_dealer(self):
        dealer = Dealer()
        dealer.name = "Dealer"
        self.dealer = dealer
        
    def _assign_seating(self):
        reserved_seat = self.human_player.seat_number
        self.seats[reserved_seat] = self.human_player
        bots_remaining = len(self.bot_players)
        if bots_remaining:
            while bots_remaining:
                seat_number = randrange(0, 5)
                if seat_number != reserved_seat and self.seats[seat_number] == []:
                    self.seats[seat_number] = self.bot_players[bots_remaining - 1]
                    bots_remaining -= 1
        self._remove_empty_seats()
                
    def _remove_empty_seats(self):
        seats = []
        for seat in self.seats:
            if seat != []:
                seats.append(seat)
        self.seats = seats
    
    def start_new_game(self):
        self._create_human_player()
        self._create_dealer()
        self.game_start_greeting()
        self._create_bot_players()
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
                    print(f"You now have {amount} worth of chips.")
                    break
                else:
                    print(validation_message)
            except ValueError:
                print(f"Invalid entry. {validation_message}")
        
    def place_bets(self):
        validation_message = f"Minimum bet is {self.minimum_bet} (True count {self.state.true_count})"
        while True:
            try:
                current_bet = float(input(f"Place your bet (min: {self.minimum_bet})[true count {self.state.true_count}]: "))
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
    
    def deal_cards(self):
        print("Dealing cards...")
        for _ in range(0, 2):
            for player in self.seats:
                player.activate(self)
                if player.is_active:
                    self.draw_card(player)
            self.draw_card(self.dealer)
    
    def draw_card(self, player):
        card = self.deck.pop()
        if card.rank == Ranks.ACE:
            player.set_soft_status()
        self.state.count_card(card, self)
        player.update_hand(card, self)
        return card
     
    def print_player_hands(self):
        for player in self.seats:
            if player != self.human_player:
                hand_value_desc = player.hand_value
                if player.soft_hand:
                    hand_value_desc = f"{player.hand_value} or {player.hand_value + 10}"
                print(f"--{player.name} shows {player.hand_description} ({hand_value_desc})")
        
        print(f"++Dealer's full hand = {self.dealer.hand_description}")
        if len(self.dealer.hand) > 2:
            print(f"++Dealer shows {self.dealer.visible_hand_description}")
        else:
            print(f"++Dealer shows {self.dealer.visible_hand_description}")
        
        hand_value_desc = self.human_player.hand_value
        if self.human_player.soft_hand:
            hand_value_desc = f"{self.human_player.hand_value} or {self.human_player.hand_value + 10}"
        print(f"Your hand: {self.human_player.hand_description} ({hand_value_desc})")

    def update_game_status(self):
        if not self.state.first_hand:
            for player in self.seats:
                if player.cash_money < self.minimum_bet:
                    if player == self.human_player:
                        print(f"Game over! The house ALWAYS wins!")
                        self.state.end_game
                        return
                    print(f"{player.name} has been eliminated!")
                    player.end_current_turn()
    
    def decide_next_round(self):
        if not self.state.first_hand:
            if self.dealer.hand_value < 17:
                self.players_make_moves()
                return
            else:
                self.dealer_collects_or_pays_out()
        else:
            self.check_for_blackjacks()
            self.players_make_moves()
            self.state.end_first_hand()
    
    def check_for_blackjacks(self):
        print("Checking for blackjacks")
        if self.dealer.dealer_shows_initial_ace():
            player_pays_insurance = self.request_insurance()
            if player_pays_insurance:
                self.human_player.pay_insurance_fee(self)
        
        dealer_has_blackjack = self.dealer.has_blackjack()
        
        if dealer_has_blackjack:
            for player in self.seats:
                if player.is_active:
                    if player.insurance_paid > 0:
                        player.cash_money += player.insurance_paid * 2
                    else:
                        player.loses_hand()
            print("reset the hand state")
            
        for player in self.seats:
            if player.is_active:
                if player.hand_value == 21:
                    player.has_blackjack()
                elif player.soft_hand and player.hand_value + 10 == 21:
                    player.has_blackjack()
    
    def request_insurance(self):
        while True:
            try:
                insurance = input("Dealer shows Ace! Insurance? Enter 'y' or 'n': ")
                if insurance == 'y':
                    return True
                elif insurance == 'n':
                    return False
            except ValueError:
                print("Plese enter 'y' or 'n'")
            
    
    def dealer_collects_or_pays_out(self):
        if self.dealer.hand_value > 21:
            for player in self.seats:
                if player.is_active:
                    player.wins()
        elif 17 <= self.dealer.hand_value <= 21:
            print(f"Dealer has {self.dealer.hand_value}")
            for player in self.seats:
                if player.hand_value > 21:
                    player.breaks()
                elif player.hand_value == self.dealer.hand_value:
                    player.pushes()
                elif player.hand_value > self.dealer.hand_value:
                    player.wins()
                elif player.hand_value < self.dealer.hand_value:
                    player.loses_hand()
        else:
            for player in self.seats:
                print(f"dealer collecting. dealer {self.dealer.hand_value} v {player.name} {player.hand_value}")
                # if player.is_active:
                #     player.hand_value += player.current_bet * 2
                        
    def players_make_moves(self):
        for player in self.seats:
            if player.is_active:
                if player == self.human_player:
                    player.human_player_next_play(self)
                else:
                    player.bot_player_next_play(self)
        self.dealer.makes_moves(self)
        self.dealer_collects_or_pays_out()
    
    def start_next_round(self):
        self._reset_game_state()
        self.place_bets()
        self.deal_cards()
    
    def _reset_game_state(self):
        self.state.first_hand = True
        for player in self.seats:
            player.reset()
        self.dealer.reset()