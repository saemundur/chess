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
    if len(self.move_log) != 0:
      move = self.move_log.pop()
      self.board[move.start_row][move.start_col] = move.piece_moved
      self.board[move.end_row][move.end_col] = move.piece_captured
      self.white_to_move = not self.white_to_move
    pass

  def get_valid_moves(self):
    return self.get_all_possible_moves()
    # Get a list of valid moves in the current game state
    pass

  def get_all_possible_moves(self):
    # Get a list of all possible moves in the current game state
    moves = []
    for r in range(len(self.board)):
      for c in range(len(self.board[r])):
        turn = self.board[r][c][0]
        if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
          piece = self.board[r][c][1]
          if piece == "P":
            self.get_pawn_moves(r, c, moves)
          elif piece == "R":
            self.get_rook_moves(r, c, moves)
          elif piece == "N":
            self.get_knight_moves(r, c, moves)
          elif piece == "B":
            self.get_bishop_moves(r, c, moves)
          elif piece == "Q":
            self.get_queen_moves(r, c, moves)
          elif piece == "K":
            self.get_king_moves(r, c, moves)
    return moves

  def get_pawn_moves(self, r, c, moves):
    # Get a list of valid pawn moves
    if self.white_to_move and r >= 1:
      if self.board[r-1][c] == "--":
        moves.append(Move((r, c), (r-1, c), self.board))
        if r == 6 and self.board[r-2][c] == "--":
          moves.append(Move((r, c), (r-2, c), self.board))
      if c-1 >= 0:
        if self.board[r-1][c-1][0] == "b":
          moves.append(Move((r, c), (r-1, c-1), self.board))
      if c+1 <= 7:
        if self.board[r-1][c+1][0] == "b":
          moves.append(Move((r, c), (r-1, c+1), self.board))
    elif not self.white_to_move and r <= 6:
      if self.board[r+1][c] == "--":
        moves.append(Move((r, c), (r+1, c), self.board))
        if r == 1 and self.board[r+2][c] == "--":
          moves.append(Move((r, c), (r+2, c), self.board))
      if c-1 >= 0:
        if self.board[r+1][c-1][0] == "w":
          moves.append(Move((r, c), (r+1, c-1), self.board))
      if c+1 <= 7:
        if self.board[r+1][c+1][0] == "w":
          moves.append(Move((r, c), (r+1, c+1), self.board))
    return moves

  def get_rook_moves(self, r, c, moves):
    # Get a list of valid rook moves
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
    for d in directions:
      for i in range(1, 8):
        end_row = r + d[0]*i
        end_col = c + d[1]*i
        if 0 <= end_row < 8 and 0 <= end_col < 8:
          end_piece = self.board[end_row][end_col]
          if end_piece == "--":
            moves.append(Move((r, c), (end_row, end_col), self.board))
          elif end_piece[0] != self.board[r][c][0]:
            moves.append(Move((r, c), (end_row, end_col), self.board))
            break
          else:
            break
    return moves
  
  def get_knight_moves(self, r, c, moves):
    # Get a list of valid knight moves
    directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
    for d in directions:
      end_row = r + d[0]
      end_col = c + d[1]
      if 0 <= end_row < 8 and 0 <= end_col < 8:
        end_piece = self.board[end_row][end_col]
        if end_piece == "--" or end_piece[0] != self.board[r][c][0]:
          moves.append(Move((r, c), (end_row, end_col), self.board))
    return moves
  
  def get_bishop_moves(self, r, c, moves):
    # Get a list of valid bishop moves
    directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    for d in directions:
      for i in range(1, 8):
        end_row = r + d[0]*i
        end_col = c + d[1]*i
        if 0 <= end_row < 8 and 0 <= end_col < 8:
          end_piece = self.board[end_row][end_col]
          if end_piece == "--":
            moves.append(Move((r, c), (end_row, end_col), self.board))
          elif end_piece[0] != self.board[r][c][0]:
            moves.append(Move((r, c), (end_row, end_col), self.board))
            break
          else:
            break
    return moves
  
  def get_queen_moves(self, r, c, moves):
    # Get a list of valid queen moves
    self.get_rook_moves(r, c, moves)
    self.get_bishop_moves(r, c, moves)
    return moves
  
  def get_king_moves(self, r, c, moves):
    # Get a list of valid king moves
    directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for d in directions:
      end_row = r + d[0]
      end_col = c + d[1]
      if 0 <= end_row < 8 and 0 <= end_col < 8:
        end_piece = self.board[end_row][end_col]
        if end_piece == "--" or end_piece[0] != self.board[r][c][0]:
          moves.append(Move((r, c), (end_row, end_col), self.board))
    return moves
  
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
    self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

  def __eq__(self, other):
    if isinstance(other, Move):
      return self.move_id == other.move_id
    return False

  def get_chess_notation(self):
    return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
  
  def get_rank_file(self, r, c):
    return self.cols_to_file[c] + self.rows_to_rank[r]