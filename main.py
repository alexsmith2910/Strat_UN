import random
import math
import inspect
import secrets
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from pyglet.graphics import *
import globals
import objects
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
        self.push_handlers(self.player_sprite)
        self.push_handlers(self.player_sprite.key_handler)
        self.game_objects = [self.player_sprite]
        self.squares, self.bg_batch = self.tiles_map()
        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        # fps_display = pyglet.clock.ClockDisplay()
        self.fps_display = pyglet.window.FPSDisplay(self)

    def update(self, dt):
        for obj in self.game_objects:
            obj.update(dt)
            obj.check_bounds()
            #obj.update(dt)
        # for i in self.squares:
        #     for j in i:
        #         if j.get_barrier_state():
        #             tempx = j.x + 10
        #             tempy = j.y + 10
        #         if j.get_barrier_state() and tempx - self.player_sprite.get_x() == 0.0 and tempy - self.player_sprite.get_y() == 0:
        #             for i in self.squares:
        #                 for j in i:
        #                     j.color = (255, 0, 0)

    def on_draw(self):
        self.clear()
        self.bg_batch.draw()
        for i in globals.building_objects:
            if isinstance(i, objects.Basic_Turret):
                i.get_tracer().draw()
            i.draw()
        self.player_sprite.draw()
        self.fps_display.draw()
            # print(i)
            # wont find this until u read it yeah well I found it so shut
        # self.player_sprite.draw()
        # self.fps_display.draw()
        # pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
        #                      ('v2i', (500, 500))
        #                      )#this is currently in use to show the target that the turret is supposed to point at

    def get_game_objects(self):
        return self.game_objects

    def tiles_map(self, resx=globals.screenresx, resy=globals.screenresy, size=20):
        ylayers = resy // size
        print(ylayers)
        print(ylayers)
        tiles = []
        for i in range(ylayers):
            tiles.append([])
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
        for i in range(len(tiles)):
            choice = secrets.randbelow(3)
            if choice == 0:
                x_choice = secrets.randbelow(16)
                (tiles[i])[x_choice].color = (0, 0, 255)
                (tiles[i])[x_choice].make_barrier()
                val_list = []
                for i in range(4):
                    for i in range(10):
                        val_list.append(secrets.randbelow(2))
                    if val_list[0] == 1:
                        (tiles[i])[x_choice - 1].color = (100, 100, 255)
                    elif val_list[1] == 1:
                        (tiles[i])[x_choice + 1].color = (100, 100, 255)
                    elif val_list[2] == 1:
                        (tiles[i - 1])[x_choice].color = (100, 100, 255)
                    elif val_list[3] == 1 and i < resy // 2:
                        (tiles[i + 1])[x_choice].color = (100, 100, 255)

        return tiles, tilebatch

class data_window(pyglet.window.Window):
    def __init__(self):
        super().__init__()#self, game_window

        self.set_vsync(False)
        self.obj_text = "objects here"
        self.obj_label = pyglet.text.Label(self.obj_text,
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
        self.obj_text = ""
        #print(building_objects)
        for i in globals.building_objects:
            i.update(dt)
            # self.obj_text += str(i)
        self.obj_text = "Mineral: " + str(round(globals.player1_lv1_res, 1))#ℤens
        self.obj_label.text = self.obj_text
        self.selection_text_temp = str(game_window_run.player_sprite.get_select()).split("'")
        self.selection_text_temp = str((self.selection_text_temp[1])[8:])
        self.selection_text = "Selection: " + str(self.selection_text_temp)
        self.selection_label.text = self.selection_text
    def on_draw(self):
        self.clear()
        self.obj_label.draw()
        self.selection_label.draw()


# label = pyglet.text.Label('Fuck off nick', j
#                           font_name='Have Heart One',
#                           font_size=36,
#                           x=game_window.width//2, y=game_window.height//2,
#                           anchor_x='center', anchor_y='center')


    #vertex_list = pyglet.graphics.vertex_list(1024, 'v3f', 'c4B', 't2f', 'n3f')
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)#used to find events to connect to commands
game_window_run = game_window()#width = screenresx, height=screenresy
data_window_run = data_window()
pyglet.app.run()# kek or cringe


