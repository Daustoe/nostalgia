from pygame import Surface, draw, Color
from core.gui.element import Element


class Pixel(Element):
    """
    Some notes!!!
    perhaps we want render() to draw the outline of each pixel, instead of relying on
    separatePixels() in our sprite object.
    It would make it simpler to manage each 'pixel' of a sprite, and make it easier to see.
    We are also going to want to add actionEvents for each pixel if it is clicked on, in order
    to change the pixels mouse clicks
    """
    def __init__(self, x, y, width, height, color=Color('0x000000')):
        super(Pixel, self).__init__(x, y, width, height, color)
        if color == (0, 0, 0):
            self.color = None
        self.surface.set_alpha(255)
        self.null_pixel = Surface(self.size())
        self.null_pixel.fill((255, 255, 255))
        draw.line(self.null_pixel, (150, 0, 0), (0, 0), self.size(), 2)
        draw.line(self.null_pixel, (150, 0, 0), (self.frame.w, 0), (0, self.frame.h), 2)
        self.clicked = False

    def save_color(self):
        return self.color

    def change_color(self, color):
        self.color = color
        self.surface = Surface(self.size())
        if color is not None:
            self.surface.fill(self.color)

    def get_color(self):
        return self.color

    def render(self, window):
        if self.color is None:
            window.blit(self.null_pixel, self.position())
        else:
            super(Pixel, self).render(window)

    def mouse_down(self, button, point):
        self.change_color(self.parent.color_box.get_color())

    def mouse_drag(self, view, position, event):
        if event.buttons == (1, 0, 0):
            self.change_color(self.parent.color_box.get_color())