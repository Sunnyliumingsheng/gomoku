from __future__ import annotations

from dataclasses import dataclass

from tqdm import tqdm

from gomoku_ai import Board, Move, Stone
from gomoku_ai.ai import AI


@dataclass
class MatchResult:
    winner: Stone | None
    moves_played: int


@dataclass
class EvaluationResult:
    black_wins: int = 0
    white_wins: int = 0
    draws: int = 0
    total_moves: int = 0

    @property
    def games(self) -> int:
        return self.black_wins + self.white_wins + self.draws

    @property
    def average_moves(self) -> float:
        if self.games == 0:
            return 0.0
        return self.total_moves / self.games


class FixedMovePlayer:
    def __init__(self, moves: list[Move]) -> None:
        self.moves = moves
        self.index = 0

    def select_move(self, board: Board) -> Move:
        if self.index >= len(self.moves):
            raise ValueError("fixed player has no moves left")
        move = self.moves[self.index]
        self.index += 1
        return move


def create_ai(mode: str) -> AI:
    player = AI()
    player.AI_mode = mode
    return player


def play_match(black_player: object, white_player: object, size: int = 15) -> MatchResult:
    board = Board(size=size)
    players = {
        Stone.BLACK: black_player,
        Stone.WHITE: white_player,
    }
    moves_played = 0

    while not board.is_game_over():
        player = players[board.current_player]
        move = player.select_move(board)
        board.play(move[0], move[1])
        moves_played += 1

    return MatchResult(winner=board.winner(), moves_played=moves_played)


def evaluate_players(
    black_mode: str,
    white_mode: str,
    games: int = 100,
    size: int = 15,
    show_progress: bool = False,
) -> EvaluationResult:
    result = EvaluationResult()

    progress = tqdm(
        range(games),
        disable=not show_progress,
        desc=f"Black {black_mode} vs White {white_mode}",
    )
    for _ in progress:
        match = play_match(
            black_player=create_ai(black_mode),
            white_player=create_ai(white_mode),
            size=size,
        )
        result.total_moves += match.moves_played

        if match.winner == Stone.BLACK:
            result.black_wins += 1
        elif match.winner == Stone.WHITE:
            result.white_wins += 1
        else:
            result.draws += 1

        if show_progress:
            progress.set_postfix(
                black_wins=result.black_wins,
                white_wins=result.white_wins,
                draws=result.draws,
                avg_moves=f"{result.average_moves:.1f}",
            )

    return result


def main() -> None:
    black_mode = "heuristic"
    white_mode = "minimax"
    result = evaluate_players(black_mode, white_mode, games=20, show_progress=True)
    print(f"Black {black_mode} vs White {white_mode}")
    print(f"games: {result.games}")
    print(f"black wins: {result.black_wins}")
    print(f"white wins: {result.white_wins}")
    print(f"draws: {result.draws}")
    print(f"average moves: {result.average_moves:.1f}")


if __name__ == "__main__":
    main()
