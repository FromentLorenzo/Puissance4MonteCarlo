import numpy as np
import pygame
import sys
import math
 
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
 
ROW_COUNT = 6
COLUMN_COUNT = 7
 
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board
 
def drop_piece(board, row, col, piece):
    board[row][col] = piece
 
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
 
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
 
def print_board(board):
    print(np.flip(board, 0))
 
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
 
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
 
 
board = create_board()
print_board(board)
game_over = False
turn = 0
 
#initalize pygame
pygame.init()
 
#define our screen size
SQUARESIZE = 100
 
#define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
 
size = (width, height)
 
RADIUS = int(SQUARESIZE/2 - 5)
 
screen = pygame.display.set_mode(size)
#Calling function draw_board again
draw_board(board)
pygame.display.update()
 
myfont = pygame.font.SysFont("monospace", 75)
 
import random

# Monte Carlo Simulation parameters
SIMULATIONS = 200

def monte_carlo(board, piece):
    # Vérifier si on peut gagner immédiatement
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, piece)
            if winning_move(temp_board, piece):  # Si on gagne immédiatement
                return col  # Jouer ce coup gagnant

    # Vérifier si l'adversaire peut gagner et bloquer
    opponent_piece = 3 - piece
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, opponent_piece)
            if winning_move(temp_board, opponent_piece):  # Si l'adversaire gagne
                return col  # Bloquer l'adversaire

    # Simulations Monte Carlo
    win_counts = np.zeros(COLUMN_COUNT)
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            for _ in range(SIMULATIONS):
                temp_board = board.copy()
                row = get_next_open_row(temp_board, col)
                drop_piece(temp_board, row, col, piece)

                # Simuler le jeu aléatoire
                result = simulate_random_game(temp_board, piece)
                if result == piece:
                    win_counts[col] += 1

    # Choisir la colonne avec le plus de victoires simulées
    best_col = np.argmax(win_counts)
    return best_col


def simulate_random_game(board, piece):
    """Simulates a random game until it ends and returns the winning piece."""
    current_piece = piece
    while not is_game_over(board):
        valid_moves = [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]
        col = random.choice(valid_moves)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, current_piece)

        if winning_move(board, current_piece):
            return current_piece
        current_piece = 3 - current_piece  # Switch between 1 and 2
    return 0  # Draw

def is_game_over(board):
    # Check for a win or a full board (no valid locations)
    if winning_move(board, 1) or winning_move(board, 2):
        return True
    return np.all(board[ROW_COUNT-1] != 0)


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:  # Seulement pour le joueur 1
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            # Monte Carlo joue immédiatement après le joueur 1
            if not game_over and turn == 1:
                col = monte_carlo(board, 2)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
