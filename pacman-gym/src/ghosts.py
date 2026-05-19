from collision import CollisionHelper
import random

LOOKAHEAD = 1


class Ghost:
    def __init__(self, game, color, x, y):
        self.game = game
        self.color = color
        self.x = x
        self.y = y
        self.collision_helper = CollisionHelper(self.game)
        self.facing = "down"
        self.speed = 2
        self.state = "alive"

    def _next_pos_by(self, facing, x, y, amount):
        if facing == "right":
            return x + amount, y
        if facing == "left":
            return x - amount, y
        if facing == "up":
            return x, y - amount
        if facing == "down":
            return x, y + amount

    def _can_move(self, facing, x, y):
        for step in range(1, LOOKAHEAD + 1, self.speed):
            sx, sy = self._next_pos_by(facing, x, y, step)
            if self.collision_helper.blocked(sx, sy):
                return False
        return True

    def update(self):
        if self.game.state == "game_running":
            # check if touching pacman
            if self.collision_helper.overlap(
                self.x, self.y, self.game.player.x, self.game.player.y
            ):
                if self.state == "dead":
                    pass
                elif self.game.player.is_powered_up():
                    self.state = "dead"
                else:
                    self.game.emit("game_over")

            # get all possible directions to move
            dirs = ["up", "down", "left", "right"]
            mask = [self._can_move(face, self.x, self.y) for face in dirs]
            possible_directions = [d for d, keep in zip(dirs, mask) if keep]

            if self.facing not in possible_directions:
                self.facing = random.choice(possible_directions)

            next_x, next_y = self._next_pos_by(self.facing, self.x, self.y, self.speed)
            self.x = next_x
            self.y = next_y
