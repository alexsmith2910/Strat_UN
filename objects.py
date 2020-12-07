import os
import math
import pyglet
from pyglet.window import key
import secrets  # Used for better randomness
import random  # Used to save time complexity for common actions
import globals

from src.animations.animation import drill_frames

random.seed(a=os.urandom(1024))  # Used to drastically reduce predictability and therefore chance of abusing of the RNG

grid_set = []

building_placeholder_image = pyglet.image.load("src/sprite/Building-placeholder.png")
building_placeholder_image.anchor_x = 10
building_placeholder_image.anchor_y = 10

troop_placeholder_image = pyglet.image.load("src/sprite/Troop-placeholder.png")
troop_placeholder_image.anchor_x = 10
troop_placeholder_image.anchor_y = 10

player_image = pyglet.image.load("src/sprite/P1-sprite.png")
player_image.anchor_x = 10
player_image.anchor_y = 10

player_2_image = pyglet.image.load("src/sprite/P2-sprite.png")
player_2_image.anchor_x = 10
player_2_image.anchor_y = 10

HQ_image = pyglet.image.load("src/sprite/HQ-sprite.png")
HQ_image.anchor_x = 10
HQ_image.anchor_y = 10

drill_image = pyglet.image.load("src/sprite/Drill-sprite.png")
drill_image.anchor_x = 10
drill_image.anchor_y = 10

refinery_image = pyglet.image.load("src/sprite/Refinery-sprite.png")
refinery_image.anchor_x = 10
refinery_image.anchor_y = 10

turret_image = pyglet.image.load("src/sprite/Basic-turret-sprite.png")
turret_image.anchor_x = 10
turret_image.anchor_y = 10

barracks_image = pyglet.image.load("src/sprite/Barracks-20px.png")
barracks_image.anchor_x = 10
barracks_image.anchor_y = 10

dev_tank_image = pyglet.image.load("src/sprite/Dev-tank-sprite-60.png")
dev_tank_image.anchor_x = 15
dev_tank_image.anchor_y = 30

infantry_image = pyglet.image.load("src/sprite/Basic-infantry-sprite.png")
infantry_image.anchor_x = 10
infantry_image.anchor_y = 10

sniper_image = pyglet.image.load("src/sprite/Sniper-Sprite.png")
sniper_image.anchor_x = 10
sniper_image.anchor_y = 10

#drill_ani = pyglet.resource.animation("Drill_animation.gif")

#drill_frames = []
# for subdir, dirs, files in os.walk(drill_path):
#     for filename in files:
#         filepath = subdir + os.sep + filename
#         drill_frames.append(pyglet.resource.image(filepath))
# print(drill_frames)

drill_ani = pyglet.image.Animation.from_image_sequence(drill_frames, duration=0.017, loop=True)



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
        self.modifier = 1
        self.owner = ""
        self.barrier = False

    def make_barrier(self):
        self.barrier = True

    def remove_barrier(self):
        self.barrier = False

    def set_modifier(self, new_mod):
        self.modifier = new_mod

    def get_modifier(self):
        return self.modifier

    def get_barrier_state(self):
        return self.barrier

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

class Building(TileObject):
    def __init__(self, *args, **kwargs):
        super().__init__(img=building_placeholder_image, *args, **kwargs)
        self.class_type = "Building"
        self.batch = globals.building_batch
        self.max_health = 1000
        self.health = self.max_health
        self.object_type = "Building"
        self.menu_options = False
        self.overlay_name = "Null"
        self.owner_id = None
        self.owner_num = None
        self.name = None
        self.lv = 1
        self.armour = 0
        self.max_shield = 0
        self.shield = self.max_shield
        self.regen = 0
        self.range = -1
        self.damage = 50
        self.armour_pen = 0
        self.first_burst = True
        self.targeting = False
        self.auto_targeting = "N/A"
        self.targeted = None
        self.immobilizer = False
        self.immobilizer_strength = None
        self.dot = False
        self.dot_strength = None
        self.fire_rate = 1.0

        self.dot_damage = 0

    def key_left_func(self):
        pass

    def key_right_func(self):
        pass

    def enter_func(self):
        pass

    def hit(self, damage, imm_strength=None, dot_strength=None, armour_pen=0):
        pierced = damage * min((1 - (self.armour / 100) + (self.armour_pen / 100)), 1)
        if self.shield > 0:
            self.shield -= damage
            damage = 0
            if self.shield < 0:
                damage = self.shield * -1
                self.shield = 0

        elif self.shield <= 0:
            self.health -= pierced

        if dot_strength != None:
            self.dot_damage += dot_strength

    def shield_regen(self, dt):
        if self.shield < self.max_shield:
            self.shield += self.regen * dt
            if self.shield > self.max_shield:
                self.shield = self.max_shield

    def death_check(self):
        if self.health <= 0:
            del globals.building_objects[globals.building_objects.index(self)]
            print(globals.building_objects)
            # self.x = -100000000
            # self.y = -100000000

    def get_owner(self):
        return self.owner_num

    def get_owner_id(self):
        return self.owner_id

    def get_name(self):
        return self.name

    def get_overlay_name(self):
        return self.overlay_name

    def get_range(self):
        return self.range

    def get_obj_type(self):
        return self.object_type

    def get_needs_menu(self):
        return self.menu_options

    def get_health(self):
        return self.health

    def get_shield(self):
        return self.shield

    def get_targetbool(self):
        return self.auto_targeting

    def set_owner(self, new_owner_id_set):
        self.owner_id = new_owner_id_set[0]
        self.owner_num = new_owner_id_set[1]
        if self.owner_num == 1:
            self.color = globals.p1_color
        elif self.owner_num == 2:
            self.color = globals.p2_color
        elif self.owner_num == 3:
            self.color = globals.p3_color
        elif self.owner_num == 4:
            self.color = globals.p4_color
        #print(self.owner)

    def hit(self, damage):
        self.health -= damage

