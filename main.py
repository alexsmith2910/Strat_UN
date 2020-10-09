import motion
import random
import secrets
import math
import pyglet
from pyglet.gl import *
from pyglet.window import key, mouse
from pyglet.graphics import *

# vertex_list = pyglet.graphics.vertex_list(2,
#                                           ('v2i', (10, 15, 30, 35)),
#                                           ('c3B', (0, 0, 255, 0, 255, 0))
#                                           )
# vertex_list.draw(pyglet.gl.GL_POINTS)
# player.draw()

game_window = pyglet.window.Window(width = 800, height=600)
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
def tiles(no_squares):
    tiles = []
    tilebatch = pyglet.graphics.Batch()
    for i in range(no_squares):
        x_num = secrets.randbelow(800)
        y_num = secrets.randbelow(800)
        w_num = secrets.randbelow(100)
        h_num = secrets.randbelow(100)
        r = secrets.randbelow(255)
        g = secrets.randbelow(255)
        b = secrets.randbelow(255)
        tiles.append(motion.TileBG(x=x_num, y=y_num, anchor_x=10, anchor_y=10, width=w_num, height=h_num, color=(r, g, b), batch=tilebatch))
    return tiles, tilebatch
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
            tiles[i-1].append(motion.TileBG(x=size*j, y=size*i, width=size, height=size, color=(0, g3, 0), batch=tilebatch))
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
class Player(motion.TileObject):

    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)

        self.pixels = 20
        self.key_handler = key.KeyStateHandler()
        self.thrust = 6000.0
        self.rotate_speed = 199.0
        self.scounter = 0
        self.ucounter = 0
        self.dcounter = 0
        self.lcounter = 0
        self.rcounter = 0
        self.keys = dict(left=False, right=False, up=False, down=False, w=False, a=False, s=False, d=False)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def update(self, dt):
        super(Player, self).update(dt)
        if self.key_handler[key.W]:
            if self.key_handler[key.W] and self.scounter == 0:
                # self.position[0] += 50
                #Player.update()
                self.y += self.pixels
            self.scounter += 1

        if self.key_handler[key.A]:
            if self.key_handler[key.A] and self.scounter == 0:
                # self.position[0] += 50
                #Player.update()
                self.x -= self.pixels
            self.scounter += 1

        if self.key_handler[key.S]:
            if self.key_handler[key.S] and self.scounter == 0:
                # self.position[0] += 50
                #Player.update()
                self.y -= self.pixels
            self.scounter += 1

        if self.key_handler[key.D]:
            if self.key_handler[key.D] and self.scounter == 0:
                # self.position[0] += 50
                #Player.update()
                self.x += self.pixels
            self.scounter += 1


        if self.scounter == 15:#self.ucounter == 30 or self.lcounter == 30 or self.rcounter == 30 or self.dcounter == 30 or
            self.velocity_x = 0
            self.velocity_y = 0
            self.scounter = 0 if self.scounter == 15 else self.scounter

player = motion.TileObject(img=player_image, x=0, y=0)
player.rotation = random.randint(0, 360)
player.velocity_x = random.random() * 40
player.velocity_y = random.random() * 40
rock_image = pyglet.image.load("rock-r.png")
rock = motion.PhysicalObject(img=rock_image, x=0, y=0)
rock.rotation = random.randint(0, 360)
rock.velocity_x = random.random() * 120
rock.velocity_y = random.random() * 120


player_ship = Player(x=410, y=310)
game_window.push_handlers(player_ship)
game_window.push_handlers(player_ship.key_handler)
squares, test_batch = tiles_map()
game_objects = [player_ship]

def update(dt):
    for obj in game_objects:
        obj.update(dt)
        obj.check_bounds()
    for i in squares:
        for j in i:
            temp = j.x+10
            if j.get_barrier_state():
                print(temp-player_ship.get_x()+j.get_barrier_state())
            #print(Player.x)

            if j.get_barrier_state() and temp-player_ship.get_x() == 0.0:
                print("test")
                print(j.get_barrier_state())
                print(player_ship.get_x()-temp)
                for i in squares:
                    for j in i:
                        j.color = (255, 0, 0)

pyglet.clock.schedule_interval(update, 1/120.0)

@game_window.event
def on_draw():
    game_window.clear()
    test_batch.draw()
    #label.draw()
    #poly.draw()
    player_ship.draw()
    # player.draw()
    #rock.draw()

    #vertex_list = pyglet.graphics.vertex_list(1024, 'v3f', 'c4B', 't2f', 'n3f')
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)#used to find events to connect to commands

pyglet.app.run()# kek or cringe