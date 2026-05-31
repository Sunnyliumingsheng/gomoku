from gomoku_ai import Board
from gomoku_ai import Stone
from gomoku_ai import Move

def find_winning_move(board:Board,player:Stone)->Move:
    for move in board.legal_moves():
        count=0
        directions=[(1,0),(0,1),(1,1),(1,-1)]
        for direction in directions:
            count=count_direction(board,player,move,direction)
            if count>=4:
                return move
            continue
    return None

def find_best_move(board:Board,player:Stone)->Move:
    best_score=-1
    best_move=None
    winning_move=find_winning_move(board,player)
    opponent_winning_move=find_winning_move(board,player.opponent)
    if winning_move is not None:
        return winning_move
    if opponent_winning_move is not None:
        return opponent_winning_move
    for move in board.legal_moves():
        score=evaluate_move(board,player,move)
        if score>best_score:
            best_score=score
            best_move=move
    return best_move
        

def evaluate_move(board:Board,player:Stone,move:Move)->Move:
    score=0
    # 优先选择防守
    defense_score=evaluate_stone(board,player.opponent,move)*1.1
    attack_score=evaluate_stone(board,player,move)
    center_score=get_center_score(board,move)
    return defense_score+attack_score+center_score

def evaluate_stone(board:Board,player:Stone,move:Move)->int:
    score=0
    directions=[(1,0),(0,1),(1,1),(1,-1)]
    for direction in directions:
        count=count_direction(board,player,move,direction)
        score+=count_score_list(count)
    return score


def count_direction(board:Board,player:Stone,move:Move,direction:tuple[int, int])->int:
    count=1
    positive_count=1
    negative_count=1
    #positive
    while(board.is_on_board(move[0]+positive_count*direction[0],move[1]+positive_count*direction[1]) and board.stone_at(move[0]+positive_count*direction[0],move[1]+positive_count*direction[1])==player):
        positive_count+=1
    #negative
    while(board.is_on_board(move[0]-negative_count*direction[0],move[1]-negative_count*direction[1]) and board.stone_at(move[0]-negative_count*direction[0],move[1]-negative_count*direction[1])==player):
        negative_count+=1
    count+=positive_count+negative_count-2
    return count

def get_center_score(board:Board,move:Move)->int:
    center=board.size/2
    distance=abs(center-move[0])+abs(center-move[1])
    return board.size-distance

def count_score_list(count:int)->int:
    if count==4:
        return 1000
    if count==3:
        return 100
    if count==2:
        return 10
    if count==1:
        return 1
    return 0