class Troop(TileObject):
    overlay_name = "Unedited troop"
    training_time = 5
    def __init__(self, *args, **kwargs):
        super().__init__(img=troop_placeholder_image, *args, **kwargs)
        # General Identifiers
        self.class_type = "Troop"
        self.object_type = "Troop"
        self.overlay_name = "Null"
        self.owner_id = None
        self.owner_num = None
        self.name = None
        self.lv = 1
        self.menu_options = False
        # Defence characteristics
        self.max_health = 250
        self.health = self.max_health
        self.h_bar = pyglet.shapes.Rectangle((self.x - 10), (self.y + 22), 20, 2, (0, 255, 0), batch=globals.bar_batch)
        self.armour = 0
        self.max_shield = 0
        self.shield = self.max_shield
        self.s_bar = pyglet.shapes.Rectangle((self.x - 10), (self.y + 20), 20, 2, (0, 0, 255), batch=globals.bar_batch)
        self.regen = 0
        # Movement and pathfinding characteristics
        self.accel = 0.2
        self.speed = 0
        self.topspeed = 20
        self.speed = 0
        self.targeting_p = False
        self.targeted_p = None
        self.cpath = [] # c for 'current' path that it is using
        self.ctarget = None # current target coords
        self.last_tile = None
        self.current_tile = None
        self.current_mod = 1
        self.firstpathstep = True
        self.auto_shooting = False
        # Weapon characteristics
        self.auto_targeting = False
        self.target_type_allowed = ("Troop", "Preferred")
        self.target_type = None #Building or troop
        self.damage = 50
        self.armour_pen = 0
        self.range = 50
        self.fire_rate = 100 # num/255 per second
        self.first_burst = True
        self.targeting = False
        self.targeted = None
        self.targetx = None
        self.targety = None
        self.tracer_colour = (255, 255, 255)
        self.tracer_width = 2
        self.tracer = pyglet.shapes.Line(0, 0, 0, 0, 0, color=self.tracer_colour)
        self.trace_opacity = 255
        self.has_tracer = False
        self.immobilizer = False
        self.immobilizer_strength = None
        self.dot = False
        self.dot_strength = None

        self.dot_damage = 0

    def key_left_func(self):
        pass

    def key_right_func(self):
        pass

    def enter_func(self):
        pass

    def range_sort(self, array):
        self.auto_targeting_array = []
        for i in array:
            if self.auto_targeting_array == []:
                self.auto_targeting_array.append(i)
            else:
                for j in array[0:]:
                    for count, k in enumerate(self.auto_targeting_array):
                        if self.get_distance(j.get_x(), j.get_y()) > self.get_distance(k.get_x(), k.get_y()):
                            pass
                        else:
                            self.auto_targeting_array.insert(count, i)
                            break
        #print(self.auto_targeting_array)

    def pathfind(self, target_coords=(550, 550)):
        self.cpath = []
        self.ctarget = None
        # print("beginning pathfinding to: " + str(target_coords)) # used for debugging, same applies for lines marked 'D'
        astar_start_coords = self.get_astar_coords(self.x, globals.screenresy - self.y)
        astar_target_coords = self.get_astar_coords(target_coords[0], globals.screenresy - target_coords[1])
        # print("a*" + str(self.get_astar_coords(self.x, self.y))) # D
        start = globals.astar_matrix.node(astar_start_coords[0], (astar_start_coords[1]))
        end = globals.astar_matrix.node(int(astar_target_coords[0]), int((astar_target_coords[1])))
        path, runs = globals.finder.find_path(start, end, globals.astar_matrix)
        # print(globals.astar_matrix.grid_str(path=path, start=start, end=end))# use this if you want to see the path in the console
        # print("runs: " + str(runs)) # D
        counter = 0
        for counter, i in enumerate(path):
            self.cpath.append([])
            # print(i) # D
            #print(path)
            for countj, j in enumerate(i):
                if countj == 0:# x coord
                    temp = ((j * 20) + 10)
                else:# ycoord - 'flip' coord to make it compatable with pyglet
                    temp = globals.screenresy - ((j * 20) + 10)

                self.cpath[counter].append(int(temp))
        # del self.cpath[0]
        # for i in self.cpath:
        #     i[1] += 20
        # print(self.cpath) # D
        # print(globals.astar_matrix.grid_str(path=path, start=start, end=end)) # D
        if self.cpath != []:
            self.ctarget = self.cpath[0]
        globals.astar_matrix.cleanup()

    def auto_target(self):
        found = False
        self.auto_targeting_array = []
        if self.target_type_allowed[0] == "Building":
            self.range_sort(globals.building_objects)
            for i in self.auto_targeting_array:
                if i.get_owner() != self.owner_num and i.get_range() < self.range:
                    # print("found target" + str(i)) # D
                    self.pathfind((i.get_x(), i.get_y()))
                    break

            if self.targeted == None:
                for i in self.auto_targeting_array:
                    if i.get_owner() != self.owner_num:
                        self.pathfind((i.get_x(), i.get_y()))
                        break

        elif self.target_type_allowed[0] == "Troop":
            self.range_sort(globals.troop_objects)
            for i in self.auto_targeting_array:
                if i.get_owner() != self.owner_num and i.get_range() < self.range:
                    self.pathfind((i.get_x(), i.get_y()))
                    break

            if self.targeted == None:
                for i in self.auto_targeting_array:
                    if i.get_owner() != self.owner_num:
                        self.pathfind((i.get_x(), i.get_y()))
                        break

        if self.target_type_allowed[0] == "Troop" and \
                self.target_type_allowed[1] == "Preferred" and not self.targeting:
            self.range_sort(globals.building_objects)
            for i in self.auto_targeting_array:
                if i.get_owner() != self.owner_num and i.get_range() < self.range:
                    self.pathfind((i.get_x(), i.get_y()))
                    break

            if self.targeted == None:
                for i in self.auto_targeting_array:
                    if i.get_owner() != self.owner_num:
                        self.pathfind((i.get_x(), i.get_y()))
                        break

        if self.target_type_allowed[0] == "Building" and \
                self.target_type_allowed[1] == "Preferred" and not self.targeting:
            self.range_sort(globals.troop_objects)
            for i in self.auto_targeting_array:
                if i.get_owner() != self.owner_num and i.get_range() < self.range:
                    self.pathfind((i.get_x(), i.get_y()))
                    break

            if self.targeted == None:
                for i in self.auto_targeting_array:
                    if i.get_owner() != self.owner_num:
                        self.pathfind((i.get_x(), i.get_y()))
                        break

    def hit(self, damage, imm_strength=None, dot_strength=None, armour_pen=0):
        pierced = damage * min((1 - (self.armour / 100) + (self.armour_pen / 100)), 1)
        if self.shield > 0:
            self.shield -= damage
            damage = 0
            if self.shield < 0:
                damage = self.shield * -1
                self.shield = 0

        elif self.shield <= 0:
            self.health -= pierced

        if dot_strength != None:
            self.dot_damage += dot_strength

        if imm_strength != None:
            temp = self.speed
            self.speed -= (self.speed * imm_strength)

    def shield_regen(self, dt):
        if self.shield < self.max_shield:
            self.shield += self.regen * dt
            if self.shield > self.max_shield:
                self.shield = self.max_shield

    def death_check(self):
        if self.health <= 0:
            del globals.troop_objects[globals.troop_objects.index(self)]
            print(globals.troop_objects)
            # self.x = -100000000
            # self.y = -100000000

    def get_centred_coords(self, x, y):
        x_remainder = x % 20
        y_remainder = y % 20
        x_centred = (x - x_remainder) + 10
        y_centred = (y - y_remainder) + 10
        return x_centred, y_centred

    def move(self, dt):
        cur_tile = self.get_centred_coords(self.x, self.y)
        if (self.last_tile != cur_tile or self.last_tile is None):
            for i in globals.squares:
                for j in i:
                    if self.get_centred_coords(j.get_x(), j.get_y()) == cur_tile:
                        self.current_tile = j
                        self.last_tile = (self.current_tile.get_x(), self.current_tile.get_y())
                        self.current_mod = self.current_tile.get_modifier()
                        # print(self.current_mod)
                        break


        if self.ctarget != None:
            if self.firstpathstep:
                # print("pathing to: " + str(self.ctarget)) # D
                self.firstpathstep = False
            rawangle = None
            if self.speed < self.topspeed:
                self.speed += (self.accel * dt)
            xdiff = self.ctarget[0] - self.x
            ydiff = self.y - self.ctarget[1]
            if xdiff == 0 or ydiff == 0:
                if self.ctarget[0] > self.x and self.ctarget[1] == self.y:
                    self.rotation = 90
                elif self.ctarget[0] == self.x and self.ctarget[1] < self.y:
                    self.rotation = 180
                elif self.ctarget[0] < self.x and self.ctarget[1] == self.y:
                    self.rotation = 270
                elif self.ctarget[0] == self.x and self.ctarget[1] > self.y:
                    self.rotation = 0
            else:
                rawangle = math.atan(ydiff / xdiff)
            if (self.ctarget[0] < self.x and self.ctarget[1] > self.y) or (self.ctarget[0] < self.x and self.ctarget[1] < self.y):
                self.rotation = 270 + math.degrees(rawangle)
            elif (self.ctarget[0] > self.x and self.ctarget[1] > self.y) or (self.ctarget[0] > self.x and self.ctarget[1] < self.y):
                self.rotation = 90 + math.degrees(rawangle)

            if rawangle != None:
                if self.x < self.ctarget[0] and self.y < self.ctarget[1]: #NE
                    self.x += self.speed * math.cos(rawangle) * dt * self.current_mod
                    self.y -= self.speed * math.sin(rawangle) * dt * self.current_mod
                if self.x < self.ctarget[0] and self.y > self.ctarget[1]: #SE
                    self.x += self.speed * math.cos(rawangle) * dt * self.current_mod
                    self.y -= self.speed * math.sin(rawangle) * dt * self.current_mod
                if self.x > self.ctarget[0] and self.y > self.ctarget[1]: #SW
                    self.x -= self.speed * math.cos(rawangle) * dt * self.current_mod
                    self.y += self.speed * math.sin(rawangle) * dt * self.current_mod
                if self.x > self.ctarget[0] and self.y < self.ctarget[1]: #NW
                    self.x -= self.speed * math.cos(rawangle) * dt * self.current_mod
                    self.y += self.speed * math.sin(rawangle) * dt * self.current_mod

            else:
                if self.ctarget[0] > self.x and self.ctarget[1] == self.y:
                    self.x += self.speed * dt * self.current_mod
                elif self.ctarget[0] == self.x and self.ctarget[1] < self.y:
                    self.y -= self.speed * dt * self.current_mod
                elif self.ctarget[0] < self.x and self.ctarget[1] == self.y:
                    self.x -= self.speed * dt * self.current_mod
                elif self.ctarget[0] == self.x and self.ctarget[1] > self.y:
                    self.y += self.speed * dt * self.current_mod

            if math.sqrt(((self.x - self.ctarget[0]) ** 2) + ((self.y - self.ctarget[1]) ** 2)) <= 1:
                self.x = self.ctarget[0]
                self.y = self.ctarget[1]

            if self.x == self.ctarget[0] and self.y == self.ctarget[1]:
                self.firstpathstep = True
                self.ctarget = None
                if self.cpath != []:
                    del self.cpath[0]
                    if self.cpath != []:
                        self.ctarget = self.cpath[0]
                    else:
                        self.speed = 0
                        self.last_tile = None
                        self.current_tile = None
                        self.current_mod = 1
            # if self.firstpathstep: # D
                # print("angle: " + str(rawangle)) # D NOTE: angle is recorded in radians

    def fire(self):
        self.targeted.hit(damage=self.damage, armour_pen=self.armour_pen)
        self.targeted.death_check()

    def shoot(self, dt):
        if self.trace_opacity > 0:
            self.trace_opacity -= (self.fire_rate * dt)
            self.tracer.opacity = self.trace_opacity
        if self.targeted is None:
            if self.auto_shooting == True:
                self.auto_shooting = False
            if self.trace_opacity < 1:
                self.trace_opacity = 0
            else:
                self.trace_opacity -= (100 * dt)
            self.tracer.opacity = self.trace_opacity
        if self.targeted is not None:
            if self.auto_targeting:
                self.cpath = []
                self.ctarget = None
                self.auto_shooting = True
            try:
                if globals.building_objects.index(self.targeted):
                        self.targetx = self.targeted.get_x()
                        self.targety = self.targeted.get_y()
                        if math.sqrt(((self.x - self.targetx) ** 2) + ((self.y - self.targety) ** 2)) <= self.range:
                            self.targeting = True
            except:
                self.targeted = None
                self.targeting = False
                #self.tracer.opacity = 0
        else:
            if self.target_type_allowed[0] == "Building":
                for i in globals.building_objects:
                    if i.get_owner() != self.owner_num and self.targeting is False:
                        self.targetx = i.get_x()
                        self.targety = i.get_y()
                        if math.sqrt(((self.x - self.targetx)**2) + ((self.y - self.targety)**2)) <= self.range:
                            self.targeting = True
                            self.targeted = i
                            self.cpath = []
                        else:
                            self.targeting = False
                            self.targeted = None

            elif self.target_type_allowed[0] == "Troop":
                for i in globals.troop_objects:
                    if i.get_owner() != self.owner_num and self.targeting is False:
                        self.targetx = i.get_x()
                        self.targety = i.get_y()
                        if math.sqrt(((self.x - self.targetx)**2) + ((self.y - self.targety)**2)) <= self.range:
                            self.targeting = True
                            self.targeted = i
                            self.cpath = []
                        else:
                            self.targeting = False
                            self.targeted = None

            if self.target_type_allowed[0] == "Troop" and self.target_type_allowed[1] == "Preferred" and not self.targeting:
                for i in globals.building_objects:
                    if i.get_owner() != self.owner_num and self.targeting is False:
                        self.targetx = i.get_x()
                        self.targety = i.get_y()
                        if math.sqrt(((self.x - self.targetx)**2) + ((self.y - self.targety)**2)) <= self.range:
                            self.targeting = True
                            self.targeted = i
                            self.cpath = []
                        else:
                            self.targeting = False
                            self.targeted = None

            if self.target_type_allowed[0] == "Building" and self.target_type_allowed[1] == "Preferred" and not self.targeting:
                for i in globals.troop_objects:
                    if i.get_owner() != self.owner_num and self.targeting is False:
                        self.targetx = i.get_x()
                        self.targety = i.get_y()
                        if math.sqrt(((self.x - self.targetx)**2) + ((self.y - self.targety)**2)) <= self.range:
                            self.targeting = True
                            self.targeted = i
                            self.cpath = []
                        else:
                            self.targeting = False
                            self.targeted = None

        self.trace_opacity -= (self.fire_rate * dt)
        if self.targeting:
            if self.trace_opacity < 1 and self.ctarget == None:
                self.trace_opacity = 255
                self.targeted.hit(self.damage)
                if self.targeted is not None:
                    self.fire()
                    self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, 2, color=self.tracer_colour)
            if self.ctarget == None:
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
                    self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, self.tracer_width, color=self.tracer_colour)
                    self.first_burst = False
                self.tracer.opacity = self.trace_opacity

                if self.auto_targeting and self.targeting and self.speed != 0:
                    self.speed = 0

    def bars(self):
        if self.health == self.max_health and self.shield == self.max_shield:
            self.h_bar.opacity = 0
            self.s_bar.opacity = 0
        else:
            self.h_bar.opacity = 255
            self.s_bar.opacity = 255

            self.h_bar.width = round((self.health / self.max_health) * 20)
            self.h_bar.x = (self.x - 10)
            self.h_bar.y = (self.y + 22)
            if self.max_shield > 0:
                self.s_bar.width = round((self.shield / self.max_shield) * 20)
                self.s_bar.x = (self.x - 10)
                self.s_bar.y = (self.y + 20)
            else:
                self.s_bar.width = 0

    def update(self, dt):
        self.shoot(dt)
        self.bars()
        if self.targeted is None or not self.auto_targeting:
            self.move(dt)
        if not self.targeting and not self.auto_shooting and self.auto_targeting and self.ctarget == None:
            self.auto_target()
        if self.ctarget == None and self.cpath == []:
            self.speed == 0
        if self.max_shield > 0:
            self.shield_regen(dt)

    def set_owner(self, new_owner_id_set):
        self.owner_id = new_owner_id_set[0]
        self.owner_num = new_owner_id_set[1]
        if self.owner_num == 1:
            self.color = globals.p1_color
        elif self.owner_num == 2:
            self.color = globals.p2_color
        elif self.owner_num == 3:
            self.color = globals.p3_color
        elif self.owner_num == 4:
            self.color = globals.p4_color
        #print(self.owner)

    def set_targetx(self, var):
        self.targetx = var

    def set_targety(self, var):
        self.targety = var

    def get_astar_coords(self, x, y):
        # print(x, y)
        astarx = int(((x - 10)/20))
        astary = int(((y - 10)/20))
        # print(astarx, astary)
        return astarx, astary

    def get_distance(self, targetx, targety):
        return math.sqrt(((self.x - targetx) ** 2) + ((self.y - targety) ** 2))

    def get_weapon_tracing(self):
        return self.has_tracer

    def get_owner(self):
        return self.owner_num

    def get_name(self):
        return self.name

    def get_obj_type(self):
        return self.building_type

    def get_tracer(self):
        return self.tracer

    def get_tracer(self):
        return self.tracer

    def get_range(self):
        return self.range

    def get_overlay_name(self):
        return self.overlay_name

    def get_health(self):
        return self.health

    def get_shield(self):
        return self.shield

    def get_targetbool(self):
        return self.auto_targeting

    def get_owner_id(self):
        return self.owner_id

    def get_needs_menu(self):
        return self.menu_options



