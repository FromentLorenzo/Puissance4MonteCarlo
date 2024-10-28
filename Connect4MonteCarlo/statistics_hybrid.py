from ConnectState import ConnectState
from meta import GameMeta
from q_learning_mcts_agent import QLearningAgent  # Import the QLearningAgent class
from MCTS import MCTS  # Import the MCTS class
from hybrid_agent import HybridAgent

def play_game(hybrid_agent, mcts, starting_player="Q"):
    state = ConnectState()
    q_learning_turn = GameMeta.PLAYERS['one'] if starting_player == "Q" else GameMeta.PLAYERS['two']
    mcts_turn = GameMeta.PLAYERS['two'] if starting_player == "Q" else GameMeta.PLAYERS['one']

    while not state.game_over():
        if state.to_play == q_learning_turn:
            move = hybrid_agent.choose_action(state)
        else:
            mcts = MCTS(state)
            mcts.search(time_limit=0.1)  # Run MCTS for 1 second
            move = mcts.best_move()
        
        state.move(move)
        mcts.move(move)

    winner = state.get_outcome()
    #state.print()
    if winner == q_learning_turn:
        return "H"
    elif winner == mcts_turn:
        return "M"
    else:
        return "Draw"

def run_statistics(num_games=100):
    q_agent = QLearningAgent()
    q_agent.load_q_table()  # Load Q-table if pre-trained
    hybrid_mcts = MCTS(ConnectState())
    hybrid_agent = HybridAgent(q_agent, hybrid_mcts)

    hybrid_wins = 0
    mcts_wins = 0
    draws = 0

    for game in range(num_games):
        starting_player = "H" if game % 2 == 0 else "M"  # Alternate starting player
        result = play_game(hybrid_agent, MCTS(ConnectState()), starting_player)

        if result == "H":
            hybrid_wins += 1
        elif result == "M":
            mcts_wins += 1
        else:
            draws += 1

        print(f"Game {game + 1}/{num_games}: {result} wins")

    print("\nResults after", num_games, "games:")
    print("Hybrid Agent wins:", hybrid_wins)
    print("MCTS Agent wins:", mcts_wins)
    print("Draws:", draws)

if __name__ == "__main__":
    run_statistics(num_games=100)
