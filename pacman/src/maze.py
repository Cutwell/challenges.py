import pygame

MAZE = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#P####.#####.##.#####.####P#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "######.#####.##.#####.######",
    "######.##..........##.######",
    "######.##.###  ###.##.######",
    "######.##.#--  --#.##.######",
    "          #--  --#          ",
    "######.##.#--  --#.##.######",
    "######.##.########.##.######",
    "######.##..........##.######",
    "######.##.########.##.######",
    "######.##.########.##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#P..##................##..P#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################",
]


class Maze:
    def __init__(self, game):
        self.game = game
        self.size = 8
        self.tiles = {
            "h": pygame.transform.scale(game.images.straight_tile_h, (8, 8)),
            "v": pygame.transform.scale(game.images.straight_tile_v, (8, 8)),
            "0": pygame.transform.scale(game.images.corner_tile_0, (8, 8)),
            "90": pygame.transform.scale(game.images.corner_tile_90, (8, 8)),
            "180": pygame.transform.scale(game.images.corner_tile_180, (8, 8)),
            "270": pygame.transform.scale(game.images.corner_tile_270, (8, 8)),
        }

    def is_wall(self, r, c):
        return 0 <= r < len(MAZE) and 0 <= c < len(MAZE[0]) and MAZE[r][c] == "#"

    def draw(self, canvas, offset_y=0):
        for r, row in enumerate(MAZE):
            for c, char in enumerate(row):
                if char != "#": continue
                
                u, d, l, r_ = self.is_wall(r-1, c), self.is_wall(r+1, c), self.is_wall(r, c-1), self.is_wall(r, c+1)
                if u and d and l and r_: continue # internal wall

                # Priority: Corners
                if d and l and not u and not r_: tile = self.tiles["0"]
                elif d and r_ and not u and not l: tile = self.tiles["90"]
                elif u and r_ and not d and not l: tile = self.tiles["180"]
                elif u and l and not d and not r_: tile = self.tiles["270"]
                # Straights and Junctions
                elif (u and d) and not (l or r_): tile = self.tiles["v"]
                elif (l and r_) and not (u or d): tile = self.tiles["h"]
                elif u and d: tile = self.tiles["v"]
                elif l and r_: tile = self.tiles["h"]
                elif u or d: tile = self.tiles["v"]
                else: tile = self.tiles["h"]

                canvas.blit(tile, (c * self.size, r * self.size + offset_y))