# Miscellaneous

class Target(Building):
    overlay_name = "Target"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "Target"
        self.overlay_name = "Target"
        self.owner_id = "Null"
        self.owner_num = -1

    def set_owner(self, *args, **kwargs):
        pass

# Static buildings

class HQ(Building):
    overlay_name = "HQ"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#img=drill_image,
        self.image = HQ_image
        self.color = (0, 0, 0)
        self.name = "HQ"
        self.overlay_name = "HQ"
        self.building_type = "Static"
        self.max_health = 50000
        self.armour = 85
        self.health = self.max_health
        #self.mine_rate = secrets.choice([2.5, 2.75, 3, 3.25, 3.5])
        #self.built = False
        #self.activation_timer = 10.0

    def update(self, dt):
        pass

# Industry buildings
class Drill(Building): # TODO: complete and ensure all objects work correctly with player 2, incorrect colouring for P2 confirmed.
    overlay_name = "Drill"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#img=drill_image,
        self.image = drill_image
        self.color = (0, 0, 0)
        self.name = "Drill"
        self.overlay_name = "Drill"
        self.building_type = "Industry"
        self.mine_rate = secrets.choice([2.5, 2.75, 3, 3.25, 3.5])
        self.built = False
        self.activation_timer = 10.0

    def update(self, dt):
        if not self.built:
            self.activation_timer -= dt
            if self.activation_timer <= 0:
                self.image = drill_ani
                # self.x -= 10
                # self.y -= 10 # done because the anchor for position changes from the centre to bottom left corner
                self.built = True
                if self.owner_num == 1:
                    globals.player1_lv1_gen += self.mine_rate
                elif globals.offline_multi:
                    globals.player2_lv1_gen += self.mine_rate

        else:
            mined = self.mine_rate * dt
            #print(self.owner_num)
            if self.owner_num == 1:
                globals.player1_lv1_res += mined
            if self.owner_num == 2:
                globals.player2_lv1_res += mined

    def upgrade(self):
        self.mine_rate *= 1.2

