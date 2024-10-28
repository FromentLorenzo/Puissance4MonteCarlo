from MCTS import MCTS

class HybridAgent:
    def __init__(self, q_agent, mcts):
        self.q_agent = q_agent  # Q-learning agent
        self.mcts = mcts  # MCTS instance

    def choose_action(self, state):
        """Choose an action using MCTS or fallback to Q-learning if MCTS is uncertain."""
        # Run MCTS search
        self.mcts = MCTS(state)
        self.mcts.search(time_limit=0.1)  # Run MCTS with a time limit of 5 second

        # Get the statistics for MCTS rollouts and best move
        move = self.mcts.best_move()
        win_probability, _ = self.mcts.get_confidence_for_best_move(move)

        # Define a threshold for MCTS confidence
        confidence_threshold = 0.55  # Example threshold: MCTS must have high confidence in the move
        # If MCTS is confident enough (above threshold), use its move
        if win_probability > confidence_threshold:
            #print(f"MCTS chooses move {move} with {win_probability*100}% confidence.")
            return move
        else:
            # Fall back to Q-learning if MCTS isn't confident
            #print("MCTS is uncertain, falling back to Q-learning agent.")
            return self.q_agent.choose_action(state)
