import unittest
import sys
sys.path.append('src')

from game import *


class TestTextNode(unittest.TestCase):
    def test_new_player(self):
        player = Player()
        self.assertEqual(player.cash_money, 0)
        self.assertEqual(player.hand, [])
    
    def test_new_game(self):
        player = Player()
        game = Game(player)
        self.assertEqual(game.human_player, player)
        self.assertEqual(game.bot_players, [])
        self.assertEqual(game.deck, None)
        self.assertEqual(game.is_shuffled, False)
        self.assertEqual(game.minimum_bet, 5)
        
    def test_bot_players(self):
        player = Player()
        game = Game(player, 2)
        self.assertEqual(len(game.bot_players), 2)
        self.assertNotEqual(game.bot_players[0], game.bot_players[1])
    
    def test_bot_players_invalid_values(self):
        player = Player()
        game = Game(player, -5)
        self.assertEqual(len(game.bot_players), 0)
        
if __name__ == "__main__":
    unittest.main()