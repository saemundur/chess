import pygame as p
import ChessEngine as CE
import ChessAI as AI
from pandas import *
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 300
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("icons/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def draw_game_state(screen, gs, sq_selected, move_log_font):
  draw_board(screen)
  draw_pieces(screen, gs.board)
  highlight_square(screen, gs, sq_selected)
  draw_move_log(screen, gs, move_log_font)

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

def draw_move_log(screen, gs, move_log_font):
  move_log_rect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
  p.draw.rect(screen, p.Color('black'), move_log_rect)
  move_log = gs.move_log
  move_texts = []
  for i in range(0, len(move_log), 2):
      move_string = str(i // 2 + 1) + '. ' + move_log[i].get_chess_notation() + " "
      if i + 1 < len(move_log):
          move_string += move_log[i + 1].get_chess_notation() + "  "
      move_texts.append(move_string)

  moves_per_row = 3
  padding = 5
  line_spacing = 2
  text_y = padding
  for i in range(0, len(move_texts), moves_per_row):
      text = ""
      for j in range(moves_per_row):
          if i + j < len(move_texts):
              text += move_texts[i + j]

      text_object = move_log_font.render(text, True, p.Color('white'))
      text_location = move_log_rect.move(padding, text_y)
      screen.blit(text_object, text_location)
      text_y += text_object.get_height() + line_spacing

def draw_end_game_text(screen, text):
  font = p.font.SysFont(None, 32)
  # Shadow text
  text_object = font.render(text, 0, p.Color("Grey"))
  text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH//2 - text_object.get_width()//2, BOARD_HEIGHT//2 - text_object.get_height()//2)
  screen.blit(text_object, text_location)
  # Main text
  text_object = font.render(text, 0, p.Color("Black"))
  screen.blit(text_object, text_location.move(2, 2))
  
def main():
  p.init()
  screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
  clock = p.time.Clock()
  screen.fill(p.Color("white"))
  load_images()
  move_log_font = p.font.SysFont("Arial", 16, False, False)

  gs = CE.GameState()
  valid_moves = gs.get_valid_moves()
  running = True
  sq_selected = () # No square is selected, keep track of the last click of the user (tuple: (row, col))
  player_clicks = [] # Keep track of player clicks (two tuples: [(6, 4), (4, 4)])
  move_made = False # Flag variable for when a move is made
  player_one = False # If a human is playing white, then this will be True. If an AI is playing, then it will be False
  player_two = False # Same as above, but for black
  game_over = False
  move_undone = False
  AI_thinking = False
  move_finder_process = None

  while running:
    human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
    for e in p.event.get():
      if e.type == p.QUIT:
        running = False
      # Mouse handler 
      elif e.type == p.MOUSEBUTTONDOWN:
        if not game_over:
          location = p.mouse.get_pos()
          col = location[0]//SQ_SIZE
          row = location[1]//SQ_SIZE
          # Deselect the square if it is already selected or if the click is out of bounds
          if sq_selected == (row, col) or col >= 8 or row >= 8:
            sq_selected = ()
          else:
            sq_selected = (row, col)
            player_clicks.append(sq_selected)
          if len(player_clicks) == 2 and human_turn:
            # Second click, make the move
            move = CE.Move(player_clicks[0], player_clicks[1], gs.board)
            for i in range(len(valid_moves)):
              if move == valid_moves[i]:
                # If the move is valid, make it
                gs.make_move(valid_moves[i])
                move_made = True
                sq_selected = ()
                player_clicks = []
                if gs.checkmate or gs.stalemate:
                  game_over = True
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
          if AI_thinking:
            move_finder_process.terminate()
            AI_thinking = False
        if e.key == p.K_r: # Reset the board when 'r' is pressed
          gs = CE.GameState()
          valid_moves = gs.get_valid_moves()
          sq_selected = ()
          player_clicks = []
          game_over = False
          move_undone = True

    if gs.checkmate or gs.stalemate:
      game_over = True

    # AI move finder
    if not human_turn and not game_over and not move_undone:
      if not AI_thinking:
        AI_thinking = True
        return_queue = Queue()
        move_finder_process = Process(target=AI.find_best_move, args=(gs, valid_moves, return_queue))
        move_finder_process.start()
      
      if not move_finder_process.is_alive():
        AIMove = return_queue.get()
        if AIMove is None:
          AIMove = AI.find_random_move(valid_moves)
      valid_moves = gs.get_valid_moves()
      AIMove = AI.find_best_move(gs, valid_moves, return_queue)
      if AIMove is None and valid_moves:
        AIMove = AI.find_random_move(valid_moves)
      if AIMove is not None:
        gs.make_move(AIMove)
        if gs.checkmate or gs.stalemate:
          game_over = True
      move_made = True

    if move_made:
      valid_moves = gs.get_valid_moves()
      move_made = False
      move_undone = False

    draw_game_state(screen, gs, sq_selected, move_log_font)
    if game_over:
      text = "Stalemate" if gs.stalemate else "Black wins by checkmate" if gs.white_to_move else "White wins by checkmate"
      draw_end_game_text(screen, text)

    clock.tick(MAX_FPS)
    p.display.flip()

if __name__ == "__main__":
  main()