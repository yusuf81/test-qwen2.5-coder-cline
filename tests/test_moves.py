import sys
import os

# Tambahkan direktori root ke path Python agar bisa import modul board
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from moves import (
    switch_player,
    initialize_game,
    get_player_move,
    get_computer_move,
    get_move,
    update_board,
    play_game,
)
from board import print_board, check_winner, check_draw


def test_switch_player():
    assert switch_player("X") == "O"
    assert switch_player("O") == "X"


def test_initialize_game():
    board, player = initialize_game(3)
    assert len(board) == 9
    assert all(cell == " " for cell in board)
    assert player in ["X", "O"]


def test_get_player_move(monkeypatch):
    # Mock user input to return '5'
    monkeypatch.setattr("builtins.input", lambda _: "5")
    move = get_player_move([" "] * 9, 3)
    assert move == 4

    # Mock user input to return an invalid input and then a valid one
    inputs = iter(["a", "10", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    move = get_player_move([" "] * 9, 3)
    assert move == 4


def test_get_computer_move():
    board = ["X", "O", " ", " ", " ", " ", " ", " ", " "]
    strategy = "random"
    player = "O"
    size = 3
    move = get_computer_move(board, strategy, player, size)
    assert move in [2, 3, 4, 5, 6, 7, 8]

    strategy = "strategic"
    move = get_computer_move(board, strategy, player, size)
    # Assuming strategic move logic is correct, we can't predict the exact move but it should be valid
    assert board[move] == " "

    strategy = "minimax"
    move = get_computer_move(board, strategy, player, size)
    # Similarly, minimax move logic is assumed to be correct
    assert board[move] == " "

    strategy = "worst"
    move = get_computer_move(board, strategy, player, size)
    # Worst move logic is assumed to be correct
    assert board[move] == " "


def test_get_move(monkeypatch):
    board = ["X", "O", " ", " ", " ", " ", " ", " ", " "]
    player = "X"
    strategy = "random"
    size = 3

    # Mock user input to return '5'
    monkeypatch.setattr("builtins.input", lambda _: "5")
    move = get_move(player, board, strategy, size)
    assert move == 4

    # Test computer move with random strategy
    player = "O"
    move = get_move(player, board, strategy, size)
    assert move in [2, 3, 4, 5, 6, 7, 8]


def test_update_board():
    board = [" "] * 9
    move = 4
    player = "X"
    update_board(board, move, player)
    assert board[move] == player

    # Test updating another position
    move = 0
    player = "O"
    update_board(board, move, player)
    assert board[move] == player
