from game import *
def main():
    player = Player()
    game = Game(player)
    game.start_new_game()    
    print(game.deck[0].name)
main()