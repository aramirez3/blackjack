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
    
    def deactivate(self):
        self.is_active = False
        
    def play_basic_strategy(self, game):
        print(f"basic strategy moves for {self.name}")
        while True:
            if len(self.hand) == 2 and self.hand[0].rank == self.hand[1].rank:
                self.basic_strategy_pairs(game)
            if self.soft_hand:
                self.basic_strategy_soft(game)
            else:
                self.basic_strategy_hard(game)
    
    def basic_strategy_soft(self, game):
        print("Player's hand contains one Ace card")
        pass
    
    def basic_strategy_hard(self, game):
        print("Player's hand contains no Aces")
        up_card = game.dealer.up_card
        while True:
            exit = False
            print(f"first_hand {game.state.first_hand}")
            print(f"hand value {self.hand_value}")
            input()
            
            if self.hand_value > 21:
                self.breaks(game)
                exit = True
                break
            elif self.hand_value >= 17:
                self.stay()
                exit = True
                break
            if up_card.value >= 7 or up_card.rank == Ranks.ACE:
                if 12 <= self.hand_value <= 16:
                    self.hit(game)
                    continue
                elif self.hand_value == 11:
                    if self.cash_money > self.current_bet:
                        if game.state.first_hand:
                            self.double_down(game)
                            return
                        else:
                            self.hit()
                            continue
                    else:
                        self.hit(game)
                        continue
                elif self.hand_value == 10:
                    if up_card.value == 10 or up_card.rank == Ranks.ACE:
                        self.hit(game)
                        continue
                else:
                    self.hit(game)
                    continue
            else:
                if 13 <= self.hand_value <= 17:
                    self.stay()
                    exit = True
                    break
                elif self.hand_value == 12:
                    if 4 <= up_card.value <= 6:
                        self.stay()
                        exit = True
                        break
                    else:
                        self.hit(game)
                        continue
                elif self.hand_value == 11:
                    if game.state.first_hand:
                        self.double_down(game)
                        exit = True
                        break
                    else:
                        self.hit()
                        continue
                elif self.hand_value == 10:
                    if 2<= up_card.value <= 9:
                        self.double_down(game)
                        exit = True
                        break
                    else:
                        self.hit(game)
                        continue
                elif self.hand_value == 9:
                    if 3 <= up_card.value <= 6:
                        if game.state.first_hand:
                            self.double_down(game)
                            exit = True
                            break
                        else:
                            self.hit()
                            continue
                else:
                    self.hit(game)
            print(f"first_hand {game.state.first_hand}")
            game.state.end_first_hand()
            print(f"first_hand {game.state.first_hand}")
            print(f"hand value {self.hand_value}")
            print(f"Exit loop? {exit}")
            input()
            if exit:
                return
                        
    
    def basic_strategy_pairs(self):
        pass
    
    def stay(self):
        print(f"{self.name} stays")
    
    def hit(self, game):
        card = game.draw_card(self)
        print(f"{self.name} draws {card.value} ({self.hand_value})")
    
    def double_down(self, game):
        print(f"{self.name} doubles down")
        self.cash_money -= self.current_bet
        self.hit(game)
    
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
                            card = game.draw_card(self)
                            print(f"Hit - card draw is {card.name}")
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

    def set_soft_status(self):
        self.soft_hand = True
    
    def pay_insurance_fee(self, game):
        fee = self.current_bet / 2
        self.cash_money -= fee
        game.state.insurance_collected[self] = fee

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
        