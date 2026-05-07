import pygame

mask_surface = pygame.image.load("src/images/mask.png").convert()

class CollisionHelper:
    def __init__(self, game):
        self.game = game
        self.width = 16 * self.game.scale
        self.height = 16 * self.game.scale

    def overlap(self, x1, y1, x2, y2):
        return (
            abs(x1 - x2) * 2 < (self.width) and
            abs(y1 - y2) * 2 < (self.height)
        )

    def blocked(self, next_x, next_y):
        """
        Check all edges of the 16x16 hitbox against the collision mask.

        black pixel = blocked
        white pixel = walkable
        """

        # hitbox corners + edge midpoints
        sample_points = [
            # corners
            (next_x, next_y),
            (next_x + self.width - 1, next_y),
            (next_x, next_y + self.height - 1),
            (next_x + self.width - 1, next_y + self.height - 1),
            # edge centers
            (next_x + self.width // 2, next_y),
            (next_x + self.width // 2, next_y + self.height - 1),
            (next_x, next_y + self.height // 2),
            (next_x + self.width - 1, next_y + self.height // 2),
        ]

        for px, py in sample_points:
            px = int(px)
            py = int(py)

            # prevent leaving screen
            if px < 0 or py < 0 or px >= self.game.game_width or py >= self.game.game_height:
                return True

            # convert scaled coords -> original mask coords
            mx = px // self.game.scale
            my = py // self.game.scale

            color = mask_surface.get_at((mx, my))

            # black = wall
            if color.r < 20 and color.g < 20 and color.b < 20:
                return True

        return False