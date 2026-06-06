from __future__ import annotations
from gomoku_ai.board import Board, Move, Stone
from gomoku_ai import ai

STONE_SYMBOLS = {
    Stone.EMPTY: ".",
    Stone.BLACK: "X",
    Stone.WHITE: "O",
}

LAST_MOVE_SYMBOLS = {
    Stone.BLACK: "x",
    Stone.WHITE: "o",
}

PLAYER_NAMES = {
    Stone.BLACK: "Black(X)",
    Stone.WHITE: "White(O)",
}


def render_board(board: Board, highlight_last_move: bool = False) -> str:
    width = len(str(board.size - 1))
    header = " " * (width + 1) + " ".join(f"{col:>{width}}" for col in range(board.size))
    rows = []

    for row in range(board.size):
        cells = " ".join(
            f"{stone_symbol(board, row, col, highlight_last_move):>{width}}"
            for col in range(board.size)
        )
        rows.append(f"{row:>{width}} {cells}")

    return "\n".join([header, *rows])


def stone_symbol(board: Board, row: int, col: int, highlight_last_move: bool) -> str:
    stone = board.stone_at(row, col)
    if highlight_last_move and board.last_move == (row, col) and stone != Stone.EMPTY:
        return LAST_MOVE_SYMBOLS[stone]
    return STONE_SYMBOLS[stone]


def parse_move(text: str) -> Move:
    parts = text.strip().replace(",", " ").split()
    if len(parts) != 2:
        raise ValueError("please enter a move as: row col")

    try:
        row, col = (int(part) for part in parts)
    except ValueError as exc:
        raise ValueError("row and col must be integers") from exc

    return row, col


def run_game(size: int = 15) -> None:
    board = Board(size=size)

    print("Welcome to Gomoku!\nEnter B or W to choose your stone, or press Enter to play as Black (X).")
    choice = input("Your choice: ").strip().upper()
    ai_color=Stone.WHITE  # Default to White
    if choice == "W":
        ai_color = Stone.BLACK

    print(
        "\n Select your opponent: A for random AI, B for a simple heuristic AI, "
        "C for minimax AI, or press Enter for random AI."
    )
    choice = input("Your choice: ").strip().upper()
    AI=ai.AI()
    if choice=="B":
        AI.AI_mode="heuristic"
    if choice=="C":
        AI.AI_mode="minimax"

    while not board.is_game_over():
        print(render_board(board, highlight_last_move=True))
        if board.current_player == ai_color:
            print(f"{PLAYER_NAMES[ai_color]} (AI) is thinking...")
            move = AI.select_move(board)
            board.play(move[0],move[1])
            print(f"\n>>> {PLAYER_NAMES[ai_color]} (AI) played: {move[0]} {move[1]} <<<\n")
            continue

        player = PLAYER_NAMES[board.current_player]
        text = input(f"{player} move [row col]: ")

        try:
            row, col = parse_move(text)
            board.play(row, col)
        except ValueError as exc:
            print(f"Invalid move: {exc}")
            continue

    print(render_board(board, highlight_last_move=True))
    winner = board.winner()
    if winner is None:
        print("Draw.")
    else:
        print(f"{PLAYER_NAMES[winner]} wins.")


def main() -> None:
    run_game()


if __name__ == "__main__":
    main()
