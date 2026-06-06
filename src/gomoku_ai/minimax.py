from gomoku_ai import Board
from gomoku_ai import Stone
from gomoku_ai import Move
from gomoku_ai.heuristic import evaluate_move, evaluate_stone, find_winning_move

def minimax_find_best_move(board:Board,player:Stone)->Move:
    winning_move=find_winning_move(board,player)
    if winning_move is not None:
        return winning_move
    blocking_move=find_winning_move(board,player.opponent)
    if blocking_move is not None:
        return blocking_move

    max_score = float("-inf")
    best_move=None
    valuable_moves=top_candidate_moves(board,player,1,30)
    for move in valuable_moves:
        copy_board=board.copy()
        copy_board.play(move[0],move[1])
        mini_score=10000000
        for opponent_move in top_candidate_moves(copy_board,player.opponent,1,30):
            copy_copy_board=copy_board.copy()
            copy_copy_board.play(opponent_move[0],opponent_move[1])
            next_score=evaluate_position(copy_copy_board,player)
            mini_score=min(mini_score,next_score)
        if mini_score>max_score:
            max_score=mini_score
            best_move=move
    if best_move is None:
        raise ValueError("no minimax move found")
    return best_move

def top_candidate_moves(board:Board,player:Stone,limit:int,top:int)->list[Move]:
    candidate_moves=find_candidate_moves(board,limit)
    moves_list=[]
    for move in candidate_moves:
        move_score=evaluate_move(board,player,move)
        moves_list.append((move_score,move))
    moves_list.sort(key=lambda item: item[0], reverse=True)
    return [move for score, move in moves_list[:top]]


def evaluate_position(board:Board,player:Stone)->float:
    winner=board.winner()
    if winner==player:
        return 100000000
    if winner==player.opponent:
        return -100000000
    candidate_moves=find_candidate_moves(board,2)
    # 先评估自己的，也就是current player的情况，然后让自己的分数和减去对手的分数和。
    score=0
    opponent_score=0
    score_list=[]
    opponent_score_list=[]
    for move in candidate_moves:
        score_list.append(evaluate_stone(board,player,move))
        opponent_score_list.append(evaluate_stone(board,player.opponent,move))
    score_list.sort(reverse=True)
    opponent_score_list.sort(reverse=True)
    for i in range(min(5,len(score_list))):
        score+=score_list[i]
    for i in range(min(5,len(opponent_score_list))):
        opponent_score+=opponent_score_list[i]
    return score-opponent_score

def find_candidate_moves(board:Board,limit:int)->list[Move]:
    #先找到现在有的棋子的边界
    min_row=board.size
    max_row=-1
    min_col=board.size
    max_col=-1
    for row in range(board.size):
        for col in range(board.size):
            if board.grid[row][col]!=Stone.EMPTY:
                min_row=min(min_row,row)
                max_row=max(max_row,row)
                min_col=min(min_col,col)
                max_col=max(max_col,col)
    #返回在这个范围内的合法落子
    moves=[]
    for row in range(max(0,min_row-limit),min(board.size,max_row+limit+1)):
        for col in range(max(0,min_col-limit),min(board.size,max_col+limit+1)):
            if board.grid[row][col]==Stone.EMPTY:
                moves.append((row,col))
    if max_row==-1:
        #如果没有棋子了，就返回中心位置
        moves.append((board.size//2,board.size//2))
    return moves
