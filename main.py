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
from pathfinding.finder.bi_a_star import BiAStarFinder

finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always)


class game_window(pyglet.window.Window):
    def __init__(self):
        super().__init__()  # self, game_window
        self.set_vsync(False)
        self.player_image = pyglet.image.load("P1-sprite.png")
        self.player_image.anchor_x = 10
        self.player_image.anchor_y = 10
        self.set_size(globals.screenresx, globals.screenresy)
        self.player_one = objects.Player(x=550, y=550)
        self.player_one.set_id("Zestyy", 1)
        self.game_objects = [self.player_one]
        if globals.offline_multi:
            self.player_two = objects.Player(x=650, y=650)
            self.player_two.set_id("Guest", 2)
            self.game_objects.append(self.player_two)
        globals.troop_objects.append(objects.Dev_Tank(x=410, y=490))
        globals.troop_objects[len(globals.troop_objects) - 1].set_owner(("Zestyy", 1))
        # globals.troop_objects.append(objects.Dev_Tank(x=710, y=710))
        # globals.troop_objects[len(globals.troop_objects) - 1].set_owner(("Guest", 2))
        # globals.troop_objects.append(objects.Dev_Tank(x=990, y=210))
        # globals.troop_objects[len(globals.troop_objects) - 1].set_owner(("Frenemy", 3))
        # globals.troop_objects.append(objects.Dev_Tank(x=210, y=710))
        # globals.troop_objects[len(globals.troop_objects) - 1].set_owner(("Pixie", 4))
        # self.push_handlers(self.player_one)
        self.push_handlers(globals.key_handler)
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
        self.clicked_object = None

    def gen_overlay(self, xres=globals.screenresx, yres=globals.screenresy):
        #TODO: make overlay compatible with 2 player play, either if else 2 generations or let the original be generated then move
        if not globals.offline_multi:
            self.overlay_bg = pyglet.shapes.Rectangle(500, 0, 500, 300, (0, 0, 0), batch=globals.overlay_batch)
            self.overlay_bg.opacity = 150
            self.overlay_bg_frameh = pyglet.shapes.Line(500, 300, 1000, 300, 1, (255, 255, 255),
                                                        batch=globals.overlay_batch)
            self.overlay_bg_framev1 = pyglet.shapes.Line(500, 0, 500, 300, 1, (255, 255, 255), batch=globals.overlay_batch)
            self.overlay_bg_framev2 = pyglet.shapes.Line(1000, 0, 1000, 300, 1, (255, 255, 255),
                                                         batch=globals.overlay_batch)
            self.mineral_text = "Mineral text here"
            self.metal_text = "Metal text here"
            self.oil_text = "Oil text here"
            self.selection_text = "Selection text here"
            self.clickable_text = ""
            self.clickable_text_temp = ""
            self.clickable_owner_text = "Owner text here"
            self.clickable_owner_text_temp = ""
            self.clickable_targetbool_text = "Targeting text here"
            self.clickable_targetbool_text_temp = ""

            self.clickable_return_l1_temp = ""
            self.clickable_return_l2_temp = ""
            self.clickable_return_l3_temp = ""
            self.clickable_return_l4_temp = ""

            self.clickable_return_l1_text = ""
            self.clickable_return_l2_text = ""
            self.clickable_return_l3_text = ""
            self.clickable_return_l4_text = ""
            self.overlay_mineral_label = pyglet.text.Label(self.mineral_text,
                                                           font_name='Bebas Neue',
                                                           font_size=15,
                                                           x=505, y=280, batch=globals.overlay_batch)
            self.overlay_metal_label = pyglet.text.Label(self.metal_text,
                                                         font_name='Bebas Neue',
                                                         font_size=15,
                                                         x=505, y=260, batch=globals.overlay_batch)
            self.overlay_oil_label = pyglet.text.Label(self.oil_text,
                                                       font_name='Bebas Neue',
                                                       font_size=15,
                                                       x=505, y=240, batch=globals.overlay_batch)
            self.overlay_selection_label = pyglet.text.Label(self.selection_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=505, y=220, batch=globals.overlay_batch)
            self.overlay_clickable_label = pyglet.text.Label(self.clickable_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=505, y=200, batch=globals.overlay_batch)
            self.overlay_clickable_owner_label = pyglet.text.Label(self.clickable_owner_text,
                                                                   font_name='Bebas Neue',
                                                                   font_size=15,
                                                                   x=505, y=180, batch=globals.overlay_batch)
            self.overlay_clickable_targetbool_label = pyglet.text.Label(self.clickable_targetbool_text,
                                                                        font_name='Bebas Neue',
                                                                        font_size=15,
                                                                        x=505, y=160, batch=globals.overlay_batch)
            # anchor_x='center', anchor_y='center'
            self.overlay_clickable_return_l1_label = pyglet.text.Label(self.clickable_return_l1_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=750, y=80, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            # align="center",
            self.overlay_clickable_return_l2_label = pyglet.text.Label(self.clickable_return_l2_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=750, y=60, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            self.overlay_clickable_return_l3_label = pyglet.text.Label(self.clickable_return_l3_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=750, y=40, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            self.overlay_clickable_return_l4_label = pyglet.text.Label(self.clickable_return_l4_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=12,
                                                                       x=750, y=20, anchor_x='center',
                                                                       batch=globals.overlay_batch)
        else:
            #player 1's overlay
            self.overlay_bg = pyglet.shapes.Rectangle(200, 0, 500, 300, (1, 49, 122), batch=globals.overlay_batch)
            self.overlay_bg.opacity = 100
            self.overlay_bg_frameh = pyglet.shapes.Line(200, 300, 700, 300, 1, (255, 255, 255),
                                                        batch=globals.overlay_batch)
            self.overlay_bg_framev1 = pyglet.shapes.Line(200, 0, 200, 300, 1, (255, 255, 255),
                                                         batch=globals.overlay_batch)
            self.overlay_bg_framev2 = pyglet.shapes.Line(700, 0, 700, 300, 1, (255, 255, 255),
                                                         batch=globals.overlay_batch)
            self.mineral_text = "Mineral text here"
            self.metal_text = "Metal text here"
            self.oil_text = "Oil text here"
            self.selection_text = "Selection text here"
            self.clickable_text = ""
            self.clickable_text_temp = ""
            self.clickable_owner_text = "Owner text here"
            self.clickable_owner_text_temp = ""
            self.clickable_targetbool_text = "Targeting text here"
            self.clickable_targetbool_text_temp = ""

            self.clickable_return_l1_temp = ""
            self.clickable_return_l2_temp = ""
            self.clickable_return_l3_temp = ""
            self.clickable_return_l4_temp = ""

            self.clickable_return_l1_text = ""
            self.clickable_return_l2_text = ""
            self.clickable_return_l3_text = ""
            self.clickable_return_l4_text = ""
            self.overlay_mineral_label = pyglet.text.Label(self.mineral_text,
                                                           font_name='Bebas Neue',
                                                           font_size=15,
                                                           x=205, y=280, batch=globals.overlay_batch)
            self.overlay_metal_label = pyglet.text.Label(self.metal_text,
                                                         font_name='Bebas Neue',
                                                         font_size=15,
                                                         x=205, y=260, batch=globals.overlay_batch)
            self.overlay_oil_label = pyglet.text.Label(self.oil_text,
                                                       font_name='Bebas Neue',
                                                       font_size=15,
                                                       x=205, y=240, batch=globals.overlay_batch)
            self.overlay_selection_label = pyglet.text.Label(self.selection_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=205, y=220, batch=globals.overlay_batch)
            self.overlay_clickable_label = pyglet.text.Label(self.clickable_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=205, y=200, batch=globals.overlay_batch)
            self.overlay_clickable_owner_label = pyglet.text.Label(self.clickable_owner_text,
                                                                   font_name='Bebas Neue',
                                                                   font_size=15,
                                                                   x=205, y=180, batch=globals.overlay_batch)
            self.overlay_clickable_targetbool_label = pyglet.text.Label(self.clickable_targetbool_text,
                                                                        font_name='Bebas Neue',
                                                                        font_size=15,
                                                                        x=205, y=160, batch=globals.overlay_batch)
            # anchor_x='center', anchor_y='center'
            self.overlay_clickable_return_l1_label = pyglet.text.Label(self.clickable_return_l1_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=450, y=80, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            # align="center",
            self.overlay_clickable_return_l2_label = pyglet.text.Label(self.clickable_return_l2_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=450, y=60, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            self.overlay_clickable_return_l3_label = pyglet.text.Label(self.clickable_return_l3_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=450, y=40, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            self.overlay_clickable_return_l4_label = pyglet.text.Label(self.clickable_return_l4_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=12,
                                                                       x=450, y=20, anchor_x='center',
                                                                       batch=globals.overlay_batch)

            #player 2's overlay
            self.p2_overlay_bg = pyglet.shapes.Rectangle(800, 0, 500, 300, (130, 39, 39), batch=globals.overlay_batch)
            self.p2_overlay_bg.opacity = 100
            self.p2_overlay_bg_frameh = pyglet.shapes.Line(800, 300, 1300, 300, 1, (255, 255, 255),
                                                        batch=globals.overlay_batch)
            self.p2_overlay_bg_framev1 = pyglet.shapes.Line(800, 0, 800, 300, 1, (255, 255, 255),
                                                         batch=globals.overlay_batch)
            self.p2_overlay_bg_framev2 = pyglet.shapes.Line(1300, 0, 1300, 300, 1, (255, 255, 255),
                                                         batch=globals.overlay_batch)
            self.p2_mineral_text = "Mineral text here"
            self.p2_metal_text = "Metal text here"
            self.p2_oil_text = "Oil text here"
            self.p2_selection_text = "Selection text here"
            self.p2_clickable_text = ""
            self.p2_clickable_text_temp = ""
            self.p2_clickable_owner_text = "Owner text here"
            self.p2_clickable_owner_text_temp = ""
            self.p2_clickable_targetbool_text = "Targeting text here"
            self.p2_clickable_targetbool_text_temp = ""

            self.p2_clickable_return_l1_temp = ""
            self.p2_clickable_return_l2_temp = ""
            self.p2_clickable_return_l3_temp = ""
            self.p2_clickable_return_l4_temp = ""

            self.p2_clickable_return_l1_text = ""
            self.p2_clickable_return_l2_text = ""
            self.p2_clickable_return_l3_text = ""
            self.p2_clickable_return_l4_text = ""
            self.p2_overlay_mineral_label = pyglet.text.Label(self.p2_mineral_text,
                                                           font_name='Bebas Neue',
                                                           font_size=15,
                                                           x=805, y=280, batch=globals.overlay_batch)
            self.p2_overlay_metal_label = pyglet.text.Label(self.p2_metal_text,
                                                         font_name='Bebas Neue',
                                                         font_size=15,
                                                         x=805, y=260, batch=globals.overlay_batch)
            self.p2_overlay_oil_label = pyglet.text.Label(self.p2_oil_text,
                                                       font_name='Bebas Neue',
                                                       font_size=15,
                                                       x=805, y=240, batch=globals.overlay_batch)
            self.p2_overlay_selection_label = pyglet.text.Label(self.p2_selection_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=805, y=220, batch=globals.overlay_batch)
            self.p2_overlay_clickable_label = pyglet.text.Label(self.p2_clickable_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=805, y=200, batch=globals.overlay_batch)
            self.p2_overlay_clickable_owner_label = pyglet.text.Label(self.p2_clickable_owner_text,
                                                                   font_name='Bebas Neue',
                                                                   font_size=15,
                                                                   x=805, y=180, batch=globals.overlay_batch)
            self.p2_overlay_clickable_targetbool_label = pyglet.text.Label(self.p2_clickable_targetbool_text,
                                                                        font_name='Bebas Neue',
                                                                        font_size=15,
                                                                        x=805, y=160, batch=globals.overlay_batch)
            # anchor_x='center', anchor_y='center'
            self.p2_overlay_clickable_return_l1_label = pyglet.text.Label(self.p2_clickable_return_l1_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=1050, y=80, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            # align="center",
            self.p2_overlay_clickable_return_l2_label = pyglet.text.Label(self.p2_clickable_return_l2_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=1050, y=60, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            self.p2_overlay_clickable_return_l3_label = pyglet.text.Label(self.p2_clickable_return_l3_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=1050, y=40, anchor_x='center',
                                                                       batch=globals.overlay_batch)
            self.p2_overlay_clickable_return_l4_label = pyglet.text.Label(self.p2_clickable_return_l4_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=12,
                                                                       x=1050, y=20, anchor_x='center',
                                                                       batch=globals.overlay_batch)

    def update(self, dt):
        # super(game_window, self).update(dt)
        # print(self.game_objects)
        for obj in self.game_objects:
            obj.update(dt)
            obj.check_bounds()
        for i in globals.building_objects:
            i.update(dt)
        for i in globals.troop_objects:
            i.update(dt)

        if self.clicked_object is not None:
            globals.clickable = self.clicked_object
            self.tracked_type = self.clicked_object.get_overlay_name()
            self.tracked_health = self.clicked_object.get_health()
            self.tracked_shield = self.clicked_object.get_shield()
            self.tracked_owner = self.clicked_object.get_owner_id()
            self.tracked_targetbool = self.clicked_object.get_targetbool()
            self.clickable_text_temp = (str(self.tracked_type) + " - Health: " +
                                        str(round(self.tracked_health, 1)) + " + " +
                                        str(round(self.tracked_shield, 1)) + " Shield")
            self.clickable_owner_text_temp = (str(self.tracked_owner))
            self.clickable_targetbool_text_temp = ("Enabled" if self.clicked_object.get_targetbool() else "Disabled")
            if globals.offline_multi:
                self.p2_tracked_type = self.clicked_object.get_overlay_name()
                self.p2_tracked_health = self.clicked_object.get_health()
                self.p2_tracked_shield = self.clicked_object.get_shield()
                self.p2_tracked_owner = self.clicked_object.get_owner_id()
                self.p2_tracked_targetbool = self.clicked_object.get_targetbool()
                self.p2_clickable_text_temp = (str(self.tracked_type) + " - Health: " +
                                            str(round(self.tracked_health, 1)) + " + " +
                                            str(round(self.tracked_shield, 1)) + " Shield")
                self.p2_clickable_owner_text_temp = (str(self.tracked_owner))
                self.p2_clickable_targetbool_text_temp = ("Enabled" if self.clicked_object.get_targetbool() else "Disabled")

            if self.clicked_object.get_needs_menu():
                if self.clicked_object.get_owner() == 1:
                    self.overlay_clickable_return_l1_label.text, self.overlay_clickable_return_l2_label.text, \
                    self.overlay_clickable_return_l3_label.text, self.overlay_clickable_return_l4_label.text = \
                        self.clicked_object.gen_overlay_text()[0], \
                        self.clicked_object.gen_overlay_text()[1], \
                        self.clicked_object.gen_overlay_text()[2], \
                        self.clicked_object.gen_overlay_text()[3]

                    self.p2_overlay_clickable_return_l1_label.text = ""
                    self.p2_overlay_clickable_return_l2_label.text = ""
                    self.p2_overlay_clickable_return_l3_label.text = ""
                    self.p2_overlay_clickable_return_l4_label.text = ""

                elif globals.offline_multi and self.clicked_object.get_owner() == 2:
                    self.p2_overlay_clickable_return_l1_label.text, self.p2_overlay_clickable_return_l2_label.text, \
                    self.p2_overlay_clickable_return_l3_label.text, self.p2_overlay_clickable_return_l4_label.text = \
                        self.clicked_object.gen_overlay_text()[0], \
                        self.clicked_object.gen_overlay_text()[1], \
                        self.clicked_object.gen_overlay_text()[2], \
                        self.clicked_object.gen_overlay_text()[3]

                    self.overlay_clickable_return_l1_label.text = ""
                    self.overlay_clickable_return_l2_label.text = ""
                    self.overlay_clickable_return_l3_label.text = ""
                    self.overlay_clickable_return_l4_label.text = ""

            else:
                self.overlay_clickable_return_l1_label.text = ""
                self.overlay_clickable_return_l2_label.text = ""
                self.overlay_clickable_return_l3_label.text = ""
                self.overlay_clickable_return_l4_label.text = ""
                if globals.offline_multi:
                    self.p2_overlay_clickable_return_l1_label.text = ""
                    self.p2_overlay_clickable_return_l2_label.text = ""
                    self.p2_overlay_clickable_return_l3_label.text = ""
                    self.p2_overlay_clickable_return_l4_label.text = ""

        if self.clicked_object is None:
            globals.clickable = None
            if self.overlay_clickable_return_l1_label.text != "":
                self.overlay_clickable_return_l1_label.text = ""
                self.overlay_clickable_return_l2_label.text = ""
                self.overlay_clickable_return_l3_label.text = ""
                self.overlay_clickable_return_l4_label.text = ""
                if globals.offline_multi:
                    self.p2_overlay_clickable_return_l1_label.text = ""
                    self.p2_overlay_clickable_return_l2_label.text = ""
                    self.p2_overlay_clickable_return_l3_label.text = ""
                    self.p2_overlay_clickable_return_l4_label.text = ""

        # Overlay editing
        self.mineral_text = ("Mineral: " + str(round(globals.player1_lv1_res, 1)) + " (" + str(
            round(globals.player1_lv1_gen, 2)) + "/s)")  # ℤens
        self.overlay_mineral_label.text = self.mineral_text
        self.metal_text = ("Metal: " + str(round(globals.player1_lv2_res, 1)) + " (" + str(
            round(globals.player1_lv2_gen, 2)) + "/s)")  # ℤens
        self.overlay_metal_label.text = self.metal_text
        self.oil_text = ("Oil: " + str(round(globals.player1_lv3_res, 1)) + " (" + str(
            round(globals.player1_lv3_gen, 2)) + "/s)")  # ℤens
        self.overlay_oil_label.text = self.oil_text
        self.selection_text_temp = str(game_window_run.player_one.get_select()).split("'")
        self.selection_text_temp = str((self.selection_text_temp[1])[8:])
        self.selection_text = "Selection: " + str(self.selection_text_temp)
        self.overlay_selection_label.text = self.selection_text
        # Definitions for selecting and tracking data on objects
        self.clickable_text = "Mouse last selected: " + self.clickable_text_temp
        self.overlay_clickable_label.text = self.clickable_text
        self.clickable_owner_text = "Owner: " + self.clickable_owner_text_temp
        self.overlay_clickable_owner_label.text = self.clickable_owner_text
        self.clickable_targetbool_text = "Auto-targeting: " + self.clickable_targetbool_text_temp
        self.overlay_clickable_targetbool_label.text = self.clickable_targetbool_text
        self.tracked_type = None
        self.tracked_health = 0
        self.tracked_shield = 0
        self.tracked_owner = None

        if globals.offline_multi:
            # Overlay editing
            self.p2_mineral_text = ("Mineral: " + str(round(globals.player2_lv1_res, 1)) + " (" + str(
                round(globals.player2_lv1_gen, 2)) + "/s)")  # ℤens
            self.p2_overlay_mineral_label.text = self.p2_mineral_text
            self.p2_metal_text = ("Metal: " + str(round(globals.player2_lv2_res, 1)) + " (" + str(
                round(globals.player2_lv2_gen, 2)) + "/s)")  # ℤens
            self.p2_overlay_metal_label.text = self.p2_metal_text
            self.p2_oil_text = ("Oil: " + str(round(globals.player2_lv3_res, 1)) + " (" + str(
                round(globals.player2_lv3_gen, 2)) + "/s)")  # ℤens
            self.p2_overlay_oil_label.text = self.p2_oil_text
            self.p2_selection_text_temp = str(game_window_run.player_two.get_select()).split("'")
            self.p2_selection_text_temp = str((self.p2_selection_text_temp[1])[8:])
            self.p2_selection_text = "Selection: " + str(self.p2_selection_text_temp)
            self.p2_overlay_selection_label.text = self.p2_selection_text
            # Definitions for selecting and tracking data on objects
            self.p2_clickable_text = "Mouse last selected: " + self.clickable_text_temp
            self.p2_overlay_clickable_label.text = self.clickable_text
            self.p2_clickable_owner_text = "Owner: " + self.clickable_owner_text_temp
            self.p2_overlay_clickable_owner_label.text = self.clickable_owner_text
            self.p2_clickable_targetbool_text = "Auto-targeting: " + self.clickable_targetbool_text_temp
            self.p2_overlay_clickable_targetbool_label.text = self.clickable_targetbool_text
            self.p2_tracked_type = None
            self.p2_tracked_health = 0
            self.p2_tracked_shield = 0
            self.p2_tracked_owner = None


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
        print(symbol)
        if symbol == key.ENTER:
            globals.code = self.input_text.upper()
            self.input_text = ''
            if globals.code == "MEMENTOMORI":
                for i in globals.building_objects:
                    if i.get_obj_type() == "Drill":
                        i.image = animations.animations.DUA_ani
                        objects.Drill.image = animations.animations.DUA_ani
        elif symbol == key.SLASH:
            self.show_overlay = not (self.show_overlay)
            # Control.handleraltered = False
        elif symbol == key.BACKSLASH:
            if self.clicked_object is not None:
                self.clicked_object.auto_targeting = not (self.clicked_object.auto_targeting)
        elif symbol == key.BACKSPACE:
            self.input_text = self.input_text[:-1]

        if symbol == key.LEFT:  # TODO: choose whether the menu function buttons should be the same
                                # TODO: or different for each player (only one player's building can be accessed at once)
            if self.clicked_object is not None:
                if self.clicked_object.get_needs_menu():
                    self.clicked_object.key_left_func()

        if symbol == key.RIGHT:
            if self.clicked_object is not None:
                if self.clicked_object.get_needs_menu():
                    self.clicked_object.key_right_func()

        if symbol == key.ENTER or symbol == key.RETURN:
            if self.clicked_object is not None:
                if self.clicked_object.get_needs_menu():
                    self.clicked_object.enter_func()

            # Labels.playername_label.input_text = Typein.input_text
        elif symbol:
            return True

    def get_centred_coords(self, x, y):
        x_remainder = x % 20
        y_remainder = y % 20
        x_centred = (x - x_remainder) + 10
        y_centred = (y - y_remainder) + 10
        return x_centred, y_centred

    def on_mouse_press(self, x, y, button, modifiers):
        # print(str(button) + "Pressed at: " + str(x) + " " + str(y))
        got_troop = False
        got_building = False
        for i in globals.troop_objects:
            if self.get_centred_coords(i.get_x(), i.get_y()) == self.get_centred_coords(x, y):
                self.tracked_type = i.get_overlay_name()
                self.tracked_health = i.get_health()
                self.tracked_shield = i.get_shield()
                self.tracked_owner = i.get_owner_id()
                self.clickable_text_temp = (str(self.tracked_type) + " - Health: " +
                                            str(round(self.tracked_health, 1)) + " + " +
                                            str(round(self.tracked_shield, 1)) + " Shield\n"
                                            + "Owner: " + str(self.tracked_owner))
                got_troop = True
                self.clicked_object = i
                break
        if not got_troop:
            for i in globals.building_objects:
                if self.get_centred_coords(i.get_x(), i.get_y()) == self.get_centred_coords(x, y):
                    self.tracked_type = i.get_overlay_name()
                    self.tracked_health = i.get_health()
                    self.tracked_shield = i.get_shield()
                    self.tracked_owner = i.get_owner_id()
                    self.clickable_text_temp = (str(self.tracked_type) + " - Health: " +
                                                str(round(self.tracked_health, 1)) + " + " +
                                                str(round(self.tracked_shield, 1)) + " Shield\n"
                                                + "Owner: " + str(self.tracked_owner))
                    got_building = True
                    self.clicked_object = i
                    break
        if not got_troop and not got_building:
            self.clicked_object = None
            tile_coords = self.get_centred_coords(x, y)
            self.clickable_text_temp = ("Empty tile at:  " + str(tile_coords[0]) + ", " + str(tile_coords[1]))
            self.overlay_clickable_owner_label.text = "Owner: "
            self.overlay_clickable_targetbool_label.text = "Auto-targeting: "
            self.clickable_owner_text_temp = ""
            self.clickable_targetbool_text_temp = ""

        # print("You clicked on the tile centred at " + str(x_centred) + " " + str(y_centred))

    def on_draw(self):
        self.clear()
        self.bg_batch.draw()
        # globals.tracer_batch.draw() # Tracer batch doesn't seem to work even after setting the tracer's batch to it
        globals.building_batch.draw()
        globals.small_troop_batch.draw()
        globals.medium_troop_batch.draw()
        globals.large_troop_batch.draw()
        for i in globals.building_objects:
            if i.get_obj_type() == "Tracing turret":
                i.get_tracer().draw()
        for i in globals.troop_objects:
            if i.get_weapon_tracing():
                i.get_tracer().draw()
        globals.bar_batch.draw()
        #     i.draw()
        # for i in globals.troop_objects:
        #     i.draw()

        # self.player_one.draw()
        for i in self.game_objects:
            i.draw()
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
                globals.astar_map[i - 1].append(1)
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

        return tiles, tilebatch


class data_window(pyglet.window.Window):
    def __init__(self):
        super().__init__()  # self, game_window

        self.set_vsync(False)
        self.mineral_text = "mineral count here"
        self.mineral_label = pyglet.text.Label(self.mineral_text,
                                               font_name='Bebas Neue',
                                               font_size=36,
                                               x=self._width // 2, y=(self._height // 2) + 40,
                                               anchor_x='center', anchor_y='center')

        self.metal_text = "metal count here"
        self.metal_label = pyglet.text.Label(self.mineral_text,
                                             font_name='Bebas Neue',
                                             font_size=36,
                                             x=self._width // 2, y=self._height // 2,
                                             anchor_x='center', anchor_y='center')

        self.selection_text = "selection of building here"
        self.selection_label = pyglet.text.Label(self.selection_text,
                                                 font_name='Bebas Neue',
                                                 font_size=36,
                                                 x=self._width // 2, y=(self._height // 2) - 40,
                                                 anchor_x='center', anchor_y='center')

        pyglet.clock.schedule_interval(self.update, 1 / 120.0)

    def update(self, dt):
        self.mineral_text = ""
        # print(building_objects)
        # self.mineral_text += str(i)
        self.mineral_text = "Mineral: " + str(round(globals.player1_lv1_res, 1))  # ℤens
        self.mineral_label.text = self.mineral_text
        self.metal_text = "Metal: " + str(round(globals.player1_lv2_res, 1))  # ℤens
        self.metal_label.text = self.metal_text
        self.selection_text_temp = str(game_window_run.player_one.get_select()).split("'")
        self.selection_text_temp = str((self.selection_text_temp[1])[8:])
        self.selection_text = "Selection: " + str(self.selection_text_temp)
        self.selection_label.text = self.selection_text
        # print(globals.code)

    def on_draw(self):
        self.clear()
        self.mineral_label.draw()
        self.metal_label.draw()
        self.selection_label.draw()


game_window_run = game_window()  # width = screenresx, height=screenresy
# data_window_run = data_window() # Deprecated - overlay replaces data window

# class Typein(object):


pyglet.app.run()  # kek or cringe
