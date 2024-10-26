from game import *
def main():
    game = Game()
    game.start_new_game()
    while (game.is_active):
        print("game loop")
        game.place_bets()
        game.deal_cards()
        game.print_player_hands()
        game.update_game_status()
    print("game over")
main()