"""
No color wheel yet, may want to use a third party source for this (I believe TKinter has a nice one).
Modifying this to have a history of selected colors. We want the current selected color below, with a short (last 10)
history of previously selected colors above. Sliders will remain the same.

Also want to add the rgb label to this color panel as that is directly related to the currently selected color.
"""
from core.gui.view import View
from core.gui.slider import Slider
from core.gui.label import Label
from core.gui.element import Element
from pygame.color import Color


class ColorPanel(View):
    def __init__(self, x, y, width, height, color=Color('0x323232')):
        """
        Initializes the sliders, and adds them to the ColorPanel object. Default background color is rgb=505050
        """
        super(ColorPanel, self).__init__(x, y, width, height, color)
        self.square = Element(127, 150, 40, 40)
        initial_history = Element(10, 10, 30, 30, color=self.square.color)
        self.history = [initial_history]
        self.add(initial_history)

        self.red = Slider(10, 200, 275, 15, Color('0xffc8c8'), Color('red'))
        self.green = Slider(10, 220, 275, 15, Color('0xc8ffc8'), Color('green'))
        self.blue = Slider(10, 240, 275, 15, Color('0xc8c8ff'), Color('blue'))
        self.add(self.red)
        self.add(self.green)
        self.add(self.blue)
        self.add(self.square)
        self.blue.on_value_changed.connect(self.update_color)
        self.green.on_value_changed.connect(self.update_color)
        self.red.on_value_changed.connect(self.update_color)

    def set_color(self, new_color):
        self.color = new_color

    def get_color(self):
        return self.square.color

    def update_color(self):
        self.square.color = Color(int(self.red.value * 255), int(self.green.value * 255), int(self.blue.value * 255))
        self.square.surface.fill(self.square.color)

    def render(self, window):
        super(ColorPanel, self).render(window)
        for each in self.history:
            each.render(window)

    def add_to_history(self):
        if self.history[-1].color != self.square.color:
            frame = self.history[-1].frame
            surface = Element(frame.x + 35, frame.y, frame.w, frame.h, color=self.square.color)
            self.history.append(surface)
