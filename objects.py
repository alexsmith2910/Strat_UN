import pyglet
from pyglet.window import key, mouse
global game_objects
game_objects = []
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
        max_x = 800 + self.image.width / 2
        max_y = 600 + self.image.height / 2
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

    def set_owner(self, new_owner):
        self.owner = new_owner

    def get_owner(self):
        return self.owner

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = 800 + self.image.width / 2
        max_y = 600 + self.image.height / 2
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

player_image = pyglet.image.load("Test-sprite.png")
player_image.anchor_x = 10
player_image.anchor_y = 10

class Player(TileObject):
    """class for generating a object for the player to control"""

    def __init__(self, *args, **kwargs):
        super().__init__(img=player_image, *args, **kwargs)

        self.pixels = 20
        self.key_handler = key.KeyStateHandler()
        self.scounter = 0
        self.bcounter = 0

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
            # for i in squares:
            #     for j in i:
            #         tempx = j.x + 10
            #         tempy = j.y + 10
            #         if tempx - player_sprite.get_x() == 0.0 and tempy - player_sprite.get_y() == 0:
            #             j.color = (255, 255, 255)
            tempx = self.x + 10
            tempy = self.y + 10
            game_objects.append(" ")
            print(game_objects)
            self.bcounter += 1

        if self.bcounter != 0:
            self.bcounter += 1

        if self.scounter != 0:
            self.scounter += 1

        if self.scounter == 15:
            self.velocity_x = 0
            self.velocity_y = 0
            self.scounter = 0 if self.scounter == 15 else self.scounter
        if self.bcounter == 120:
            self.bcounter = 0 if self.bcounter == 120 else self.bcounter
