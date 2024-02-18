import pygame as p
import ChessEngine as CE

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("icons/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs):
  drawBoard(screen)
  drawPieces(screen, gs.board)

def drawBoard(screen):
  colors = [p.Color("white"), p.Color("dark green")]
  for r in range(DIMENSION):
    for c in range(DIMENSION):
      color = colors[((r + c) % 2)]
      p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
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
  loadImages()
  running = True
  sqSelected = () # No square is selected, keep track of the last click of the user (tuple: (row, col))
  playerClicks = [] # Keep track of player clicks (two tuples: [(6, 4), (4, 4)])
  while running:
    for e in p.event.get():
      if e.type == p.QUIT:
        running = False
      elif e.type == p.MOUSEBUTTONDOWN:
        location = p.mouse.get_pos()
        col = location[0]//SQ_SIZE
        row = location[1]//SQ_SIZE
        if sqSelected == (row, col):
          sqSelected = () # Deselect
        else:
          sqSelected = (row, col)
          playerClicks.append(sqSelected)
        if len(playerClicks) == 2:
          move = CE.Move(playerClicks[0], playerClicks[1], gs.board)
          print(move.get_chess_notation())
          gs.make_move(move)
          sqSelected = ()
          playerClicks = []
    drawGameState(screen, gs)
    clock.tick(MAX_FPS)
    p.display.flip()

if __name__ == "__main__":
  main()