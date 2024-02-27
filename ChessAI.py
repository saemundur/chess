import random

piceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2


def find_random_move(valid_moves):
    return random.choice(valid_moves)

def find_best_move(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    # best_move = find_greediest_move(gs, valid_moves, turn_multiplier)
    # best_move = find_move_2l_minimax(gs, valid_moves, turn_multiplier)
    # best_move = find_move_rec_minimax(gs, valid_moves)
    # best_move = find_move_negamax(gs, valid_moves, DEPTH, turn_multiplier)
    best_move = find_move_negamax_alpha_beta(gs, valid_moves, DEPTH, turn_multiplier)
    return best_move

def find_move_2l_minimax(gs, valid_moves, turn_multiplier):
    opponent_minimax_score = CHECKMATE
    best_player_move = None
    random.shuffle(valid_moves) # Randomize the order of moves to prevent the AI from playing the same game every time
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
            score = find_move_rec_minimax_helper(gs, next_moves, depth-1, False)
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
            score = find_move_rec_minimax_helper(gs, next_moves, depth-1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score

def find_move_rec_minimax(gs, valid_moves):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
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
    random.shuffle(valid_moves)
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
        score = -negamax_helper(gs, next_moves, depth-1, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
    return max_score

def find_move_negamax_alpha_beta(gs, valid_moves, depth, turn_multiplier):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    negamax_alpha_beta_helper(gs, valid_moves, depth, turn_multiplier, -CHECKMATE, CHECKMATE)
    return next_move

def negamax_alpha_beta_helper(gs, valid_moves, depth, turn_multiplier, alpha, beta):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(gs)
    # Move ordering
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -negamax_alpha_beta_helper(gs, next_moves, depth-1, -turn_multiplier, -beta, -alpha)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

def score_board(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    return score_material(gs.board)

def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piceScore[square[1]]
            elif square[0] == 'b':
                score -= piceScore[square[1]]
    return score