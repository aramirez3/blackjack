from game import *
def main():
    game = Game()
    game.start_new_game()
    while (game.is_active):
        game.place_bets()
main()