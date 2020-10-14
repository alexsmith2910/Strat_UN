import os
import math
import pyglet
from pyglet.window import key, mouse
import secrets
import globals
import animations.animations

building_placeholder_image = pyglet.image.load("Placeholder-building.png")
building_placeholder_image.anchor_x = 10
building_placeholder_image.anchor_y = 10

player_image = pyglet.image.load("Test-sprite.png")
player_image.anchor_x = 10
player_image.anchor_y = 10

drill_image = pyglet.image.load("Building test sprite-drill.png")
drill_image.anchor_x = 10
drill_image.anchor_y = 10

turret_image = pyglet.image.load("Strat_UN Turret.png")
turret_image.anchor_x = 10
turret_image.anchor_y = 10

#drill_ani = pyglet.resource.animation("Drill_animation.gif")

#drill_frames = []
# for subdir, dirs, files in os.walk(drill_path):
#     for filename in files:
#         filepath = subdir + os.sep + filename
#         drill_frames.append(pyglet.resource.image(filepath))
# print(drill_frames)

drill_ani = pyglet.image.Animation.from_image_sequence(animations.animations.drill_frames, duration=0.017, loop=True)



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

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

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
        super().__init__(img=building_placeholder_image, *args, **kwargs)
        self.health = 1000
        self.owner_id = None
        self.owner_num = None
        self.name = None
        self.lv = 1

    def get_owner(self):
        return self.owner_num

    def get_name(self):
        return self.name

    def set_owner(self, new_owner_id_set):
        self.owner_id = new_owner_id_set[0]
        self.owner_num = new_owner_id_set[1]
        #print(self.owner)

    def hit(self, damage):
        self.health -= damage

class Target(Building):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Target"
        self.owner_id = "Null"
        self.owner_num = -1

    def set_owner(self, *args, **kwargs):
        pass

class Drill(Building):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#img=drill_image,
        self.image = drill_image
        self.color = (0, 0, 0)
        self.name = "Drill"
        self.mine_rate = secrets.choice([2.5, 2.75, 3, 3.25, 3.5])
        self.built = False
        self.build_timer = 10.0

    def update(self, dt):
        if not self.built:
            self.build_timer -= dt
            if self.build_timer <= 0:
                self.image = drill_ani
                # self.x -= 10
                # self.y -= 10 # done because the anchor for position changes from the centre to bottom left corner
                self.color = (0, 255, 0)
                self.built = True
        else:
            mined = self.mine_rate * dt
            #print(self.owner_num)
            if self.owner_num == 1:
                globals.player1_lv1_res += mined
            if self.owner_num == 2:
                globals.player2_lv1_res += mined

    def upgrade(self):
        self.mine_rate *= 1.2


class Basic_Turret(Building):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = turret_image
        self.name = "Turret"
        self.fire_rate = 1.0
        self.targetx = 500
        self.targety = 500
        self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, 0, color=(50, 225, 30))
        self.trace_opacity = 255
        self.damage = 50
        self.first_burst = True
        self.targeting = False

    def update(self, dt):
        for i in globals.building_objects:
            if i.get_owner() != self.owner_num and self.targeting == False:
                #print("found target" + str(i))
                self.targetx = i.get_x()
                self.targety = i.get_y()
                if math.sqrt(((self.x - self.targetx)**2) + ((self.y - self.targety)**2)) <= 250:
                    self.targeting = True
        self.trace_opacity -= (400 * dt)
        if self.targeting:
            if self.trace_opacity < 1:
                self.trace_opacity = 255
                self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, 2, color=(255, 0, 0))
            xdiff = self.targetx - self.x
            ydiff = self.y - self.targety
            if xdiff == 0 or ydiff == 0:
                if self.targetx > self.x and self.targety == self.y:
                    self.rotation = 90
                elif self.targetx == self.x and self.targety < self.y:
                    self.rotation = 180
                elif self.targetx < self.x and self.targety == self.y:
                    self.rotation = 270
                elif self.targetx == self.x and self.targety > self.y:
                    self.rotation = 0
            else:
                rawangle = math.atan(ydiff/xdiff)
            if (self.targetx < self.x and self.targety > self.y) or (self.targetx < self.x and self.targety < self.y):
                self.rotation = 270 + math.degrees(rawangle)
            elif (self.targetx > self.x and self.targety > self.y) or (self.targetx > self.x and self.targety < self.y):
                self.rotation = 90 + math.degrees(rawangle)

            if self.first_burst:
                self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, 2, color=(255, 0, 0))
                self.first_burst = False
            #print(self.trace_opacity)
            self.tracer.opacity = self.trace_opacity

    def set_targetx(self, var):
        self.targetx = var

    def set_targety(self, var):
        self.targety = var

    def get_tracer(self):
        return self.tracer


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
        self.selection = Drill
        self.select_text = "Drill"
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

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_select(self):
        return self.selection

    def add_scounter(self):
        self.scounter += 1

    def add_bcounter(self):
        self.bcounter += 1

    def update(self, dt):
        super(Player, self).update(dt)
        if self.key_handler[key._1]:
            self.selection = Drill

        if self.key_handler[key._2]:
            self.selection = Basic_Turret

        if self.key_handler[key._3]:
            self.selection = Target

        if self.key_handler[key.W]:
            if self.key_handler[key.W] and self.scounter == 0:
                self.y += self.pixels
            if self.scounter == 0:
                self.scounter += 1 * dt

        if self.key_handler[key.A]:
            if self.key_handler[key.A] and self.scounter == 0:
                self.x -= self.pixels
            if self.scounter == 0:
                self.scounter += 1 * dt

        if self.key_handler[key.S]:
            if self.key_handler[key.S] and self.scounter == 0:
                self.y -= self.pixels
            if self.scounter == 0:
                self.scounter += 1 * dt

        if self.key_handler[key.D]:
            if self.key_handler[key.D] and self.scounter == 0:
                self.x += self.pixels
            if self.scounter == 0:
                self.scounter += 1 * dt

        if self.key_handler[key.B] and self.bcounter == 0:  # create some sort of build function
            globals.building_objects.append(self.selection(x=self.x, y=self.y))
            print(globals.building_objects)
            globals.building_objects[len(globals.building_objects)-1].set_owner(self.get_id())
            #building_objects[len(player_list) - 1].color = (0, 0, 255) # NOTE: color function acts as a 'tint' added to sprites
            self.bcounter += 1 * dt

        if self.bcounter > 0:
            self.bcounter += 1 * dt

        if self.scounter > 0:
            self.scounter += 1 * dt

        if self.scounter >= 0.25:
            self.velocity_x = 0
            self.velocity_y = 0
            self.scounter = 0 if self.scounter >= 0.25 else self.scounter
        if self.bcounter >= 10:
            self.bcounter = 0 if self.bcounter >= 10 else self.bcounter