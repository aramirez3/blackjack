from enum import Enum

class Enum_Helper(Enum):
    def __str__(self):
        return self.value

class Suits(Enum_Helper):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"
    
    
class Ranks(Enum_Helper):
    ACE = "Ace"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"
    
class PlayerMoves(Enum_Helper):
    HIT = "h = hit"
    STAY = "s = stay"
    DOUBLE_DOWN = "d = double down"
    SPLIT = "s = split"