class Refinery(Building):
    overlay_name = "Refinery"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#img=drill_image,
        self.image = refinery_image
        self.color = (0, 0, 0)
        self.name = "Refinery"
        self.overlay_name = "Refinery"
        self.building_type = "Industry"
        self.process_rate = 0.75
        self.built = False
        self.activation_timer = 10.0

    def update(self, dt):
        if not self.built:
            self.activation_timer -= dt
            if self.activation_timer <= 0:
                #self.image = drill_ani
                # self.x -= 10
                # self.y -= 10 # done because the anchor for position changes from the centre to bottom left corner
                self.built = True

                if self.owner_num == 1:
                    globals.player1_lv1_gen -= (10 * self.process_rate)
                    globals.player1_lv2_gen += self.process_rate
                elif globals.offline_multi:
                    globals.player2_lv1_gen -= (10 * self.process_rate)
                    globals.player2_lv2_gen += self.process_rate

        else:
            purified = self.process_rate * dt
            # print(self.owner_num)
            if self.owner_num == 1:
                globals.player1_lv2_res += purified
                globals.player1_lv1_res -= 10 * purified
            elif globals.offline_multi:
                globals.player2_lv2_res += purified
                globals.player2_lv1_res -= 10 * purified


class Oil_Rig(Building):
    overlay_name = "Oil Rig"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#img=drill_image,
        #self.image = refinery_image
        self.color = (0, 0, 0)
        self.name = "Oil Rig"
        self.overlay_name = "Oil Rig"
        self.building_type = "Industry"
        self.process_rate = 0.75
        self.prev_process_rate = self.process_rate
        self.built = False
        self.activation_timer = 10.0

    def update(self, dt):
        if not self.built:
            self.activation_timer -= dt
            if self.activation_timer <= 0:
                self.built = True
                if self.owner_num == 1:
                    globals.player1_lv3_gen += self.process_rate

                elif globals.offline_multi:
                    globals.player2_lv3_gen += self.process_rate
        else:
            self.prev_process_rate = self.process_rate
            pumped = self.process_rate * dt
            if self.owner_num == 1:
                globals.player1_lv3_res += pumped
            elif globals.offline_multi:
                globals.player2_lv3_res += pumped
            if secrets.randbelow(2) == 0:
                self.process_rate -= dt * 0.3 # simulation of concentration of oil to be pumped changing
                if self.process_rate < 0.5:
                    self.process_rate == 0.5
            else:
                self.process_rate += dt * 0.3
                if self.process_rate < 1.5:
                    self.process_rate == 1.5

            if self.owner_num == 1:
                globals.player1_lv3_gen -= self.prev_process_rate
                globals.player1_lv3_gen += self.process_rate

            elif globals.offline_multi:
                globals.player2_lv3_gen -= self.prev_process_rate
                globals.player2_lv3_gen += self.process_rate

