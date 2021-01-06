import sys
import pathlib
from pathlib import Path

import pyglet

import globals

dir_path = Path(sys.path[0])  # More consistent relative path
base = Path("D:/Strat/LPx64/")
placeholder_path = base / "src" / "sprite" / "Placeholder-building.png"

placeholder = pyglet.image.load(placeholder_path)

class PathError(Exception):
    """Attributes:
        args[0] = Error Message
        args[1] = Issue/Reason raised
    """

    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.issue = args[1]
        else:
            self.message = None
            self.issue = None

        if self.issue == 0:
            self.issue = "Generate Path"
        elif self.issue == 1:
            self.issue = "Validate arguments"
        else:
            raise InitError

    def __str__(self):
        if self.message:
            return "BranchError, Failed to {0}, message: {1}".format(self.issue, self.message)
            # raise
        else:
            return "BranchError has been raised."
            # raise


class InitError(Exception):
    pass


class BranchError(Exception):
    """Attributes:
        args[0] = Error Message
        args[1] = Issue/Reason raised
    """

    def __init__(self, *args):
        if args:
            self.message = args[0]
            self.issue = args[1]
        else:
            self.message = None
            self.issue = None

        if self.issue == 0:
            self.issue = "Initiate branch"
        elif self.issue == 1:
            self.issue = "Validate arguments"
        else:
            raise InitError

    def __str__(self):
        if self.message:
            return "BranchError, Failed to {0}, message: {1}".format(self.issue, self.message)
            # raise
        else:
            return "BranchError has been raised."
            # raise


class Branch():
    """A class to simplify creating a 'branch'
    shape for the research tree."""
    def __init__(self, startx=500, starty=500, height=200, width=100, direction="NE", line_width=1, colour=(255, 255, 255),
                 variant="mid", batch=globals.research_overlay_batch):
        self.lines = []
        self.startx = startx
        self.starty = starty
        self.height = height
        self.width = width
        self.direction = direction
        self.line_width = line_width
        self.colour = colour
        self.batch = batch

        self.build()

    def build(self):
        """Function to use the arguments given to create the correct shape.
        If the arguments are changed after creation, this will need to be called to
        implement those changes.

        Directions allowed:
            NE - North East
            NW - North West
            SE - South East
            SW - South West"""

        if self.width == 0 or self.height == 0:
            raise BranchError("Branch cannot have a width or height of zero." % 1)
        if self.width < 0 or self.height < 0:
            raise BranchError("Found negative values in width and/or height. "
                              "If you want to alter the direction of the branch, "
                              "the direction argument can be used.")

        if self.lines:  # if self.lines != []:
            for i in self.lines:
                del i
        self.lines = []

        if self.direction == "NE":
            mid_y = self.starty + (self.height / 2)
            end_x = self.startx + self.width
            end_y = self.starty + self.height

            self.lines.append(
                pyglet.shapes.Line(self.startx, self.starty, self.startx, mid_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))
            self.lines.append(
                pyglet.shapes.Line(self.startx, mid_y - 1, end_x, mid_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))
            self.lines.append(
                pyglet.shapes.Line(end_x, mid_y, end_x, end_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))


        elif self.direction == "NW":
            mid_y = self.starty + (self.height / 2)
            end_x = self.startx - self.width
            end_y = self.starty + self.height

            self.lines.append(
                pyglet.shapes.Line(self.startx, self.starty, self.startx, mid_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))
            self.lines.append(
                pyglet.shapes.Line(self.startx, mid_y - 1, end_x, mid_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))
            self.lines.append(
                pyglet.shapes.Line(end_x, mid_y - 1, end_x, end_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))

        elif self.direction == "SW":
            mid_y = self.starty - (self.height / 2)
            end_x = self.startx - self.width
            end_y = self.starty - self.height

            self.lines.append(
                pyglet.shapes.Line(self.startx, self.starty, self.startx, mid_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))
            self.lines.append(
                pyglet.shapes.Line(self.startx, mid_y - 1, end_x, mid_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))
            self.lines.append(
                pyglet.shapes.Line(end_x, mid_y, end_x, end_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))

        elif self.direction == "SE":
            mid_y = self.starty - (self.height / 2)
            end_x = self.startx + self.width
            end_y = self.starty - self.height

            self.lines.append(
                pyglet.shapes.Line(self.startx, self.starty, self.startx, mid_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))
            self.lines.append(
                pyglet.shapes.Line(self.startx, mid_y - 1, end_x, mid_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))
            self.lines.append(
                pyglet.shapes.Line(end_x, mid_y, end_x, end_y,
                                   1, self.colour, batch=self.batch, group=globals.ol_prim_group))

        else:
            raise BranchError("Direction incorrectly input.", 0)


class ResearchSlot():
    """A class to create a bordered rectangle with a sprite contained inside it."""
    def __init__(self, startx=500, starty=500, width=20, height=20, borderwidth=1, colour=(255, 255, 255), spritesrc=placeholder):
        self.startx = startx
        self.starty = starty
        self.width = width
        self.height = height
        self.borderwidth = borderwidth
        self.colour = colour
        self.spritesrc = spritesrc

        if getattr(self.spritesrc, '__module__', None) == pathlib.__name__:
            self.sprite = pyglet.image.load(self.spritesrc)

        elif type(self.spritesrc) == str:
            try:
                self.spritesrc = Path(self.spritesrc)
            except:
                raise PathError("String given could not be used to create Path object", 0)

            self.sprite = pyglet.image.load(self.spritesrc)

# if type(placeholder_path) == pathlib.Path:
#     print("is path")
# else:
#     print(type(placeholder_path))
#
# if getattr(placeholder_path, '__module__', None) == pathlib.__name__:
#     print("from pathlib")
print(type(placeholder))
# <class 'pyglet.image.ImageData'>