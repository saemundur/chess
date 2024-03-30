from ChessEngine import Move as Move
from Resources.PieceSquareTables import PieceSquareTable

piceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
POSITION_SCORE_MULTIPLIER = 0.01
DEPTH = 3
PST = PieceSquareTable()


def find_random_move(valid_moves):
    print("Random move")
    return valid_moves[0]
    # return random.choice(valid_moves)


def find_best_move(gs, valid_moves, return_queue):
    global next_move
    next_move = None
    turn_multiplier = 1 if gs.white_to_move else -1
    find_move_negamax_alpha_beta(gs, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, turn_multiplier)
    return_queue.put(next_move)


def find_move_negamax_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * score_board(gs)

    # TODO Move ordering
    max_score = -CHECKMATE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_negamax_alpha_beta(
            gs, next_moves, depth - 1, -beta, -alpha, -turn_multiplier
        )
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
    return score_material(gs)


def score_material(gs):
    score = 0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            if square != "--":
                # Score material
                score_multiplier = 1 if square[0] == "w" else -1
                score += piceScore[square[1]] * score_multiplier
                # Score position
                score += (
                    PST.get_piece_position_score(
                        square[1], row, col, len(gs.move_log), gs.white_to_move
                    )
                    * POSITION_SCORE_MULTIPLIER * score_multiplier
                )
    final_score = score
    return final_score
