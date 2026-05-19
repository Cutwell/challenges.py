from typing import Optional
import numpy as np
import gymnasium as gym
from enum import IntEnum


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    PELLET = 2
    POWER_PELLET = 3
    GHOST_HOUSE = 4
    TUNNEL = 5
    GHOST = 6
    GHOST_VULNERABLE_FOR_1 = 7
    GHOST_VULNERABLE_FOR_2 = 8
    GHOST_VULNERABLE_FOR_3 = 9
    GHOST_VULNERABLE_FOR_4 = 10
    GHOST_VULNERABLE_FOR_5 = 11
    GHOST_VULNERABLE_FOR_6 = 12
    GHOST_VULNERABLE_FOR_7 = 13
    GHOST_VULNERABLE_FOR_8 = 14
    GHOST_VULNERABLE_FOR_9 = 15
    GHOST_VULNERABLE_FOR_10 = 16


MAZE = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ###--### ##.######",
    "######.## ###  ### ##.######",
    "      .   ###  ###   .      ",
    "######.## ###  ### ##.######",
    "######.## ######## ##.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################",
]

char_to_tile = {
    "#": Tile.WALL,
    ".": Tile.PELLET,
    "o": Tile.POWER_PELLET,
    " ": Tile.EMPTY,
    "-": Tile.GHOST_HOUSE,
    "g": Tile.GHOST,
    "0": Tile.GHOST_VULNERABLE_FOR_1,
    "1": Tile.GHOST_VULNERABLE_FOR_2,
    "2": Tile.GHOST_VULNERABLE_FOR_3,
    "3": Tile.GHOST_VULNERABLE_FOR_4,
    "4": Tile.GHOST_VULNERABLE_FOR_5,
    "5": Tile.GHOST_VULNERABLE_FOR_6,
    "6": Tile.GHOST_VULNERABLE_FOR_7,
    "7": Tile.GHOST_VULNERABLE_FOR_8,
    "8": Tile.GHOST_VULNERABLE_FOR_9,
    "9": Tile.GHOST_VULNERABLE_FOR_10,
}

ghost_vulnerable_states = [
    Tile.GHOST_VULNERABLE_FOR_1,
    Tile.GHOST_VULNERABLE_FOR_2,
    Tile.GHOST_VULNERABLE_FOR_3,
    Tile.GHOST_VULNERABLE_FOR_4,
    Tile.GHOST_VULNERABLE_FOR_5,
    Tile.GHOST_VULNERABLE_FOR_6,
    Tile.GHOST_VULNERABLE_FOR_7,
    Tile.GHOST_VULNERABLE_FOR_8,
    Tile.GHOST_VULNERABLE_FOR_9,
    Tile.GHOST_VULNERABLE_FOR_10,
]


