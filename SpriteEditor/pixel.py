from core.gui.element import Element


class Pixel(Element):
    """
    This is the Pixel object for the Sprite Editor. These Pixels represent individual pixels in the sprite and are used
    to help render pixels in an object oriented fashion for the sprite. Each pixel knows where it's surface is located
    and knows when it is clicked on. It holds onto the current color it is set to.
    """
    def __init__(self, x, y, width, height, color=(0, 0, 0)):
        super(Pixel, self).__init__(x, y, width, height)
        self.color = color
        self.surface.set_alpha(0)

    def change_color(self, color):
        if color is None:
            self.color = (0, 0, 0)
            self.surface.set_alpha(0)
        else:
            self.color = color
            self.surface.set_alpha(255)
            self.surface.fill(self.color)

    def get_color(self):
        return self.color

    def get_alpha(self):
        return self.surface.get_alpha()

    def set_alpha(self, alpha):
        self.surface.set_alpha(alpha)

    def mouse_down(self, button, point):
        if button == 1:
            self.change_color(self.parent.color_box.get_color())
            self.parent.color_box.catalog_current()
        if button == 3:
            self.parent.color_box.set_color(self.color)

    def mouse_drag(self, view, position, event):
        if event.buttons == (1, 0, 0):
            self.change_color(self.parent.color_box.get_color())