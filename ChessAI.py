import random

piceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0


def find_random_move(valid_moves):
    return random.choice(valid_moves)

def find_best_move(gs, valid_moves):
    turn_multiplier = 1 if gs.white_to_move else -1
    # best_move = find_greediest_move(gs, valid_moves, turn_multiplier)
    best_move = find_minimax_move(gs, valid_moves, turn_multiplier)
    return best_move

def find_minimax_move(gs, valid_moves, turn_multiplier):
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
                score = -turn_multiplier * score_material(gs.board)
            if score > opponent_max_score:
                opponent_max_score = score
            gs.undo_move()
        if opponent_max_score < opponent_minimax_score:
            opponent_minimax_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move



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
            score = turn_multiplier * score_material(gs.board)
        if score > max_score:
            max_score = score
            best_move = move
        gs.undo_move()
    return best_move

def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piceScore[square[1]]
            elif square[0] == 'b':
                score -= piceScore[square[1]]
    return score