import random
from board import check_winner, check_draw

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
    available_moves = [i for i, x in enumerate(board) if x == " "]
    
    # First, avoid any moves that would result in an immediate win
    non_winning_moves = []
    for move in available_moves:
        board_copy = board[:]
        board_copy[move] = player
        if not check_winner(board_copy, player, size):
            non_winning_moves.append(move)
    
    if not non_winning_moves:
        return random.choice(available_moves)
    
    # Among non-winning moves, prefer moves that allow opponent to win next turn
    worst_moves = []
    for move in non_winning_moves:
        board_copy = board[:]
        board_copy[move] = player
        # Check if opponent can win in their next move
        for opp_move in range(size * size):
            if board_copy[opp_move] == " ":
                board_copy_2 = board_copy[:]
                board_copy_2[opp_move] = opponent
                if check_winner(board_copy_2, opponent, size):
                    worst_moves.append(move)
                    break
    
    if worst_moves:
        return random.choice(worst_moves)
    
    # If no moves lead to opponent win, choose any non-winning move
    return random.choice(non_winning_moves)
