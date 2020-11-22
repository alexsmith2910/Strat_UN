import pyglet
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
drill_path = dir_path + "\\drill\\"
drillUA_path = dir_path + "\\drill_UA\\"
drill_frames = os.listdir(drill_path)
DUA_frames = os.listdir(drillUA_path)
for count, i in enumerate(drill_frames):
    drill_frames[count] = pyglet.image.load(drill_path + i)
    drill_frames[count].anchor_x = 10
    drill_frames[count].anchor_y = 10

for count, i in enumerate(DUA_frames):
    DUA_frames[count] = pyglet.image.load(drillUA_path + i)
    DUA_frames[count].anchor_x = 10
    DUA_frames[count].anchor_y = 10
#drill_ani = pyglet.image.Animation.from_image_sequence(images, duration=1.5, loop=True)