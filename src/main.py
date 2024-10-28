from game import *
def main():
    game = Game()
    game.start_new_game()
    while game.state.game_is_active:
        print("game loop")
        game.place_bets()
        game.deal_cards()
        while game.state.hand_is_active:
            print("hand loop")
            game.print_player_hands()
            game.decide_next_round()
            game.update_game_status()
            input(f"Remaining chips: {game.human_player.cash_money} (press enter to continue)")
            game.start_next_round()
        input("restart game loop (press enter to continue)")
    print("game over")
main()