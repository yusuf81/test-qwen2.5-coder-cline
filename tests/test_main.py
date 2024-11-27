import sys
import os
# Tambahkan direktori root ke path Python agar bisa import modul board
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from main import get_strategy_and_size, main

def test_get_strategy_and_size_valid():
    with patch('sys.argv', ['main.py', 'random', '3']):
        strategy, size = get_strategy_and_size()
        assert strategy == 'random'
        assert size == 3

def test_get_strategy_and_size_invalid_strategy():
    with patch('sys.argv', ['main.py', 'invalid', '3']):
        try:
            get_strategy_and_size()
        except SystemExit as e:
            assert e.code == 1
        else:
            pytest.fail("SystemExit not raised")

def test_get_strategy_and_size_invalid_size():
    with patch('sys.argv', ['main.py', 'random', '2']):
        try:
            get_strategy_and_size()
        except SystemExit as e:
            assert e.code == 1
        else:
            pytest.fail("SystemExit not raised")

def test_get_strategy_and_size_missing_arguments():
    with patch('sys.argv', ['main.py']):
        try:
            get_strategy_and_size()
        except SystemExit as e:
            assert e.code == 1
        else:
            pytest.fail("SystemExit not raised")

@patch('main.initialize_game')
@patch('main.play_game')
def test_main_calls_initialize_and_play(mock_play, mock_init):
    with patch('sys.argv', ['main.py', 'random', '3']):
        mock_init.return_value = ([" "]*9, "X")  # Ensure initialize_game returns a tuple
        main()
        mock_init.assert_called_once_with(3)
        board, current_player = mock_init.return_value
        mock_play.assert_called_once_with(board, current_player, 'random', 3)
