from ChessEngine import Move as Move
from Resources.PieceSquareTables import PieceSquareTable

piceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
POSITION_SCORE_MULTIPLIER = 0
DEPTH = 1
PST = PieceSquareTable()


def find_move_2l_minimax(gs, valid_moves, turn_multiplier):
    opponent_minimax_score = CHECKMATE
    best_player_move = None
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponent_moves = gs.get_valid_moves()
        opponent_max_score = -CHECKMATE
        for opponent_move in opponent_moves:
            gs.make_move(opponent_move)
            if gs.checkmate:
                score = -turn_multiplier * CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turn_multiplier * score_board(gs)
            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()
        if opponent_max_score < opponent_minimax_score:
            opponent_minimax_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move


def find_move_rec_minimax_helper(gs, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return score_board(gs)
    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_rec_minimax_helper(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_rec_minimax_helper(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score


def find_move_rec_minimax(gs, valid_moves):
    global next_move
    next_move = None
    find_move_rec_minimax_helper(gs, valid_moves, DEPTH, True)
    return next_move


def find_greediest_move(gs, valid_moves, turn_multiplier):
    max_score = -CHECKMATE
    best_move = None
    for move in valid_moves:
        gs.make_move(move)
        if gs.checkmate:
            score = -turn_multiplier * CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = turn_multiplier * score_board(gs)
        if score > max_score:
            max_score = score
            best_move = move
        gs.undo_move()
    return best_move


def find_move_negamax(gs, valid_moves, depth, turn_multiplier):
    global next_move
    next_move = None
    negamax_helper(gs, valid_moves, depth, turn_multiplier)
    return next_move


def negamax_helper(gs, valid_moves, depth, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(gs)
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -negamax_helper(gs, next_moves, depth - 1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    return max_score

