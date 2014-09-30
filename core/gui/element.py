from pygame import Color, Surface, Rect
from signal import Signal


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
        if self.color is not None:
            self.surface.fill(self.color)
        self.parent = None
        self.on_mouse_up = Signal()
        self.on_mouse_down = Signal()
        self.on_mouse_drag = Signal()
        self.draggable = False
        self.enabled = True
        self.hidden = False

    def size(self):
        """Returns size of element."""
        return self.frame.size

    def hit(self, mouse_pos):
        if self.hidden or not self.enabled:
            return None
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
        if not self.hidden:
            window.blit(self.surface, self.position())

    def set_parent(self, parent):
        """
        Sets the master handler of this object. Master's can be panels or the main console window. This updates this
        objects position in a way that makes the origin (0, 0) that of its masters (x, y) position. It takes the master
        object as an argument.
        """
        self.parent = parent
        self.update_position()

    def update_position(self):
        """
        The method updatePosition, sets this objects position based upon its masters position. See the setMaster
        definition for a more thorough explanation.
        """
        if hasattr(self.parent, 'frame'):
            x = self.frame.x + self.parent.frame.x
            y = self.frame.y + self.parent.frame.y
            self.frame.x, self.frame.y = x, y

    def mouse_up(self, button, point):
        self.on_mouse_up(self, button, point)

    def mouse_down(self, button, point):
        self.on_mouse_down(self, button, point)

    def mouse_drag(self, view, position, event):
        self.on_mouse_drag(self, position, event)