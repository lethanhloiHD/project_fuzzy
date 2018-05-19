import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 64*18   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 64*12 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap"
# BGCOLOR = BROWN

TILESIZE = 64
# GRIDWIDTH = WIDTH / TILESIZE
# GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'
STONE_IMG= 'stone.png'
MAKER_IMG_S ='flag.png'
MAKER_IMG_E ='fl.png'
TRAFFIC_IMG='traffic-lights.png'

# Car settings
PLAYER_SPEED = 100
PLAYER_IMG = 'car_2.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
# BARREL_OFFSET = vec(30, 10)
