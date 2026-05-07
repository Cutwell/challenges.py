"""
spriteloader.py
---------------
Sprite loader for the Pac-Man spritesheet (224x248 px) for Pygame Zero (pgzrun).
Place spritesheet.png in your game's `images/` folder.

All animation frames — including Pac-Man directional walk — are retrieved
through a single unified call:

    surf = sheet.get_frame("pacman_walk_right", tick)
    surf = sheet.get_frame("ghost_red_left", tick)
    surf = sheet.get_frame("pacman_die", tick)

Animation definitions are plain lists of (sprite_name, transform) pairs.
Transforms handle flipping and rotating derived frames (e.g. pac-man up/down)
so no sprite data needs to be duplicated on the sheet.
"""

import pygame

# ---------------------------------------------------------------------------
# Sprite coordinate registry  (x, y, width, height)
# ---------------------------------------------------------------------------
SPRITES: dict[str, tuple[int, int, int, int]] = {

    # ── Pac-Man walk (left-facing source frames) ──────────────────────────────
    "pacman_open_left":     (  0,  0, 16, 16),
    "pacman_halfopen_left": ( 16,  0, 16, 16),
    "pacman_closed":        ( 32,  0, 16, 16),

    # ── Pac-Man death sequence ────────────────────────────────────────────────
    "pacman_die_0": ( 48,  0, 16, 16),
    "pacman_die_1": ( 64,  0, 16, 16),
    "pacman_die_2": ( 80,  0, 16, 16),
    "pacman_die_3": ( 96,  0, 16, 16),
    "pacman_die_4": (112,  0, 16, 16),
    "pacman_die_5": (128,  0, 16, 16),
    "pacman_die_6": (144,  0, 16, 16),
    "pacman_die_7": (160,  0, 16, 16),
    "pacman_die_8": (176,  0, 16, 16),

    # ── Pac-Man large (32×32) ─────────────────────────────────────────────────
    "pacman_large_open_right":     (  0, 16, 32, 32),
    "pacman_large_halfopen_right": ( 16, 16, 32, 32),
    "pacman_large_open_left":      ( 32, 16, 32, 32),
    "pacman_large_halfopen_left":  ( 48, 16, 32, 32),
    "pacman_large_closed":         ( 96, 16, 32, 32),

    # ── Fruits ────────────────────────────────────────────────────────────────
    "fruit_cherries":   ( 32, 48, 16, 16),
    "fruit_strawberry": ( 48, 48, 16, 16),
    "fruit_peach":      ( 64, 48, 16, 16),
    "fruit_apple":      ( 80, 48, 16, 16),
    "fruit_grapes":     ( 96, 48, 16, 16),
    "fruit_galaxian":   (112, 48, 16, 16),
    "fruit_bell":       (128, 48, 16, 16),
    "fruit_key":        (144, 48, 16, 16),

    # ── Ghost — Blinky (red)  y=64 cols 0–7 ──────────────────────────────────
    "ghost_red_right_1": (  0, 64, 16, 16),
    "ghost_red_right_2": ( 16, 64, 16, 16),
    "ghost_red_left_1":  ( 32, 64, 16, 16),
    "ghost_red_left_2":  ( 48, 64, 16, 16),
    "ghost_red_up_1":    ( 64, 64, 16, 16),
    "ghost_red_up_2":    ( 80, 64, 16, 16),
    "ghost_red_down_1":  ( 96, 64, 16, 16),
    "ghost_red_down_2":  (112, 64, 16, 16),

    # ── Ghost — Pinky (pink)  y=80 cols 0–7 ──────────────────────────────────
    "ghost_pink_right_1": (  0, 80, 16, 16),
    "ghost_pink_right_2": ( 16, 80, 16, 16),
    "ghost_pink_left_1":  ( 32, 80, 16, 16),
    "ghost_pink_left_2":  ( 48, 80, 16, 16),
    "ghost_pink_up_1":    ( 64, 80, 16, 16),
    "ghost_pink_up_2":    ( 80, 80, 16, 16),
    "ghost_pink_down_1":  ( 96, 80, 16, 16),
    "ghost_pink_down_2":  (112, 80, 16, 16),

    # ── Ghost — Inky (cyan)  y=96 cols 0–7 ───────────────────────────────────
    "ghost_cyan_right_1": (  0, 96, 16, 16),
    "ghost_cyan_right_2": ( 16, 96, 16, 16),
    "ghost_cyan_left_1":  ( 32, 96, 16, 16),
    "ghost_cyan_left_2":  ( 48, 96, 16, 16),
    "ghost_cyan_up_1":    ( 64, 96, 16, 16),
    "ghost_cyan_up_2":    ( 80, 96, 16, 16),
    "ghost_cyan_down_1":  ( 96, 96, 16, 16),
    "ghost_cyan_down_2":  (112, 96, 16, 16),

    # ── Ghost — Clyde (orange)  y=112 cols 0–7 ───────────────────────────────
    "ghost_orange_right_1": (  0, 112, 16, 16),
    "ghost_orange_right_2": ( 16, 112, 16, 16),
    "ghost_orange_left_1":  ( 32, 112, 16, 16),
    "ghost_orange_left_2":  ( 48, 112, 16, 16),
    "ghost_orange_up_1":    ( 64, 112, 16, 16),
    "ghost_orange_up_2":    ( 80, 112, 16, 16),
    "ghost_orange_down_1":  ( 96, 112, 16, 16),
    "ghost_orange_down_2":  (112, 112, 16, 16),

    # ── Ghost — Frightened (blue)  y=64 cols 8–9 ─────────────────────────────
    # Pixel-verified: dark blue body frames at x=128,144 on the Blinky row.
    # Only 2 unique frightened frames on this trimmed sheet; cycled twice to
    # produce a 4-step animation.
    "ghost_frightened_1": (128, 64, 16, 16),
    "ghost_frightened_2": (144, 64, 16, 16),
    "ghost_frightened_3": (128, 64, 16, 16),   # repeat of frame 1
    "ghost_frightened_4": (144, 64, 16, 16),   # repeat of frame 2

    # ── Ghost — Flashing (power expiring)  y=64 cols 10–11 ───────────────────
    # Pixel-verified: pinkish/white flash frames at x=160,176 on the Blinky row.
    "ghost_flashing_1": (160, 64, 16, 16),
    "ghost_flashing_2": (176, 64, 16, 16),

    # ── Ghost — Dead (eyes only)  y=80 cols 8–11 ─────────────────────────────
    # Pixel-verified: muted blue-purple eye sprites at x=128–176 on the Pinky row.
    "ghost_dead_right": (128, 80, 16, 16),
    "ghost_dead_left":  (144, 80, 16, 16),
    "ghost_dead_up":    (160, 80, 16, 16),
    "ghost_dead_down":  (176, 80, 16, 16),

    # ── Ghost eyes (directional, living ghosts)  — same cells as dead eyes ───
    # Kept as aliases for compatibility; same coords as ghost_dead_*.
    "ghost_eye_right": (128, 80, 16, 16),
    "ghost_eye_left":  (144, 80, 16, 16),
    "ghost_eye_up":    (160, 80, 16, 16),
    "ghost_eye_down":  (176, 80, 16, 16),
}


