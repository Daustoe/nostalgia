from core.gui.element import Element


class Pixel(Element):
    """
    This is the Pixel object for the Sprite Editor. These Pixels represent individual pixels in the sprite and are used
    to help render pixels in an object oriented fashion for the sprite. Each pixel knows where it's surface is located
    and knows when it is clicked on. It holds onto the current color it is set to.
    """
    def __init__(self, x, y, width, height, color=None):
        super(Pixel, self).__init__(x, y, width, height)
        self.color = color
        self.surface.set_alpha(255)

    def change_color(self, color):
        self.color = color
        if color is not None:
            self.surface.fill(self.color)

    def get_color(self):
        return self.color

    def render(self, window):
        if self.color is not None:
            super(Pixel, self).render(window)

    def mouse_down(self, button, point):
        if button == 1:
            self.change_color(self.parent.color_box.get_color())
            self.parent.color_box.catalog_current()
        if button == 3:
            self.parent.color_box.set_color(self.color)

    def mouse_drag(self, view, position, event):
        if event.buttons == (1, 0, 0):
            self.change_color(self.parent.color_box.get_color())