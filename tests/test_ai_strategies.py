import sys
import os
# Tambahkan direktori root ke path Python agar bisa import modul board
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_strategies import get_strategic_move, get_minimax_move, get_worst_move

def test_get_strategic_move():
    board = ["X", "O", " ", "X", "O", " ", " ", " ", " "]
    player = "X"
    size = 3
    move = get_strategic_move(board, player, size)
    assert move in [2, 5, 6, 7, 8]

def test_get_minimax_move():
    board = ["X", "O", " ", "X", "O", " ", " ", " ", " "]
    player = "X"
    size = 3
    move = get_minimax_move(board, player, size)
    assert move in [2, 5, 6, 7, 8]

def test_get_worst_move():
    # Test getting the worst move for the computer
    board = ["X", "O", " ", "X", "O", " ", " ", " ", " "]  # Corrected spacing and commas
    player = "X"
    size = 3
    assert get_worst_move(board, player, size) in [2, 6, 8]
