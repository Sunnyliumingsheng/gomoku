from __future__ import annotations
from gomoku_ai.board import Board, Move, Stone
from gomoku_ai import ai

STONE_SYMBOLS = {
    Stone.EMPTY: ".",
    Stone.BLACK: "X",
    Stone.WHITE: "O",
}

PLAYER_NAMES = {
    Stone.BLACK: "Black(X)",
    Stone.WHITE: "White(O)",
}


def render_board(board: Board) -> str:
    width = len(str(board.size - 1))
    header = " " * (width + 1) + " ".join(f"{col:>{width}}" for col in range(board.size))
    rows = []

    for row in range(board.size):
        cells = " ".join(f"{STONE_SYMBOLS[board.stone_at(row, col)]:>{width}}" for col in range(board.size))
        rows.append(f"{row:>{width}} {cells}")

    return "\n".join([header, *rows])


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
    player_color = Stone.BLACK  # Default to Black
    ai_color=Stone.WHITE  # Default to White
    if choice == "W":
        player_color = Stone.WHITE
        ai_color = Stone.BLACK

    print("\n Select your opponent: A for random AI, B for a simple heuristic AI, or press Enter for random AI.")
    choice = input("Your choice: ").strip().upper()
    AI=ai.AI()
    if choice=="B":
        AI.AI_mode="heuristic"

    while not board.is_game_over():
        print(render_board(board))
        if board.current_player == ai_color:
            print(f"{PLAYER_NAMES[ai_color]} (AI) is thinking...")
            move = AI.select_move(board)
            board.play(move[0],move[1])
            continue

        player = PLAYER_NAMES[board.current_player]
        text = input(f"{player} move [row col]: ")

        try:
            row, col = parse_move(text)
            board.play(row, col)
        except ValueError as exc:
            print(f"Invalid move: {exc}")
            continue

    print(render_board(board))
    winner = board.winner()
    if winner is None:
        print("Draw.")
    else:
        print(f"{PLAYER_NAMES[winner]} wins.")


def main() -> None:
    run_game()


if __name__ == "__main__":
    main()
