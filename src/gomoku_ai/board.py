from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class Stone(IntEnum):
    EMPTY = 0
    BLACK = 1
    WHITE = -1

    @property
    def opponent(self) -> "Stone":
        if self == Stone.BLACK:
            return Stone.WHITE
        if self == Stone.WHITE:
            return Stone.BLACK
        raise ValueError("empty stone has no opponent")


Move = tuple[int, int]


@dataclass
class Board:
    size: int = 15
    win_length: int = 5
    grid: list[list[Stone]] = field(init=False)
    current_player: Stone = Stone.BLACK
    last_move: Move | None = None


    def __post_init__(self) -> None:
        if self.size < self.win_length:
            raise ValueError("board size must be at least win_length")
        self.grid = [[Stone.EMPTY for _ in range(self.size)] for _ in range(self.size)]

    def copy(self) -> "Board":
        copied = Board(size=self.size, win_length=self.win_length)
        copied.grid = [row[:] for row in self.grid]
        copied.current_player = self.current_player
        copied.last_move = self.last_move
        return copied

    def is_on_board(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def stone_at(self, row: int, col: int) -> Stone:
        if not self.is_on_board(row, col):
            raise ValueError(f"move is outside board: {(row, col)}")
        return self.grid[row][col]

    def legal_moves(self) -> list[Move]:
        return [
            (row, col)
            for row in range(self.size)
            for col in range(self.size)
            if self.grid[row][col] == Stone.EMPTY
        ]

    def is_legal_move(self, row: int, col: int) -> bool:
        return self.is_on_board(row, col) and self.grid[row][col] == Stone.EMPTY

    def play(self, row: int, col: int) -> None:
        if not self.is_legal_move(row, col):
            raise ValueError(f"illegal move: {(row, col)}")

        self.grid[row][col] = self.current_player
        self.last_move = (row, col)
        self.current_player = self.current_player.opponent

    def winner(self) -> Stone | None:
        if self.last_move is None:
            return None

        row, col = self.last_move
        stone = self.grid[row][col]
        if stone == Stone.EMPTY:
            return None

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for row_delta, col_delta in directions:
            count = 1
            count += self._count_direction(row, col, row_delta, col_delta, stone)
            count += self._count_direction(row, col, -row_delta, -col_delta, stone)
            if count >= self.win_length:
                return stone

        return None

    def is_full(self) -> bool:
        return all(stone != Stone.EMPTY for row in self.grid for stone in row)

    def is_game_over(self) -> bool:
        return self.winner() is not None or self.is_full()

    def _count_direction(
        self,
        row: int,
        col: int,
        row_delta: int,
        col_delta: int,
        stone: Stone,
    ) -> int:
        count = 0
        row += row_delta
        col += col_delta

        while self.is_on_board(row, col) and self.grid[row][col] == stone:
            count += 1
            row += row_delta
            col += col_delta

        return count
    
    # 输入坐标和假设在这个坐标中填入某个棋子，输出形成的连子数量
    def count_all_directions(self,row:int,col:int,stone: Stone)-> int:
        directions=[[1,0],[1,1],[0,1],[1,-1]]
        max_count=1
        for direction in (directions):
            count=1
            positive_count=1
            negative_count=1
            #positive
            while(self.is_on_board(row+positive_count*direction[0],col+positive_count*direction[1]) and self.stone_at(row+positive_count*direction[0],col+positive_count*direction[1])==stone):
                positive_count+=1
            while(self.is_on_board(row-negative_count*direction[0],col-negative_count*direction[1]) and self.stone_at(row-negative_count*direction[0],col-negative_count*direction[1])==stone):
                negative_count+=1
            count=positive_count+negative_count-1
            max_count=max(max_count,count)
        return max_count