# class data_window(pyglet.window.Window):
#     def __init__(self):
#         super().__init__()  # self, game_window
#
#         self.set_vsync(False)
#         self.mineral_text = "mineral count here"
#         self.mineral_label = pyglet.text.Label(self.mineral_text,
#                                                font_name='Bebas Neue',
#                                                font_size=36,
#                                                x=self._width // 2, y=(self._height // 2) + 40,
#                                                anchor_x='center', anchor_y='center')
#
#         self.metal_text = "metal count here"
#         self.metal_label = pyglet.text.Label(self.mineral_text,
#                                              font_name='Bebas Neue',
#                                              font_size=36,
#                                              x=self._width // 2, y=self._height // 2,
#                                              anchor_x='center', anchor_y='center')
#
#         self.selection_text = "selection of building here"
#         self.selection_label = pyglet.text.Label(self.selection_text,
#                                                  font_name='Bebas Neue',
#                                                  font_size=36,
#                                                  x=self._width // 2, y=(self._height // 2) - 40,
#                                                  anchor_x='center', anchor_y='center')
#
#         pyglet.clock.schedule_interval(self.update, 1 / 120.0)
#
#     def update(self, dt):
#         self.mineral_text = ""
#         # print(building_objects)
#         # self.mineral_text += str(i)
#         self.mineral_text = "Mineral: " + str(round(globals.player1_lv1_res, 1))  # ℤens
#         self.mineral_label.text = self.mineral_text
#         self.metal_text = "Metal: " + str(round(globals.player1_lv2_res, 1))  # ℤens
#         self.metal_label.text = self.metal_text
#         self.selection_text_temp = str(game_window_run.player_one.get_select()).split("'")
#         self.selection_text_temp = str((self.selection_text_temp[1])[8:])
#         self.selection_text = "Selection: " + str(self.selection_text_temp)
#         self.selection_label.text = self.selection_text
#         # print(globals.code)
#
#     def on_draw(self):
#         self.clear()
#         self.mineral_label.draw()
#         self.metal_label.draw()
#         self.selection_label.draw()


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

# pyglet.graphics.draw(1, pyglet.gl.GL_LINES,
#                      ("v4i", (int(self.x), int(self.y), int(self.targetx), int(self.targety)))
# )

# for obj in globals.building_objects: # testing for turret targeting
#     if isinstance(obj, objects.Basic_Turret):
#         obj.set_targetx(self.player_one.get_x())
#         obj.set_targety(self.player_one.get_y())

# for i in self.squares:
#     for j in i:
#         if j.get_barrier_state():
#             tempx = j.x + 10
#             tempy = j.y + 10
#         if j.get_barrier_state() and tempx - self.player_one.get_x() == 0.0 and tempy - self.player_one.get_y() == 0:
#             for i in self.squares:
#                 for j in i:
#                     j.color = (255, 0, 0)

# Code started for relative overlay drawing, revisit if thinking of adding changing resolutions
# self.overlay_bg = pyglet.shapes.Rectangle((xres - 200), (yres // 3), xres, ((yres // 3) * 2), (0, 0, 0), batch=globals.overlay_batch)
# self.overlay_bg_frameh = pyglet.shapes.Line((xres - 200), (yres//3), (xres-200), ((yres//3)*2), 1, (255, 255, 255), batch=globals.overlay_batch)

# Auto targeting removed code
# self.targeting = True
# self.targeted = i
# self.cpath = []
# else:
#     self.targeting = False
#     self.targeted = None

# label = pyglet.input_text.Label('Fuck off nick', j
#                           font_name='Have Heart One',
#                           font_size=36,
#                           x=game_window.width//2, y=game_window.height//2,
#                           anchor_x='center', anchor_y='center')


# vertex_list = pyglet.graphics.vertex_list(1024, 'v3f', 'c4B', 't2f', 'n3f')
# event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)#used to find events to connect to commands


# start = globals.astar_matrix.node(0, 0)
# end = globals.astar_matrix.node(2, 17)
#
# finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
# path, runs = finder.find_path(start, end, globals.astar_matrix)
#
# print('operations:', runs, 'path length:', len(path))
# print("Path: ", path)
# print(globals.astar_matrix.grid_str(path=path, start=start, end=end))

# for i in globals.troop_objects:
#     i.auto_targeting = not i.auto_targeting
# print("auto targeting toggled.")

# grad_final = []
# for j in range(len(grad[0])):
#     grad_final.append([])

# for counti, i in enumerate(range(len(grad[0]))):
#     for countj, j in enumerate(range(len(grad))):
#         grad_final[countj][counti].append(grad[counti][countj])
#
# print(str(len(grad_final)))
# print(str(len(grad_final[0])))

# g = secrets.randbelow(128)
# g2 = secrets.randbelow(64)
# g3 = g - g2
# if g3 < 1:
#     g3 = 20
# g3 += 25
# b = secrets.randbelow(255)

# globals.astar_map[i - 1].append(1)
# globals.astar_map.insert(0, [])
# for i in range(resx // size):
#     globals.astar_map[0].append(-1)

# for i in range(len(tiles)):
#     choice = secrets.randbelow(3)
#     if choice == 0:
#         x_choice = secrets.randbelow(16)
#         (tiles[i])[x_choice].color = (0, 0, 255)
#         (tiles[i])[x_choice].make_barrier()
#         (globals.astar_map[i])[x_choice] = -1
#
#         val_list = []
#         for i in range(4):
#             for i in range(10):
#                 val_list.append(secrets.randbelow(2))
#             if val_list[0] == 1:
#                 (tiles[i])[x_choice - 1].color = (100, 100, 255)
#                 (tiles[i])[x_choice - 1].make_barrier()
#                 (globals.astar_map[i])[x_choice - 1] = -1
#             elif val_list[1] == 1:
#                 (tiles[i])[x_choice + 1].color = (100, 100, 255)
#                 (tiles[i])[x_choice + 1].make_barrier()
#                 (globals.astar_map[i])[x_choice + 1] = -1
#             elif val_list[2] == 1:
#                 (tiles[i - 1])[x_choice].color = (100, 100, 255)
#                 (tiles[i - 1])[x_choice].make_barrier()
#                 (globals.astar_map[i - 1])[x_choice] = -1
#             elif val_list[3] == 1 and i < resy // 2:
#                 (tiles[i + 1])[x_choice].color = (100, 100, 255)
#                 (tiles[i + 1])[x_choice].make_barrier()
#                 (globals.astar_map[i + 1])[x_choice] = -1


# globals.bg_batch.draw()
# if self.show_grid:
#     globals.grid_batch.draw()
# globals.building_batch.draw()
# globals.small_troop_batch.draw()
# globals.medium_troop_batch.draw()
# globals.large_troop_batch.draw()
# for i in globals.troop_objects:
#     if i.get_weapon_tracing():
#         i.get_tracer().draw()
# globals.tracer_batch.draw()  # Tracer batch doesn't seem to work even after setting the tracer's batch to it
# globals.hud_batch.draw()
#     i.draw()
# for i in globals.troop_objects:
#     i.draw()

# self.player_one.draw()
# for i in self.game_objects:
#     i.draw()
