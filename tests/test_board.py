import pytest
import sys
import os

# Tambahkan direktori root ke path Python agar bisa import modul board
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board import print_board, check_winner, check_draw

def test_check_winner_horizontal():
    """Menguji kemenangan horizontal"""
    # Kemenangan horizontal pertama
    board1 = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
    assert check_winner(board1, "X", 3) == True
    assert check_winner(board1, "O", 3) == False

    # Kemenangan horizontal kedua
    board2 = [" ", " ", " ", "O", "O", "O", " ", " ", " "]
    assert check_winner(board2, "O", 3) == True
    assert check_winner(board2, "X", 3) == False

def test_check_winner_vertical():
    """Menguji kemenangan vertikal"""
    # Kemenangan vertikal pertama
    board1 = ["X", " ", " ", "X", " ", " ", "X", " ", " "]
    assert check_winner(board1, "X", 3) == True
    assert check_winner(board1, "O", 3) == False

    # Kemenangan vertikal ketiga
    board2 = [" ", " ", "O", " ", " ", "O", " ", " ", "O"]
    assert check_winner(board2, "O", 3) == True
    assert check_winner(board2, "X", 3) == False

def test_check_winner_diagonal():
    """Menguji kemenangan diagonal"""
    # Diagonal utama
    board1 = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
    assert check_winner(board1, "X", 3) == True
    assert check_winner(board1, "O", 3) == False

    # Diagonal terbalik
    board2 = [" ", " ", "O", " ", "O", " ", "O", " ", " "]
    assert check_winner(board2, "O", 3) == True
    assert check_winner(board2, "X", 3) == False

def test_check_draw():
    """Menguji kondisi draw"""
    # Board penuh tanpa pemenang
    board_draw = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
    assert check_draw(board_draw) == True

    # Board belum penuh
    board_not_draw = ["X", "O", "X", " ", "O", "O", "O", "X", "X"]
    assert check_draw(board_not_draw) == False

def test_check_winner_no_winner():
    """Menguji kondisi tidak ada pemenang"""
    board = [" "] * 9
    assert check_winner(board, "X", 3) == False
    assert check_winner(board, "O", 3) == False

def test_board_size_4x4():
    """Menguji fungsi dengan board ukuran 4x4"""
    board_4x4 = [" "] * 16
    board_4x4[0] = board_4x4[5] = board_4x4[10] = board_4x4[15] = "X"
    assert check_winner(board_4x4, "X", 4) == True

def test_board_size_5x5():
    """Menguji fungsi dengan board ukuran 5x5"""
    # Diagonal win
    board_5x5_diagonal = [" "] * 25
    board_5x5_diagonal[0] = board_5x5_diagonal[6] = board_5x5_diagonal[12] = board_5x5_diagonal[18] = board_5x5_diagonal[24] = "O"
    assert check_winner(board_5x5_diagonal, "O", 5) == True

    # Horizontal win
    board_5x5_horizontal = [" "] * 25
    for i in range(5):
        board_5x5_horizontal[i] = "X"
    assert check_winner(board_5x5_horizontal, "X", 5) == True

    # Vertical win
    board_5x5_vertical = [" "] * 25
    for i in range(0, 25, 5):
        board_5x5_vertical[i] = "O"
    assert check_winner(board_5x5_vertical, "O", 5) == True
