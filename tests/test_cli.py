import pytest

from gomoku_ai.board import Board
from gomoku_ai.cli import parse_move, render_board


def test_parse_move_accepts_spaces() -> None:
    assert parse_move("7 8") == (7, 8)


def test_parse_move_accepts_comma() -> None:
    assert parse_move("7,8") == (7, 8)


def test_parse_move_rejects_wrong_shape() -> None:
    with pytest.raises(ValueError):
        parse_move("7")


def test_parse_move_rejects_non_integer() -> None:
    with pytest.raises(ValueError):
        parse_move("a b")


def test_render_board_shows_coordinates_and_stones() -> None:
    board = Board(size=5)
    board.play(2, 2)
    board.play(1, 3)

    assert render_board(board) == "\n".join(
        [
            "  0 1 2 3 4",
            "0 . . . . .",
            "1 . . . O .",
            "2 . . X . .",
            "3 . . . . .",
            "4 . . . . .",
        ]
    )


def test_render_board_can_highlight_last_move() -> None:
    board = Board(size=5)
    board.play(2, 2)
    board.play(1, 3)

    assert render_board(board, highlight_last_move=True) == "\n".join(
        [
            "  0 1 2 3 4",
            "0 . . . . .",
            "1 . . . o .",
            "2 . . X . .",
            "3 . . . . .",
            "4 . . . . .",
        ]
    )
