import pygame

class Pellet:
    def __init__(self, game, x, y, is_powerup=False):
        self.game = game
        self.x = x
        self.y = y
        self.eaten = False
        self.is_powerup = is_powerup

    def update(self, playerX, playerY):
        if not self.eaten:
            # Player is now 8x8
            player_center_x = playerX + 4
            player_center_y = playerY + 4

            dist_x = abs(self.x - player_center_x)
            dist_y = abs(self.y - player_center_y)

            threshold = 4

            if dist_x < threshold and dist_y < threshold:
                self.eaten = True
                if self.is_powerup:
                    self.game.score += 10
                    sound = self.game.sound_manager.intermission
                    self.game.sound_manager.play_priority(sound)
                    self.game.player.powerup_end_ms = pygame.time.get_ticks() + self.game.sound_manager.get_length_ms(sound)
                else:
                    self.game.score += 1

    def draw(self, canvas, offset_y=0):
        if not self.eaten:
            size = 2 if not self.is_powerup else 4
            canvas.filled_circle((self.x, self.y + offset_y), size, "white")
