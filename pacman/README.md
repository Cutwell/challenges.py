# Pac-man

## Getting started

* Install with `uv sync`
* Run with `uv run pgzrun src/main.py`

## About

This game is built using [Pygame Zero](https://pygame-zero.readthedocs.io/en/stable/introduction.html) (<-- the introduction linked here is recommended reading before progressing), a wrapper for [Pygame](https://www.pygame.org/docs/) intended for educative settings, simplfying Pygame and making it easier to use.

Both of these libraries are Python-based game frameworks, meaning their main focus is allowing a developer to draw graphics onto the game screen. Many files, such as `spriteloader.py`, or the `draw` methods in the various game object files, can be (mostly) ignored for this challenge (with the exception of small edits to the `draw` method in `game.py` for challenges 3 & 4).

Pac-man is a classic game, with a tight and simple game loop - small decisions around Ghost AI can turn the game from boring to addictive. The purpose of this challenge is to explore pathfinding algorithms, a core concept in computer science, as well as interacting with a codebase written by another developer, requriring you to understand their design decisions before you can start making your own changes.

To get started, I recommend you read through the core game loop - starting briefly in `main.py`, then progressing to `game.py` for core logic; how `__init__` and `update` work together to create the player, ghosts, and pellets, then updates them each game `tick` to let them interact.

Some features you will notice:

* Pac-man doesn't tell pellets they've been eaten, pellets check each `update` if Pac-man is nearby and notifies Pac-man that they have eaten _them_.
* Ghosts operate similarly - if they collide with Pac-man, they check what to do (do nothing if they're dead, die if Pac-man is powered up, or kill Pac-man in any other case), then inform the wider game if e.g.: we need to show a game over screen.

These features were deliberate design decisions - e.g.: in the case of pellets, I wanted the logic to eat a pellet to belong to the pellet itself, rather than Pac-man having to know exactly _which_ pellet it's eating and then tell it that it has been eaten (if you take a look at `collision.py` and how we use those methods, you'll understand that this way is easier than the alternative!).

Finally, since you can't ignore AI in software development; these challenges might be hard, but prevailing by yourself teaches far more than resorting to the use of AI to fix problems for you, and you'll become a far better developer as a result - good luck!

## Challenges

1. The Ghosts can't respawn! In original Pac-man, ghosts would path back to their spawnpoint then become "whole" again, but in this version they stay dead forever - implement basic pathing to guide the ghosts home from wherever they died on the maze.
2. The current Ghosts randomly roam the maze, bumping around corners - take a look at [here](https://pacman30thanniversary.net/pacman-ghost-movement-pattern/) to understand how the original Pac-man AI worked, and consider how to make some better AI.
3. High score doesn't get updated, even if you beat it - change it from a hard coded number to a variable tracked by `game` - maybe even save it onto the disk so it persists between games?
4. Pac-man doesn't have lives - one hit and it's game over! We have a "1UP" indicator in the game, but it's hard coded - change it to be a variable tracked by `game` - if Pac-man eats all the pellets in the maze, award them with an extra life, or if they die to a ghost but have an extra life remaining, replace the `GAME OVER` text with `CONTINUE`, resetting the game as normal but retaining their score (but if they die without any spare lives, that's the end!)

## Attribution

* Graphics obtained from https://www.spriters-resource.com/arcade/pacman/
* Sound effects obtained from https://www.classicgaming.cc/classics/pac-man/sounds
* Font obtained from https://www.dafont.com/pixel-3.font
