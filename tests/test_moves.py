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


def test_play_game(monkeypatch):
    """Test the play_game function with mocked moves and print statements."""
    size = 3
    strategy = "random"

    # Mock all print-related functions to do nothing
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: None)

    # Mock print_board to do nothing
    def mock_print_board(board, size):
        return

    monkeypatch.setattr("board.print_board", mock_print_board)

    # Mock check_winner to simulate a win condition
    def mock_check_winner(board, player, size):
        # Simulate a win for 'X' when center and adjacent cells are filled
        if player == "X":
            return board[4] == "X" and board[3] == "X" and board[5] == "X"
        return False

    monkeypatch.setattr("board.check_winner", mock_check_winner)

    # Mock check_draw to simulate a draw
    def mock_check_draw(board):
        return " " not in board

    monkeypatch.setattr("board.check_draw", mock_check_draw)

    # Win scenario
    def mock_get_move_win(player, board, strategy, size):
        win_moves = {
            "X": [4, 3, 5],  # Center and adjacent moves for 'X'
            "O": [1, 7, 0],  # Other moves
        }
        return win_moves[player].pop(0)

    monkeypatch.setattr("moves.get_move", mock_get_move_win)

    # Test win scenario
    board, current_player = initialize_game(size)
    play_game(board, current_player, strategy, size)

    # Verify win condition
    assert board[4] == "X"
    assert board[3] == "X"
    assert board[5] == "X"

    # Draw scenario
    def mock_get_move_draw(player, board, strategy, size):
        draw_moves = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        return draw_moves.pop(0)

    monkeypatch.setattr("moves.get_move", mock_get_move_draw)

    board, current_player = initialize_game(size)
    play_game(board, current_player, strategy, size)

    # Verify no winner and board is full
    assert " " not in board
