import json
import os
from ConnectState import ConnectState
from meta import GameMeta
from MCTS import MCTS

class TrainAgent:
    def __init__(self, num_games=100):
        self.num_games = num_games
        self.training_data = []

    def save_training_data(self):
        with open("training_data.json", "w") as f:
            json.dump(self.training_data, f)

    def load_training_data(self):
        if os.path.exists("training_data.json"):
            with open("training_data.json", "r") as f:
                return json.load(f)
        return []

    def train(self):
        self.training_data = self.load_training_data()  # Load existing training data

        for game_number in range(self.num_games):
            state = ConnectState()
            mcts1 = MCTS(state)
            mcts2 = MCTS(state)
            game_moves = []  # List to store moves for the current game
            winner = None
            game_over = False

            while not game_over:
                # Player 1 (AI 1)
                mcts1.search(1)  # AI 1 makes a move
                move1 = mcts1.best_move()
                state.move(move1)
                mcts1.move(move1)
                mcts2.move(move1)

                # Record the current board state
                current_board = state.get_board()  # Method to get the board state
                game_moves.append({
                    "column": move1,
                    "player": 1,
                    "board": current_board
                })

                if state.game_over():
                    winner = 1  # AI 1 wins
                    game_over = True
                    break

                # Player 2 (AI 2)
                mcts2.search(1)  # AI 2 makes a move
                move2 = mcts2.best_move()
                state.move(move2)
                mcts1.move(move2)
                mcts2.move(move2)

                # Record the current board state
                current_board = state.get_board()  # Method to get the board state
                game_moves.append({
                    "column": move2,
                    "player": 2,
                    "board": current_board
                })


                if state.game_over():
                    winner = 2  # AI 2 wins
                    game_over = True
                    break

            self.training_data.append({
                    "game_number": game_number + 1,
                    "moves": game_moves,
                    "winner": winner
                })
            print(f"Game {game_number + 1}/{self.num_games} finished.")
            state.print()

        # Save the training data after all games
        self.save_training_data()

if __name__ == "__main__":
    trainer = TrainAgent(num_games=10)
    trainer.train()
 