class PacmanEnv(gym.Env):

    def __init__(self):
        self.num_ghosts = 4
        self.num_pellets = 240
        self.num_power_pellets = 4
        self.rows = 31
        self.cols = 28
        self.powerup_mode_remaining_steps = 0

        self.grid = [[char_to_tile.get(c, Tile.EMPTY) for c in row] for row in MAZE]

        self.pellets_remaining = self.num_pellets
        self.power_pellets_remaining = self.num_power_pellets

        # Initialize positions - will be set randomly in reset()
        # Using -1,-1 as "uninitialized" state
        self._agent_location = np.array([-1, -1], dtype=np.int32)
        self._ghost_locations = np.full((self.num_ghosts, 2), -1, dtype=np.int32)

        # Define what the agent can observe
        # Dict space gives us structured, human-readable observations
        self.observation_space = gym.spaces.Dict(
            {
                "grid": gym.spaces.Box(
                    0, 16, shape=(self.rows, self.cols), dtype=np.uint8
                ),
                "agent": gym.spaces.Box(
                    0, max(self.rows, self.cols), shape=(2,), dtype=np.int32
                ),
                "ghosts": gym.spaces.Box(
                    0,
                    max(self.rows, self.cols),
                    shape=(self.num_ghosts, 2),
                    dtype=np.int32,
                ),
            }
        )

        # Define what actions are available (4 directions)
        self.action_space = gym.spaces.Discrete(4)

        # Map action numbers to actual movements on the grid
        # This makes the code more readable than using raw numbers
        self._action_to_direction = {
            0: np.array([0, 1]),  # Move right (column + 1)
            1: np.array([-1, 0]),  # Move up (row - 1)
            2: np.array([0, -1]),  # Move left (column - 1)
            3: np.array([1, 0]),  # Move down (row + 1)
        }

    def refresh_from_grid(self):
        self.pellets_remaining = np.sum(self.grid == Tile.PELLET)
        self.power_pellets_remaining = np.sum(self.grid == Tile.POWER_PELLET)

    def step(self, action):
        """Execute one timestep within the environment.

        Args:
            action: The action to take (0-3 for directions)

        Returns:
            tuple: (observation, reward, terminated, truncated, info)
        """
        step_reward = -0.01

        # decrement powerup steps if set
        if self.powerup_mode_remaining_steps > 0:
            self.powerup_mode_remaining_steps -= 1

        # Map the discrete action (0-3) to a movement direction
        direction = self._action_to_direction[action]

        new_location = self._agent_location + direction

        # Wrap horizontally, block vertically
        new_location[1] = new_location[1] % self.cols

        in_bounds = 0 <= new_location[0] < self.rows
        
        # Check if moving into a wall
        if in_bounds and self.grid[new_location[0]][new_location[1]] == Tile.WALL:
            step_reward -= 0.05
        elif in_bounds:
            self._agent_location = new_location

        # Check if agent eaten by ghost (lose)
        terminated_by_ghost = np.any(
            np.all(self._ghost_locations == self._agent_location, axis=1)
        )
        if terminated_by_ghost:
            step_reward -= 10

        # Check if agent ate a pellet
        r, c = self._agent_location[0], self._agent_location[1]
        if self.grid[r][c] == Tile.PELLET:
            self.grid[r][c] = Tile.EMPTY
            step_reward += 1
            self.pellets_remaining -= 1

        if self.grid[r][c] == Tile.POWER_PELLET:
            self.grid[r][c] = Tile.EMPTY
            step_reward += 10
            self.powerup_mode_remaining_steps = 10
            self.power_pellets_remaining -= 1

        if self.powerup_mode_remaining_steps > 0 and self.grid[r][c] == Tile.GHOST:
            self.grid[r][c] = Tile.EMPTY
            step_reward += 50

        # Check if agent won by eating all pellets
        terminated_by_pellets = (
            self.pellets_remaining + self.power_pellets_remaining
        ) == 0
        if terminated_by_pellets:
            step_reward += 100

        terminated = terminated_by_ghost or terminated_by_pellets

        # We don't use truncation in this simple environment
        truncated = False

        observation = self._get_obs()
        info = self._get_info()

        return observation, step_reward, terminated, truncated, info

    def _get_obs(self):
        """Convert internal state to observation format.

        Returns:
            dict: Observation with POI positions
        """

        grid = np.array(self.grid, dtype=np.uint8)

        # replace ghosts in grid with vulnerable states during powerup mode
        if self.powerup_mode_remaining_steps > 0:
            vulnerable_tile = ghost_vulnerable_states[
                min(self.powerup_mode_remaining_steps - 1, len(ghost_vulnerable_states) - 1)
            ]
            grid[grid == Tile.GHOST] = vulnerable_tile

        return {
            "agent": self._agent_location.copy(),
            "ghosts": self._ghost_locations.copy(),
            "grid": grid,
        }

    def _get_info(self):
        """Compute auxiliary information for debugging.

        Returns:
            dict: Info with game state
        """

        self.refresh_from_grid()

        return {
            "pellets": self.pellets_remaining,
            "power_pellets": self.power_pellets_remaining,
        }

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        """Start a new episode.

        Args:
            seed: Random seed for reproducible episodes
            options: Additional configuration

        Returns:
            tuple: (observation, info) for the initial state
        """
        # IMPORTANT: Must call this first to seed the random number generator
        super().reset(seed=seed)

        self._agent_location = np.array([0, 14], dtype=np.int32)
        self._ghost_locations = np.array(
            [
                [13, 13],
                [14, 14],
                [15, 13],
                [15, 14],
            ],
            dtype=np.int32,
        )

        observation = self._get_obs()
        info = self._get_info()

        return observation, info
    
    def render(self):
        """Render the environment for human viewing."""
        if self.render_mode == "human":
            # Print a simple ASCII representation
            for y in range(self.rows - 1, -1, -1):  # Top to bottom
                row = ""
                for x in range(self.cols):
                    if np.array_equal([x, y], self._agent_location):
                        row += "🟡"  # Agent
                    elif np.array_equal([x, y], self._ghost_locations):
                        row += "👻"  # Target
                    elif self.grid[y][x] == Tile.WALL:
                        row += "#"  # Wall
                    else:
                        row += " "  # Empty
                print(row)
            print()

gym.register(
    id="Pacman-v0",
    entry_point=PacmanEnv,
    max_episode_steps=300,  # Prevent infinite episodes
)
