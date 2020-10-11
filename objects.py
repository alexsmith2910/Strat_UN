import pyglet
from pyglet.window import key, mouse
#import globals
import globals

player_image = pyglet.image.load("Test-sprite.png")
player_image.anchor_x = 10
player_image.anchor_y = 10

drill_image = pyglet.image.load("Building test sprite-drill.png")
drill_image.anchor_x = 10
drill_image.anchor_y = 10

class NameError(Exception):
    """Attributes:
        args[0] = Error Message
        args[1] = Issue
    """

    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.issue = args[1]
        else:
            self.message = None
            self.issue = None

        if self.issue == 0:
            self.issue = "Generate object"
        elif self.issue == 1:
            self.issue = "Extra issue"
        else:
            self.issue = "Commit to unknown operation"

    def __str__(self):
        if self.message:
            return "NameError, Failed to {0}, message: {1}".format(self.issue, self.message)
            # raise
        else:
            return "NameError, has been raised."
            # raise

class PhysicalObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = globals.screenresx + self.image.width / 2
        max_y = globals.screenresy + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

class TileObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.owner = None

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = globals.screenresx + self.image.width / 2
        max_y = globals.screenresy + self.image.height / 2
        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

class TileBG(pyglet.shapes.Rectangle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.owner = ""
        self.barrier = False

    def make_barrier(self):
        self.barrier = True

    def remove_barrier(self):
        self.barrier = False

    def get_barrier_state(self):
        return self.barrier

class Building(TileObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=drill_image, *args, **kwargs)
        self.owner_id = None
        self.owner_num = None

    def get_owner(self):
        return self.owner_num

    def set_owner(self, new_owner_id_set):
        self.owner_id = new_owner_id_set[0]
        self.owner_num = new_owner_id_set[1]
        #print(self.owner)

class Drill(Building):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#img=drill_image,
        self.color = (0, 255, 0)
        self.mine_rate = 7.5

    def update(self, dt):
        mined = self.mine_rate * dt
        #print(self.owner_num)
        if self.owner_num == 1:
            globals.player1_res += mined
        if self.owner_num == 2:
            globals.player2_res += mined


class Player(TileObject):
    """class for generating a object for the player to control"""

    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.num = -1
        self.id = None
        self.pixels = 20
        self.key_handler = key.KeyStateHandler()
        self.scounter = 0
        self.bcounter = 0
        globals.player_list.append(self)

    def set_id(self, new_name, num=1):
        """sets the name for the player, use ONCE per player ONLY"""
        if self.id == None:
            self.id = str(new_name)
            self.num = num
            globals.player_list.append(str(new_name))

    def get_id(self):
        if self.id != None:
            return self.id, self.num
        else:
            raise NameError("Object has been attempted to be generated without player being given an ID", 0)


    def add_scounter(self):
        self.scounter += 1

    def add_bcounter(self):
        self.bcounter += 1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def update(self, dt):
        super(Player, self).update(dt)
        if self.key_handler[key.W]:
            if self.key_handler[key.W] and self.scounter == 0:
                self.y += self.pixels
            if self.scounter == 0:
                self.scounter += 1

        if self.key_handler[key.A]:
            if self.key_handler[key.A] and self.scounter == 0:
                self.x -= self.pixels
            if self.scounter == 0:
                self.scounter += 1

        if self.key_handler[key.S]:
            if self.key_handler[key.S] and self.scounter == 0:
                self.y -= self.pixels
            if self.scounter == 0:
                self.scounter += 1

        if self.key_handler[key.D]:
            if self.key_handler[key.D] and self.scounter == 0:
                self.x += self.pixels
            if self.scounter == 0:
                self.scounter += 1

        if self.key_handler[key.B] and self.bcounter == 0:  # create some sort of build function
            globals.building_objects.append(Drill(x=self.x, y=self.y))
            print(globals.building_objects)
            globals.building_objects[len(globals.building_objects)-1].set_owner(self.get_id())
            #building_objects[len(player_list) - 1].color = (0, 0, 255) # NOTE: color function acts as a 'tint' added to sprites
            self.bcounter += 1

        if self.bcounter != 0:
            self.bcounter += 1

        if self.scounter != 0:
            self.scounter += 1

        if self.scounter == 15:
            self.velocity_x = 0
            self.velocity_y = 0
            self.scounter = 0 if self.scounter == 15 else self.scounter
        if self.bcounter == 600:
            self.bcounter = 0 if self.bcounter == 600 else self.bcounter