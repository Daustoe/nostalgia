from pygame import Color, Surface, Rect


class Element(object):
    """
    The Element object is the abstract class that all gui elements of nostalgia inherit from. It has the basic
    definitions and variables needed by the by the Console object to hand events and rendering.


    for child in self.children:
            child.stylize()
        style = theme.current.get_dict(self)
        for key, val in style.iteritems():
            kvc.set_value_for_keypath(self, key, val)
        self.layout()
    """
    def __init__(self, x, y, width, height, color=Color('0x000000')):
        super(Element, self).__init__()
        self.frame = Rect(x, y, width, height)
        self.surface = Surface(self.size())
        self.color = color
        self.surface.fill(self.color)
        self.master = None
        self.clicked = False

    def size(self):
        """Returns size of element."""
        return self.frame.w, self.frame.h

    def hit(self, mouse_pos):
        # TODO here is where we would check if this object is enabled to the user
        # if self.hidden or not self.enabled
        if not self.frame.collidepoint(mouse_pos):
            return None
        else:
            return self

    def position(self):
        """Returns position of the element."""
        return self.frame.x, self.frame.y

    def render(self, window):
        """
        The render definition takes a surface as an argument and blits its surface to the one given.
        """
        window.blit(self.surface, self.position())

    def set_parent(self, master):
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
        if hasattr(self.master, 'frame'):
            x = self.frame.x + self.master.frame.x
            y = self.frame.y + self.master.frame.y
            self.frame.x, self.frame.y = x, y