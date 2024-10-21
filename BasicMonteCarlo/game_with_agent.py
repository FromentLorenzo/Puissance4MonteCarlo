from ConnectState import ConnectState
from meta import GameMeta
from q_learning_mcts_agent import QLearningAgent  # Import your Q-learning agent
import pygame
import sys

# Constants for the display
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SQUARESIZE = SCREEN_HEIGHT // 7

def play():
    pygame.init()
    
    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Connect Four with Q-Learning Agent")

    # Initialize the game state and Q-learning agent
    state = ConnectState()
    q_agent = QLearningAgent()  # Initialize Q-learning agent
    q_agent.load_q_table()  # Load the pre-trained Q-table

    state.draw_board(screen, SQUARESIZE)
    
    # Colors
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Game loop
    game_over = False
    font = pygame.font.SysFont("monospace", 50)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if state.to_play == GameMeta.PLAYERS['one']:
                    pygame.draw.circle(screen, RED, (posx, SQUARESIZE // 2), SQUARESIZE // 2 - 5)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SQUARESIZE))
                # Human player (Player one) move
                if state.to_play == GameMeta.PLAYERS['one']:
                    posx = event.pos[0]
                    col = posx // SQUARESIZE

                    if col in state.get_legal_moves():
                        state.move(col)  # Apply human move to game state

                        state.draw_board(screen, SQUARESIZE)

                        if state.game_over():
                            label = font.render("Player 1 wins!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                            break

                        # Q-learning agent's move
                        print("Agent is thinking...")
                        move = q_agent.choose_action(state)  # Get action from Q-learning agent

                        state.move(move)  # Apply the agent's move
                        
                        state.draw_board(screen, SQUARESIZE)

                        if state.game_over():
                            label = font.render("Player 2 wins!", 1, BLUE)
                            screen.blit(label, (40, 10))
                            game_over = True
                            break

        pygame.display.update()

    pygame.display.update()
    pygame.time.wait(3000)

if __name__ == "__main__":
    play()
