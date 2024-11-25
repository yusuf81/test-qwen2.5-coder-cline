import random
from ai_strategies import get_strategic_move, get_minimax_move, get_worst_move
from board import print_board, check_winner, check_draw


def get_player_move(board, size):
    """Gets a valid move from the player using zero-based indexing internally."""
    while True:
        try:
            move = input(f"Enter your move (1-{size*size}): ").strip()
            if move.isdigit() and 1 <= int(move) <= size * size:
                move = int(move) - 1
                if board[move] == " ":
                    return move
                else:
                    print(f"Position {move + 1} is already taken. Try again.")
            else:
                print(
                    f"Invalid input. Please enter a number between 1 and {size*size}."
                )
        except ValueError:
            print("Please enter a valid number.")


def get_computer_move(board, strategy, player, size):
    """Gets a move for the computer based on the chosen strategy."""
    if strategy == "random":
        available_moves = [i for i, x in enumerate(board) if x == " "]
        return random.choice(available_moves)
    elif strategy == "strategic":
        return get_strategic_move(board, player, size)
    elif strategy == "minimax":
        return get_minimax_move(board, player, size)
    elif strategy == "worst":
        return get_worst_move(board, player, size)
    else:
        raise ValueError(
            "Invalid strategy. Choose 'random', 'strategic', 'minimax', or 'worst'."
        )


def switch_player(current_player):
    """Switches the current player."""
    return "O" if current_player == "X" else "X"


def initialize_game(size):
    """Initializes the game by setting up the board and choosing a starting player."""
    board = [" "] * (size * size)
    current_player = random.choice(["X", "O"])  # Randomly choose starting player
    return board, current_player


def play_game(board, current_player, strategy, size):
    """Plays the game loop."""
    while True:
        print_board(board, size)
        move = get_move(current_player, board, strategy, size)
        update_board(board, move, current_player)

        if check_winner(board, current_player, size):
            print_board(board, size)
            print(f"Player {current_player} wins!")
            break
        elif check_draw(board):
            print_board(board, size)
            print("It's a draw!")
            break

        current_player = switch_player(current_player)


def get_move(player, board, strategy, size):
    """Gets the move for the current player."""
    if player == "X":
        return get_player_move(board, size)
    else:
        return get_computer_move(board, strategy, player, size)


def update_board(board, move, player):
    """Updates the board with the player's move."""
    board[move] = player
    print(f"Move made by {player} at position {move + 1}")
