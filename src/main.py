from game import *
def main():
    game = Game()
    game.start_new_game()
    while game.state.game_is_active:
        print("game loop")
        game.place_bets()
        game.deal_cards(2)
        while game.state.hand_is_active:
            print("hand loop")
            game.print_player_hands()
            game.decide_next_round()
            game.update_game_status()
            input("restart hand loop (press enter to continue)")
        input("restart game loop (press enter to continue)")
    print("game over")
main()