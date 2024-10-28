# Blackjack

A text-based blackjack game! Card counts are tracked and the game's [hi-lo true count](https://en.wikipedia.org/wiki/Card_counting#Running_counts_versus_true_counts_in_balanced_counting_systems) is displayed during each bet. 

## Requirements
- Python3

## Run
```
./main.sh
```

## Game Rules

### Dealer
- Dealer stands on 17
- Dealer stands on soft 17

### Bots
- The bots will hit until 17

### Player
- Player sits at Seat #1 if a `seat_number` pref is not given. Meaning they will be the first to play each round.