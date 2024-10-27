class Game_State():
    def __init__(self):
        self.game_is_active = True
        self.hand_is_active = True
        self.first_hand = True
        
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
        