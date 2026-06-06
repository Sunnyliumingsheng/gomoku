from gomoku_ai import Stone
from gomoku_ai.match import FixedMovePlayer, evaluate_players, play_match


def test_play_match_returns_winner_and_move_count() -> None:
    black = FixedMovePlayer([(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])
    white = FixedMovePlayer([(1, 0), (1, 1), (1, 2), (1, 3)])

    result = play_match(black, white, size=5)

    assert result.winner == Stone.BLACK
    assert result.moves_played == 9


def test_evaluate_players_counts_requested_games() -> None:
    result = evaluate_players("random", "random", games=3, size=5)

    assert result.games == 3
    assert result.black_wins + result.white_wins + result.draws == 3
    assert result.average_moves > 0
