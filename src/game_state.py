from constants import *

class Game_State():
    def __init__(self):
        self.game_is_active = True
        self.hand_is_active = True
        self.first_hand = True
        self.running_count = 0
        self.true_count = 0
        self.insurance_collected = {}
        
    def start_game(self):
        self.game_is_active = True
        
    def end_game(self):
        self.game_is_active = False
        
    def start_hand(self):
        self.hand_is_active = True
        
    def end_hand(self):
        self.hand_is_active = False
        
    def set_first_hand(self):
        self.first_hand = True
        
    def end_first_hand(self):
        self.first_hand = False
        
    def count_card(self, card, game):
        if card.rank == Ranks.TWO or card.rank == Ranks.THREE or card.rank == Ranks.FOUR or card.rank == Ranks.FIVE:
            game.state.running_count += 1
        if card.rank == Ranks.ACE or card.rank == Ranks.JACK or card.rank == Ranks.QUEEN or card.rank == Ranks.KING:
            game.state.running_count -= 1
        game.state.true_count = round(game.state.running_count / (len(game.deck) / 52))
        print(f"running count: {game.state.running_count} / true count: {game.state.true_count}")