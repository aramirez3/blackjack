from game import *
from constants import *

class Player():
    valid_moves = {
        "h": "Hit",
        "s": "Stay",
        "dd": "Double Down",
        "ss": "Split"
    }
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
            self.valid_moves["h"],
            self.valid_moves["s"],
            self.valid_moves["dd"]
        ]
        if len(self.hand) == 2:
            if self.hand[0].rank == self.hand[1].rank:
                available_moves.append(self.valid_moves["ss"])
        dealer_shows = f"{game.dealer.visible_hand_description} ({game.dealer.visible_value})"
        print(f"Dealer shows {dealer_shows}. Your hand is {self.hand_description} ({self.hand_value}).")
        while True:
            try:
                move = input(f"Next move? {', '.join(map(lambda x: f"{self.valid_moves[x].key}: {self.valid_moves[x].value}", available_moves))}: ")
                if move in self.valid_moves:
                    break
            except ValueError:
                print("Please enter one of the valid options")
                
        match move:
            case "h":
                print("Hit")
            case "s":
                print("Stay")
                return
            case "dd":
                print("Double Down")
            case "ss":
                print("Split")


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.visible_value = 0
        self.visible_hand_description = ""
        