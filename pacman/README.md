# Pac-man

## Getting started

* Install with `uv sync`
* Run with `uv run pgzrun src/main.py`

## Challenges

1. The Ghosts can't respawn! In original Pac-man, ghosts would path back to their spawnpoint then become "whole" again, but in this version they stay dead forever - implement basic pathing to guide the ghosts home from wherever they died on the maze.
2. The current Ghosts randomly roam the maze, bumping around corners - take a look at [here](https://pacman30thanniversary.net/pacman-ghost-movement-pattern/) to understand how the original Pac-man AI worked, and consider how to make some better AI.
3. High score doesn't get updated, even if you beat it - change it from a hard coded number to a variable tracked by `game` - maybe even save it onto the disk so it persists between games?
4. Pac-man doesn't have lives - one hit and it's game over! We have a "1UP" indicator in the game, but it's hard coded - change it to be a variable tracked by `game` - if Pac-man eats all the pellets in the maze, award them with an extra life, or if they die to a ghost but have an extra life remaining, replace the `GAME OVER` text with `CONTINUE`, resetting the game as normal but retaining their score (but if they die without any spare lives, that's the end!)

## Attribution

* Graphics obtained from https://www.spriters-resource.com/arcade/pacman/
* Sound effects obtained from https://www.classicgaming.cc/classics/pac-man/sounds
* Font obtained from https://www.dafont.com/pixel-3.font
