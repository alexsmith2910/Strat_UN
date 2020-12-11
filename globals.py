import pyglet
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder

finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always)

#use to comtrol offline multiplayer
offline_multi = False

# NOTE: currently being used since my keyboard seems to treak the numpad as OEM.
# set this to True if your numpad does nothing in 2 player mode (i.e not selecting the different buildings for P2)
distribution = False

p1_color = (150, 200, 255)
p2_color = (255, 100, 100)
p3_color = (160, 255, 100)
p4_color = (255, 255, 100)

p1_name = "Zestyy"
p2_name = "Elite"
p3_name = "AJS"
p4_name = "P4"

p1_HQL = True # HQ Life - flag for if the player's HQ is still in play
p2_HQL = True
p3_HQL = True
p4_HQL = True

astar_map = []
astar_matrix = None
game_objects = []
building_objects = []
turret_objects = []
troop_objects = []
player_num = 0
player_list = []
player1_lv1_res = 1000.0
player1_lv2_res = 0.0
player1_lv3_res = 0.0
player1_lv1_gen = 0.0
player1_lv2_gen = 0.0
player1_lv3_gen = 0.0
player2_lv1_res = 1000.0
player2_lv2_res = 0.0
player2_lv3_res = 0.0
player2_lv1_gen = 0.0
player2_lv2_gen = 0.0
player2_lv3_gen = 0.0
player1_x = 0
player1_y = 0
screenresx = 1500
screenresy = 1000
bg_tiles = []
bg_batch = pyglet.graphics.Batch()
grid_batch = pyglet.graphics.Batch()
overlay_batch = pyglet.graphics.Batch()
hud_batch = pyglet.graphics.Batch()
building_batch = pyglet.graphics.Batch()
small_troop_batch = pyglet.graphics.Batch()
medium_troop_batch = pyglet.graphics.Batch()
large_troop_batch = pyglet.graphics.Batch()
tracer_batch = pyglet.graphics.Batch()
building_costs = {"Target": (0, 0, 0), "Drill": (100, 0, 0), "Refinery": (500, 0, 0), "Oil_Rig": (500, 0, 0), "Basic_Turret": (1000, 0, 0), "Barracks": (500, 0, 0)}
barracks_selection = 0
code = ""
clickable = None
key_handler = pyglet.window.key.KeyStateHandler()


def get_centred_coords(self, x, y):
    x_remainder = x % 20
    y_remainder = y % 20
    x_centred = (x - x_remainder) + 10
    y_centred = (y - y_remainder) + 10
    return x_centred, y_centred