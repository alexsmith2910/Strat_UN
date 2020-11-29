import pyglet
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
#from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.bi_a_star import BiAStarFinder
finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always)

#use to comtrol offline multiplayer
offline_multi = False

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
overlay_batch = pyglet.graphics.Batch()
bar_batch = pyglet.graphics.Batch()
building_batch = pyglet.graphics.Batch()
small_troop_batch = pyglet.graphics.Batch()
medium_troop_batch = pyglet.graphics.Batch()
large_troop_batch = pyglet.graphics.Batch()
tracer_batch = pyglet.graphics.Batch()
building_costs = {"Target": (0, 0, 0), "Drill": (100, 0, 0), "Refinery": (500, 0, 0), "Oil_Rig": (500, 0, 0), "Basic_Turret": (1000, 0, 0), "Barracks": (500, 0, 0)}
barracks_selection = 0
code = ""
key_handler = pyglet.window.key.KeyStateHandler()