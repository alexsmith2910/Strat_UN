from pyglet.window import key
from pyglet.graphics import *

import secrets
import socket
import select

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.bi_a_star import BiAStarFinder

finder = BiAStarFinder(diagonal_movement=DiagonalMovement.always)

import objects
import globals
import src
# import gui.research_elements.elements as research_elements
import gui
import threading
import net

myappid = u'Zestyy.Strat_UN.Main.V0.2BETA'  # these lines are used to seperate the app from the python 'umbrella'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

win_icon = pyglet.resource.image("src/icon/Strat_un-icon-N.png")

pyglet.font.add_file("src/BebasNeue-Regular.otf")


class serverThread(threading.Thread):  # threading.Thread
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.name = "Server thread"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # if globals.recipient == "localhost":
        #     self.s.bind((socket.gethostname(), 5469))
        # else:
        #     print(globals.recipient)
        if globals.local_connect:  # Used when localhost is being used, mainly for testing
            self.s.bind((globals.recipient, 5469))
        else:  # Used when an external IP is supplied
            self.s.connect((globals.recipient, 5469))
            self.s.send(b"0000")
            #  Causes error that crashes strat, being OSError 10060
            #  Essentially a timeout from there being no response to its connection
            #  Since the Client can print its errors before the program crashes,
            #  It seems that the connection is possible, and *not* the server locking the client
            #  (i.e it stopping the client threat so it can't respond)

            # _, _ = self.s.accept()
            #  External IP usage results in error, check if port forwarding is needed

    def dataPush(self):
        """Pushes relavent data into globals for later usage as a message."""
        playerPos = globals.p1Pos
        data = {"position": [playerPos[0], playerPos[1]],
                "resources": [globals.player1_lv1_res, globals.player1_lv2_res, globals.player1_lv3_res],
                "generation": [globals.player1_lv1_gen, globals.player1_lv2_gen, globals.player1_lv3_gen]}

        # for keys in globals.online_sending:
        #     data[keys] = globals.online_sending.pop(keys)

        #  Syncing usernames
        if "username" in globals.online_sending:
            data["username"] = globals.online_sending.pop("username")
        if "confirm_u" in globals.online_sending:
            data["confirm_u"] = globals.online_sending.pop("confirm_u")

        if "spawn" in globals.online_sending:
            # print("found spawn tag: {0}".format(str(globals.online_sending)))
            data["spawn"] = globals.online_sending.pop("spawn")

        if "build" in globals.online_sending:
            # print("found spawn tag: {0}".format(str(globals.online_sending)))
            data["build"] = globals.online_sending.pop("build")

        if "move" in globals.online_sending:
            data["move"] = globals.online_sending.pop("move")

        # globals.onl_sending = {}  # When all keys are popped this shouldn't be necessary
        return data

    def run(self, dt=None):
        # print("serving")
        try:
            # self.s.listen(5)
            #  Listen attempts to make a new connection with a client, so this should not be needed,
            #  And will error as a connetion should already exist
            # # s.settimeout(0.5)
            # # s.setblocking(0)
            #
            data = self.dataPush()
            # clientsocket, address = self.s.accept()
            #  self.s by this point is connected to the other player, so we do not need a new one through accept
            # clientsocket.send(net.dicttomessage(data))
            self.s.send(net.dicttomessage(data))
        except socket.timeout:
            print("Timed out")
        except Exception as e:
            print("Server: " + str(e))
            # pass

    def kill(self):
        self.s.close()
        del self