# ---------------------------------------------------------------------------
# Transform helpers — applied after cropping the raw sprite
# ---------------------------------------------------------------------------
FLIP_H = ("flip", True, False)
FLIP_V = ("flip", False, True)
ROT_90 = ("rotate", 90)  # counter-clockwise — faces up
ROT_270 = ("rotate", 270)  # clockwise — faces down


def _apply_transform(surf: pygame.Surface, transform) -> pygame.Surface:
    kind = transform[0]
    if kind == "flip":
        return pygame.transform.flip(surf, transform[1], transform[2])
    if kind == "rotate":
        return pygame.transform.rotate(surf, transform[1])
    raise ValueError(f"Unknown transform: {kind!r}")


# ---------------------------------------------------------------------------
# Animation definitions
#
# Each entry is a list of frames. A frame is either:
#   "sprite_name"                      — raw sprite, no transform
#   ("sprite_name", TRANSFORM, ...)    — sprite with one or more transforms
#
# Pac-Man up/down are derived from the left frames so nothing is duplicated.
# ---------------------------------------------------------------------------
ANIMATIONS: dict[str, list] = {
    # --- Pac-Man walk -------------------------------------------------------
    # right: explicit frames (flipped to face right)
    "pacman_walk_right": [
        "pacman_open_left",
        "pacman_halfopen_left",
        "pacman_closed",
        "pacman_halfopen_left",
    ],
    # left: horizontal flip of right frames
    "pacman_walk_left": [
        ("pacman_open_left", FLIP_H),
        ("pacman_halfopen_left", FLIP_H),
        ("pacman_closed", FLIP_H),
        ("pacman_halfopen_left", FLIP_H),
    ],
    # up: rotate right frames 90° CCW
    "pacman_walk_up": [
        ("pacman_open_left", ROT_90),
        ("pacman_halfopen_left", ROT_90),
        ("pacman_closed", ROT_90),
        ("pacman_halfopen_left", ROT_90),
    ],
    # down: rotate right frames 90° CW
    "pacman_walk_down": [
        ("pacman_open_left", ROT_270),
        ("pacman_halfopen_left", ROT_270),
        ("pacman_closed", ROT_270),
        ("pacman_halfopen_left", ROT_270),
    ],
    # --- Pac-Man death -------------------------------------------------------
    "pacman_die": [
        "pacman_die_0",
        "pacman_die_1",
        "pacman_die_2",
        "pacman_die_3",
        "pacman_die_4",
        "pacman_die_5",
        "pacman_die_6",
        "pacman_die_7",
        "pacman_die_8",
    ],
    # --- Ghosts --------------------------------------------------------------
    "ghost_red_right": ["ghost_red_right_1", "ghost_red_right_2"],
    "ghost_red_left": ["ghost_red_left_1", "ghost_red_left_2"],
    "ghost_red_up": ["ghost_red_up_1", "ghost_red_up_2"],
    "ghost_red_down": ["ghost_red_down_1", "ghost_red_down_2"],
    "ghost_pink_right": ["ghost_pink_right_1", "ghost_pink_right_2"],
    "ghost_pink_left": ["ghost_pink_left_1", "ghost_pink_left_2"],
    "ghost_pink_up": ["ghost_pink_up_1", "ghost_pink_up_2"],
    "ghost_pink_down": ["ghost_pink_down_1", "ghost_pink_down_2"],
    "ghost_cyan_right": ["ghost_cyan_right_1", "ghost_cyan_right_2"],
    "ghost_cyan_left": ["ghost_cyan_left_1", "ghost_cyan_left_2"],
    "ghost_cyan_up": ["ghost_cyan_up_1", "ghost_cyan_up_2"],
    "ghost_cyan_down": ["ghost_cyan_down_1", "ghost_cyan_down_2"],
    "ghost_orange_right": ["ghost_orange_right_1", "ghost_orange_right_2"],
    "ghost_orange_left": ["ghost_orange_left_1", "ghost_orange_left_2"],
    "ghost_orange_up": ["ghost_orange_up_1", "ghost_orange_up_2"],
    "ghost_orange_down": ["ghost_orange_down_1", "ghost_orange_down_2"],
    "ghost_frightened": [
        "ghost_frightened_1",
        "ghost_frightened_2",
        "ghost_frightened_3",
        "ghost_frightened_4",
    ],
    "ghost_flashing": [
        "ghost_frightened_1",
        "ghost_flashing_1",
        "ghost_frightened_2",
        "ghost_flashing_2",
        "ghost_frightened_3",
        "ghost_flashing_1",
        "ghost_frightened_4",
        "ghost_flashing_2",
    ],
    "ghost_dead_right": ["ghost_dead_right"],
    "ghost_dead_left": ["ghost_dead_left"],
    "ghost_dead_up": ["ghost_dead_up"],
    "ghost_dead_down": ["ghost_dead_down"],
}


