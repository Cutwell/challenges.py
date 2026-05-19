from collections import defaultdict
import gymnasium as gym
import numpy as np
from environment import Tile


class PacmanAgent:
    def __init__(
        self,
        env: gym.Env,
        learning_rate: float,
        initial_epsilon: float,
        epsilon_decay: float,
        final_epsilon: float,
        discount_factor: float = 0.95,
    ):
        """Initialize a Q-Learning agent.

        Args:
            env: The training environment
            learning_rate: How quickly to update Q-values (0-1)
            initial_epsilon: Starting exploration rate (usually 1.0)
            epsilon_decay: How much to reduce epsilon each episode
            final_epsilon: Minimum exploration rate (usually 0.1)
            discount_factor: How much to value future rewards (0-1)
        """
        self.env = env

        # Q-table: maps (state, action) to expected reward
        # defaultdict automatically creates entries with zeros for new states
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor  # How much we care about future rewards

        # Exploration parameters
        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        # Track learning progress
        self.training_error = []

    def _get_state_key(self, obs: dict) -> tuple:
        """Convert the observation dictionary into a simplified hashable state key."""
        agent_pos = obs["agent"]
        grid = obs["grid"]
        r, c = agent_pos
        rows, cols = grid.shape

        # 1. Surrounding walls
        up = grid[r - 1, c] == Tile.WALL if r > 0 else True
        down = grid[r + 1, c] == Tile.WALL if r < rows - 1 else True
        left = grid[r, (c - 1) % cols] == Tile.WALL
        right = grid[r, (c + 1) % cols] == Tile.WALL

        # 2. Direction to nearest pellet
        pellet_indices = np.argwhere(
            (grid == Tile.PELLET) | (grid == Tile.POWER_PELLET)
        )
        if len(pellet_indices) > 0:
            # Manhattan distance to find nearest pellet
            distances = np.abs(pellet_indices[:, 0] - r) + np.abs(
                pellet_indices[:, 1] - c
            )
            nearest_idx = pellet_indices[np.argmin(distances)]
            dr = np.sign(nearest_idx[0] - r)
            dc = np.sign(nearest_idx[1] - c)
        else:
            dr, dc = 0, 0

        return (r, c, int(up), int(down), int(left), int(right), int(dr), int(dc))

    def get_action(self, obs: dict) -> int:
        """Choose an action using epsilon-greedy strategy.

        Returns:
            action: 0-3 for directions (Right, Up, Left, Down)
        """
        state_key = self._get_state_key(obs)
        # With probability epsilon: explore (random action)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()

        # With probability (1-epsilon): exploit (best known action)
        else:
            return int(np.argmax(self.q_values[state_key]))

    def update(
        self,
        obs: dict,
        action: int,
        reward: float,
        terminated: bool,
        next_obs: dict,
    ):
        """Update Q-value based on experience.

        This is the heart of Q-learning: learn from (state, action, reward, next_state)
        """
        state_key = self._get_state_key(obs)
        next_state_key = self._get_state_key(next_obs)

        # What's the best we could do from the next state?
        # (Zero if episode terminated - no future rewards possible)
        future_q_value = (not terminated) * np.max(self.q_values[next_state_key])

        # What should the Q-value be? (Bellman equation)
        target = reward + self.discount_factor * future_q_value

        # How wrong was our current estimate?
        temporal_difference = target - self.q_values[state_key][action]

        # Update our estimate in the direction of the error
        # Learning rate controls how big steps we take
        self.q_values[state_key][action] = (
            self.q_values[state_key][action] + self.lr * temporal_difference
        )

        # Track learning progress (useful for debugging)
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        """Reduce exploration rate after each episode."""
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
