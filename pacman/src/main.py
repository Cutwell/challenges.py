import pgzrun
from game import Game

SCALE = 2
GAME_WIDTH = 224 * SCALE
GAME_HEIGHT = 248 * SCALE
UI_HEIGHT = 40 * SCALE

WIDTH = GAME_WIDTH
HEIGHT = GAME_HEIGHT + UI_HEIGHT
TITLE = "Pac-man"

game = Game(images, keys, width=GAME_WIDTH, height=GAME_HEIGHT, scale=SCALE)
game.window_width = WIDTH
game.window_height = HEIGHT
game.y_offset = UI_HEIGHT

def draw():
    game.draw()

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
