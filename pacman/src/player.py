import pygame
from collision import CollisionHelper

LOOKAHEAD = 16  # must be a clear run, not just 2px


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.facing = "right"
        self.queued_facing = None  # buffered turn request
        self.speed = 2
        self.collision_helper = CollisionHelper(self.game)
        self.death_tick = None
        self.powerup_end_ms = 0

    @property
    def powerup_ms(self):
        return max(0, self.powerup_end_ms - pygame.time.get_ticks())

    def draw(self):
        if self.game.state == "game_running":
            frame = self.game.sheet.get_frame(
                f"pacman_walk_{self.facing}", self.game.tick
            )
            self.game.screen.surface.blit(frame, (self.x, self.y + self.game.y_offset))

        elif self.game.state == "game_over":
            elapsed = self.game.tick - self.death_tick

            if elapsed < 9 * 6:
                frame = self.game.sheet.get_frame_once(
                    "pacman_die", elapsed, frame_speed=6
                )
                self.game.screen.surface.blit(frame, (self.x, self.y + self.game.y_offset))

    def on_key_down(self, key):
        if key is self.game.keys.W or key is self.game.keys.UP:
            self.queued_facing = "up"
        elif key is self.game.keys.S or key is self.game.keys.DOWN:
            self.queued_facing = "down"
        elif key is self.game.keys.A or key is self.game.keys.LEFT:
            self.queued_facing = "left"
        elif key is self.game.keys.D or key is self.game.keys.RIGHT:
            self.queued_facing = "right"

    def _can_move(self, facing, x, y):
        for step in range(1, LOOKAHEAD + 1, self.speed):
            sx, sy = self._next_pos_by(facing, x, y, step)
            if self.collision_helper.blocked(sx, sy):
                return False
        return True

    def _next_pos_by(self, facing, x, y, amount):
        if facing == "right":
            return x + amount, y
        if facing == "left":
            return x - amount, y
        if facing == "up":
            return x, y - amount
        if facing == "down":
            return x, y + amount
        
    def is_powered_up(self):
        return self.powerup_ms > 0

    def update(self):
        if self.game.state == "game_running":
            if self.queued_facing:
                if self._can_move(self.queued_facing, self.x, self.y):
                    self.facing = self.queued_facing
                    self.queued_facing = None

            next_x, next_y = self._next_pos_by(self.facing, self.x, self.y, self.speed)
            if not self.collision_helper.blocked(next_x, next_y):
                self.x = next_x
                self.y = next_y
