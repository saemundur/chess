import pygame as p
import ChessEngine as CE
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

def draw_game_state(screen, gs):
  draw_board(screen)
  draw_pieces(screen, gs.board)

def draw_board(screen):
  colors = [p.Color("white"), p.Color("dark green")]
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
  while running:
    for e in p.event.get():
      if e.type == p.QUIT:
        running = False
      # Mouse handler 
      elif e.type == p.MOUSEBUTTONDOWN:
        location = p.mouse.get_pos()
        col = location[0]//SQ_SIZE
        row = location[1]//SQ_SIZE
        if sq_selected == (row, col):
          sq_selected = () # Deselect
        else:
          sq_selected = (row, col)
          player_clicks.append(sq_selected)
        if len(player_clicks) == 2:
          move = CE.Move(player_clicks[0], player_clicks[1], gs.board)
          if move in valid_moves:
            print(move.get_chess_notation())
            gs.make_move(move)
            move_made = True
          sq_selected = ()
          player_clicks = []
          # print(DataFrame(gs.board))

      # Key handler
      elif e.type == p.KEYDOWN:
        if e.key == p.K_z: # Undo when 'z' is pressed
          gs.undo_move()
          move_made = True
          sq_selected = ()
          player_clicks = []

    if move_made:
      valid_moves = gs.get_valid_moves()
      move_made = False

    draw_game_state(screen, gs)
    clock.tick(MAX_FPS)
    p.display.flip()

if __name__ == "__main__":
  main()