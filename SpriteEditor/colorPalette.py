from core.gui.view import View
from colorButton import ColorButton
from pygame.color import Color
from core.gui.button import Button
from colorSelector import ColorSelector


class ColorPalette(View):
    def __init__(self, x, y, width, height, font, color=Color('0x323232')):
        super(ColorPalette, self).__init__(x, y, width, height, color)
        self.main_color = Button(5, 635, 100, 20, '', font, color=Color(0, 0, 0, 255))
        self.second_color = Button(5, 660, 100, 20, '', font, color=Color(255, 255, 255, 255))
        self.history = []
        self.font = font
        self.selector = ColorSelector(5, 545, 290, 90, self.font, color=Color('0x101020'))
        self.add(self.selector)
        self.add(self.main_color)
        self.add(self.second_color)

    def set_color(self, new_color):
        if new_color is not None:
            self.main_color.color = new_color
            self.main_color.surface.fill(self.main_color.color)
            self.add_to_history(new_color)
            self.selector.update_sliders(self.main_color.color)

    def reset(self):
        self.history = []
        self.selector.reset()

    def get_color(self, button):
        if button == 1:
            return self.main_color.color
        elif button == 3:
            return self.second_color.color

    def update_color(self, color):
        self.main_color.color = color
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