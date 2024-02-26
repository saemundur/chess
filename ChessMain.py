import pygame as p
import ChessEngine as CE
import ChessAI as AI
from pandas import *

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("icons/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def draw_game_state(screen, gs, sq_selected):
  draw_board(screen)
  draw_pieces(screen, gs.board)
  highlight_square(screen, gs, sq_selected)

def draw_board(screen):
  colors = [p.Color("white"), p.Color("light grey")]
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      color = colors[((r + c) % 2)]
      p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      piece = board[r][c]
      if piece != "--":
        screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlight_square(screen, gs, sq_selected):
  valid_moves = gs.get_valid_moves()
  if sq_selected != ():
    r, c = sq_selected
    if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
      # Highlight the selected square
      s = p.Surface((SQ_SIZE, SQ_SIZE))
      s.set_alpha(100) # Transparency value
      s.fill(p.Color("blue"))
      screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
      # Highlight the moves from that square
      s.fill(p.Color("yellow"))
      for move in valid_moves:
        if move.start_row == r and move.start_col == c:
          screen.blit(s, (move.end_col*SQ_SIZE, move.end_row*SQ_SIZE))

def main():
  p.init()
  screen = p.display.set_mode((WIDTH, HEIGHT))
  clock = p.time.Clock()
  screen.fill(p.Color("white"))
  gs = CE.GameState()
  valid_moves = gs.get_valid_moves()
  move_made = False # Flag variable for when a move is made

  load_images()
  running = True
  sq_selected = () # No square is selected, keep track of the last click of the user (tuple: (row, col))
  player_clicks = [] # Keep track of player clicks (two tuples: [(6, 4), (4, 4)])
  player_one = False # If a human is playing white, then this will be True. If an AI is playing, then it will be False
  player_two = False # Same as above, but for black
  game_over = False
  move_undone = False
  while running:
    human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)

    for e in p.event.get():
      if e.type == p.QUIT:
        running = False
      # Mouse handler 
      elif e.type == p.MOUSEBUTTONDOWN:
        if human_turn and not game_over:
          location = p.mouse.get_pos()
          col = location[0]//SQ_SIZE
          row = location[1]//SQ_SIZE
          if sq_selected == (row, col):
            sq_selected = () # Deselect
          else:
            sq_selected = (row, col)
            player_clicks.append(sq_selected)
          if len(player_clicks) == 2:
            # Second click, make the move
            move = CE.Move(player_clicks[0], player_clicks[1], gs.board)
            for i in range(len(valid_moves)):
              if move == valid_moves[i]:
                # If the move is valid, make it
                print(move.get_chess_notation())
                gs.make_move(valid_moves[i])
                move_made = True
                sq_selected = ()
                player_clicks = []
                human_turn = False
            if not move_made:
              player_clicks = [sq_selected]
      # Key handler
      elif e.type == p.KEYDOWN:
        if e.key == p.K_z: # Undo when 'z' is pressed
          gs.undo_move()
          move_made = True
          sq_selected = ()
          player_clicks = []
          game_over = False
          move_undone = True
        if e.key == p.K_r: # Reset the board when 'r' is pressed
          gs = CE.GameState()
          valid_moves = gs.get_valid_moves()
          sq_selected = ()
          player_clicks = []
          game_over = False
          
    # AI move finder
    if not human_turn and not game_over and not move_undone:
      valid_moves = gs.get_valid_moves()
      if valid_moves:
        AIMove = AI.find_random_move(valid_moves)
        print(AIMove.get_chess_notation())
        gs.make_move(AIMove)
        move_made = True

    if move_made:
      valid_moves = gs.get_valid_moves()
      move_made = False
      move_undone = False

    draw_game_state(screen, gs, sq_selected)

    if gs.checkmate or gs.stalemate:
      font = p.font.SysFont(None, 32)
      text = "Stalemate" if gs.stalemate else "Black wins by checkmate" if gs.white_to_move else "White wins by checkmate"
      text = font.render(text, True, p.Color("black"))
      screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    clock.tick(MAX_FPS)
    p.display.flip()

if __name__ == "__main__":
  main()