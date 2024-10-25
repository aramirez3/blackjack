from constants import Suits, Ranks

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.name = f"{rank} of {suit}"
        self.value = None
        self.ace = False
        self.soft_ace = False
        self._set_value()
        
    def _set_value(self):
        match (self.rank):
            case Ranks.ACE:
                if self.ace and not self.soft_ace:
                    self.value = 11
                else:
                    self.value = 1
            case Ranks.TWO:
                self.value = 2
            case Ranks.THREE:
                self.value = 3
            case Ranks.FOUR:
                self.value = 4
            case Ranks.FIVE:
                self.value = 5
            case Ranks.SIX:
                self.value = 6
            case Ranks.SEVEN:
                self.value = 7
            case Ranks.EIGHT:
                self.value = 8
            case Ranks.NINE:
                self.value = 9
            case Ranks.TEN:
                self.value = 10
            case Ranks.JACK:
                self.value = 10
            case Ranks.QUEEN:
                self.value = 10
            case Ranks.KING:
                self.value = 10
            case _:
                return

class Deck():
    def __init__(self):
        self.game_deck = []
        self._populate_deck()
    
    def _populate_deck(self):
        single_deck = []
        for suit in Suits:
            for rank in Ranks:
                single_deck.append(Card(suit, rank))
        self.game_deck = single_deck * 6