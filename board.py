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
