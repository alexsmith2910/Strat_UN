import pyglet
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder
from socket import gethostname
import configparser

settings = configparser.ConfigParser()
settings.read("settings.ini")

if settings["ONLINE"]["address"] == "localhost":
    recipient = gethostname()
else:
    recipient = settings["ONLINE"]["address"]

finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always)

#use to comtrol offline multiplayer
offline_multi = False

# Online multiplayer control and data storage
online_multi = True

online_sending = {}
online_received = {}

onl_r_spawns = {}

# NOTE: currently being used since my keyboard seems to treat the numpad as OEM.
# set this to True if your numpad does nothing in 2 player mode (i.e not selecting the different buildings for P2)
distribution = False

bg_batch = pyglet.graphics.Batch()
grid_batch = pyglet.graphics.Batch()
data_overlay_batch = pyglet.graphics.Batch()
research_overlay_batch = pyglet.graphics.Batch()
hud_batch = pyglet.graphics.Batch()
building_batch = pyglet.graphics.Batch()
small_troop_batch = pyglet.graphics.Batch()
medium_troop_batch = pyglet.graphics.Batch()
large_troop_batch = pyglet.graphics.Batch()
tracer_batch = pyglet.graphics.Batch()

game_batch = pyglet.graphics.Batch()
data_overlay_batch = pyglet.graphics.Batch()
research_overlay_batch = pyglet.graphics.Batch()

map_group = pyglet.graphics.OrderedGroup(0)
grid_group = pyglet.graphics.OrderedGroup(1)
s_building_group = pyglet.graphics.OrderedGroup(2)
m_building_group = pyglet.graphics.OrderedGroup(3)
l_building_group = pyglet.graphics.OrderedGroup(4)
s_troop_group = pyglet.graphics.OrderedGroup(5)
m_troop_group = pyglet.graphics.OrderedGroup(6)
l_troop_group = pyglet.graphics.OrderedGroup(7)
player_group = pyglet.graphics.OrderedGroup(8)
trace_group = pyglet.graphics.OrderedGroup(9)
ol_bg_group = pyglet.graphics.OrderedGroup(10)
ol_border_group = pyglet.graphics.OrderedGroup(11)
ol_prim_group = pyglet.graphics.OrderedGroup(12)
ol_fg_group = pyglet.graphics.OrderedGroup(13)


p1_color = (150, 200, 255)
p2_color = (255, 100, 100)
p3_color = (160, 255, 100)
p4_color = (255, 255, 100)

p1_name = "Zestyy"
p2_name = "The creep"
p3_name = "Smuuvi"
p4_name = "AJS"

p1_HQL = True # HQ Life - flag for if the player's HQ is still in play
p2_HQL = True
p3_HQL = True
p4_HQL = True

p1Pos = [0, 0]
p2Pos = [0, 0]
p3Pos = [0, 0]
p4Pos = [0, 0]

h_bar_colour = (15, 255, 0)
s_bar_colour = (25, 82, 255)

astar_map = []
astar_matrix = None
game_objects = []
building_objects = []
turret_objects = []
troop_objects = []

player_num = 0
player_list = []

p1_researched_list = []
p2_researched_list = []

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