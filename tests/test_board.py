import pytest
import sys
import os

# Tambahkan direktori root ke path Python agar bisa import modul board
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board import print_board, check_winner, check_draw

def test_print_board(capfd):
    """Menguji fungsi print_board"""
    board = [" "] * 9
    board[0] = "X"
    board[4] = "O"
    
    print_board(board, 3)
    out, _ = capfd.readouterr()
    
    expected_output = (
        "X |   | \n"
        "-----------\n"
        "  | O | \n"
        "-----------\n"
        "  |   | "
    )
    
    assert out.strip() == expected_output.strip()
    
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
    board_5x5 = [" "] * 25
    board_5x5[0] = board_5x5[6] = board_5x5[12] = board_5x5[18] = board_5x5[24] = "O"
    assert check_winner(board_5x5, "O", 5) == True