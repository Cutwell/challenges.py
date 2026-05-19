import pgzrun
from game import Game

SCALE = 2
GAME_WIDTH = 224 * SCALE
GAME_HEIGHT = 248 * SCALE
UI_HEIGHT = 40 * SCALE

WIDTH = GAME_WIDTH
HEIGHT = GAME_HEIGHT + UI_HEIGHT
TITLE = "Pac-man"

game = Game(images, keys, scale=SCALE)

def draw():
    game.draw(screen)

isSetup = False

def update():
    global isSetup
    if not isSetup:
        game.setScreen(screen)
        isSetup = True
    game.update()

def on_key_down(key):
    game.on_key_down(key)

pgzrun.go()
