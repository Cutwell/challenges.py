import pygame
from canvas import Canvas
from maze import Maze, MAZE
from player import Player
from pellets import Pellet
from ghosts import Ghost
from spriteloader import SpriteSheet
from sound import SoundManager

class Game:
    def __init__(self, images, keys, scale) -> None:
        self.score = 0
        self.keys = keys
        self.images = images
        self.scale = scale
        self.state = "game_running"
        self.tick = 0
        self.isSetup = False
        
        # Virtual resolution: 224x288 (40px UI + 248px Game)
        self.canvas = Canvas(224, 288, scale=scale)
        self.ui_height = 40
        self.tile_size = 8
        
        # Native scale for sprites (16x16)
        self.sheet = SpriteSheet("spritesheet", scale=1)
        self.sound_manager = SoundManager(self)
        self.maze = Maze(self)

        # UI background (native size 224x40)
        self.ui_background = self.images.ui
        
        # Entities use virtual coordinates
        # 8x8 hitbox aligned to 8x8 grid
        self.player = Player(self, x=104, y=184)
        
        self.pellets = []
        for r, row in enumerate(MAZE):
            for c, char in enumerate(row):
                px, py = c * 8 + 4, r * 8 + 4 # center of 8x8 tile
                if char == ".":
                    self.pellets.append(Pellet(self, px, py, is_powerup=False))
                elif char == "P":
                    self.pellets.append(Pellet(self, px, py, is_powerup=True))

        # Ghost start: centered in house
        self.ghosts = [
            Ghost(self, color, 104, 112)
            for color in ["red", "pink", "cyan", "orange"]
        ]

    def draw(self, screen):
        self.canvas.clear()
        
        # Draw UI
        self.canvas.blit(self.ui_background, (0, 0))
        self.canvas.draw_text("1UP", (24, 8), fontsize=12)
        self.canvas.draw_text(str(self.score), (24, 20), fontsize=12)
        self.canvas.draw_text("HIGH SCORE", (88, 8), fontsize=12)
        self.canvas.draw_text("10000" if self.score < 10000 else str(self.score), (88, 20), fontsize=12)

        
        # Draw Game
        self.maze.draw(self.canvas, offset_y=self.ui_height)
        
        for p in self.pellets:
            p.draw(self.canvas, offset_y=self.ui_height)
            
        self.player.draw(self.canvas, offset_y=self.ui_height)
        
        for g in self.ghosts:
            g.draw(self.canvas, offset_y=self.ui_height)

        if self.state == "game_over":
            # Simple game over text if we had a canvas text method
            pass
            
        # Final scale to screen
        self.canvas.render_to_screen(screen)

    def update(self):
        if not self.isSetup:
            self.isSetup = True
            self.setup()

        self.tick += 1
        self.player.update()

        for p in self.pellets:
            p.update(self.player.x, self.player.y)

        for g in self.ghosts:
            g.update()

        if self.pellets and all(p.eaten for p in self.pellets):
            self.sound_manager.queue_sound(self.sound_manager.extrapac)
            for p in self.pellets: p.eaten = False

        self.sound_manager.update()

    def reset(self):
        self.player.x, self.player.y = 104, 184
        self.tick = 0
        self.score = 0
        self.player.facing = "right"
        self.player.queued_facing = None
        self.player.death_tick = None
        self.player.powerup_end_ms = 0

        for g in self.ghosts:
            g.x, g.y = 104, 112
            g.state = "alive"

        for p in self.pellets:
            p.eaten = False

    def setup(self):
        self.sound_manager.queue_sound(self.sound_manager.beginning)
        pygame.display.set_icon(self.images.pacman)

    def emit(self, new_state):
        if new_state != self.state:
            self.state = new_state
            if new_state == "game_over":
                self.player.death_tick = self.tick
                self.sound_manager.queue_sound(self.sound_manager.death)
            elif new_state == "game_running":
                self.reset()

    def on_key_down(self, key):
        if self.state == "game_running":
            self.player.on_key_down(key)
        elif self.state == "game_over":
            self.emit("game_running")

    def setScreen(self, screen):
        # We don't really need pgz screen anymore for game logic,
        # but pgzrun passes it.
        pass
