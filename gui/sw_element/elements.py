import pyglet


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
    def __init__(self, startx=0, starty=0, height=200, width=100, direction="NE", batch=None):
        self.startx = startx
        self.starty = starty
        self.height = height
        self.width = width
        self.direction = direction
        try:
            if self.width == 0 or self.height == 0:
                raise BranchError("Branch cannot have a width or height of zero." % 1)
            if self.width < 0 or self.height < 0:
                raise BranchError("Found negative values in width and/or height. "
                                  "If you want to alter the direction of the branch, "
                                  "the direction argument can be used.")
        except:
            raise BranchError("Failed to initiate, unknown reason." % 0)
