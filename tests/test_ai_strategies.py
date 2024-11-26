import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from ai_strategies import get_strategic_move, evaluate, minimax, get_minimax_move, get_worst_move
from board import check_winner, check_draw

def test_evaluate():
    # Test winning state for player
    board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]  # Corrected spacing and commas
    player = "X"
    opponent = "O"
    size = 3
    assert evaluate(board, player, opponent, size) == 10

    # Test winning state for opponent
    board = ["O", "O", "O", " ", " ", " ", " ", " ", " "]  # Corrected spacing and commas
    player = "X"
    opponent = "O"
    size = 3
    assert evaluate(board, player, opponent, size) == -10

    # Test draw state
    board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]  # Corrected spacing and commas
    player = "X"
    opponent = "O"
    size = 3
    assert evaluate(board, player, opponent, size) == 0

def test_minimax():
    # Test minimax for a winning move
    board = ["X", "O", " ", "X", "O", " ", " ", " ", " "]  # Corrected spacing and commas
    depth = 0
    is_maximizing = True
    player = "X"
    opponent = "O"
    size = 3
    alpha = -float("inf")
    beta = float("inf")
    max_depth = 3
    assert minimax(board, depth, is_maximizing, player, opponent, size, alpha, beta, max_depth) == 10


def test_get_worst_move():
    # Test getting the worst move for the computer
    board = ["X", "O", " ", "X", "O", " ", " ", " ", " "]  # Corrected spacing and commas
    player = "X"
    size = 3
    assert get_worst_move(board, player, size) in [2, 6, 8]
