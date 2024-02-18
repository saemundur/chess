class GameState():
  def __init__(self):
    # Initialize the game state
    self.board = [
      ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    self.white_to_move = True
    self.move_log = []

  def make_move(self, move):
    self.board[move.start_row][move.start_col] = "--"
    self.board[move.end_row][move.end_col] = move.piece_moved
    self.move_log.append(move)
    self.white_to_move = not self.white_to_move
    
  def undo_move(self):
    # Undo the last move
    pass

  def get_valid_moves(self):
    # Get a list of valid moves in the current game state
    pass

  def is_checkmate(self):
    # Check if the game is in checkmate
    pass

  def is_stalemate(self):
    # Check if the game is in stalemate
    pass

  def is_draw(self):
    # Check if the game is a draw
    pass

  def evaluate(self):
    # Evaluate the current game state
    pass

  def get_best_move(self):
    # Get the best move for the current game state
    pass

class Move():
  # Maps keys to values
  rank_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
  rows_to_rank = {v: k for k, v in rank_to_rows.items()}
  file_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
  cols_to_file = {v: k for k, v in file_to_cols.items()}

  def __init__(self, start_sq, end_sq, board):
    self.start_row = start_sq[0]
    self.start_col = start_sq[1]
    self.end_row = end_sq[0]
    self.end_col = end_sq[1]
    self.piece_moved = board[self.start_row][self.start_col]
    self.piece_captured = board[self.end_row][self.end_col]

  def get_chess_notation(self):
    return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
  
  def get_rank_file(self, r, c):
    return self.cols_to_file[c] + self.rows_to_rank[r]