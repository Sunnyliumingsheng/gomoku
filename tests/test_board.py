import pytest

from gomoku_ai.board import Board, Stone


def test_black_moves_first_then_turn_switches() -> None:
    board = Board()

    board.play(7, 7)

    assert board.stone_at(7, 7) == Stone.BLACK
    assert board.current_player == Stone.WHITE


def test_rejects_outside_move() -> None:
    board = Board()

    with pytest.raises(ValueError):
        board.play(-1, 0)


def test_rejects_occupied_move() -> None:
    board = Board()
    board.play(7, 7)

    with pytest.raises(ValueError):
        board.play(7, 7)


def test_horizontal_win() -> None:
    board = Board(size=9)

    for col in range(4):
        board.play(4, col)
        board.play(0, col)
    board.play(4, 4)

    assert board.winner() == Stone.BLACK
    assert board.is_game_over()


def test_vertical_win() -> None:
    board = Board(size=9)

    for row in range(4):
        board.play(row, 3)
        board.play(row, 0)
    board.play(4, 3)

    assert board.winner() == Stone.BLACK


def test_main_diagonal_win() -> None:
    board = Board(size=9)

    for index in range(4):
        board.play(index, index)
        board.play(index, 8)
    board.play(4, 4)

    assert board.winner() == Stone.BLACK


def test_anti_diagonal_win() -> None:
    board = Board(size=9)

    for index in range(4):
        board.play(index, 4 - index)
        board.play(index, 8)
    board.play(4, 0)

    assert board.winner() == Stone.BLACK


def test_legal_moves_only_include_empty_points() -> None:
    board = Board(size=5)
    board.play(1, 1)

    assert len(board.legal_moves()) == 24
    assert (1, 1) not in board.legal_moves()


def test_copy_is_independent() -> None:
    board = Board(size=9)
    board.play(4, 4)

    copied = board.copy()
    copied.play(4, 5)

    assert board.stone_at(4, 5) == Stone.EMPTY
    assert copied.stone_at(4, 5) == Stone.WHITE