class game_window(pyglet.window.Window):
    def __init__(self):
        super().__init__()  # self, game_window
        self.set_caption("Strat_UN")
        self.set_vsync(False)
        self.set_icon(win_icon)
        self.research_items = []
        # print(objects.str_to_class("Barracks"))  # tested and works in main namespace
        # self.set_fullscreen(True)
        self.player_image = pyglet.image.load("src/sprite/P1-sprite.png")
        self.player_image.anchor_x = 10
        self.player_image.anchor_y = 10
        self.set_minimum_size(globals.screenresx, globals.screenresy)
        self.set_size(globals.screenresx, globals.screenresy)
        globals.bg_tiles, globals.bg_batch = self.tiles_map()
        self.player_one = objects.Player(x=550, y=550)
        self.player_one.set_id(globals.p1_name, 1)
        self.player_two = objects.OnlinePlayer(x=700, y=700)
        self.player_two.set_id(globals.p2_name, 2)
        self.game_objects = [self.player_one, self.player_two]
        if globals.offline_multi:
            self.player_two = objects.Player(x=650, y=650)
            self.player_two.set_id(globals.p2_name, 2)
            self.game_objects.append(self.player_two)
        #  Testing code that spawns 4 dev tanks in

        # globals.troop_objects.append(objects.Dev_Tank(x=globals.building_objects[0].get_x()+100, y=globals.building_objects[0].get_y()+100))
        # globals.troop_objects.append(objects.Dev_Tank(x=610, y=610))
        # globals.troop_objects[len(globals.troop_objects) - 1].set_owner((globals.p1_name, 1))
        # globals.troop_objects[len(globals.troop_objects) - 1].health = 500
        # globals.troop_objects.append(objects.Dev_Tank(x=710, y=410))
        # globals.troop_objects[len(globals.troop_objects) - 1].set_owner((globals.p2_name, 2))
        # print(globals.troop_objects[len(globals.troop_objects) - 1].get_id())
        # globals.troop_objects.append(objects.Dev_Tank(x=1010, y=810))
        # globals.troop_objects[len(globals.troop_objects) - 1].set_owner((globals.p3_name, 3))
        # globals.troop_objects.append(objects.Dev_Tank(x=110, y=510))
        # globals.troop_objects[len(globals.troop_objects) - 1].set_owner((globals.p4_name, 4))

        # self.HQ_spawn()
        p1HQ = (objects.HQ(x=110, y=50))
        p2HQ = (objects.HQ(x=1430, y=510))
        globals.building_objects[p1HQ.get_id()] = p1HQ
        globals.building_objects[p2HQ.get_id()] = p2HQ
        globals.building_objects[p1HQ.get_id()].set_owner((globals.p1_name, 1))
        globals.building_objects[p2HQ.get_id()].set_owner((globals.p2_name, 2))

        # print(globals.building_objects[0].get_id())
        self.push_handlers(globals.key_handler)
        pyglet.clock.schedule_interval(self.update, 1 / 120.0)
        self.client = net.client.ClientThread()
        self.client.start()  # TODO: test if starting the client first allows for the connection to be heard, to fix the issue.
        self.winThread = serverThread()
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.input_text = ''
        self.firstt = True  # this serves to avoid the first 't' used to activate the typing,
        # not to get stored as first character of the input_text.
        self.main_key_handler = key.KeyStateHandler()
        self.gen_overlays()
        # Data parts for overlay
        self.show_grid = True
        self.show_data_overlay = False
        self.show_research_overlay = False
        self.clicked_object = None
        self.winThread.start()  # TODO: if not, test if the failure comes from it getting to the server and being forced to stay on it
        # self.client.start()
        pyglet.clock.schedule_interval(self.winThread.run, 0.05)

    def HQ_spawn(self, players=2, distance=120):
        cur_player = 0
        for i in range(players):
            tile_copy = []
            cur_player += 1
            for i in globals.bg_tiles:
                for j in i:
                    if not j.get_barrier_state():
                        if cur_player == 1:
                            if j.x <= distance:
                                tile_copy.append(j)
                        elif cur_player == 2:
                            if j.x >= globals.screenresx - distance:
                                tile_copy.append(j)
            chosen = secrets.choice(tile_copy)
            newHQ = objects.HQ(x=chosen.get_x() + 10, y=chosen.get_y() + 10)
            HQID = newHQ.get_id()
            globals.building_objects[HQID] = newHQ
            if cur_player == 1:
                globals.building_objects[HQID].set_owner((globals.p1_name, 1))
            elif cur_player == 2:
                globals.building_objects[HQID].set_owner((globals.p2_name, 2))

    def gen_overlays(self, xres=globals.screenresx, yres=globals.screenresy):
        # TODO: make overlay compatible with 2 player play, either if else 2 generations or let the original be generated then move

        if not globals.offline_multi:
            self.ol_range = pyglet.shapes.Circle(x=0, y=0, radius=200, color=(255, 255, 255),
                                                 batch=globals.data_overlay_batch, group=globals.ol_bg_group)
            self.ol_range.opacity = 50

            self.overlay_bg = pyglet.shapes.Rectangle(500, 0, 500, 300, (0, 0, 0), batch=globals.data_overlay_batch,
                                                      group=globals.ol_bg_group)
            self.overlay_bg.opacity = 150
            self.overlay_bg_frameh = pyglet.shapes.Line(500, 300, 1000, 300, 1, (255, 255, 255),
                                                        batch=globals.data_overlay_batch, group=globals.ol_border_group)
            self.overlay_bg_framev1 = pyglet.shapes.Line(500, 0, 500, 300, 1, (255, 255, 255),
                                                         batch=globals.data_overlay_batch,
                                                         group=globals.ol_border_group)
            self.overlay_bg_framev2 = pyglet.shapes.Line(1000, 0, 1000, 300, 1, (255, 255, 255),
                                                         batch=globals.data_overlay_batch,
                                                         group=globals.ol_border_group)
            self.mineral_text = "Mineral text here"
            self.metal_text = "Metal text here"
            self.oil_text = "Oil text here"
            self.selection_text = "Selection text here"
            self.clickable_text = ""
            self.clickable_text_temp = ""
            self.clickable_owner_text = "Owner text here"
            self.clickable_owner_text_temp = ""
            self.clickable_targetbool_text = "Targeting text here"
            self.clickable_targetbool_text_temp = ""

            self.clickable_return_l1_temp = ""
            self.clickable_return_l2_temp = ""
            self.clickable_return_l3_temp = ""
            self.clickable_return_l4_temp = ""

            self.clickable_return_l1_text = ""
            self.clickable_return_l2_text = ""
            self.clickable_return_l3_text = ""
            self.clickable_return_l4_text = ""
            self.overlay_mineral_label = pyglet.text.Label(self.mineral_text,
                                                           font_name='Bebas Neue',
                                                           font_size=15,
                                                           x=505, y=280, batch=globals.data_overlay_batch,
                                                           group=globals.ol_fg_group)
            self.overlay_metal_label = pyglet.text.Label(self.metal_text,
                                                         font_name='Bebas Neue',
                                                         font_size=15,
                                                         x=505, y=260, batch=globals.data_overlay_batch,
                                                         group=globals.ol_fg_group)
            self.overlay_oil_label = pyglet.text.Label(self.oil_text,
                                                       font_name='Bebas Neue',
                                                       font_size=15,
                                                       x=505, y=240, batch=globals.data_overlay_batch,
                                                       group=globals.ol_fg_group)
            self.overlay_selection_label = pyglet.text.Label(self.selection_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=505, y=220, batch=globals.data_overlay_batch,
                                                             group=globals.ol_fg_group)
            self.overlay_clickable_label = pyglet.text.Label(self.clickable_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=505, y=200, batch=globals.data_overlay_batch,
                                                             group=globals.ol_fg_group)
            self.overlay_clickable_owner_label = pyglet.text.Label(self.clickable_owner_text,
                                                                   font_name='Bebas Neue',
                                                                   font_size=15,
                                                                   x=505, y=180, batch=globals.data_overlay_batch,
                                                                   group=globals.ol_fg_group)
            self.overlay_clickable_targetbool_label = pyglet.text.Label(self.clickable_targetbool_text,
                                                                        font_name='Bebas Neue',
                                                                        font_size=15,
                                                                        x=505, y=160, batch=globals.data_overlay_batch,
                                                                        group=globals.ol_fg_group)
            # anchor_x='center', anchor_y='center'
            self.overlay_clickable_return_l1_label = pyglet.text.Label(self.clickable_return_l1_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=750, y=80, anchor_x='center',
                                                                       batch=globals.data_overlay_batch,
                                                                       group=globals.ol_fg_group)
            # align="center",
            self.overlay_clickable_return_l2_label = pyglet.text.Label(self.clickable_return_l2_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=750, y=60, anchor_x='center',
                                                                       batch=globals.data_overlay_batch,
                                                                       group=globals.ol_fg_group)
            self.overlay_clickable_return_l3_label = pyglet.text.Label(self.clickable_return_l3_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=750, y=40, anchor_x='center',
                                                                       batch=globals.data_overlay_batch,
                                                                       group=globals.ol_fg_group)
            self.overlay_clickable_return_l4_label = pyglet.text.Label(self.clickable_return_l4_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=12,
                                                                       x=750, y=20, anchor_x='center',
                                                                       batch=globals.data_overlay_batch,
                                                                       group=globals.ol_fg_group)

            # Elements for the reasearch overlay

            self.roverlay_bg = pyglet.shapes.Rectangle(0, 0, xres, yres, (0, 0, 0),
                                                       batch=globals.research_overlay_batch, group=globals.ol_bg_group)
            self.roverlay_bg.opacity = 150

            self.roverlay_framel = pyglet.shapes.Line(0, 0, 0, yres, 1, (255, 255, 255),
                                                      batch=globals.research_overlay_batch,
                                                      group=globals.ol_border_group)
            self.roverlay_framer = pyglet.shapes.Line(xres, 0, xres, yres, 1, (255, 255, 255),
                                                      batch=globals.research_overlay_batch,
                                                      group=globals.ol_border_group)
            self.roverlay_framet = pyglet.shapes.Line(0, yres, xres, yres, 1, (255, 255, 255),
                                                      batch=globals.research_overlay_batch,
                                                      group=globals.ol_border_group)
            self.roverlay_frameb = pyglet.shapes.Line(0, 0, xres, 0, 1, (255, 255, 255),
                                                      batch=globals.research_overlay_batch,
                                                      group=globals.ol_border_group)
            self.roverlay_title = pyglet.text.Label("Research",
                                                    font_name='Bebas Neue',
                                                    font_size=15,
                                                    x=720, y=975, batch=globals.research_overlay_batch,
                                                    group=globals.ol_fg_group)
            self.roverlay_tree = gui.research_elements.Branch(direction="NW")
            self.research_items.append(gui.research_elements.ResearchSlot(700, 700,
                                                                          spritesrc=pyglet.image.load(
                                                                              "src/sprite/Basic-infantry.png"),
                                                                          heldclass=objects.Basic_infantry))
            # self.timg = pyglet.image.load("src/sprite/Dev-tank-sprite.png")
            # self.rtank = pyglet.sprite.Sprite(self.timg, 200, 500, batch=globals.research_overlay_batch, group=globals.ol_fg_group)
            # self.rtank.scale = 0.2


        else:
            # player 1's overlay
            self.overlay_bg = pyglet.shapes.Rectangle(200, 0, 500, 300, (1, 49, 122), batch=globals.data_overlay_batch,
                                                      group=globals.ol_bg_group)
            self.overlay_bg.opacity = 100
            self.overlay_bg_frameh = pyglet.shapes.Line(200, 300, 700, 300, 1, (255, 255, 255),
                                                        batch=globals.data_overlay_batch, group=globals.ol_border_group)
            self.overlay_bg_framev1 = pyglet.shapes.Line(200, 0, 200, 300, 1, (255, 255, 255),
                                                         batch=globals.data_overlay_batch,
                                                         group=globals.ol_border_group)
            self.overlay_bg_framev2 = pyglet.shapes.Line(700, 0, 700, 300, 1, (255, 255, 255),
                                                         batch=globals.data_overlay_batch,
                                                         group=globals.ol_border_group)
            self.mineral_text = "Mineral text here"
            self.metal_text = "Metal text here"
            self.oil_text = "Oil text here"
            self.selection_text = "Selection text here"
            self.clickable_text = ""
            self.clickable_text_temp = ""
            self.clickable_owner_text = "Owner text here"
            self.clickable_owner_text_temp = ""
            self.clickable_targetbool_text = "Targeting text here"
            self.clickable_targetbool_text_temp = ""

            self.clickable_return_l1_temp = ""
            self.clickable_return_l2_temp = ""
            self.clickable_return_l3_temp = ""
            self.clickable_return_l4_temp = ""

            self.clickable_return_l1_text = ""
            self.clickable_return_l2_text = ""
            self.clickable_return_l3_text = ""
            self.clickable_return_l4_text = ""
            self.overlay_mineral_label = pyglet.text.Label(self.mineral_text,
                                                           font_name='Bebas Neue',
                                                           font_size=15,
                                                           x=205, y=280, batch=globals.data_overlay_batch,
                                                           group=globals.ol_fg_group)
            self.overlay_metal_label = pyglet.text.Label(self.metal_text,
                                                         font_name='Bebas Neue',
                                                         font_size=15,
                                                         x=205, y=260, batch=globals.data_overlay_batch,
                                                         group=globals.ol_fg_group)
            self.overlay_oil_label = pyglet.text.Label(self.oil_text,
                                                       font_name='Bebas Neue',
                                                       font_size=15,
                                                       x=205, y=240, batch=globals.data_overlay_batch,
                                                       group=globals.ol_fg_group)
            self.overlay_selection_label = pyglet.text.Label(self.selection_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=205, y=220, batch=globals.data_overlay_batch,
                                                             group=globals.ol_fg_group)
            self.overlay_clickable_label = pyglet.text.Label(self.clickable_text,
                                                             font_name='Bebas Neue',
                                                             font_size=15,
                                                             x=205, y=200, batch=globals.data_overlay_batch,
                                                             group=globals.ol_fg_group)
            self.overlay_clickable_owner_label = pyglet.text.Label(self.clickable_owner_text,
                                                                   font_name='Bebas Neue',
                                                                   font_size=15,
                                                                   x=205, y=180, batch=globals.data_overlay_batch,
                                                                   group=globals.ol_fg_group)
            self.overlay_clickable_targetbool_label = pyglet.text.Label(self.clickable_targetbool_text,
                                                                        font_name='Bebas Neue',
                                                                        font_size=15,
                                                                        x=205, y=160, batch=globals.data_overlay_batch,
                                                                        group=globals.ol_fg_group)
            # anchor_x='center', anchor_y='center'
            self.overlay_clickable_return_l1_label = pyglet.text.Label(self.clickable_return_l1_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=450, y=80, anchor_x='center',
                                                                       batch=globals.data_overlay_batch,
                                                                       group=globals.ol_fg_group)
            # align="center",
            self.overlay_clickable_return_l2_label = pyglet.text.Label(self.clickable_return_l2_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=450, y=60, anchor_x='center',
                                                                       batch=globals.data_overlay_batch,
                                                                       group=globals.ol_fg_group)
            self.overlay_clickable_return_l3_label = pyglet.text.Label(self.clickable_return_l3_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=15,
                                                                       x=450, y=40, anchor_x='center',
                                                                       batch=globals.data_overlay_batch,
                                                                       group=globals.ol_fg_group)
            self.overlay_clickable_return_l4_label = pyglet.text.Label(self.clickable_return_l4_text,
                                                                       font_name='Bebas Neue',
                                                                       font_size=12,
                                                                       x=450, y=20, anchor_x='center',
                                                                       batch=globals.data_overlay_batch,
                                                                       group=globals.ol_fg_group)

            # player 2's overlay
            self.p2_overlay_bg = pyglet.shapes.Rectangle(800, 0, 500, 300, (130, 39, 39),
                                                         batch=globals.data_overlay_batch, group=globals.ol_bg_group)
            self.p2_overlay_bg.opacity = 100
            self.p2_overlay_bg_frameh = pyglet.shapes.Line(800, 300, 1300, 300, 1, (255, 255, 255),
                                                           batch=globals.data_overlay_batch,
                                                           group=globals.ol_border_group)
            self.p2_overlay_bg_framev1 = pyglet.shapes.Line(800, 0, 800, 300, 1, (255, 255, 255),
                                                            batch=globals.data_overlay_batch,
                                                            group=globals.ol_border_group)
            self.p2_overlay_bg_framev2 = pyglet.shapes.Line(1300, 0, 1300, 300, 1, (255, 255, 255),
                                                            batch=globals.data_overlay_batch,
                                                            group=globals.ol_border_group)
            self.p2_mineral_text = "Mineral text here"
            self.p2_metal_text = "Metal text here"
            self.p2_oil_text = "Oil text here"
            self.p2_selection_text = "Selection text here"
            self.p2_clickable_text = ""
            self.p2_clickable_text_temp = ""
            self.p2_clickable_owner_text = "Owner text here"
            self.p2_clickable_owner_text_temp = ""
            self.p2_clickable_targetbool_text = "Targeting text here"
            self.p2_clickable_targetbool_text_temp = ""

            self.p2_clickable_return_l1_temp = ""
            self.p2_clickable_return_l2_temp = ""
            self.p2_clickable_return_l3_temp = ""
            self.p2_clickable_return_l4_temp = ""

            self.p2_clickable_return_l1_text = ""
            self.p2_clickable_return_l2_text = ""
            self.p2_clickable_return_l3_text = ""
            self.p2_clickable_return_l4_text = ""
            self.p2_overlay_mineral_label = pyglet.text.Label(self.p2_mineral_text,
                                                              font_name='Bebas Neue',
                                                              font_size=15,
                                                              x=805, y=280, batch=globals.data_overlay_batch,
                                                              group=globals.ol_fg_group)
            self.p2_overlay_metal_label = pyglet.text.Label(self.p2_metal_text,
                                                            font_name='Bebas Neue',
                                                            font_size=15,
                                                            x=805, y=260, batch=globals.data_overlay_batch,
                                                            group=globals.ol_fg_group)
            self.p2_overlay_oil_label = pyglet.text.Label(self.p2_oil_text,
                                                          font_name='Bebas Neue',
                                                          font_size=15,
                                                          x=805, y=240, batch=globals.data_overlay_batch,
                                                          group=globals.ol_fg_group)
            self.p2_overlay_selection_label = pyglet.text.Label(self.p2_selection_text,
                                                                font_name='Bebas Neue',
                                                                font_size=15,
                                                                x=805, y=220, batch=globals.data_overlay_batch,
                                                                group=globals.ol_fg_group)
            self.p2_overlay_clickable_label = pyglet.text.Label(self.p2_clickable_text,
                                                                font_name='Bebas Neue',
                                                                font_size=15,
                                                                x=805, y=200, batch=globals.data_overlay_batch,
                                                                group=globals.ol_fg_group)
            self.p2_overlay_clickable_owner_label = pyglet.text.Label(self.p2_clickable_owner_text,
                                                                      font_name='Bebas Neue',
                                                                      font_size=15,
                                                                      x=805, y=180, batch=globals.data_overlay_batch,
                                                                      group=globals.ol_fg_group)
            self.p2_overlay_clickable_targetbool_label = pyglet.text.Label(self.p2_clickable_targetbool_text,
                                                                           font_name='Bebas Neue',
                                                                           font_size=15,
                                                                           x=805, y=160,
                                                                           batch=globals.data_overlay_batch,
                                                                           group=globals.ol_fg_group)
            # anchor_x='center', anchor_y='center'
            self.p2_overlay_clickable_return_l1_label = pyglet.text.Label(self.p2_clickable_return_l1_text,
                                                                          font_name='Bebas Neue',
                                                                          font_size=15,
                                                                          x=1050, y=80, anchor_x='center',
                                                                          batch=globals.data_overlay_batch,
                                                                          group=globals.ol_fg_group)
            # align="center",
            self.p2_overlay_clickable_return_l2_label = pyglet.text.Label(self.p2_clickable_return_l2_text,
                                                                          font_name='Bebas Neue',
                                                                          font_size=15,
                                                                          x=1050, y=60, anchor_x='center',
                                                                          batch=globals.data_overlay_batch,
                                                                          group=globals.ol_fg_group)
            self.p2_overlay_clickable_return_l3_label = pyglet.text.Label(self.p2_clickable_return_l3_text,
                                                                          font_name='Bebas Neue',
                                                                          font_size=15,
                                                                          x=1050, y=40, anchor_x='center',
                                                                          batch=globals.data_overlay_batch,
                                                                          group=globals.ol_fg_group)
            self.p2_overlay_clickable_return_l4_label = pyglet.text.Label(self.p2_clickable_return_l4_text,
                                                                          font_name='Bebas Neue',
                                                                          font_size=12,
                                                                          x=1050, y=20, anchor_x='center',
                                                                          batch=globals.data_overlay_batch,
                                                                          group=globals.ol_fg_group)

    def update(self, dt):
        # super(game_window, self).update(dt)
        # print(self.game_objects)

        #  Code that uses data received online to
        #  Appropriately manipulate the game
        if globals.online_multi:

            globals.sync_timer += dt
            if globals.sync_timer >= globals.sync_time:
                globals.sync_timer = 0.0

            globals.p1Pos = self.player_one.get_pos()
            self.player_two.x = globals.p2Pos[0]
            self.player_two.y = globals.p2Pos[1]
            if "spawn" in globals.online_received:
                spawnData = globals.online_received.pop("spawn")
                # print(spawnData)
                for troop_spawn in spawnData:
                    globals.troop_objects[troop_spawn] = (objects.str_to_class(troop_spawn.split(".")[0])
                        (
                        x=spawnData[troop_spawn]["locate"][0],
                        y=spawnData[troop_spawn]["locate"][1],
                        set_id=troop_spawn))
                    #  Finds correct troop using class name, and spawns it with the other
                    #  Client's ID for it
                    globals.troop_objects[troop_spawn].set_owner((globals.p2_name, 2))
                    # TODO: update to seperate online player from being a generic 2nd player
                    # print(troop_spawn)
                    if "path" in spawnData:
                        globals.troop_objects[troop_spawn].pathfind(
                            globals.onl_r_spawns[troop_spawn]["path"])
            if "build" in globals.online_received:
                buildData = globals.online_received.pop("build")
                for build_key in buildData:
                    globals.building_objects[build_key] = (objects.str_to_class(build_key.split(".")[0])
                                                           (x=buildData[build_key]["locate"][0],
                                                            y=buildData[build_key]["locate"][1],
                                                            set_id=build_key))
                    globals.building_objects[len(globals.building_objects) - 1].set_owner((globals.p2_name, 2))
            if "move" in globals.online_received:
                moveData = globals.online_received.pop("move")
                for move_event in moveData:
                    for i in globals.troop_objects:
                        if move_event == globals.troop_objects[i].get_id():
                            globals.troop_objects[i].ctarget = moveData[move_event]["path"][0]
                            globals.troop_objects[i].cpath = moveData[move_event]["path"][1:]
                            break

            #  TODO: Building and spawning done, now create sync
            #  TODO: Settings file?
            #  TODO: Buildings now in dictionary, now do troops/turrets, etc

        # print(globals.p2Pos)
        for obj in self.game_objects:
            obj.update(dt)
            obj.check_bounds()
        for i in globals.building_objects:
            globals.building_objects[i].update(dt)
        for i in globals.troop_objects:
            globals.troop_objects[i].update(dt)
        for i in globals.bg_tiles:
            for j in i:
                j.update(dt)

        if self.clicked_object is not None:
            globals.clickable = self.clicked_object
            self.tracked_type = self.clicked_object.get_overlay_name()
            self.tracked_health = self.clicked_object.get_health()
            self.tracked_shield = self.clicked_object.get_shield()
            self.tracked_owner = self.clicked_object.get_owner_id()
            self.tracked_targetbool = self.clicked_object.get_targetbool()
            self.clickable_text_temp = (str(self.tracked_type) + " - Health: " +
                                        str(round(self.tracked_health, 1)) + " + " +
                                        str(round(self.tracked_shield, 1)) + " Shield")
            self.clickable_owner_text_temp = (str(self.tracked_owner))
            self.clickable_targetbool_text_temp = ("Enabled" if self.clicked_object.get_targetbool() else "Disabled")
            if globals.offline_multi:
                self.p2_tracked_type = self.clicked_object.get_overlay_name()
                self.p2_tracked_health = self.clicked_object.get_health()
                self.p2_tracked_shield = self.clicked_object.get_shield()
                self.p2_tracked_owner = self.clicked_object.get_owner_id()
                self.p2_tracked_targetbool = self.clicked_object.get_targetbool()
                self.p2_clickable_text_temp = (str(self.tracked_type) + " - Health: " +
                                               str(round(self.tracked_health, 1)) + " + " +
                                               str(round(self.tracked_shield, 1)) + " Shield")
                self.p2_clickable_owner_text_temp = (str(self.tracked_owner))
                self.p2_clickable_targetbool_text_temp = (
                    "Enabled" if self.clicked_object.get_targetbool() else "Disabled")

            if self.clicked_object.get_needs_menu():
                if self.clicked_object.get_owner() == 1:
                    self.overlay_clickable_return_l1_label.text, self.overlay_clickable_return_l2_label.text, \
                    self.overlay_clickable_return_l3_label.text, self.overlay_clickable_return_l4_label.text = \
                        self.clicked_object.gen_overlay_text()[0], \
                        self.clicked_object.gen_overlay_text()[1], \
                        self.clicked_object.gen_overlay_text()[2], \
                        self.clicked_object.gen_overlay_text()[3]

                    if globals.offline_multi:
                        self.p2_overlay_clickable_return_l1_label.text = ""
                        self.p2_overlay_clickable_return_l2_label.text = ""
                        self.p2_overlay_clickable_return_l3_label.text = ""
                        self.p2_overlay_clickable_return_l4_label.text = ""

                elif globals.offline_multi and self.clicked_object.get_owner() == 2:
                    self.p2_overlay_clickable_return_l1_label.text, self.p2_overlay_clickable_return_l2_label.text, \
                    self.p2_overlay_clickable_return_l3_label.text, self.p2_overlay_clickable_return_l4_label.text = \
                        self.clicked_object.gen_overlay_text()[0], \
                        self.clicked_object.gen_overlay_text()[1], \
                        self.clicked_object.gen_overlay_text()[2], \
                        self.clicked_object.gen_overlay_text()[3]

                    self.overlay_clickable_return_l1_label.text = ""
                    self.overlay_clickable_return_l2_label.text = ""
                    self.overlay_clickable_return_l3_label.text = ""
                    self.overlay_clickable_return_l4_label.text = ""

            else:
                self.overlay_clickable_return_l1_label.text = ""
                self.overlay_clickable_return_l2_label.text = ""
                self.overlay_clickable_return_l3_label.text = ""
                self.overlay_clickable_return_l4_label.text = ""
                if globals.offline_multi:
                    self.p2_overlay_clickable_return_l1_label.text = ""
                    self.p2_overlay_clickable_return_l2_label.text = ""
                    self.p2_overlay_clickable_return_l3_label.text = ""
                    self.p2_overlay_clickable_return_l4_label.text = ""

            if self.clicked_object.get_range() > 0:
                self.ol_range.anchor_x = self.clicked_object.get_x()
                self.ol_range.anchor_y = self.clicked_object.get_y()
                self.ol_range.radius = self.clicked_object.get_range()
                if self.clicked_object.get_owner() == 1:
                    self.ol_range.color = globals.p1_color
                elif self.clicked_object.get_owner() == 2:
                    self.ol_range.color = globals.p2_color
                elif self.clicked_object.get_owner() == 3:
                    self.ol_range.color = globals.p3_color
                elif self.clicked_object.get_owner() == 4:
                    self.ol_range.color = globals.p4_color

            elif self.clicked_object.get_range() <= 0:
                self.ol_range.anchor_x = 10000

        if self.clicked_object is None:
            globals.clickable = None
            self.ol_range.anchor_x = 10000
            if self.overlay_clickable_return_l1_label.text != "":
                self.overlay_clickable_return_l1_label.text = ""
                self.overlay_clickable_return_l2_label.text = ""
                self.overlay_clickable_return_l3_label.text = ""
                self.overlay_clickable_return_l4_label.text = ""
                if globals.offline_multi:
                    self.p2_overlay_clickable_return_l1_label.text = ""
                    self.p2_overlay_clickable_return_l2_label.text = ""
                    self.p2_overlay_clickable_return_l3_label.text = ""
                    self.p2_overlay_clickable_return_l4_label.text = ""

        # Overlay editing
        # TODO: update so when a collector is destroyed it will show the collection rate being reduced
        self.mineral_text = ("Mineral: " + str(round(globals.player1_lv1_res, 1)) + " (" + str(
            round(globals.player1_lv1_gen, 2)) + "/s)")  # ℤens
        self.overlay_mineral_label.text = self.mineral_text
        self.metal_text = ("Metal: " + str(round(globals.player1_lv2_res, 1)) + " (" + str(
            round(globals.player1_lv2_gen, 2)) + "/s)")  # ℤens
        self.overlay_metal_label.text = self.metal_text
        self.oil_text = ("Oil: " + str(round(globals.player1_lv3_res, 1)) + " (" + str(
            round(globals.player1_lv3_gen, 2)) + "/s)")  # ℤens
        self.overlay_oil_label.text = self.oil_text
        self.selection_text_temp = str(game_window_run.player_one.get_select()).split("'")
        self.selection_text_temp = str((self.selection_text_temp[1])[8:])
        self.selection_text = "Selection: " + str(self.selection_text_temp)
        self.overlay_selection_label.text = self.selection_text
        # Definitions for selecting and tracking data on objects
        self.clickable_text = "Mouse last selected: " + self.clickable_text_temp
        self.overlay_clickable_label.text = self.clickable_text
        self.clickable_owner_text = "Owner: " + self.clickable_owner_text_temp
        self.overlay_clickable_owner_label.text = self.clickable_owner_text
        self.clickable_targetbool_text = "Auto-targeting: " + self.clickable_targetbool_text_temp
        self.overlay_clickable_targetbool_label.text = self.clickable_targetbool_text
        self.tracked_type = None
        self.tracked_health = 0
        self.tracked_shield = 0
        self.tracked_owner = None

        if globals.offline_multi:
            # Overlay editing
            self.p2_mineral_text = ("Mineral: " + str(round(globals.player2_lv1_res, 1)) + " (" + str(
                round(globals.player2_lv1_gen, 2)) + "/s)")  # ℤens
            self.p2_overlay_mineral_label.text = self.p2_mineral_text
            self.p2_metal_text = ("Metal: " + str(round(globals.player2_lv2_res, 1)) + " (" + str(
                round(globals.player2_lv2_gen, 2)) + "/s)")  # ℤens
            self.p2_overlay_metal_label.text = self.p2_metal_text
            self.p2_oil_text = ("Oil: " + str(round(globals.player2_lv3_res, 1)) + " (" + str(
                round(globals.player2_lv3_gen, 2)) + "/s)")  # ℤens
            self.p2_overlay_oil_label.text = self.p2_oil_text
            self.p2_selection_text_temp = str(game_window_run.player_two.get_select()).split("'")
            self.p2_selection_text_temp = str((self.p2_selection_text_temp[1])[8:])
            self.p2_selection_text = "Selection: " + str(self.p2_selection_text_temp)
            self.p2_overlay_selection_label.text = self.p2_selection_text
            # Definitions for selecting and tracking data on objects
            self.p2_clickable_text = "Mouse last selected: " + self.clickable_text_temp
            self.p2_overlay_clickable_label.text = self.clickable_text
            self.p2_clickable_owner_text = "Owner: " + self.clickable_owner_text_temp
            self.p2_overlay_clickable_owner_label.text = self.clickable_owner_text
            self.p2_clickable_targetbool_text = "Auto-targeting: " + self.clickable_targetbool_text_temp
            self.p2_overlay_clickable_targetbool_label.text = self.clickable_targetbool_text
            self.p2_tracked_type = None
            self.p2_tracked_health = 0
            self.p2_tracked_shield = 0
            self.p2_tracked_owner = None

    def on_text(self, text):
        if self.firstt == True and self.input_text == 't':
            self.input_text = ''
            self.firstt = False
        self.input_text += text
        # if Typein.firstt != True:
        #     Labels.playername_label.input_text = Typein.input_text
        # Control.CurrentPlayer.name = Typein.input_text

    def on_key_press(self, symbol, modifiers):
        # print(symbol) # use for finding id of button
        if symbol == key.ENTER:
            globals.code = self.input_text.upper()
            self.input_text = ''
            if globals.code == "MEMENTOMORI":
                for i in globals.building_objects:
                    if globals.building_objects[i].get_obj_type() == "Drill":
                        i.image = src.animations.animation.DUA_ani
                        objects.Drill.image = src.animations.animation.DUA_ani

        elif symbol == key.SLASH:
            if modifiers & key.MOD_SHIFT:
                self.show_grid = not (self.show_grid)
                if self.show_grid:
                    for i in objects.grid_set:
                        i.opacity = 255
                else:
                    for i in objects.grid_set:
                        i.opacity = 0
            else:
                self.show_data_overlay = not (self.show_data_overlay)
            # Control.handleraltered = False

        elif symbol == key.HASH:
            self.show_research_overlay = not (self.show_research_overlay)

        elif symbol == key.BACKSLASH:
            if self.clicked_object is not None:
                self.clicked_object.auto_targeting = not (self.clicked_object.auto_targeting)
        elif symbol == key.BACKSPACE:
            self.input_text = self.input_text[:-1]

        if symbol == key.LEFT:  # TODO: choose whether the menu function buttons should be the same
            # TODO: or different for each player (only one player's building can be accessed at once)
            if self.clicked_object is not None:
                if self.clicked_object.get_needs_menu():
                    self.clicked_object.key_left_func()

        if symbol == key.RIGHT:
            if self.clicked_object is not None:
                if self.clicked_object.get_needs_menu():
                    self.clicked_object.key_right_func()

        if symbol == key.ENTER or symbol == key.RETURN:
            if self.clicked_object is not None:
                if self.clicked_object.get_needs_menu():
                    self.clicked_object.enter_func()

            # Labels.playername_label.input_text = Typein.input_text
        elif symbol:
            return True

    def get_centred_coords(self, x, y):
        x_remainder = x % 20
        y_remainder = y % 20
        x_centred = (x - x_remainder) + 10
        y_centred = (y - y_remainder) + 10
        return x_centred, y_centred

    def on_mouse_press(self, x, y, button, modifiers):
        # print(str(button) + "Pressed at: " + str(x) + " " + str(y))
        got_troop = False
        got_building = False
        # TODO: look at building an algorithm or another way to more quickly get the clicked object.
        for i in globals.troop_objects:
            if self.get_centred_coords(globals.troop_objects[i].get_x(),
                                       globals.troop_objects[i].get_y()) == self.get_centred_coords(x, y):
                self.tracked_type = globals.troop_objects[i].get_overlay_name()
                self.tracked_health = globals.troop_objects[i].get_health()
                self.tracked_shield = globals.troop_objects[i].get_shield()
                self.tracked_owner = globals.troop_objects[i].get_owner_id()
                self.clickable_text_temp = (str(self.tracked_type) + " - Health: " +
                                            str(round(self.tracked_health, 1)) + " + " +
                                            str(round(self.tracked_shield, 1)) + " Shield\n"
                                            + "Owner: " + str(self.tracked_owner))
                got_troop = True
                self.clicked_object = i
                break
        if not got_troop:
            for i in globals.building_objects:
                if self.get_centred_coords(globals.building_objects[i].get_x(),
                                           globals.building_objects[i].get_y()) == self.get_centred_coords(x, y):
                    self.tracked_type = i.get_overlay_name()
                    self.tracked_health = i.get_health()
                    self.tracked_shield = i.get_shield()
                    self.tracked_owner = i.get_owner_id()
                    self.clickable_text_temp = (str(self.tracked_type) + " - Health: " +
                                                str(round(self.tracked_health, 1)) + " + " +
                                                str(round(self.tracked_shield, 1)) + " Shield\n"
                                                + "Owner: " + str(self.tracked_owner))
                    got_building = True
                    self.clicked_object = i
                    break
        if not got_troop and not got_building:
            self.clicked_object = None
            tile_coords = self.get_centred_coords(x, y)
            self.clickable_text_temp = ("Empty tile at:  " + str(tile_coords[0]) + ", " + str(tile_coords[1]))
            self.overlay_clickable_owner_label.text = "Owner: "
            self.overlay_clickable_targetbool_label.text = "Auto-targeting: "
            self.clickable_owner_text_temp = ""
            self.clickable_targetbool_text_temp = ""

        if self.show_research_overlay:
            for i in self.research_items:
                if x >= i.startx and x <= (i.startx + i.width) and y >= i.starty and y <= (i.starty + i.height):
                    print(i.slot)
                    break

        # print("You clicked on the tile centred at " + str(x_centred) + " " + str(y_centred))

    def on_draw(self):
        self.clear()
        globals.game_batch.draw()

        globals.small_troop_batch.draw()
        globals.medium_troop_batch.draw()
        globals.large_troop_batch.draw()

        for i in globals.building_objects:
            if globals.building_objects[i].get_obj_type() == "Tracing turret":
                i.get_tracer().draw()

        if self.show_data_overlay:
            globals.data_overlay_batch.draw()
        self.fps_display.draw()

        if self.show_research_overlay:
            globals.research_overlay_batch.draw()

        globals.hud_batch.draw()
        globals.tracer_batch.draw()

    def get_game_objects(self):
        return self.game_objects

    def dataPush(self):
        """Pushes relavent data into globals for later usage as a message."""
        playerPos = self.player_one.get_pos()
        return {"position": [playerPos[0], playerPos[1]],
                "resources": [globals.player1_lv1_res, globals.player1_lv2_res, globals.player1_lv3_res],
                "generation": [globals.player1_lv1_gen, globals.player1_lv2_gen, globals.player1_lv3_gen]}

    def serveData(self, dt=None):
        print("serving")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 1235))
        # s.setblocking(False)
        s.listen(5)

        data = self.dataPush()
        clientsocket, address = s.accept()
        clientsocket.send(net.dicttomessage(data))

        # s.close()

    def tiles_map(self, resx=globals.screenresx, resy=globals.screenresy, size=20):
        grad = src.pixel_approx.tileize(src.pixel_approx.get_noise(), size)

        ylayers = resy // size
        # print(ylayers)
        tiles = []
        deep_water = (19, 15, 64)
        shallow_water = (41, 128, 185)
        shore = (236, 204, 104)
        land = (0, 148, 50)
        raised = (44, 22, 8)
        hill = (45, 52, 54)
        mountain = (223, 230, 233)
        for i in range(ylayers):
            tiles.append([])
            globals.astar_map.append([])
            # print(str(len(tiles)) + ";ayers")
        tilebatch = pyglet.graphics.Batch()
        for i in range(resy // size):
            # print("layer" + str(i))
            for j in range(resx // size):
                # r = secrets.randbelow(255)
                colournum = (grad[j][i])[0]
                tile_colour = None
                # NOTE: higher tilemod means higher cost on a* map, and SLOWER movement on tile. -1 is impassable terrain
                if colournum >= 0 and colournum < 50:
                    tile_colour = deep_water
                    tilemod = -1
                elif colournum >= 50 and colournum < 90:
                    tile_colour = shallow_water
                    tilemod = -1
                elif colournum >= 90 and colournum < 110:
                    tile_colour = shore
                    tilemod = 1
                elif colournum >= 110 and colournum < 150:
                    tile_colour = land
                    tilemod = 1
                elif colournum >= 150 and colournum < 175:
                    tile_colour = raised
                    tilemod = 2
                elif colournum >= 175 and colournum < 210:
                    tile_colour = hill
                    tilemod = 3
                elif colournum >= 210 and colournum <= 255:
                    tile_colour = mountain
                    tilemod = 10

                current_tile = objects.TileBG(x=size * j, y=size * i, width=size, height=size, color=tile_colour,
                                              batch=globals.game_batch, group=globals.map_group)  # batch=tilebatch

                globals.astar_map[ylayers - i - 1].append(tilemod)
                if tilemod < 0:
                    current_tile.modifier = 0.0001
                    current_tile.make_barrier()
                else:
                    current_tile.modifier = 1 / tilemod

                tiles[i - 1].append(current_tile)

        for i in range(resx // size):
            objects.grid_set.append((
                pyglet.shapes.Line(xcoord := i * 20, 0, xcoord, resy, 1, (35, 35, 35), batch=globals.game_batch,
                                   group=globals.grid_group)
            ))

        for i in range(resy // size):
            objects.grid_set.append((
                pyglet.shapes.Line(0, ycoord := i * 20, resx, ycoord, 1, (35, 35, 35), batch=globals.game_batch,
                                   group=globals.grid_group)
            ))

        globals.astar_matrix = Grid(matrix=globals.astar_map)

        return tiles, tilebatch


game_window_run = game_window()  # width = screenresx, height=screenresy
# data_window_run = data_window() # Deprecated - overlay replaces data window

# class Typein(object):


pyglet.app.run()  # kek or cringe
