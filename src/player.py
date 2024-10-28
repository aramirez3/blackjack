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
        self.split = None
        
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
        
    def reduce_player_money(self, amount):
        self.cash_money -= amount
        
    def increment_player_money(self, amount):
        self.cash_money += amount
        
    def increment_current_bet(self, amount):
        self.current_bet += amount
        
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
    
    def hit(self, game, take_hard_value=False):
        print(f"{self.name} hits")
        card = game.draw_card(self)
        hand_value_desc = self.hand_value
        if take_hard_value:
            self.take_hard_ace()
        else:
            if card.rank == Ranks.ACE:
                if self.soft_hand:
                    hand_value_desc = f"{self.hand_value} or {self.hand_value + 10}"
        print(f"{self.name} draws {card.name} ({hand_value_desc})")
    
    def double_down(self, game):
        print(f"{self.name} doubles down")
        self.hit(game, True)
        self.reduce_player_money(self.current_bet)
        self.end_current_turn()
        
    def split(self, game):
        print(f"{self.name} splits")
        self.reduce_player_money(self.current_bet)
        card1 = self.hand[0]
        card2 = self.hand[1]
        self.split = {
            "hands": [
                { 
                    "cards": [card1],
                    "value": card1.value
                },
                {
                    "cards": [card2],
                    "value": card2.value
                }
            ]
        }
        for hand in self.split.hands:
            cards = hand.cards
            current_value = hand.value
            first_card = game.deck.pop()
            cards.append(first_card)
            current_value += first_card
            print(f"{self.name} draws {first_card.name} ({current_value})")
            while True:
                try:
                    move = input("h = hit, s = stay")
                    if move == "h":
                        print(f"{self.name} hits")
                        card = game.deck.pop()
                        cards.append(card)
                        current_value += card
                    elif move == "s":
                        print(f"{self.name} stays")
                        break
                    if current_value > 21:
                        print(f"{self.name}'s split hand busts")
                        break
                except ValueError:
                    print("Please enter one of the valid options")
            
    
    def get_valid_moves(self, game):
        available_moves = [
            f"h = {self.valid_moves['h']}",
            f"s = {self.valid_moves['s']}",
        ]
        if len(self.hand) == 2:
            if self.hand[0].rank == self.hand[1].rank:
                available_moves.append(f"ss = {self.valid_moves['ss']}")
            if game.state.first_hand:
                available_moves.append(f"dd = {self.valid_moves['dd']}")
        return available_moves
                
    def human_player_next_play(self, game):
        dealer_shows = f"{game.dealer.visible_hand_description} ({game.dealer.visible_value})"
        print(f"Dealer shows {dealer_shows}. Your hand is {self.hand_description} ({self.hand_value}).")
        while True:
            available_moves = self.get_valid_moves(game)
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
                            self.split(game)
                            break
                    
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
        self.increment_player_money(self.current_bet)
        self.end_current_turn()
    
    def wins(self):
        print(f"{self.name} wins!")
        self.increment_player_money(self.current_bet * 2)
        self.end_current_turn()
        
    def has_blackjack(self):
        print(f"{self.name} has blackjack!")
        self.increment_player_money(self.current_bet * 3 / 2)
        self.end_current_turn()

    def set_soft_status(self):
        self.soft_hand = True
        
    def take_hard_ace(self):
        self.soft_hand = False
        self.hand_value += 10
    
    def pay_insurance_fee(self, game):
        fee = self.current_bet / 2
        self.reduce_player_money(fee)
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
        