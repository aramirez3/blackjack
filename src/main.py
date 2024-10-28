from game import *
def main():
    game = Game()
    game.start_new_game()
    while game.state.game_is_active:
        print('++++++++++++++++++++++++++++')
        game.place_bets()
        game.deal_cards()
        while game.state.hand_is_active:
            print('++++++++++++++++++++++++++++')
            game.print_player_hands()
            game.decide_next_round()
            game.update_game_status()
            game._reset_game_state()
            print(f"Remaining chips: {game.human_player.cash_money}")
            break
        input("Press enter to continue")
    print("game over")
main()