# Workshop

class Workshop(Building):
    overlay_name = "Workshop"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)#img=drill_image,
        self.image = refinery_image
        self.color = (0, 0, 0)
        self.name = "Workshop"
        self.building_type = "Industry"
        self.process_rate = 0.75
        self.built = False
        self.activation_timer = 10.0



# Defense buildings
class Basic_Turret(Building):
    overlay_name = "Turret"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = turret_image
        self.name = "Turret"
        self.building_type = "Tracing turret"
        self.overlay_name = "Turret"
        self.fire_rate = 1.0
        self.targetx = 500
        self.targety = 500
        self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, 0, color=(50, 225, 30))
        self.trace_opacity = 255
        self.damage = 50
        self.first_burst = True
        self.targeting = False
        self.targeted = None

    def fire(self):
        self.targeted.hit(self.damage)
        self.targeted.death_check()

    def update(self, dt):
        if self.targeted is None:
            if self.trace_opacity < 1:
                self.trace_opacity = 0
            else:
                self.trace_opacity -= (400 * dt)
            self.tracer.opacity = self.trace_opacity
        if self.targeted is not None:
            try:
                if globals.building_objects.index(self.targeted):
                        self.targetx = self.targeted.get_x()
                        self.targety = self.targeted.get_y()
                        if math.sqrt(((self.x - self.targetx) ** 2) + ((self.y - self.targety) ** 2)) <= 250:
                            self.targeting = True
            except:
                self.targeted = None
                self.targeting = False
                #self.tracer.opacity = 0
        else:
            for i in globals.building_objects:
                if i.get_owner() != self.owner_num and self.targeting is False:
                    #print("found target" + str(i))
                    self.targetx = i.get_x()
                    self.targety = i.get_y()
                    if math.sqrt(((self.x - self.targetx)**2) + ((self.y - self.targety)**2)) <= 250:
                        self.targeting = True
                        self.targeted = i
                    else:
                        self.targeting = False
                        self.targeted = None
        self.trace_opacity -= (400 * dt)
        if self.targeting:
            if self.trace_opacity < 1:
                self.trace_opacity = 255
                if self.targeted is not None:
                    self.fire()
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

