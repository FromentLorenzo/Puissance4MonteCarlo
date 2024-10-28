import random
import json
import os
from copy import deepcopy
from ConnectState import ConnectState
from meta import GameMeta
from MCTS import MCTS  # Importing the MCTS class

class QLearningAgent:
    def __init__(self, alpha=0.2, gamma=0.9, epsilon=0.2, num_games=10000):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.num_games = num_games
        self.q_table = {}  # Q-table to store state-action pairs

    def load_q_table(self, file_name="q_table.json"):
        """Load the Q-table from a file."""
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                self.q_table = json.load(f)
        else:
            self.q_table = {}

    def save_q_table(self, file_name="q_table.json"):
        """Save the Q-table to a file."""
        with open(file_name, "w") as f:
            json.dump(self.q_table, f, indent=4)

    def get_state_key(self, state):
        """Convert the current board state to a hashable key (string representation)."""
        return str(state.get_board())  # Convert the board to a string representation

    def choose_action(self, state):
        """Choose an action using MCTS."""
        # Initialize MCTS with the current state
        mcts = MCTS(state)
        mcts.search(time_limit=0.1)  # Set a time limit for MCTS search (1 second here)
        return mcts.best_move()

    def update_q_value(self, state, action, reward, next_state):
        """Update the Q-value for the given state-action pair."""
        state_key = self.get_state_key(state)

        # Initialize state-action pairs if they do not exist in the Q-table
        if state_key not in self.q_table:
            self.q_table[state_key] = {str(col): 0 for col in state.get_legal_moves()}

        # Handle the terminal state where next_state is None (game over)
        if next_state is None or next_state.game_over():
            max_future_q = 0  # No future reward after the game ends
        else:
            next_state_key = self.get_state_key(next_state)
            if next_state_key not in self.q_table:
                self.q_table[next_state_key] = {str(col): 0 for col in next_state.get_legal_moves()}
            future_q_values = [self.q_table[next_state_key].get(str(col), 0) for col in next_state.get_legal_moves()]
            max_future_q = max(future_q_values)

        # Update Q-value using Q-learning formula
        old_q_value = self.q_table[state_key].get(str(action), 0)
        new_q_value = old_q_value + self.alpha * (reward + self.gamma * max_future_q - old_q_value)
        self.q_table[state_key][str(action)] = new_q_value

    def get_reward(self, winner, player):
        """Return the reward based on the game outcome."""
        if winner == GameMeta.OUTCOMES['draw']:
            return 0  # Draw has no reward
        elif winner == player:
            return 1  # Winning gives +1 reward
        else:
            return -1  # Losing gives -1 reward

    def train(self):
        """Train the Q-learning agent by playing against itself."""
        for game_number in range(self.num_games):
            state = ConnectState()
            game_over = False
            move_history = []  # Track moves for learning

            while not game_over:
                current_player = state.to_play  # Get the current player (either 'one' or 'two')
                action = self.choose_action(state)  # MCTS agent chooses an action
                
                # Save the current state (the entire state, not just the board)
                previous_state = deepcopy(state)
                state.move(action)  # Apply the action
                
                # Store the move (state, action) for post-game reward assignment
                move_history.append((deepcopy(previous_state), action, current_player))
                
                if state.game_over():  # Check if the game is over
                    winner = state.get_outcome()  # Determine the winner
                    
                    # Backpropagate rewards to all moves
                    for prev_state, action, player in move_history:
                        reward = self.get_reward(winner, player)
                        next_state = None if prev_state == move_history[-1][0] else state
                        self.update_q_value(prev_state, action, reward, next_state)

                    print(f"Game {game_number + 1}/{self.num_games} finished. Winner: {winner}")
                    game_over = True
                else:
                    current_player = GameMeta.PLAYERS['two'] if current_player == GameMeta.PLAYERS['one'] else GameMeta.PLAYERS['one']

        # Save Q-table after training
        self.save_q_table()

if __name__ == "__main__":
    for i in range(100): # Launching 10000 training game, saving Q-table every hundred
        agent = QLearningAgent(num_games=100)
        agent.load_q_table()  # Load existing Q-table if available
        agent.train()  # Train the agent by playing against itself
        print(f"{i}% done")
