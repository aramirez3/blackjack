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
        self.soft_hand = False
        self.current_bet = 0
        self.insurance_paid = 0
        
    def update_hand_description(self, game):
        if len(self.hand) >= 2:
            self.hand_description = ", ".join(map(lambda x: x.name, self.hand))
            if self == game.dealer:
                self.visible_hand_description = ", ".join(map(lambda x: x.name, self.hand[1:]))
                if game.state.first_hand:
                    self.up_card = self.hand[1]
    
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
    
    def end_current_turn(self):
        self.is_active = False
        
    def bot_player_next_play(self, game):
        while True:
            if self.hand_value > 21:
                self.breaks()
                break
            elif self.hand_value >= 17:
                self.stay()
                break
            elif 9 <= self.hand_value <= 11:
                self.double_down(game)
                break
            elif self.soft_hand:
                if self.hand_value + 10 <= 21:
                    self.take_hard_ace()
            else:
                self.hit(game)
    
    
    def basic_strategy_pairs(self):
        pass
    
    def stay(self):
        print(f"{self.name} stays")
    
    def hit(self, game):
        print(f"{self.name} hits")
        card = game.draw_card(self)
        hand_value_desc = self.hand_value
        if card.rank == Ranks.ACE:
            if self.soft_hand:
                hand_value_desc = f"{self.hand_value} or {self.hand_value + 10}"
        print(f"{self.name} draws {card.rank} ({hand_value_desc})")
    
    def double_down(self, game):
        print(f"{self.name} doubles down")
        self.hit(game)
        self.cash_money -= self.current_bet
        self.end_current_turn()
    
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
                            self.hit(game)
                        case "s":
                            self.stay()
                            break
                        case "dd":
                            self.double_down(game)
                            break
                        case "ss":
                            print("Split")
                    
                    if self.hand_value > 21:
                        self.breaks()
                        break
            except ValueError:
                print("Please enter one of the valid options")
                
    def loses_hand(self):
        print(f"{self.name} loses hand!")
        self.end_current_turn()
                  
    def breaks(self):
        print(f"{self.name} breaks!")
        self.end_current_turn()
        
    def pushes(self):
        print(f"{self.name} pushes!")
        self.cash_money += self.current_bet
        self.end_current_turn()
    
    def wins(self):
        print(f"{self.name} wins!")
        print(f"cash before payout {self.cash_money}")
        print(f"current bet amount {self.current_bet}")
        self.cash_money += self.current_bet * 2
        print(f"cash after payout {self.cash_money}")
        self.end_current_turn()
        
    def has_blackjack(self):
        print(f"{self.name} has blackjack!")
        self.cash_money += (self.current_bet * 3 / 2)
        self.end_current_turn()

    def set_soft_status(self):
        self.soft_hand = True
        
    def take_hard_ace(self):
        self.soft_hand = False
        self.hand_value += 10
    
    def pay_insurance_fee(self, game):
        fee = self.current_bet / 2
        self.cash_money -= fee
        self.insurance_paid = fee
        
    def reset(self):
        self.hand = []
        self.hand_value = 0
        self.hand_description = ""
        self.is_active = True
        self.soft_hand = False
        self.current_bet = 0
        self.insurance_paid = 0

class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.visible_value = 0
        self.visible_hand_description = ""
        self.up_card = None
        
    def dealer_shows_initial_ace(self):
        if self.hand[1].rank == Ranks.ACE:
            return True
        return False
    
    def has_blackjack(self):
        print("Checking for dealer blackjack")
        if self.hand_value == 21:
            print("Dealer has blackjack!")
            return True
        return False
    
    def makes_moves(self, game):
        while self.hand_value < 17:
            self.hit(game)
    
    def reset(self):
        self.hand = []
        self.hand_value = 0
        self.hand_description = ""
        self.is_active = True
        self.soft_hand = False
        self.current_bet = 0
        self.visible_value = 0
        self.visible_hand_description = ""
        self.up_card = None
        