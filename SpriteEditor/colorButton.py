__author__ = 'cjpowell'
from core.gui.button import Button
from core.gui.signal import Signal


class ColorButton(Button):
    def __init__(self, x, y, width, height, font, color):
        super(ColorButton, self).__init__(x, y, width, height, '', font, color=color)
        self.on_clicked = Signal()

    def mouse_up(self, button, point):
        self.on_clicked(self.color)