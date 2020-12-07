import pyglet
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
drill_path = dir_path + "\\drill\\"
drill_frames = os.listdir(drill_path)

for count, i in enumerate(drill_frames):
    drill_frames[count] = pyglet.image.load(drill_path + i)
    drill_frames[count].anchor_x = 10
    drill_frames[count].anchor_y = 10
<<<<<<< HEAD:src/animations/animation.py
#drill_ani = pyglet.image.Animation.from_image_sequence(images, duration=1.5, loop=True)
=======
#drill_ani = pyglet.image.Animation.from_image_sequence(images, duration=1.5, loop=True)
sex = "me_having"
>>>>>>> 517780568de69306dda41f6ebbddcdc154acaa4f:animations/animations.py
