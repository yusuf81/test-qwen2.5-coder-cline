import sys
from board import print_board, check_winner, check_draw
from moves import (
    get_player_move,
    get_computer_move,
    switch_player,
    initialize_game,
    play_game,
)


def get_strategy_and_size():
    """
    Gets the strategy and board size from command line arguments.

    Validates that exactly two arguments are provided:
    - The first argument is the strategy (random, strategic, minimax, worst).
    - The second argument is the board size (an integer >= 3).

    If validation fails, prints an error message and exits the program.
    """
    if len(sys.argv) != 3:
        print("Usage: python main.py [strategy] [size]")
        print("Strategy options: random, strategic, minimax, worst")
        sys.exit(1)
    strategy = sys.argv[1]
    try:
        size = int(sys.argv[2])
        if size < 3:
            raise ValueError
    except ValueError:
        print("Invalid board size. Please enter an integer greater than or equal to 3.")
        sys.exit(1)
    return strategy, size


def main():
    strategy, size = get_strategy_and_size()
    board, current_player = initialize_game(size)
    play_game(board, current_player, strategy, size)


if __name__ == "__main__":
    main()
