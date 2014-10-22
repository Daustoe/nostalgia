from core.gui.element import Element
from pygame import Color, SRCALPHA


class Pixel(Element):
    """
    This is the Pixel object for the Sprite Editor. These Pixels represent individual pixels in the sprite and are used
    to help render pixels in an object oriented fashion for the sprite. Each pixel knows where it's surface is located
    and knows when it is clicked on. It holds onto the current color it is set to.
    """
    def __init__(self, x, y, width, height, color=Color(0, 0, 0, 0)):
        super(Pixel, self).__init__(x, y, width, height)
        self.color = color

    def change_color(self, color):
        if color is None:
            self.color.a = 0
        else:
            self.color = color
            self.surface.fill(self.color)

    def get_color(self):
        return self.color

    def mouse_down(self, button, point):
        self.change_color(self.parent.color_box.get_color(button))
        self.parent.color_box.catalog_current()

    def mouse_drag(self, view, position, event):
        if event.buttons == (1, 0, 0):
            self.change_color(self.parent.color_box.get_color(1))
        elif event.buttons == (0, 0, 1):
            self.change_color(self.parent.color_box.get_color(3))