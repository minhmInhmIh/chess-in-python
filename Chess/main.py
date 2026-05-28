import pygame
import ChessEngine

pygame.init()

#CONSTANTS
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH/DIMENSION
FPS = 15
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
IMAGES = {}

#colors
WHITE = (255,255,255)
LIGHT = (239, 203, 161)
DARK = (202, 116, 62)

def loadImages():
    pieces = ["wp","wR","wN","wB","wK","wQ","bp","bR","bN","bB","bK","bQ"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQ_SIZE,SQ_SIZE))

def main(window):
    
    clock = pygame.time.Clock()
    gameState = ChessEngine.GameState()
    validMoves = gameState.getValidMove()
    moveMade = False
    loadImages()
    running = True

    sqSelected = ()
    playerClicks = []
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = int(pos[0]//SQ_SIZE)
                row = int(pos[1]//SQ_SIZE)

                if pos == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gameState.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gameState.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    gameState.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gameState.getValidMove()
            moveMade = False
        draw(window, gameState)
        
#draw whats happening in game
def drawGameState(window, gameState):
    drawBoard(window)
    drawPieces(window, gameState.board)

#draw the squares on the board
def drawBoard(window):
    colors = [LIGHT,DARK]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            pygame.draw.rect(window, color, (r*SQ_SIZE, c*SQ_SIZE, SQ_SIZE,SQ_SIZE))
#draw pieces
def drawPieces(window, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                window.blit(IMAGES[piece],pygame.Rect(c*SQ_SIZE,r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
#draw everything
def draw(window, gs):
    window.fill(WHITE)
    drawGameState(window,gs)
    pygame.display.flip()

if __name__ == "__main__":
    main(WINDOW)














