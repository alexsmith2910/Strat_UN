import sys
import os
from pathlib import Path

import pyglet

# dir_path = os.path.dirname(os.path.realpath(__file__)) # deprecated in favour of pathlib

dir_path = Path(sys.path[0])  # More consistent relative path

drill_path = dir_path / "src" / "animations" / "drill"
DUA_path = dir_path / "src" / "animations" / "DUA"
drill_frames = os.listdir(drill_path)
DUA_frames = os.listdir(DUA_path)

for count, i in enumerate(drill_frames):
    drill_frames[count] = pyglet.image.load(drill_path / i)
    drill_frames[count].anchor_x = 10
    drill_frames[count].anchor_y = 10

for count, i in enumerate(DUA_frames):
    DUA_frames[count] = pyglet.image.load(DUA_path / i)
    DUA_frames[count].anchor_x = 10
    DUA_frames[count].anchor_y = 10

drill_ani = pyglet.image.Animation.from_image_sequence(drill_frames, duration=1.5, loop=True)
DUA_ani = pyglet.image.Animation.from_image_sequence(DUA_frames, duration=1.5, loop=True)
