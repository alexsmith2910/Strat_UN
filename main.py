import random
import math
import inspect
import secrets
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from pyglet.graphics import *
import objects
import animations
import globals

pyglet.font.add_file("BebasNeue-Regular.otf")
# bebas_neue = pyglet.font.load("Bebas Neue")

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

class game_window(pyglet.window.Window):
    def __init__(self):
        super().__init__()#self, game_window
        self.set_vsync(False)
        self.player_image = pyglet.image.load("Test-sprite.png")
        self.player_image.anchor_x = 10
        self.player_image.anchor_y = 10
        self.set_size(globals.screenresx, globals.screenresy)
        self.player_sprite = objects.Player(x=550, y=550)
        self.player_sprite.set_id("Zestyy", 1)
        globals.troop_objects.append(objects.Dev_Tank(x=410, y=490))
        print(globals.troop_objects)
        globals.troop_objects[len(globals.troop_objects) - 1].set_owner(("Zestyy", 1))
        self.push_handlers(self.player_sprite)
        self.push_handlers(self.player_sprite.key_handler)
        self.game_objects = [self.player_sprite]
        self.squares, self.bg_batch = self.tiles_map()
        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.input_text = ''
        self.firstt = True  # this serves to avoid the first 't' used to activate the typing,
        # not to get stored as first character of the input_text.
        self.main_key_handler = key.KeyStateHandler()
        self.gen_overlay()

        # Data parts for overlay
        self.show_overlay = False
        self.ol_counter = 0

    def gen_overlay(self, xres = globals.screenresx, yres = globals.screenresy):
        self.overlay_bg = pyglet.shapes.Rectangle(450, 0, 500, 300, (0, 0, 0), batch=globals.overlay_batch)
        self.overlay_bg.opacity = 150
        self.overlay_bg_frameh = pyglet.shapes.Line(450, 300, 950, 300, 1, (255, 255, 255), batch=globals.overlay_batch)
        self.overlay_bg_framev1 = pyglet.shapes.Line(450, 0, 450, 300, 1, (255, 255, 255), batch=globals.overlay_batch)
        self.overlay_bg_framev2 = pyglet.shapes.Line(950, 0, 950, 300, 1, (255, 255, 255), batch=globals.overlay_batch)
        self.mineral_text = "Mineral text here"
        self.metal_text = "Metal text here"
        self.oil_text = "Oil text here"
        self.selection_text = "Selection text here"
        self.clickable_text = ""
        self.clickable_text_temp = ""
        self.overlay_mineral_label = pyglet.text.Label(self.mineral_text,
                                               font_name='Bebas Neue',
                                               font_size=15,
                                               x=455, y=280, batch=globals.overlay_batch)
        self.overlay_metal_label = pyglet.text.Label(self.metal_text,
                                                       font_name='Bebas Neue',
                                                       font_size=15,
                                                       x=455, y=260, batch=globals.overlay_batch)
        self.overlay_oil_label = pyglet.text.Label(self.oil_text,
                                                       font_name='Bebas Neue',
                                                       font_size=15,
                                                       x=455, y=240, batch=globals.overlay_batch)
        self.overlay_selection_label = pyglet.text.Label(self.selection_text,
                                                   font_name='Bebas Neue',
                                                   font_size=15,
                                                   x=455, y=220, batch=globals.overlay_batch)
        self.overlay_clickable_label = pyglet.text.Label(self.clickable_text,
                                                         font_name='Bebas Neue',
                                                         font_size=15,
                                                         x=455, y=200, batch=globals.overlay_batch)
                                               #anchor_x='center', anchor_y='center'


    def update(self, dt):
        #super(game_window, self).update(dt)
        #print(self.game_objects)
        for obj in self.game_objects:
            obj.update(dt)
            obj.check_bounds()
        for i in globals.building_objects:
            i.update(dt)
        for i in globals.troop_objects:
            i.update(dt)

        # Overlay editing
        self.mineral_text = ("Mineral: " + str(round(globals.player1_lv1_res, 1)) + " (" + str(round(globals.player1_lv1_gen, 2)) + "/s)")  # ℤens
        self.overlay_mineral_label.text = self.mineral_text # TODO: continue with overlay to replace data window
        self.metal_text = ("Metal: " + str(round(globals.player1_lv2_res, 1)) + " (" + str(round(globals.player1_lv2_gen, 2)) + "/s)")  # ℤens
        self.overlay_metal_label.text = self.metal_text
        self.oil_text = ("Oil: " + str(round(globals.player1_lv3_res, 1)) + " (" + str(round(globals.player1_lv3_gen, 2)) + "/s)")  # ℤens
        self.overlay_oil_label.text = self.oil_text
        self.selection_text_temp = str(game_window_run.player_sprite.get_select()).split("'")
        self.selection_text_temp = str((self.selection_text_temp[1])[8:])
        self.selection_text = "Selection: " + str(self.selection_text_temp)
        self.overlay_selection_label.text = self.selection_text
        self.clickable_text = "Mouse last selected: " + self.clickable_text_temp
        self.overlay_clickable_label.text = self.clickable_text
        # if self.main_key_handler[key.ENTER] and self.ol_counter == 0:
        #     self.show_overlay = not(self.show_overlay)
        #     print(self.show_overlay)
        #     self.ol_counter += dt

        if self.ol_counter > 0:
            self.ol_counter += dt

        if self.ol_counter >= 1:
            self.ol_counter = 0 if self.ol_counter >= 1 else self.ol_counter

    def on_text(self, text):
        if self.firstt == True and self.input_text == 't':
            self.input_text = ''
            self.firstt = False
        self.input_text += text
        # if Typein.firstt != True:
        #     Labels.playername_label.input_text = Typein.input_text
        # Control.CurrentPlayer.name = Typein.input_text
    # @staticmethod
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER:
            globals.code = self.input_text.upper()
            self.input_text = ''
            if globals.code == "MEMENTOMORI":
                for i in globals.building_objects:
                    if i.get_building_type() == "Drill":
                        i.image = animations.animations.DUA_ani
                        objects.Drill.image = animations.animations.DUA_ani
        elif symbol == key.SLASH:
            self.show_overlay = not(self.show_overlay)
            # Control.handleraltered = False
        elif symbol == key.BACKSPACE:
            self.input_text = self.input_text[:-1]
            # Labels.playername_label.input_text = Typein.input_text
        elif symbol:
            return True
    def on_mouse_press(self, x, y, button, modifiers):
        print(str(button) + "Pressed at: " + str(x) + " " + str(y))
        x_remainder = x % 20
        y_remainder = y % 20
        x_centred = (x - x_remainder) + 10
        y_centred = (y - y_remainder) + 10
        self.clickable_text_temp = (str(x_centred) + " " + str(y_centred))

        print("You clicked on the tile centred at " + str(x_centred) + " " + str(y_centred))
    def on_draw(self):
        self.clear()
        self.bg_batch.draw()
        for i in globals.building_objects:
            if i.get_building_type() == "Tracing turret":
                i.get_tracer().draw()
            i.draw()
        for i in globals.troop_objects:
            if i.get_weapon_tracing():
                i.get_tracer().draw()
            i.draw()
        self.player_sprite.draw()
        if self.show_overlay:
            globals.overlay_batch.draw()
        self.fps_display.draw()

    def get_game_objects(self):
        return self.game_objects

    def tiles_map(self, resx=globals.screenresx, resy=globals.screenresy, size=20):
        ylayers = resy // size
        print(ylayers)
        print(ylayers)
        tiles = []
        for i in range(ylayers):
            tiles.append([])
            globals.astar_map.append([])
            # print(str(len(tiles)) + ";ayers")
        tilebatch = pyglet.graphics.Batch()
        for i in range(resy // size):
            # print("layer" + str(i))
            for j in range(resx // size):
                # r = secrets.randbelow(255)
                g = secrets.randbelow(128)
                g2 = secrets.randbelow(64)
                g3 = g - g2
                if g3 < 1:
                    g3 = 20
                g3 += 25
                # b = secrets.randbelow(255)
                tiles[i - 1].append(
                    objects.TileBG(x=size * j, y=size * i, width=size, height=size, color=(0, g3, 0),
                                   batch=tilebatch))
                globals.astar_map[i-1].append(1)
        globals.astar_map.insert(0, [])
        for i in range(resx // size):
            globals.astar_map[0].append(-1)

        for i in range(len(tiles)):
            choice = secrets.randbelow(3)
            if choice == 0:
                x_choice = secrets.randbelow(16)
                (tiles[i])[x_choice].color = (0, 0, 255)
                (tiles[i])[x_choice].make_barrier()
                (globals.astar_map[i])[x_choice] = -1

                val_list = []
                for i in range(4):
                    for i in range(10):
                        val_list.append(secrets.randbelow(2))
                    if val_list[0] == 1:
                        (tiles[i])[x_choice - 1].color = (100, 100, 255)
                        (tiles[i])[x_choice - 1].make_barrier()
                        (globals.astar_map[i])[x_choice - 1] = -1
                    elif val_list[1] == 1:
                        (tiles[i])[x_choice + 1].color = (100, 100, 255)
                        (tiles[i])[x_choice + 1].make_barrier()
                        (globals.astar_map[i])[x_choice + 1] = -1
                    elif val_list[2] == 1:
                        (tiles[i - 1])[x_choice].color = (100, 100, 255)
                        (tiles[i - 1])[x_choice].make_barrier()
                        (globals.astar_map[i - 1])[x_choice] = -1
                    elif val_list[3] == 1 and i < resy // 2:
                        (tiles[i + 1])[x_choice].color = (100, 100, 255)
                        (tiles[i + 1])[x_choice].make_barrier()
                        (globals.astar_map[i + 1])[x_choice] = -1
        globals.astar_matrix = Grid(matrix=globals.astar_map)

        # start = globals.astar_matrix.node(0, 0)
        # end = globals.astar_matrix.node(2, 17)
        #
        # finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        # path, runs = finder.find_path(start, end, globals.astar_matrix)
        #
        # print('operations:', runs, 'path length:', len(path))
        # print("Path: ", path)
        # print(globals.astar_matrix.grid_str(path=path, start=start, end=end))

        return tiles, tilebatch

class data_window(pyglet.window.Window):
    def __init__(self):
        super().__init__()#self, game_window

        self.set_vsync(False)
        self.mineral_text = "mineral count here"
        self.mineral_label = pyglet.text.Label(self.mineral_text,
                                               font_name='Bebas Neue',
                                               font_size=36,
                                               x=self._width//2, y=(self._height//2)+40,
                                               anchor_x='center', anchor_y='center')

        self.metal_text = "metal count here"
        self.metal_label = pyglet.text.Label(self.mineral_text,
                                               font_name='Bebas Neue',
                                               font_size=36,
                                               x=self._width//2, y=self._height//2,
                                               anchor_x='center', anchor_y='center')

        self.selection_text = "selection of building here"
        self.selection_label = pyglet.text.Label(self.selection_text,
                                  font_name='Bebas Neue',
                                  font_size=36,
                                  x=self._width//2, y=(self._height//2)-40,
                                  anchor_x='center', anchor_y='center')

        pyglet.clock.schedule_interval(self.update, 1 / 120.0)


    def update(self, dt):
        self.mineral_text = ""
        #print(building_objects)
            # self.mineral_text += str(i)
        self.mineral_text = "Mineral: " + str(round(globals.player1_lv1_res, 1))#ℤens
        self.mineral_label.text = self.mineral_text
        self.metal_text = "Metal: " + str(round(globals.player1_lv2_res, 1))#ℤens
        self.metal_label.text = self.metal_text
        self.selection_text_temp = str(game_window_run.player_sprite.get_select()).split("'")
        self.selection_text_temp = str((self.selection_text_temp[1])[8:])
        self.selection_text = "Selection: " + str(self.selection_text_temp)
        self.selection_label.text = self.selection_text
        # print(globals.code)
    def on_draw(self):
        self.clear()
        self.mineral_label.draw()
        self.metal_label.draw()
        self.selection_label.draw()


# label = pyglet.input_text.Label('Fuck off nick', j
#                           font_name='Have Heart One',
#                           font_size=36,
#                           x=game_window.width//2, y=game_window.height//2,
#                           anchor_x='center', anchor_y='center')


    #vertex_list = pyglet.graphics.vertex_list(1024, 'v3f', 'c4B', 't2f', 'n3f')
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)#used to find events to connect to commands

game_window_run = game_window()#width = screenresx, height=screenresy
# data_window_run = data_window() # Deprecated - overlay replaces data window

# class Typein(object):


pyglet.app.run()# kek or cringe


