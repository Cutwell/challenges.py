from maze import MAZE

class CollisionHelper:
    def __init__(self, game):
        self.game = game
        self.tile_size = 8
        self.width = 8
        self.height = 8

    def overlap(self, x1, y1, x2, y2):
        return (
            abs(x1 - x2) * 2 < (self.width) and
            abs(y1 - y2) * 2 < (self.height)
        )

    def blocked(self, next_x, next_y, is_ghost=False):
        """
        Check all corners of the 16x16 hitbox against the MAZE grid.
        """
        # hitbox corners
        sample_points = [
            (next_x, next_y),
            (next_x + self.width - 1, next_y),
            (next_x, next_y + self.height - 1),
            (next_x + self.width - 1, next_y + self.height - 1),
        ]

        for px, py in sample_points:
            # convert virtual pixel coords -> grid coords
            gx = int(px // self.tile_size)
            gy = int(py // self.tile_size)

            # prevent leaving screen
            if gx < 0 or gy < 0 or gy >= len(MAZE) or gx >= len(MAZE[0]):
                return True

            char = MAZE[gy][gx]
            if char == "#":
                return True
            if char == "-" and is_ghost:
                return True

        return False