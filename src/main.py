from game import *
def main():
    game = Game()
    game.start_new_game()
    while (game.is_active):
        print("game loop")
        game.place_bets()
        game.deal_cards(2)
        game.print_player_hands()
        game.decide_next_round()
        game.update_game_status()
        input("pause - restart loop")
    print("game over")
main()