# ---------------------------------------------------------------------------
# SpriteSheet
# ---------------------------------------------------------------------------


class SpriteSheet:
    """
    Loads a spritesheet and exposes a single get_frame() call for all animations.

    Parameters
    ----------
    image_name : str
        Filename without extension, resolved from your images/ folder.
    scale : int
        Integer pixel-art scale (default 1 = native 16px).

    Example
    -------
        sheet = SpriteSheet("spritesheet", scale=2)

        def draw():
            screen.surface.blit(sheet.get_frame("pacman_walk_right", tick), (x, y))
            screen.surface.blit(sheet.get_frame("ghost_red_left", tick), (gx, gy))
    """

    def __init__(self, image_name: str, scale: int = 1):
        import pgzero.loaders

        self._surface: pygame.Surface = pgzero.loaders.images.load(image_name)
        self.scale = scale
        self._sprite_cache: dict[str, pygame.Surface] = {}
        self._frame_cache: dict[tuple, pygame.Surface] = {}

    def _get_sprite(self, name: str) -> pygame.Surface:
        """Crop and scale a single named sprite, cached."""
        if name not in self._sprite_cache:
            if name not in SPRITES:
                raise KeyError(f"Unknown sprite '{name}'.")
            x, y, w, h = SPRITES[name]
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            surf.blit(self._surface, (0, 0), area=pygame.Rect(x, y, w, h))
            if self.scale != 1:
                surf = pygame.transform.scale(surf, (w * self.scale, h * self.scale))
            self._sprite_cache[name] = surf
        return self._sprite_cache[name]

    def get_frame(
        self, anim_name: str, tick: int, frame_speed: int = 6
    ) -> pygame.Surface:
        """
        Return the correct animation frame Surface for the given tick.

        Works identically for Pac-Man walk (all directions), ghosts, death —
        any animation defined in ANIMATIONS.

        Parameters
        ----------
        anim_name : str
            Key from ANIMATIONS, e.g. "pacman_walk_right", "ghost_red_left".
        tick : int
            Monotonically increasing frame counter from your update loop.
        frame_speed : int
            Ticks to hold each frame before advancing (default 6).

        Returns
        -------
        pygame.Surface

        Example
        -------
            surf = sheet.get_frame("pacman_walk_up", tick)
            screen.surface.blit(surf, (pac_x, pac_y))
        """
        if anim_name not in ANIMATIONS:
            raise KeyError(f"Unknown animation '{anim_name}'.")

        frames = ANIMATIONS[anim_name]
        frame = frames[(tick // frame_speed) % len(frames)]

        # Cache key includes the exact frame spec so transforms are only done once
        cache_key = (frame,) if isinstance(frame, str) else frame
        if cache_key not in self._frame_cache:
            if isinstance(frame, str):
                surf = self._get_sprite(frame)
            else:
                sprite_name, *transforms = frame
                surf = self._get_sprite(sprite_name)
                # Copy so we don't mutate the cached sprite
                surf = surf.copy()
                for t in transforms:
                    surf = _apply_transform(surf, t)
            self._frame_cache[cache_key] = surf

        return self._frame_cache[cache_key]

    def get_frame_once(
        self, anim_name: str, tick: int, frame_speed: int = 6
    ) -> pygame.Surface:
        """
        Non-looping animation.
        Stops on the final frame instead of wrapping.
        """

        if anim_name not in ANIMATIONS:
            raise KeyError(f"Unknown animation '{anim_name}'.")

        frames = ANIMATIONS[anim_name]

        index = min(tick // frame_speed, len(frames) - 1)
        frame = frames[index]

        cache_key = ("once", frame) if isinstance(frame, str) else ("once", *frame)

        if cache_key not in self._frame_cache:
            if isinstance(frame, str):
                surf = self._get_sprite(frame)
            else:
                sprite_name, *transforms = frame
                surf = self._get_sprite(sprite_name).copy()
                for t in transforms:
                    surf = _apply_transform(surf, t)

            self._frame_cache[cache_key] = surf

        return self._frame_cache[cache_key]

    def draw_frame(
        self, screen, anim_name: str, tick: int, x: int, y: int, frame_speed: int = 6
    ):
        """Convenience: get_frame + blit in one call."""
        screen.surface.blit(self.get_frame(anim_name, tick, frame_speed), (x, y))

    def draw_frame_centered(
        self, screen, anim_name: str, tick: int, cx: int, cy: int, frame_speed: int = 6
    ):
        """Convenience: get_frame + blit centred on (cx, cy)."""
        surf = self.get_frame(anim_name, tick, frame_speed)
        screen.surface.blit(
            surf, (cx - surf.get_width() // 2, cy - surf.get_height() // 2)
        )