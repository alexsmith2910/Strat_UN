import objects
import random
import secrets
import math
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from pyglet.graphics import *
from globals import *
class game_window(pyglet.window.Window):
    def __init__(self):
        super().__init__()#self, game_window
        self.set_vsync(False)
        self.player_image = pyglet.image.load("Test-sprite.png")
        self.player_image.anchor_x = 10
        self.player_image.anchor_y = 10
        self.set_size(screenresx, screenresy)
        self.player_sprite = objects.Player(x=910, y=550)
        self.player_sprite.set_name("Zestyy")
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
        for i in self.squares:
            for j in i:
                if j.get_barrier_state():
                    tempx = j.x + 10
                    tempy = j.y + 10
                if j.get_barrier_state() and tempx - self.player_sprite.get_x() == 0.0 and tempy - self.player_sprite.get_y() == 0:
                    for i in self.squares:
                        for j in i:
                            j.color = (255, 0, 0)

    def on_draw(self):
        self.clear()
        self.bg_batch.draw()
        for i in building_objects:
            i.draw()
            # print(i)
        self.player_sprite.draw()
        self.fps_display.draw()

    def get_game_obhects(self):
        return self.game_objects

    def tiles_map(self, resx=screenresx, resy=screenresy, size=20):
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


# label = pyglet.text.Label('Fuck off nick',
#                           font_name='Have Heart One',
#                           font_size=36,
#                           x=game_window.width//2, y=game_window.height//2,
#                           anchor_x='center', anchor_y='center')


# def tiles_map(resx=screenresx, resy=screenresy, size=20):
#     ylayers = resy//size
#     print(ylayers)
#     print(ylayers)
#     tiles = []
#     for i in range(ylayers):
#         tiles.append([])
#         #print(str(len(tiles)) + ";ayers")
#     tilebatch = pyglet.graphics.Batch()
#     for i in range(resy//size):
#         #print("layer" + str(i))
#         for j in range (resx//size):
#             #r = secrets.randbelow(255)
#             g = secrets.randbelow(128)
#             g2 = secrets.randbelow(64)
#             g3 = g-g2
#             if g3 < 1:
#                 g3 = 20
#             g3 += 25
#             #b = secrets.randbelow(255)
#             tiles[i-1].append(objects.TileBG(x=size * j, y=size * i, width=size, height=size, color=(0, g3, 0), batch=tilebatch))
#     for i in range(len(tiles)):
#         choice = secrets.randbelow(3)
#         if choice == 0:
#             x_choice = secrets.randbelow(16)
#             (tiles[i])[x_choice].color = (0, 0, 255)
#             (tiles[i])[x_choice].make_barrier()
#             val_list = []
#             for i in range(4):
#                 for i in range(10):
#                     val_list.append(secrets.randbelow(2))
#                 if val_list[0] == 1:
#                     (tiles[i])[x_choice-1].color = (100, 100, 255)
#                 elif val_list[1] == 1:
#                     (tiles[i])[x_choice+1].color = (100, 100, 255)
#                 elif val_list[2] == 1:
#                     (tiles[i-1])[x_choice].color = (100, 100, 255)
#                 elif val_list[3] == 1 and i < resy//2:
#                     (tiles[i+1])[x_choice].color = (100, 100, 255)
#
#     return tiles, tilebatch

    #vertex_list = pyglet.graphics.vertex_list(1024, 'v3f', 'c4B', 't2f', 'n3f')
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)#used to find events to connect to commands

game_window_run = game_window()#width = screenresx, height=screenresy
pyglet.app.run()# kek or cringe