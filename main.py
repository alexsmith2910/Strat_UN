import objects
import random
import secrets
import math
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from pyglet.graphics import *

game_window = pyglet.window.Window(vsync=False, width = 800, height=600)
label = pyglet.text.Label('Fuck off nick',
                          font_name='Have Heart One',
                          font_size=36,
                          x=game_window.width//2, y=game_window.height//2,
                          anchor_x='center', anchor_y='center')
poly = pyglet.graphics.draw(2, pyglet.gl.GL_POINTS,
    ('v3f', (10.0, 15.0, 0.0, 30.0, 35.0, 0.0))
)
square = pyglet.shapes.Rectangle(x=200, y=200, width=200, height=200, color=(55, 55, 255))
player_image = pyglet.image.load("Test-sprite.png")
player_image.anchor_x = 10
player_image.anchor_y = 10

player_sprite = objects.Player(x=410, y=310)
game_window.push_handlers(player_sprite)
game_window.push_handlers(player_sprite.key_handler)
game_objects = [player_sprite]

def tiles_map(resx=800, resy=600, size=20):
    ylayers = resy//size
    print(ylayers)
    print(ylayers)
    tiles = []
    for i in range(ylayers):
        tiles.append([])
        #print(str(len(tiles)) + ";ayers")
    tilebatch = pyglet.graphics.Batch()
    for i in range(resy//size):
        #print("layer" + str(i))
        for j in range (resx//size):
            #r = secrets.randbelow(255)
            g = secrets.randbelow(128)
            g2 = secrets.randbelow(64)
            g3 = g-g2
            if g3 < 1:
                g3 = 20
            g3 += 25
            #b = secrets.randbelow(255)
            tiles[i-1].append(objects.TileBG(x=size * j, y=size * i, width=size, height=size, color=(0, g3, 0), batch=tilebatch))
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
                    (tiles[i])[x_choice-1].color = (100, 100, 255)
                elif val_list[1] == 1:
                    (tiles[i])[x_choice+1].color = (100, 100, 255)
                elif val_list[2] == 1:
                    (tiles[i-1])[x_choice].color = (100, 100, 255)
                elif val_list[3] == 1 and i < resy//2:
                    (tiles[i+1])[x_choice].color = (100, 100, 255)

    return tiles, tilebatch
squares, test_batch = tiles_map()




def update(dt):
    for obj in game_objects:
        obj.update(dt)
        obj.check_bounds()
    for i in squares:
        for j in i:
            if j.get_barrier_state():
                tempx = j.x+10
                tempy = j.y+10
            if j.get_barrier_state() and tempx-player_sprite.get_x() == 0.0 and tempy-player_sprite.get_y() == 0:
                for i in squares:
                    for j in i:
                        j.color = (255, 0, 0)

pyglet.clock.schedule_interval(update, 1/120.0)
#fps_display = pyglet.clock.ClockDisplay()
fps_display = pyglet.window.FPSDisplay(game_window)
@game_window.event
def on_draw():
    game_window.clear()
    test_batch.draw()
    player_sprite.draw()
    fps_display.draw()
    #vertex_list = pyglet.graphics.vertex_list(1024, 'v3f', 'c4B', 't2f', 'n3f')
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)#used to find events to connect to commands

pyglet.app.run()# kek or cringe