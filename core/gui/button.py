"""
To Do:
    Give buttons a visual for when they are clicked.
    add doc strings
"""

from label import Label
from pygame.color import Color
from signal import Signal


class Button(Label):
    def __init__(self, x, y, width, height, text, font, font_color=Color('black'), color=Color('gray')):
        super(Button, self).__init__(x, y, width, height, font, text, color, font_color)
        self.on_clicked = Signal()

    def change_color(self, (r, g, b)):
        self.color = (r, g, b)
        self.surface.fill(self.color)

    def mouse_up(self, button, point):
        self.on_clicked()