#Army buildings
class Barracks(Building):
    overlay_name = "Barracks"
    #TODO: (need sniper first for testing) make barracks train troops,
    # then make it to order and viewable by overlay
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = barracks_image
        self.ol_selection = [Basic_infantry, Sniper, Dev_Tank]
        self.selected_index = 0
        self.queue = []
        self.ol_queue = []
        self.max_health = 1000
        self.health = self.max_health
        self.object_type = "Trainer"
        self.overlay_name = "Barracks"
        self.menu_options = True
        self.owner_id = None
        self.owner_num = None
        self.name = None
        self.lv = 1
        self.armour = 15
        self.max_shield = 0
        self.shield = self.max_shield
        self.regen = 0
        self.range = -1
        self.train_flag = False
        self.train_time = 0
        self.train_lim = -1

    def train(self):
        if self.train_flag and self.train_time >= 0:
            globals.troop_objects.append(self.queue[0](x=self.x, y=self.y))
            globals.troop_objects[len(globals.building_objects) - 1].set_owner(self.get_owner_id())
            del self.queue[0]

    def queue_selected(self):
        self.queue.append(self.ol_selection[self.selected_index])

    def gen_overlay_text(self):
        l1 = "⇦ and ⇨ to change choice"
        l2 = "Add to training queue (enter):"
        l3_select = (self.ol_selection[self.selected_index])
        l3 = str(self.ol_selection[self.selected_index].overlay_name)
        self.ol_queue = []
        for i in self.queue:
            self.ol_queue.append(i.overlay_name)
        l4 = str(self.ol_queue)
        #l3 = ((self.ol_selection[self.selected_index]).get_overlay_name(self))
        return l1, l2, l3, l4

    def key_right_func(self):
        self.selected_index += 1
        if self.selected_index >= len(self.ol_selection):
            self.selected_index = 0
            # print((self.ol_selection[self.selected_index].get_overlay_name(self)))

    def key_left_func(self):
        self.selected_index -= 1
        if self.selected_index < 0:
            self.selected_index = (len(self.ol_selection) - 1)
            # print((self.ol_selection[self.selected_index].get_overlay_name(self)))

    def enter_func(self):
        # print("started training")
        self.queue_selected()
        self.train_time += 0.000001

    def update(self, dt):
        if self.train_time > 0:
            self.train_lim = self.queue[0].training_time
            self.train_time += dt
            # print(str(self.train_time - self.train_lim))
        if self.train_time >= self.train_lim and self.queue != []:
            globals.troop_objects.append((self.queue[0])(x=self.x, y=self.y))
            globals.troop_objects[(len(globals.troop_objects) - 1)]\
                .set_owner((self.get_owner_id(), self.get_owner()))
            move_x = self.x
            move_y = self.y
            while move_x == self.x and move_y == self.y and move_x <= globals.screenresx and move_y <= globals.screenresy:
                move_x = random.randint(self.x-100, self.x+100)
                move_y = random.randint(self.y-100, self.y+100)
            globals.troop_objects[(len(globals.troop_objects) - 1)] \
                .pathfind((move_x, move_y))
            #TODO: make troop move away from the building to prevent stacking
            del self.queue[0]
            if self.queue != []:
                self.train_time = 0.000001
            else:
                self.train_time = 0
            # print("trained")
