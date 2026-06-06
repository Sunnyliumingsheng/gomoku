import random
from gomoku_ai import Board
from gomoku_ai.heuristic import heuristic_find_best_move
from gomoku_ai.minimax import minimax_find_best_move
from gomoku_ai import Move


class AI:
    def __init__(self):
        pass

    def select_move(self, board):
        if self.AI_mode=="random":
            move=self.random(board)
        if self.AI_mode=="heuristic":
            move=self.heuristic(board)
        if self.AI_mode=="minimax":
            move=self.minimax(board)
        return move
    
    AI_MODELES=["random", "heuristic","minimax"]
    AI_mode=AI_MODELES[0]

    def random(self, board):
        legal_moves = board.legal_moves()
        available_moves = len(legal_moves)
        if available_moves == 0:
            raise ValueError("no legal moves available")
        i = random.randint(0, available_moves - 1)
        return legal_moves[i]
    
    def heuristic(self, board:Board):
        return heuristic_find_best_move(board,board.current_player)
    
    def minimax(self,board:Board)->Move:
        return minimax_find_best_move(board,board.current_player)
