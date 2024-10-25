import unittest
import sys
sys.path.append('src')

from src.constants import *
from deck import *


class TestTextNode(unittest.TestCase):
    def test_new_card(self):
        card = Card(Suits.HEARTS, Ranks.FIVE)
        self.assertEqual(card.suit, Suits.HEARTS)
        self.assertEqual(card.rank, Ranks.FIVE)
        self.assertEqual(card.value, 5)
        
    def test_new_deck(self):
        deck = Deck()
        self.assertEqual(len(deck.game_deck), 52*6)

if __name__ == "__main__":
    unittest.main()