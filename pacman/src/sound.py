import pygame
from collections import deque

pygame.mixer.init()

class SoundManager:
    def __init__(self, game):
        self.game = game
        self.queue = deque()

        # Dedicated channel for effects
        self.channel = pygame.mixer.Channel(0)

        # Background/default looping sound
        self.chomp = pygame.mixer.Sound("src/sounds/pacman_chomp.wav")

        # Other sounds
        self.death = pygame.mixer.Sound("src/sounds/pacman_death.wav")
        self.beginning = pygame.mixer.Sound("src/sounds/pacman_beginning.wav")
        self.intermission = pygame.mixer.Sound("src/sounds/pacman_intermission.wav")
        self.eatfruit = pygame.mixer.Sound("src/sounds/pacman_eatfruit.wav")
        self.eatghost = pygame.mixer.Sound("src/sounds/pacman_eatghost.wav")
        self.extrapac = pygame.mixer.Sound("src/sounds/pacman_extrapac.wav")

        self.default_playing = False
        self.current_sound = None

    def queue_sound(self, sound):
        self.queue.append(sound)

    def play_priority(self, sound):
        """Interrupts the current sound if it's the same, and plays the new one immediately."""
        if self.current_sound == sound:
            self.channel.stop()
        self.queue.appendleft(sound)

    def get_length_ms(self, sound):
        return int(sound.get_length() * 1000)

    def update(self):
        # If we have something queued and we're just looping the default sound,
        # stop the default sound to allow the queued sound to play.
        if self.queue and self.default_playing:
            self.channel.stop()
            self.default_playing = False

        # If channel is idle, decide what to play next
        if not self.channel.get_busy():
            self.current_sound = None
            if self.queue:
                next_sound = self.queue.popleft()
                self.channel.play(next_sound)
                self.current_sound = next_sound
                self.default_playing = False
            else:
                # Nothing queued → keep chomp looping
                if not self.default_playing and self.game.state == "game_running":
                    self.channel.play(self.chomp, loops=-1)
                    self.current_sound = self.chomp
                    self.default_playing = True
