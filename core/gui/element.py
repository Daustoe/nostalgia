from pygame import Color, Surface


class Element(object):
    """
    The Element object is the abstract class that all gui elements of nostalgia inherit from. It has the basic
    definitions and variables needed by the by the Console object to hand events and rendering.
    """
    def __init__(self, x, y, width, height, color=Color('0x000000')):
        super(Element, self).__init__()
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.surface = Surface((self.width, self.height))
        self.color = color
        self.surface.fill(self.color)
        self.master = None
        self.clicked = False

    def size(self):
        """Returns size of element."""
        size = (self.width, self.height)
        return size

    def position(self):
        """Returns position of the element."""
        position = (self.x, self.y)
        return position

    def render(self, window):
        """
        The render definition takes a surface as an argument and blits its surface to the one given.
        """
        window.blit(self.surface, self.position())

    def set_master(self, master):
        """
        Sets the master handler of this object. Master's can be panels or the main
        console window. This updates this objects position in a way that makes the
        origin (0, 0) that of its masters (x, y) position. It takes the master
        object as an argument.
        """
        self.master = master
        self.update_position()

    def update_position(self):
        """
        The method updatePosition, sets this objects position based upon its masters
        position. See the setMaster definition for a more thorough explanation.
        """
        if hasattr(self.master, 'x'):
            x = self.x + self.master.x
            y = self.y + self.master.y
            self.x, self.y = x, y