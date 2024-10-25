from game import *
def main():
    game = Game()
    game.start_new_game()    
    print(game.deck[0].name)
main()