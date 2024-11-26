import random
import sys


def print_board(board, size):
    """Prints the current state of the board."""
    for i in range(size):
        row = " | ".join(board[i * size : (i + 1) * size])
        print(row)
        if i < size - 1:
            print("-" * (size * 4 - 3))


def check_winner(board, player, size):
    """Checks if the given player has won."""
    return (
        any(
            all(board[i * size + j] == player for j in range(size)) for i in range(size)
        )
        or any(
            all(board[i * size + j] == player for i in range(size)) for j in range(size)
        )
        or all(board[i * size + i] == player for i in range(size))
        or all(board[i * size + (size - 1 - i)] == player for i in range(size))
    )


def check_draw(board):
    """Checks if the game is a draw."""
    return " " not in board


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


def get_strategic_move(board, player, size):
    """Gets a strategic move for the computer to block opponent or win."""
    opponent = "O" if player == "X" else "X"

    # Check for winning moves
    for i in range(size * size):
        if board[i] == " ":
            board_copy = board[:]
            board_copy[i] = player
            if check_winner(board_copy, player, size):
                return i

    # Block opponent's winning move
    for i in range(size * size):
        if board[i] == " ":
            board_copy = board[:]
            board_copy[i] = opponent
            if check_winner(board_copy, opponent, size):
                return i

    # Choose a random corner or center if available
    corners = [0, size - 1, (size - 1) * size, size * size - 1]
    for corner in corners:
        if board[corner] == " ":
            return corner

    if board[size // 2 * size + size // 2] == " " and size % 2 == 1:
        return size // 2 * size + size // 2

    # Choose any remaining edge
    edges = []
    for i in range(size):
        edges.append(i)  # Top row
        edges.append((size - 1) * size + i)  # Bottom row
        edges.append(i * size)  # Left column
        edges.append(i * size + (size - 1))  # Right column

    for edge in edges:
        if board[edge] == " ":
            return edge


def evaluate(board, player, opponent, size):
    """Evaluates the board state."""
    if check_winner(board, player, size):
        return 10
    elif check_winner(board, opponent, size):
        return -10
    else:
        return 0


def minimax(
    board, depth, is_maximizing, player, opponent, size, alpha, beta, max_depth
):
    """
    Implements the minimax algorithm with alpha-beta pruning and depth limiting.

    This function recursively evaluates all possible moves to determine the best move for the current player.
    It uses alpha-beta pruning to reduce the number of nodes evaluated in the game tree, improving efficiency.
    The `max_depth` parameter limits the search depth to prevent excessive computation time on larger boards.
    """
    if check_winner(board, player, size):
        return 10
    if check_winner(board, opponent, size):
        return -10
    if check_draw(board) or depth == max_depth:
        return evaluate(board, player, opponent, size)

    if is_maximizing:
        best_score = -float("inf")
        for i in range(size * size):
            if board[i] == " ":
                board_copy = board[:]
                board_copy[i] = player
                score = minimax(
                    board_copy,
                    depth + 1,
                    False,
                    player,
                    opponent,
                    size,
                    alpha,
                    beta,
                    max_depth,
                )
                board_copy[i] = " "
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float("inf")
        for i in range(size * size):
            if board[i] == " ":
                board_copy = board[:]
                board_copy[i] = opponent
                score = minimax(
                    board_copy,
                    depth + 1,
                    True,
                    player,
                    opponent,
                    size,
                    alpha,
                    beta,
                    max_depth,
                )
                board_copy[i] = " "
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_score


def get_minimax_move(board, player, size):
    """Gets the move for the computer using the minimax algorithm with alpha-beta pruning and depth limiting."""
    opponent = "O" if player == "X" else "X"
    best_score = -float("inf")
    best_move = None
    alpha = -float("inf")
    beta = float("inf")
    max_depth = 3  # Set a reasonable maximum depth for larger boards
    for i in range(size * size):
        if board[i] == " ":
            board_copy = board[:]
            board_copy[i] = player
            score = minimax(
                board_copy, 0, False, player, opponent, size, alpha, beta, max_depth
            )
            board_copy[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move


def get_worst_move(board, player, size):
    """Gets the worst move for the computer to ensure a loss."""
    opponent = "O" if player == "X" else "X"

    # Avoid moves that are part of potential win conditions for the opponent
    available_moves = [i for i, x in enumerate(board) if x == " "]
    worst_moves = []

    for move in available_moves:
        is_worst = True
        for i in range(size * size):
            if board[i] == opponent and board[move] == " ":
                board_copy = board[:]
                board_copy[move] = player
                if check_winner(board_copy, opponent, size):
                    is_worst = False
                    break
        if is_worst:
            worst_moves.append(move)

    if worst_moves:
        return random.choice(worst_moves)
    else:
        # If no such move exists, choose a random available move
        return random.choice(available_moves)


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


def get_strategy_and_size():
    """
    Gets the strategy and board size from command line arguments.

    Validates that exactly two arguments are provided:
    - The first argument is the strategy (random, strategic, minimax, worst).
    - The second argument is the board size (an integer >= 3).

    If validation fails, prints an error message and exits the program.
    """
    if len(sys.argv) != 3:
        print("Usage: python tic-tac-toe.py [strategy] [size]")
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


def main():
    strategy, size = get_strategy_and_size()
    board, current_player = initialize_game(size)
    play_game(board, current_player, strategy, size)


if __name__ == "__main__":
    main()
