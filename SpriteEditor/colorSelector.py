__author__ = 'cjpowell'
from core.gui.view import View
from core.gui.label import Label
from pygame.color import Color
from core.gui.slider import Slider


class ColorSelector(View):
    def __init__(self, x, y, width, height, font, color=Color('0x323232')):
        super(ColorSelector, self).__init__(x, y, width, height, color)
        self.font = font
        self.red = Slider(5, 30, 275, 15, Color('0xffc8c8'), Color('red'))
        self.green = Slider(5, 50, 275, 15, Color('0xc8ffc8'), Color('green'))
        self.blue = Slider(5, 70, 275, 15, Color('0xc8c8ff'), Color('blue'))
        self.color_hex = Label(5, 5, 80, 15, self.font, 'test')
        self.add(self.red)
        self.add(self.green)
        self.add(self.blue)
        self.add(self.color_hex)
        self.red.on_value_changed.connect(self.update_color)
        self.green.on_value_changed.connect(self.update_color)
        self.blue.on_value_changed.connect(self.update_color)

    def generate_hex(self):
        temp = int(self.red.value * 255) << 16
        temp += int(self.green.value * 255) << 8
        temp += int(self.blue.value * 255)
        return hex(temp)

    def update_sliders(self, color):
        self.red.set_index(color.r / 255.0)
        self.green.set_index(color.g / 255.0)
        self.blue.set_index(color.b / 255.0)
        self.color_hex.update_text(self.generate_hex())

    def reset(self):
        self.red.set_index(0)
        self.green.set_index(0)
        self.blue.set_index(0)
        self.color_hex.update_text('0x000000')

    def update_color(self):
        new_color = Color(int(self.red.value * 255), int(self.green.value * 255), int(self.blue.value * 255))
        self.color_hex.update_text(self.generate_hex())
        self.parent.update_color(new_color)