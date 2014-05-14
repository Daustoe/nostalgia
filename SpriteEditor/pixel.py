from pygame import Surface, draw, Color
import core.gui.element as Element


class Pixel(Element.Element):
    """
    Some notes!!!
    perhaps we want render() to draw the outline of each pixel, instead of relying on
    separatePixels() in our sprite object.
    It would make it simpler to manage each 'pixel' of a sprite, and make it easier to see.
    We are also going to want to add actionEvents for each pixel if it is clicked on, in order
    to change the pixels mouse clicks
    """
    def __init__(self, x, y, width, height, color=Color(200, 200, 200)):
        super(Pixel, self).__init__(x, y, width, height, color)
        self.surface.set_alpha(255)
        self.null_pixel = Surface(self.size())
        self.null_pixel.fill((255, 255, 255))
        draw.line(self.null_pixel, (150, 0, 0), (0, 0), self.size(), 2)
        draw.line(self.null_pixel, (150, 0, 0), (self.width, 0), (0, self.height), 2)
        self.clicked = False
        if self.color == (200, 200, 200):
            self.is_null = True
        else:
            self.is_null = False

    def save_color(self):
        if self.is_null:
            return None
        else:
            return self.color

    def change_color(self, color):
        if color is None:
            self.is_null = True
        else:
            self.is_null = False
            self.color = color
            self.surface = Surface(self.size())
            self.surface.fill(self.color)

    def get_color(self):
        return self.color

    def render(self, window):
        if self.is_null:
            window.blit(self.null_pixel, self.position())
        else:
            super(Pixel, self).render(window)