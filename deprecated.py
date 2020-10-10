# square = pyglet.shapes.Rectangle(x=200, y=200, width=200, height=200, color=(55, 55, 255))

# if self.key_handler[key.LEFT] or self.lcounter != 0:
#     angle_radians = -math.radians(self.rotation) + (math.pi)
#     force_x = math.cos(angle_radians) * self.thrust * dt
#     force_y = math.sin(angle_radians) * self.thrust * dt
#     if self.lcounter == 0:
#         self.velocity_x += force_x
#         self.velocity_y += force_y
#     self.lcounter += 1
# elif self.key_handler[key.RIGHT] or self.rcounter != 0:
#     angle_radians = -math.radians(self.rotation)
#     force_x = math.cos(angle_radians) * self.thrust * dt
#     force_y = math.sin(angle_radians) * self.thrust * dt
#     if self.rcounter == 0:
#         self.velocity_x += force_x
#         self.velocity_y += force_y
#     # self.rotation += self.rotate_speed * dt
#     self.rcounter += 1
# elif self.key_handler[key.UP] or self.ucounter != 0:
#     angle_radians = -math.radians(self.rotation)+(math.pi/2)
#     force_x = math.cos(angle_radians) * self.thrust * dt
#     force_y = math.sin(angle_radians) * self.thrust * dt
#     if self.ucounter == 0:
#         self.velocity_x += force_x
#         self.velocity_y += force_y
#     self.ucounter += 1
# elif self.key_handler[key.DOWN] or self.dcounter != 0:
#     angle_radians = -math.radians(self.rotation)+(math.pi/2)
#     force_x = math.cos(angle_radians) * self.thrust * dt
#     force_y = math.sin(angle_radians) * self.thrust * dt
#     if self.dcounter == 0:
#         self.velocity_x -= force_x
#         self.velocity_y -= force_y
#     self.dcounter += 1

# self.ucounter = 0 if self.ucounter == 30 else self.ucounter
# self.lcounter = 0 if self.lcounter == 30 else self.lcounter
# self.rcounter = 0 if self.rcounter == 30 else self.rcounter
# self.dcounter = 0 if self.dcounter == 30 else self.dcounter
# if self.lcounter == 30:
#     self.velocity_x = 0
#     self.velocity_y = 0
#     self.lcounter = 0
# if self.rcounter == 30:
#     self.velocity_x = 0
#     self.velocity_y = 0
#     self.rcounter = 0
# if self.keys['down']:
#     angle_radians = -math.radians(self.rotation)+(math.pi/2)
#     force_x = math.cos(angle_radians) * self.thrust * dt
#     force_y = math.sin(angle_radians) * self.thrust * dt
#     self.velocity_x -= force_x
#     self.velocity_y -= force_y

# @game_window.event
# def on_key_press(symbol, modifiers):
#     if symbol == key.A:
#         print('The "A" key was pressed.')
#     elif symbol == key.LEFT:
#         print('left')
#     elif symbol == key.ENTER:
#         print('The enter key was pressed.')


# def on_key_press(self, symbol, modifiers):
#     if symbol == key.UP:
#         self.keys['up'] = True
#     elif symbol == key.LEFT:
#         self.keys['left'] = True
#     elif symbol == key.RIGHT:
#         self.keys['right'] = True
#     elif symbol == key.DOWN:
#         self.keys['down'] = True
#
# def on_key_release(self, symbol, modifiers):
#     if symbol == key.UP:
#         self.keys['up'] = False
#     elif symbol == key.LEFT:
#         self.keys['left'] = False
#     elif symbol == key.RIGHT:
#         self.keys['right'] = False
#     elif symbol == key.DOWN:
#         self.keys['down'] = False

# def tiles(no_squares):
#     tiles = []
#     tilebatch = pyglet.graphics.Batch()
#     for i in range(no_squares):
#         x_num = secrets.randbelow(800)
#         y_num = secrets.randbelow(800)
#         w_num = secrets.randbelow(100)
#         h_num = secrets.randbelow(100)
#         r = secrets.randbelow(255)
#         g = secrets.randbelow(255)
#         b = secrets.randbelow(255)
#         tiles.append(motion.TileBG(x=x_num, y=y_num, anchor_x=10, anchor_y=10, width=w_num, height=h_num, color=(r, g, b), batch=tilebatch))
#     return tiles, tilebatch

# vertex_list = pyglet.graphics.vertex_list(2,
#                                           ('v2i', (10, 15, 30, 35)),
#                                           ('c3B', (0, 0, 255, 0, 255, 0))
#                                           )
# vertex_list.draw(pyglet.gl.GL_POINTS)
# player.draw()