#Troops

class Dev_Tank(Troop):
    overlay_name = "Overloader"
    training_time = 120
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = globals.large_troop_batch
        self.image = dev_tank_image
        self.name = "Dev_Tank"
        self.troop_type = "EMP Medium Tank"
        self.overlay_name = "Overloader"
        self.fire_rate = 100
        self.targetx = 500
        self.targety = 500
        self.tracer_colour = (129, 236, 236)
        self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, 0, color=(129, 236, 236))
        self.trace_opacity = 255
        self.has_tracer = True
        self.damage = 100
        self.range = 150
        self.lv = 1
        self.max_health = 3000
        self.health = self.max_health
        self.accel = 0.5
        self.topspeed = 10
        self.speed = 0
        self.armour = 40
        self.max_shield = 1500
        self.shield = self.max_shield
        self.regen = 15
        self.first_burst = True
        self.targeting = False
        self.targeted = None

        self.immobilizer = True
        self.immobilizer_strength = 0.5

    def fire(self):
        self.targeted.hit(self.damage)
        self.targeted.death_check()

    def set_targetx(self, var):
        self.targetx = var

    def set_targety(self, var):
        self.targety = var

class Basic_infantry(Troop):
    overlay_name = "Infantry"
    training_time = 5
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = globals.small_troop_batch
        self.image = infantry_image
        self.name = "Infantry"
        self.troop_type = "Light Infantry"
        self.overlay_name = "Infantry"
        self.fire_rate = 750
        self.targetx = 500
        self.targety = 500
        # self.tracer_colour = (129, 236, 236)
        # self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, 0, color=(129, 236, 236))
        # self.trace_opacity = 255
        self.has_tracer = False
        self.damage = 5
        self.range = 50
        self.lv = 1
        self.max_health = 200
        self.health = self.max_health
        self.accel = 2.5
        self.topspeed = 5
        self.speed = 0
        self.armour = 2
        self.max_shield = 0
        self.shield = self.max_shield
        self.regen = 0
        self.first_burst = True
        self.targeting = False
        self.targeted = None
        self.immobilizer = False

    def fire(self):
        self.targeted.hit(self.damage)
        self.targeted.death_check()

    def set_targetx(self, var):
        self.targetx = var

    def set_targety(self, var):
        self.targety = var

class Sniper(Troop):
    overlay_name = "Sniper"
    training_time = 20
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = globals.small_troop_batch
        self.image = sniper_image
        self.name = "Sniper"
        self.troop_type = "Light Sniper Infantry"
        self.overlay_name = "Sniper"
        self.fire_rate = 50
        self.targetx = 500
        self.targety = 500
        self.tracer_colour = (129, 236, 236)
        self.tracer_width = 1
        self.tracer = pyglet.shapes.Line(self.x, self.y, self.targetx, self.targety, 0, color=(129, 236, 236))
        self.trace_opacity = 255
        self.has_tracer = True
        self.damage = 450
        self.range = 50
        self.lv = 1
        self.max_health = 500
        self.health = self.max_health
        self.accel = 0.25
        self.topspeed = 5
        self.speed = 0
        self.armour = 10
        self.max_shield = 0
        self.shield = self.max_shield
        self.regen = 0
        self.first_burst = True
        self.targeting = False
        self.targeted = None
        self.immobilizer = False

