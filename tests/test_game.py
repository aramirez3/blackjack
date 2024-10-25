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
        self.assertEqual(game.deck, [])
        self.assertNotEqual(game.dealer, None)
        self.assertEqual(game.minimum_bet, 5)
        self.assertEqual(len(game.seats), 5)
    
    def test_new_game_seats(self):
        player = Player()
        game = Game(player, 4)
        self.assertEqual(game.seats[player.seat_number], player)
        self.assertNotEqual(game.seats, [[]]*5)
        seated = {}
        seated[game.seats[0]] = True
        seated[game.seats[1]] = True
        seated[game.seats[2]] = True
        seated[game.seats[3]] = True
        seated[game.seats[4]] = True
        self.assertEqual(len(seated), 5)
        
    def test_bot_players(self):
        player = Player()
        game = Game(player, 2)
        self.assertEqual(len(game.bot_players), 2)
        self.assertNotEqual(game.bot_players[0], game.bot_players[1])
    
    def test_bot_players_invalid_values(self):
        player = Player()
        game = Game(player, -5)
        self.assertEqual(len(game.bot_players), 0)
        
    def test_shuff_deck(self):
        player = Player()
        new_deck = Deck()
        game = Game(player)
        game.shuffle_deck()
        self.assertNotEqual(game.deck[0], new_deck.game_deck[0])
        self.assertNotEqual(game.deck[1], new_deck.game_deck[1])
        self.assertNotEqual(game.deck[2], new_deck.game_deck[2])
        self.assertNotEqual(game.deck[3], new_deck.game_deck[3])
        self.assertNotEqual(game.deck[4], new_deck.game_deck[4])
    
    
        
if __name__ == "__main__":
    unittest.main()