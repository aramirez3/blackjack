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
        game = Game()
        self.assertEqual(game.human_player, None)
        self.assertEqual(game.bot_players, [])
        self.assertEqual(game.deck, [])
        self.assertEqual(game.dealer, None)
        self.assertEqual(game.minimum_bet, 5)
        self.assertEqual(len(game.seats), 5)
        
    def test_start_game(self):
        game = Game()
        game.start_new_game(3);
        self.assertNotEqual(game.dealer, None)
        self.assertNotEqual(game.human_player, None)
        self.assertNotEqual(game.bot_players, [])
        self.assertEqual(game.number_of_bots, 3)
    
    def test_new_game_seats(self):
        game = Game()
        game.start_new_game(4)
        self.assertNotEqual(game.seats, [[]]*5)
        seated = {}
        seated[game.seats[0]] = True
        seated[game.seats[1]] = True
        seated[game.seats[2]] = True
        seated[game.seats[3]] = True
        seated[game.seats[4]] = True
        self.assertEqual(len(seated), 5)
        player_seat_number = game.human_player.seat_number
        self.assertEqual(game.seats[player_seat_number], game.human_player)
        
    def test_bot_players(self):
        game = Game()
        game.start_new_game(2)
        self.assertEqual(len(game.bot_players), 2)
        self.assertNotEqual(game.bot_players[0], game.bot_players[1])
    
    def test_bot_players_invalid_values(self):
        game = Game()
        game.start_new_game(-5)
        self.assertEqual(len(game.bot_players), 0)
        
    def test_shuff_deck(self):
        new_deck = Deck()
        game = Game()
        game.shuffle_deck()
        self.assertNotEqual(game.deck[0], new_deck.game_deck[0])
        self.assertNotEqual(game.deck[1], new_deck.game_deck[1])
        self.assertNotEqual(game.deck[2], new_deck.game_deck[2])
        self.assertNotEqual(game.deck[3], new_deck.game_deck[3])
        self.assertNotEqual(game.deck[4], new_deck.game_deck[4])
    
    
        
if __name__ == "__main__":
    unittest.main()