class Player(TileObject):
    """class for generating a object for the player to control"""

    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)
        self.num = -1
        self.id = None
        self.pixels = 20
        # self.key_handler = key.KeyStateHandler()
        self.scounter = 0
        self.bcounter = 0
        self.call_counter = 0
        self.ol_counter = 0
        self.selection = Drill
        self.select_text = "Drill"
        globals.player_list.append(self)

        #controls
        self.up_key = key.W
        self.left_key = key.A
        self.down_key = key.S
        self.right_key = key.D
        self.build_key = key.B
        self.call_key = key.EQUAL

        self.zero_key = key._0
        self.one_key = key._1
        self.two_key = key._2
        self.three_key = key._3
        self.four_key = key._4
        self.five_key = key._5
        self.six_key = key._6
        self.seven_key = key._7
        self.eight_key = key._8
        self.nine_key = key._9

    def set_id(self, new_name, num=1, offline=True):
        """sets the name for the player, use ONCE per player ONLY"""
        if self.id == None:
            self.id = str(new_name)
            self.num = num
            globals.player_list.append(str(new_name))

        if num == 2:
            self.image = player_2_image
            if globals.offline_multi:
                self.up_key = key.I
                self.left_key = key.J
                self.down_key = key.K
                self.right_key = key.L
                self.build_key = key.M

                if globals.distribution:
                    self.zero_key = key.NUM_0
                    self.one_key = key.NUM_1
                    self.two_key = key.NUM_2
                    self.three_key = key.NUM_3
                    self.four_key = key.NUM_4
                    self.five_key = key.NUM_5
                    self.six_key = key.NUM_6
                    self.seven_key = key.NUM_7
                    self.eight_key = key.NUM_8
                    self.nine_key = key.NUM_9
                    self.call_key = key.NUM_DECIMAL

                else:
                    self.zero_key = 65379
                    self.one_key = 65367
                    self.two_key = 65364
                    self.three_key = 65366
                    self.four_key = 65361
                    self.five_key = 51539607552
                    self.six_key = 65363
                    self.seven_key = 65360
                    self.eight_key = 65362
                    self.nine_key = 65365
                    self.call_key = 65535

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
        if globals.key_handler[self.one_key]:
            self.selection = Drill
            self.select_text = "Drill"

        if globals.key_handler[self.two_key]:
            self.selection = Refinery
            self.select_text = "Refinery"

        if globals.key_handler[self.three_key]:
            self.selection = Basic_Turret
            self.select_text = "Basic_Turret"

        if globals.key_handler[self.four_key]:
            self.selection = Oil_Rig
            self.select_text = "Oil_Rig"

        if globals.key_handler[self.five_key]:
            self.selection = Barracks
            self.select_text = "Barracks"


        if globals.key_handler[self.zero_key]:
            self.selection = Target
            self.select_text = "Target"

        if globals.key_handler[self.call_key] and self.call_counter == 0:
            if globals.clickable is not None and globals.clickable.get_owner() == self.num and globals.clickable.class_type == "Troop":
                globals.clickable.pathfind((self.x, self.y))

            # for i in globals.troop_objects:
            #     if i.get_owner() == 1:
            #         i.pathfind((self.x, self.y))
            # self.call_counter += 1 * dt

        if globals.key_handler[self.up_key]:
            if self.scounter == 0:
                self.y += self.pixels
            if self.scounter == 0:
                self.scounter += 1 * dt

        if globals.key_handler[self.left_key]:
            if self.scounter == 0:
                self.x -= self.pixels
            if self.scounter == 0:
                self.scounter += 1 * dt

        if globals.key_handler[self.down_key]:
            if self.scounter == 0:
                self.y -= self.pixels
            if self.scounter == 0:
                self.scounter += 1 * dt

        if globals.key_handler[self.right_key]:
            if self.scounter == 0:
                self.x += self.pixels
            if self.scounter == 0:
                self.scounter += 1 * dt

        if globals.key_handler[self.build_key] and self.bcounter == 0:  # create some sort of build function
            costs = globals.building_costs[self.select_text]
            if globals.player1_lv1_res >= costs[0] and\
                globals.player1_lv2_res >= costs[1] and\
                globals.player1_lv3_res >= costs[2]:

                globals.player1_lv1_res -= (globals.building_costs[self.select_text])[0]
                globals.player1_lv2_res -= (globals.building_costs[self.select_text])[1]
                globals.player1_lv3_res -= (globals.building_costs[self.select_text])[2]

                globals.building_objects.append(self.selection(x=self.x, y=self.y))
                print(globals.building_objects)
                globals.building_objects[len(globals.building_objects)-1].set_owner(self.get_id())
            #building_objects[len(player_list) - 1].color = (0, 0, 255) # NOTE: color function acts as a 'tint' added to sprites
            self.bcounter += dt

        if self.bcounter > 0:
            self.bcounter += dt

        if self.call_counter > 0:
            self.call_counter += dt

        if self.scounter > 0:
            self.scounter += dt

        if self.scounter >= 0.25:
            self.velocity_x = 0
            self.velocity_y = 0
            self.scounter = 0 if self.scounter >= 0.25 else self.scounter
        if self.bcounter >= 3:
            self.bcounter = 0 if self.bcounter >= 3 else self.bcounter
        if self.call_counter >= 5:
            self.call_counter = 0 if self.call_counter >= 5 else self.call_counter
        if self.ol_counter >= 1:
            self.ol_counter = 0 if self.ol_ounter >= 5 else self.ol_counter