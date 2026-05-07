import pygame

from spriteloader import SpriteSheet
from sound import SoundManager
from player import Player
from pellets import Pellet, pellet_coords, powerup_coords
from ghosts import Ghost


class Game:
    def __init__(self, images, keys, width, height, scale) -> None:
        self.score = 0
        self.keys = keys
        self.images = images
        self.screen = None
        self.scale = scale
        self.game_width = width
        self.game_height = height
        self.window_width = width
        self.window_height = height
        self.y_offset = 0  # Can be set later or passed in
        self.state = "game_running"
        self.offset = 4 * self.scale
        self.sheet = SpriteSheet("spritesheet", scale=self.scale)
        self.tick = 0
        self.isSetup = False
        self.background = pygame.transform.scale(
            self.images.bg, (self.game_width, self.game_height)
        )
        self.ui_background = pygame.transform.scale(
            self.images.ui, (self.game_width, 40 * self.scale)
        )
        self.sound_manager = SoundManager(self)
        self.player = Player(game=self, x=self.offset, y=self.offset)
        self.pellets = []
        for p in pellet_coords:
            self.pellets.append(
                Pellet(
                    game=self,
                    x=p[0] * self.scale,
                    y=p[1] * self.scale - 48,
                    is_powerup=False,
                )
            )
        for p in powerup_coords:
            self.pellets.append(
                Pellet(
                    game=self,
                    x=p[0] * self.scale,
                    y=p[1] * self.scale - 48,
                    is_powerup=True,
                )
            )

        self.ghosts = [
            Ghost(self, color, 104 * self.scale, 112 * self.scale)
            for color in ["red", "pink", "cyan", "orange"]
        ]

    def setScreen(self, screen):
        self.screen = screen

    def draw(self):
        self.screen.clear()
        self.screen.surface.blit(self.background, (0, self.y_offset))
        self.screen.surface.blit(self.ui_background, (0, 0))

        self.screen.draw.text(
            "1UP", (self.offset * 4, self.offset), fontname="pixel", fontsize=16
        )
        self.screen.draw.text(
            str(self.score),
            (self.offset * 4, self.offset * 4),
            fontname="pixel",
            fontsize=16,
        )

        self.screen.draw.text(
            "HIGH SCORE", (self.offset * 30, self.offset), fontname="pixel", fontsize=16
        )
        self.screen.draw.text(
            str(10000),
            (self.offset * 30, self.offset * 4),
            fontname="pixel",
            fontsize=16,
        )

        self.player.draw()
        for p in self.pellets:
            p.draw()
        for g in self.ghosts:
            g.draw()

        if self.state == "game_over":
            self.screen.draw.text(
                "GAME OVER",
                (self.window_width / 2 - 54, self.window_height * 0.6),
                fontname="pixel",
                fontsize=16,
                color="red",
            )

    def setup(self):
        self.sound_manager.queue_sound(self.sound_manager.beginning)
        pygame.display.set_icon(self.images.pacman)

    def reset(self):
        self.player.x, self.player.y = self.offset, self.offset
        self.tick = 0
        self.score = 0
        self.player.facing = "right"
        self.player.queued_facing = None
        self.player.death_tick = None
        self.player.powerup_end_ms = 0

        for g in self.ghosts:
            g.x, g.y = 104 * self.scale, 112 * self.scale
            g.state = "alive"

        for p in self.pellets:
            p.eaten = False

    def emit(self, new_state):
        if new_state != self.state:
            self.state = new_state

            if new_state == "game_over":
                self.player.death_tick = self.tick
                self.sound_manager.queue_sound(self.sound_manager.death)

            elif new_state == "game_running":
                self.reset()

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

        all_pellets_eaten = (
            True if self.pellets and all([p.eaten for p in self.pellets]) else False
        )
        if all_pellets_eaten:
            self.sound_manager.queue_sound(self.sound_manager.extrapac)
            for p in self.pellets:
                p.eaten = False

        self.sound_manager.update()

    def on_key_down(self, key):
        if self.state == "game_running":
            self.player.on_key_down(key)
        elif self.state == "game_over":
            self.emit("game_running")
