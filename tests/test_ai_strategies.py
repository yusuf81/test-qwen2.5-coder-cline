import sys
import os
# Tambahkan direktori root ke path Python agar bisa import modul board
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_strategies import get_strategic_move, get_minimax_move, get_worst_move

def test_get_strategic_move_winning():
    # Test finding winning move for X
    board = ["X", "X", " ", 
             "O", "O", " ",
             " ", " ", " "]
    move = get_strategic_move(board, "X", 3)
    assert move == 2  # Complete winning row

    # Test finding winning move for O
    board = ["X", "X", " ",
             "O", "O", " ",
             " ", " ", " "]
    move = get_strategic_move(board, "O", 3)
    assert move == 5  # Block X's winning move

def test_get_strategic_move_blocking():
    # Test blocking opponent's winning move
    board = ["O", "O", " ",
             " ", "X", " ",
             " ", " ", "X"]
    move = get_strategic_move(board, "X", 3)
    assert move == 2  # Block O's winning move

    # Test blocking diagonal win
    board = ["O", " ", " ",
             " ", "O", " ",
             " ", " ", " "]
    move = get_strategic_move(board, "X", 3)
    assert move == 8  # Block O's diagonal win

def test_get_strategic_move_corners_and_center():
    # Test taking center when available
    board = [" "] * 9
    move = get_strategic_move(board, "X", 3)
    assert move in [0, 2, 4, 6, 8]  # Should take center or corner

    # Test taking corner when center is taken
    board = [" ", " ", " ",
             " ", "O", " ",
             " ", " ", " "]
    move = get_strategic_move(board, "X", 3)
    assert move in [0, 2, 6, 8]  # Should take a corner

def test_get_minimax_move_winning():
    # Test finding winning move
    board = ["X", "X", " ",
             "O", "O", " ",
             " ", " ", " "]
    move = get_minimax_move(board, "X", 3)
    assert move == 2  # Complete winning row

    # Test blocking opponent's winning move
    board = ["O", "O", " ",
             " ", "X", " ",
             " ", " ", "X"]
    move = get_minimax_move(board, "X", 3)
    assert move == 2  # Block O's winning move

def test_get_minimax_move_strategic():
    # Test early game move
    board = ["X", " ", " ",
             " ", " ", " ",
             " ", " ", "O"]
    move = get_minimax_move(board, "X", 3)
    # Any move that doesn't lead to a forced loss is valid
    assert move in range(9)
    assert board[move] == " "  # Ensure move is valid

    # Test as O player first move
    board = ["X", " ", " ",
             " ", " ", " ",
             " ", " ", " "]
    move = get_minimax_move(board, "O", 3)
    # First move should be strategic - either center or adjacent to X
    assert move in [1, 3, 4, 5]  # Adjacent to X or center

    # Test preventing fork
    board = ["X", " ", " ",
             " ", "O", " ",
             " ", " ", "X"]
    move = get_minimax_move(board, "O", 3)
    # Must block potential fork
    assert move in [1, 3, 5, 7]

def test_get_worst_move_avoid_winning():
    # Test avoiding immediate win
    board = ["X", "X", " ",
             "O", "O", " ",
             " ", " ", " "]
    move = get_worst_move(board, "X", 3)
    assert move != 2  # Should not take winning move

    # Test choosing move that allows opponent to win
    board = ["O", " ", " ",
             " ", "X", " ",
             " ", " ", "O"]
    move = get_worst_move(board, "X", 3)
    assert move in [1, 2, 3, 5, 6, 7]  # Should choose move that doesn't block O's win

def test_get_worst_move_different_players():
    # Test as O player
    board = ["X", " ", "X",
             " ", "O", " ",
             " ", " ", " "]
    move = get_worst_move(board, "O", 3)
    assert move != 1  # Should not block X's potential win

    # Test when no immediate losing moves available
    board = [" "] * 9
    move = get_worst_move(board, "X", 3)
    assert move in range(9)  # Should return any valid move

def test_strategic_move_different_board_sizes():
    # Test with 4x4 board
    board = [" "] * 16
    board[0] = "X"
    board[1] = "X"
    board[2] = "X"
    move = get_strategic_move(board, "O", 4)
    assert move == 3  # Block X's winning move

    # Test with empty 4x4 board
    board = [" "] * 16
    move = get_strategic_move(board, "X", 4)
    assert move in [0, 3, 12, 15]  # Should take a corner

def test_minimax_move_different_board_sizes():
    # Test with 4x4 board - blocking win
    board = [" "] * 16
    board[0] = "X"
    board[1] = "X"
    board[2] = "X"
    move = get_minimax_move(board, "O", 4)
    assert move == 3  # Block X's winning move

    # Test with 4x4 board - taking win
    board = [" "] * 16
    board[0] = "O"
    board[1] = "O"
    board[2] = "O"
    move = get_minimax_move(board, "O", 4)
    assert move == 3  # Complete winning row
