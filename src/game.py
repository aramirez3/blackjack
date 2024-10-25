from deck import *

class Game():
    def __init__(self, human_player, bots = 0):
        self.deck = None
        self.is_shuffled = False
        self.human_player = human_player
        self.number_of_bots = bots
        self.bot_players = []
        self.minimum_bet = 5
        if 0 < bots < 5:
            self._create_bot_players()
        
    def _create_bot_players(self):
        bots = []
        for _ in range(self.number_of_bots):
            player = Player()
            bots.append(player)
        self.bot_players.extend(bots)
    

class Player():
    def __init__(self):
        self.hand = []
        self.cash_money = 0
        