# Screen starts from top-left. X increases from left to right, Y from top to bottom

from game import * # Modelisation
import pygame
import sys
from pygame.locals import *

red =  231, 111, 81
blue = 38, 70, 83
pink = 244, 162, 97
green = 42, 157, 143
black = 0, 0, 0
beige = 212, 163, 115
cell = 50
boardX, boardY = 150, 150
window_width, window_height = 650, 650

# Assign FPS a value
FPS = 30
FramePerSec = pygame.time.Clock()

pygame.init() # Initialize all pygame modules
surface = pygame.display.set_mode((window_width, window_height))


# Functions

def quit_game():
    """To quit the game loop"""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

def assam_move(screen, orientation, x, y):
    if orientation == EAST:
        # circle(surface, color, center, radius)
        pygame.draw.circle(screen, (165, 42, 42), (x, y), 20, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y - 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x, y + 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x + 8, y), 5, 0)
    if orientation == NORTH:
        pygame.draw.circle(screen, (165, 42, 42), (x, y), 20, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y - 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x + 8, y), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x - 8, y), 5, 0)
    if orientation == WEST:
        pygame.draw.circle(screen, (165, 42, 42), (x, y), 20, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y + 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x - 8, y), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x, y - 8), 5, 0)
    if orientation == SOUTH:
        pygame.draw.circle(screen, (165, 42, 42), (x, y), 20, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)
        pygame.draw.circle(screen, (0, 0, 0), (x, y + 8), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x - 8, y), 5, 0)
        pygame.draw.circle(screen, (0, 0, 0), (x + 8, y), 5, 0)


class ShowBoard:
    def __init__(self):
        pass

    def lines(self, screen, x, y, cell):
        for i in range(y, y + 8 * cell, cell): # Horizontal lines
            pygame.draw.line(screen, (255, 255, 255), (y, i), (y + 7 * cell, i), 2)
        for i in range(x, x + 8 * cell, cell):
            pygame.draw.line(screen, (255, 255, 255), (i, x), (i, x + 7 * cell), 2)

    def borders(self, screen, x, y, cell):
        """Les demi cercles"""
        for i in range(y + cell, y + 8 * cell, 2 * cell): # left 
            pygame.draw.circle(screen, (255, 255, 255), (x, i), cell / 2, 2)
        for i in range(x + cell, x + 8 * cell, 2 * cell): # top
            pygame.draw.circle(screen, (255, 255, 255), (i, y), cell / 2, 2)
        for i in range(y + 6 * cell, y, -2 * cell): # right
            pygame.draw.circle(screen, (255, 255, 255), (x + 7 * cell, i), cell / 2, 2)
        for i in range(x + 6 * cell, x, -2 * cell): # bottom
            pygame.draw.circle(screen, (255, 255, 255), (i, y + 7 * cell), cell / 2, 2)
        pygame.draw.rect(surface, beige, (x, y, x + 4 * cell, y + 4 * cell))

    def cells(self, screen, board):
        """Pour les tapis"""
        fontobject = pygame.font.Font(None, 15)
        for i in range(7):
            for j in range(7):
                if board.get_color(i, j) == 0:
                    continue
                elif board.get_color(i, j) == RED:
                    pygame.draw.rect(screen, red, (150 + i * 50, 150 + (6-j) * 50, 50, 50))
                    surface.blit(fontobject.render(str(int(board.get_number(i, j))), True, (255, 255, 255)),
                                 (150 + i * 50 + 22, 150 + (6-j) * 50 + 22))
                elif board.get_color(i, j) == PINK:
                    pygame.draw.rect(screen, pink, (150 + i * 50, 150 + (6-j) * 50, 50, 50))
                    surface.blit(fontobject.render(str(int(board.get_number(i, j))), True, (255, 255, 255)),
                                 (150 + i * 50 + 22, 150 + (6-j) * 50 + 22))
                elif board.get_color(i, j) == BLUE:
                    pygame.draw.rect(screen, blue, (150 + i * 50, 150 + (6-j) * 50, 50, 50))
                    surface.blit(fontobject.render(str(int(board.get_number(i, j))), True, (255, 255, 255)),
                                 (150 + i * 50 + 22, 150 + (6-j) * 50 + 22))
                else:
                    pygame.draw.rect(screen, green, (150 + i * 50, 150 + (6-j) * 50, 50, 50))
                    surface.blit(fontobject.render(str(int(board.get_number(i, j))), True, (255, 255, 255)),
                                 (150 + i * 50 + 22, 150 + (6-j) * 50 + 22))

#################### 
# --- Game loop ---
#################### 

game_board = Board()
#game_board.board[0,0] = np.array([RED, 1])
#game_board.board[1,0] = np.array([RED, 1])
#game_board.board[1,1] = np.array([BLUE, 1])
#game_board.board[1,2] = np.array([GREEN, 2]) # cover blue 1
#game_board.board[2,2] = np.array([PINK, 2])

while True:

    # Fill all the surface with 
    surface.fill(beige)
    pygame.draw.rect(surface, beige, (0, 0, window_width, window_height))

    # Show the board on the surface
    MarrakechBoard = ShowBoard()
    ShowBoard.borders(MarrakechBoard, surface, boardX, boardY, cell)
    ShowBoard.cells(MarrakechBoard, surface, game_board)
    ShowBoard.lines(MarrakechBoard, surface, boardX, boardY, cell)

    # Show the pawn
    assamX = boardX + cell / 2 + cell * game_board.pawn.position.x
    assamY = boardY + cell / 2 + cell * game_board.pawn.position.y
    assam_move(surface, game_board.pawn.orientation, assamX, assamY)

    # Random playout
    i = 0
    while not game_board.terminal():
        print(f'Turn {i}')
        # Fill all the surface with 
        surface.fill(beige)
        pygame.draw.rect(surface, beige, (0, 0, window_width, window_height))

        # Show the board on the surface
        MarrakechBoard = ShowBoard()
        ShowBoard.borders(MarrakechBoard, surface, boardX, boardY, cell)
        ShowBoard.cells(MarrakechBoard, surface, game_board)
        ShowBoard.lines(MarrakechBoard, surface, boardX, boardY, cell)

        # Show the pawn
        assamX = boardX + cell / 2 + cell * game_board.pawn.position.x
        assamY = boardY + cell / 2 + cell * game_board.pawn.position.y
        assam_move(surface, game_board.pawn.orientation, assamX, assamY)

        dice_result = game_board.throw_dice()
        moves = game_board.legal_moves(dice_result)

        # The game isn't over: rugs are remaining
        # We play another move chosen randomly
        #print(f'Number of valid moves: {len(moves)}')
        n = random.randint(0, len(moves)-1)
        #print(f'Move to play: {moves[n]}')
        game_board.play(moves[n])

        # Pay opponent
        # Pay only if the pawn is on an opponent color
        current_square_color = game_board.get_color(game_board.pawn.position.x, game_board.pawn.position.y)
        opponent_player_id = abs(game_board.current_player.id - 1)
        if current_square_color not in game_board.current_player.colors:
            amount = game_board.pawn.get_nb_same_color_squares(game_board)
            game_board.current_player.pay(amount, game_board.players[opponent_player_id])

        # Change turn 
        game_board.current_player = game_board.players[opponent_player_id]
        game_board.current_color = next(color_cycle)
        

        pygame.display.update()
        i += 1
        #print(game_board.players[0].rugs_left, game_board.players[1].rugs_left)

    quit_game()
    