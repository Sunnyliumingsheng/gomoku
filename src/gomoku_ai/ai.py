import random
from gomoku_ai import Board
from gomoku_ai import Stone
from gomoku_ai.heuristic import find_best_move


class AI:
    def __init__(self):
        pass

    def select_move(self, board):
        if self.AI_mode=="random":
            move=self.random(board)
        if self.AI_mode=="heuristic":
            move=self.heuristic(board)
        return move
    
    AI_MODELES=["random", "heuristic"]
    AI_mode=AI_MODELES[0]

    def random(self, board):
        legal_moves = board.legal_moves()
        available_moves = len(legal_moves)
        if available_moves == 0:
            raise ValueError("no legal moves available")
        i = random.randint(0, available_moves - 1)
        return legal_moves[i]
    
    def heuristic(self, board:Board):
        return find_best_move(board,board.current_player)