from core.gui.view import View
from core.gui.slider import Slider
from core.gui.element import Element
from colorButton import ColorButton
from pygame.color import Color
from core.gui.button import Button


class ColorPalette(View):
    def __init__(self, x, y, width, height, font, color=Color('0x323232')):
        super(ColorPalette, self).__init__(x, y, width, height, color)
        self.main_color = Button(5, 665, 100, 20, '', font, color=Color(0, 0, 0, 255))
        self.second_color = Button(5, 690, 100, 20, '', font, color=Color(255, 255, 255, 255))
        self.history = []
        self.font = font
        self.red = Slider(10, 200, 275, 15, Color('0xffc8c8'), Color('red'))
        self.green = Slider(10, 220, 275, 15, Color('0xc8ffc8'), Color('green'))
        self.blue = Slider(10, 240, 275, 15, Color('0xc8c8ff'), Color('blue'))
        self.add(self.red)
        self.add(self.green)
        self.add(self.blue)
        self.add(self.main_color)
        self.add(self.second_color)
        self.blue.on_value_changed.connect(self.update_color)
        self.green.on_value_changed.connect(self.update_color)
        self.red.on_value_changed.connect(self.update_color)

    def set_color(self, new_color):
        if new_color is not None:
            self.main_color.color = new_color
            self.main_color.surface.fill(self.main_color.color)
            self.add_to_history(new_color)
            self.update_sliders()

    def reset(self):
        self.history = []
        self.red.set_index(0)
        self.green.set_index(0)
        self.blue.set_index(0)

    def update_sliders(self):
        self.red.set_index(self.main_color.color.r / 255.0)
        self.green.set_index(self.main_color.color.g / 255.0)
        self.blue.set_index(self.main_color.color.b / 255.0)

    def get_color(self, button):
        if button == 1:
            return self.main_color.color
        elif button == 3:
            return self.second_color.color

    def update_color(self):
        self.main_color.color = Color(int(self.red.value * 255), int(self.green.value * 255), int(self.blue.value * 255))
        self.main_color.surface.fill(self.main_color.color)

    def render(self, window):
        super(ColorPalette, self).render(window)
        for each in self.history:
            each.render(window)

    def add_to_history(self, color):
        in_history = False
        for each in self.history:
            if each.color == color:
                in_history = True
        if not in_history and color is not None:
            new_color = ColorButton(5 + 17 * len(self.history), 5, 12, 12, self.font, color)
            self.history.append(new_color)
            new_color.on_clicked.connect(self.set_color)
            self.add(new_color)

    def catalog_current(self):
        self.add_to_history(self.main_color.color)