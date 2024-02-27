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
    self.checkmate = False
    self.stalemate = False
    self.draw = False
    self.en_passant_possible = ()
    self.en_passant_possible_log = [self.en_passant_possible]
    self.castle_rights = CastleRights(True, True, True, True)
    self.castle_rights_log = [CastleRights(self.castle_rights.wks, self.castle_rights.bks, 
                                           self.castle_rights.wqs, self.castle_rights.bqs)]
    self.white_king_location = (7, 4)
    self.black_king_location = (0, 4)
    self.move_log = []
    self.pins = []
    self.checks = []
    self.move_functions = {
      "P": self.get_pawn_moves,
      "R": self.get_rook_moves,
      "N": self.get_knight_moves,
      "B": self.get_bishop_moves,
      "Q": self.get_queen_moves,
      "K": self.get_king_moves
    }

  def make_move(self, move):
    self.board[move.start_row][move.start_col] = "--"
    self.board[move.end_row][move.end_col] = move.piece_moved
    self.move_log.append(move)
    self.white_to_move = not self.white_to_move
    
    # Update the king's location
    if move.piece_moved == "wK":
      self.white_king_location = (move.end_row, move.end_col)
    elif move.piece_moved == "bK":
      self.black_king_location = (move.end_row, move.end_col)
    
    # Mark if en passant is possible
    if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
      self.en_passant_possible = ((move.start_row + move.end_row)//2, move.start_col)
    else:
      self.en_passant_possible = ()

    # Pawn promotion
    if move.is_pawn_promotion:
      # Assume the agent promotes to a queen
      self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"
      # # Ask the user what piece to promote the pawn to
      # promoted_piece = None
      # while promoted_piece not in ["Q", "R", "N", "B", "q", "r", "n", "b"]:
      #   promoted_piece = input("Enter a piece to promote the pawn to (Q, R, N, B): ")
      #   self.board[move.end_row][move.end_col] = move.piece_moved[0] + promoted_piece.capitalize()

    # Castle move
    if move.is_castle_move:
      if move.end_col - move.start_col == 2:
        # King side castle move
        self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1]
        self.board[move.end_row][move.end_col+1] = "--"
      else: 
        # Queen side castle move
        self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]
        self.board[move.end_row][move.end_col-2] = "--"

    # En passant capture
    if move.is_en_passant_move:
      self.board[move.start_row][move.end_col] = "--"
    
    # Update the en passant possible
    self.en_passant_possible_log.append(self.en_passant_possible)

    # Update the castle rights
    self.update_castle_rights(move)
    self.castle_rights_log.append(CastleRights(self.castle_rights.wks, self.castle_rights.bks, 
                                              self.castle_rights.wqs, self.castle_rights.bqs))

  def update_castle_rights(self, move):
    # Update the castle rights based on which piece is moved
    # Kings moved
    if move.piece_moved == "wK":
      self.castle_rights.wks = False
      self.castle_rights.wqs = False
    elif move.piece_moved == "bK":
      self.castle_rights.bks = False
      self.castle_rights.bqs = False
    # Rooks moved
    elif move.piece_moved == "wR":
      if move.start_row == 7:
        if move.start_col == 0:
          self.castle_rights.wqs = False
        elif move.start_col == 7:
          self.castle_rights.wks = False
    elif move.piece_moved == "bR":
      if move.start_row == 0:
        if move.start_col == 0:
          self.castle_rights.bqs = False
        elif move.start_col == 7:
          self.castle_rights.bks = False
    # Rook is captured
    if move.piece_captured == "wR":
      if move.end_row == 7:
        if move.end_col == 0:
          self.castle_rights.wqs = False
        elif move.end_col == 7:
          self.castle_rights.wks = False
    elif move.piece_captured == "bR":
      if move.end_row == 0:
        if move.end_col == 0:
          self.castle_rights.bqs = False
        elif move.end_col == 7:
          self.castle_rights.bks = False

    self.castle_rights_log.append(CastleRights(self.castle_rights.wks, self.castle_rights.bks, 
                                              self.castle_rights.wqs, self.castle_rights.bqs))

  def undo_move(self):
    # Undo the last move
    if len(self.move_log) != 0:
      move = self.move_log.pop()
      self.board[move.start_row][move.start_col] = move.piece_moved
      self.board[move.end_row][move.end_col] = move.piece_captured
      self.white_to_move = not self.white_to_move
      
      # Update the king's location
      if move.piece_moved == "wK":
        self.white_king_location = (move.start_row, move.start_col)
      elif move.piece_moved == "bK":
        self.black_king_location = (move.start_row, move.start_col)
      
      # Undo castle rights
      self.castle_rights_log.pop()
      new_rights = self.castle_rights_log[-1]
      self.castle_rights = CastleRights(new_rights.wks, new_rights.bks, new_rights.wqs, new_rights.bqs)
      
      # Undo en passant move
      if move.is_en_passant_move:
        self.board[move.end_row][move.end_col] = "--"
        self.board[move.start_row][move.end_col] = move.piece_captured

      self.en_passant_possible_log.pop()
      self.en_passant_possible = self.en_passant_possible_log[-1]

      # Undo a castle move
      if move.is_castle_move:
        if move.end_col - move.start_col == 2:
          self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
          self.board[move.end_row][move.end_col-1] = "--"
        else:
          self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
          self.board[move.end_row][move.end_col+1] = "--"
      
      self.checkmate = False
      self.stalemate = False

  def get_valid_moves(self):
    # Get a list of valid moves
    moves = []
    self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
    
    # Note king's location
    if self.white_to_move:
      king_row = self.white_king_location[0]
      king_col = self.white_king_location[1]
    else:
      king_row = self.black_king_location[0]
      king_col = self.black_king_location[1]
    
    # Which moves are legal are based on if the player is in check or not
    if self.in_check:
      if len(self.checks) == 1:
        # Single check, block the check or move the king
        moves = self.get_all_possible_moves()
        check = self.checks[0]
        check_row = check[0]
        check_col = check[1]
        piece_checking = self.board[check_row][check_col]
        valid_squares = []
        if piece_checking[1] == "N":
          valid_squares = [(check_row, check_col)]
        else:
          for i in range(1, 8):
            valid_square = (king_row + check[2]*i,
                            king_col + check[3]*i)
            valid_squares.append(valid_square)
            if valid_square[0] == check_row and valid_square[1] == check_col:
              break
        for i in range(len(moves)-1, -1, -1):
          if moves[i].piece_moved[1] != "K":
            if not (moves[i].end_row, moves[i].end_col) in valid_squares:
              moves.remove(moves[i])
      else:
        # Double check, the king has to move
        self.get_king_moves(king_row, king_col, moves)
    else:
      # Not in check, get all possible moves
      moves = self.get_all_possible_moves()
      if self.white_to_move:
        self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
      else:
        self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)
    
    # Check if the game is in checkmate or stalemate
    if len(moves) == 0:
      if self.in_check:
        self.checkmate = True
      else:
        self.stalemate = True
    return moves

  def get_all_possible_moves(self):
    moves = []
    # Scan every square on the board
    for r in range(len(self.board)):
      for c in range(len(self.board[r])):
        turn = self.board[r][c][0]
        # Identify the player's pieces
        if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
          piece = self.board[r][c][1]
          # Call the appropriate move function based on the piece type
          self.move_functions[piece](r, c, moves)
    return moves

  def get_pawn_moves(self, r, c, moves):
    # Update moves list with the valid pawn moves
    piece_pinned = False
    pin_direction = ()

    # Check if the pawn is pinned
    for i in range(len(self.pins)-1, -1, -1):
      if self.pins[i][0] == r and self.pins[i][1] == c:
        piece_pinned = True
        pin_direction = (self.pins[i][2], self.pins[i][3])
        self.pins.remove(self.pins[i])
        break
    
    # Get a list of valid pawn moves for white
    if self.white_to_move and r >= 1:
      # Move one square up
      if self.board[r-1][c] == "--":
        if not piece_pinned or pin_direction == (-1, 0):
          moves.append(Move((r, c), (r-1, c), self.board))
          # Move two squares up
          if r == 6 and self.board[r-2][c] == "--":
            moves.append(Move((r, c), (r-2, c), self.board))
      # Capture to the left
      if c-1 >= 0:
        if self.board[r-1][c-1][0] == "b":
          if not piece_pinned or pin_direction == (-1, -1):
            moves.append(Move((r, c), (r-1, c-1), self.board))
        elif (r-1, c-1) == self.en_passant_possible:
          moves.append(Move((r, c), (r-1, c-1), self.board, is_en_passant_move=True))
      # Capture to the right
      if c+1 <= 7:
        if self.board[r-1][c+1][0] == "b":
          if not piece_pinned or pin_direction == (-1, 1):
            moves.append(Move((r, c), (r-1, c+1), self.board))
        elif (r-1, c+1) == self.en_passant_possible:
          moves.append(Move((r, c), (r-1, c+1), self.board, is_en_passant_move=True))

    # Get a list of valid pawn moves for black
    elif not self.white_to_move and r <= 6:
      # Move one square down
      if self.board[r+1][c] == "--":
        if not piece_pinned or pin_direction == (1, 0):
          moves.append(Move((r, c), (r+1, c), self.board))
          # Move two squares down
          if r == 1 and self.board[r+2][c] == "--":
            moves.append(Move((r, c), (r+2, c), self.board))
      # Capture to the left
      if c-1 >= 0:
        if self.board[r+1][c-1][0] == "w":
          if not piece_pinned or pin_direction == (1, -1):
            moves.append(Move((r, c), (r+1, c-1), self.board))
        elif (r+1, c-1) == self.en_passant_possible:
          moves.append(Move((r, c), (r+1, c-1), self.board, is_en_passant_move=True))
      # Capture to the right
      if c+1 <= 7:
        if self.board[r+1][c+1][0] == "w":
          if not piece_pinned or pin_direction == (1, 1):
            moves.append(Move((r, c), (r+1, c+1), self.board))
        elif (r+1, c+1) == self.en_passant_possible:
          moves.append(Move((r, c), (r+1, c+1), self.board, is_en_passant_move=True))

  def get_rook_moves(self, r, c, moves):
    # Get a list of valid rook moves
    piece_pinned = False
    pin_direction = ()

    # Check if the rook is pinned
    for i in range(len(self.pins)-1, -1, -1):
      if self.pins[i][0] == r and self.pins[i][1] == c:
        piece_pinned = True
        pin_direction = (self.pins[i][2], self.pins[i][3])
        if self.board[r][c][1] != "Q":
          self.pins.remove(self.pins[i])
        break
    
    # Check rook moves in all four directions
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
    enemy_color = "b" if self.white_to_move else "w"
    for d in directions:
      for i in range(1, 8):
        end_row = r + d[0]*i
        end_col = c + d[1]*i
        # Check if the square is on the board
        if 0 <= end_row < 8 and 0 <= end_col < 8:
          # Piece can move if not pinned or moving in the direction of the pin 
          if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
            end_piece = self.board[end_row][end_col]
            if end_piece == "--":
              moves.append(Move((r, c), (end_row, end_col), self.board))
            elif end_piece[0] == enemy_color:
              # Capture enemy piece
              moves.append(Move((r, c), (end_row, end_col), self.board))
              break
            else:
              # Blocked by ally piece
              break
          else:
            # Pinned
            break

  def get_knight_moves(self, r, c, moves):
    # Get a list of valid knight moves
    piece_pinned = False
    # Check if knight is pinned
    for i in range(len(self.pins)-1, -1, -1):
      if self.pins[i][0] == r and self.pins[i][1] == c:
        piece_pinned = True
        self.pins.remove(self.pins[i])
        break
    
    # Check all eight knight moves      
    directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
    for d in directions:
      end_row = r + d[0]
      end_col = c + d[1]
      if 0 <= end_row < 8 and 0 <= end_col < 8:
        if not piece_pinned:
          end_piece = self.board[end_row][end_col]
          if end_piece == "--" or end_piece[0] != self.board[r][c][0]:
            moves.append(Move((r, c), (end_row, end_col), self.board))

  def get_bishop_moves(self, r, c, moves):
    # Get a list of valid bishop moves
    piece_pinned = False
    pin_direction = ()
    for i in range(len(self.pins)-1, -1, -1):
      if self.pins[i][0] == r and self.pins[i][1] == c:
        piece_pinned = True
        pin_direction = (self.pins[i][2], self.pins[i][3])
        self.pins.remove(self.pins[i])
        break
    
    # Check bishop moves in all four directions
    directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
    for d in directions:
      for i in range(1, 8):
        end_row = r + d[0]*i
        end_col = c + d[1]*i
        # Check if the square is on the board
        if 0 <= end_row < 8 and 0 <= end_col < 8:
          if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
            end_piece = self.board[end_row][end_col]
            if end_piece == "--":
              moves.append(Move((r, c), (end_row, end_col), self.board))
            elif end_piece[0] != self.board[r][c][0]:
              # Capture enemy piece
              moves.append(Move((r, c), (end_row, end_col), self.board))
              break
            else:
              # Blocked by ally piece
              break
          else:
            # Pinned
            break

  def get_queen_moves(self, r, c, moves):
    # Get a list of valid queen moves
    self.get_rook_moves(r, c, moves)
    self.get_bishop_moves(r, c, moves)

  def get_king_moves(self, r, c, moves):
    # Get a list of valid king moves
    row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
    col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
    ally_color = "w" if self.white_to_move else "b"

    for i in range(8):
      end_row = r + row_moves[i]
      end_col = c + col_moves[i]
      # Check if the square is on the board
      if 0 <= end_row < 8 and 0 <= end_col < 8:
        end_piece = self.board[end_row][end_col]
        if end_piece[0] != ally_color:
          if ally_color == "w":
            self.white_king_location = (end_row, end_col)
          else:
            self.black_king_location = (end_row, end_col)
          in_check, _, _ = self.check_for_pins_and_checks()
          if not in_check:
            moves.append(Move((r, c), (end_row, end_col), self.board))
          if ally_color == "w":
            self.white_king_location = (r, c)
          else:
            self.black_king_location = (r, c)

  def get_castle_moves(self, r, c, moves):
    if self.square_under_attack(r, c):
      return
    if (self.white_to_move and self.castle_rights.wks) or (not self.white_to_move and self.castle_rights.bks):
      self.get_king_side_castle_moves(r, c, moves)
    if (self.white_to_move and self.castle_rights.wqs) or (not self.white_to_move and self.castle_rights.bqs):
      self.get_queen_side_castle_moves(r, c, moves)
  
  def get_king_side_castle_moves(self, r, c, moves):
    if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
      if not self.square_under_attack(r, c+1) and not self.square_under_attack(r, c+2):
        moves.append(Move((r, c), (r, c+2), self.board, is_castle_move=True))
  
  def get_queen_side_castle_moves(self, r, c, moves):
    if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
      if not self.square_under_attack(r, c-1) and not self.square_under_attack(r, c-2):
        moves.append(Move((r, c), (r, c-2), self.board, is_castle_move=True))

  def square_under_attack(self, r, c):
    self.white_to_move = not self.white_to_move
    opp_moves = self.get_all_possible_moves()
    self.white_to_move = not self.white_to_move
    for move in opp_moves:
      if move.end_row == r and move.end_col == c:
        return True
    return False

  def check_for_pins_and_checks(self):
    pins = [] # Squares where piece is pinned and direction of pin
    checks = [] # Squares where the enemy is applying a check
    in_check = False
    if self.white_to_move:
      enemy_color = "b"
      ally_color = "w"
      start_row = self.white_king_location[0]
      start_col = self.white_king_location[1]
    else:
      enemy_color = "w"
      ally_color = "b"
      start_row = self.black_king_location[0]
      start_col = self.black_king_location[1]
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
    for j in range(len(directions)):
      d = directions[j]
      possible_pin = ()
      for i in range(1, 8):
        end_row = start_row + d[0]*i
        end_col = start_col + d[1]*i
        if 0 <= end_row < 8 and 0 <= end_col < 8:
          end_piece = self.board[end_row][end_col]
          if end_piece[0] == ally_color and end_piece[1] != "K":
            if possible_pin == ():
              # First allied piece could be pinned
              possible_pin = (end_row, end_col, d[0], d[1])
            else:
              # Second allied piece, so no pin or check from this direction
              break
          elif end_piece[0] == enemy_color:
            piece_type = end_piece[1]
            # 5 possibilities here for the attacking piece to cause a check
            # 1. Straight away from the king and the piece is a rook
            # 2. Diagonally away from the king and the piece is a bishop
            # 3. 1 square away from the king and the piece is a pawn
            # 4. Any direction and the piece is a queen
            # 5. Any direction 1 square away and the piece is a king
            if (0 <= j <= 3 and piece_type == "R") or \
              (4 <= j <= 7 and piece_type == "B") or \
              (i == 1 and piece_type == "P" and ((enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or \
              (piece_type == "Q") or \
              (i == 1 and piece_type == "K"):
              if possible_pin == ():
                # No piece blocking, so check
                checks.append((end_row, end_col, d[0], d[1]))
                in_check = True
                break
              else:
                # Piece is blocking, so pin
                pins.append(possible_pin)
                break
            else:
              # Enemy piece is not applying a check
              break
        else:
          # Off board
          break

    # All 8 knight moves
    knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
    # Check if the knight is attacking the king
    for m in knight_moves:
      end_row = start_row + m[0]
      end_col = start_col + m[1]
      if 0 <= end_row < 8 and 0 <= end_col < 8:
        end_piece = self.board[end_row][end_col]
        if end_piece[0] == enemy_color and end_piece[1] == "N":
          # The knight is attacking the king
          in_check = True
          checks.append((end_row, end_col, m[0], m[1]))
    
    return in_check, pins, checks

class CastleRights():
  def __init__(self, wks, bks, wqs, bqs):
    self.wks = wks
    self.bks = bks
    self.wqs = wqs
    self.bqs = bqs

class Move():
  # Maps keys to values
  rank_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
  rows_to_rank = {v: k for k, v in rank_to_rows.items()}
  file_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
  cols_to_file = {v: k for k, v in file_to_cols.items()}

  def __init__(self, start_sq, end_sq, board, is_en_passant_move=False, is_castle_move=False):
    self.start_row = start_sq[0]
    self.start_col = start_sq[1]
    self.end_row = end_sq[0]
    self.end_col = end_sq[1]
    self.piece_moved = board[self.start_row][self.start_col]
    self.piece_captured = board[self.end_row][self.end_col]
    self.is_pawn_promotion = (self.piece_moved == "wP" and self.end_row == 0) or (self.piece_moved == "bP" and self.end_row == 7)
    self.is_castle_move = is_castle_move
    self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
    self.is_en_passant_move = is_en_passant_move
    if is_en_passant_move:
      self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

  def __eq__(self, other):
    if isinstance(other, Move):
      return self.move_id == other.move_id
    return False

  def get_chess_notation(self):
    return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

  def get_rank_file(self, r, c):
    return self.cols_to_file[c] + self.rows_to_rank[r]