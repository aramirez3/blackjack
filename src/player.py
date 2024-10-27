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
            f"h = {self.valid_moves['h']}",
            f"s = {self.valid_moves['s']}",
            f"dd = {self.valid_moves['dd']}"
        ]
        if len(self.hand) == 2:
            if self.hand[0].rank == self.hand[1].rank:
                available_moves.append(f"ss = {self.valid_moves['ss']}")
        dealer_shows = f"{game.dealer.visible_hand_description} ({game.dealer.visible_value})"
        print(f"Dealer shows {dealer_shows}. Your hand is {self.hand_description} ({self.hand_value}).")
        while True:
            try:
                move = input(f"Next move? {', '.join(map(lambda x: x, available_moves))}: ")
                if move in self.valid_moves:
                    match move:
                        case "h":
                            card = game.deck.pop()
                            print(f"Hit - card draw is {card.name}")
                            self.update_hand(card)
                            print(f"Updated hand: {self.hand_description}")
                        case "s":
                            print("Stay")
                            break
                        case "dd":
                            print("Double Down")
                        case "ss":
                            print("Split")
                    
                    if self.hand_value > 21:
                        self.breaks(game)
                        break
            except ValueError:
                print("Please enter one of the valid options")
                
    def breaks(self, game):
        print(f"{self.name} breaks!")
        self.deactivate()
        
    def pushes(self, game):
        print(f"{self.name} pushes!")
        self.deactivate()
        print("return current pot amount to player")
    
    def wins(self, game):
        print(f"{self.name} wins!")
        self.deactivate()
        print("return current pot + match to player")
        
    def has_blackjack(self, game):
        print(f"{self.name} has blackjack!")
        self.deactivate
        print("Give bet back to player + 3/2 of bet amount")


class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.visible_value = 0
        self.visible_hand_description = ""
        