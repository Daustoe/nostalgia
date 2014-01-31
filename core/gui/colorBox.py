"""
Color Box Panel

TODO
Want to enable color wheel!!!
enable more options besides rgb (hue, saturation, etc.)
docstrings
"""
import panel
import slider
import label


class ColorBox(panel.Panel):
    def __init__(self, (x, y), (width, height), color=(0, 0, 0)):
        super(ColorBox, self).__init__((x, y), (width, height), color)
        self.red = slider.Slider((10, 295), (270, 15), (255, 200, 200), (255, 0, 0))
        self.green = slider.Slider((10, 315), (270, 15), (200, 255, 200), (0, 255, 0))
        self.blue = slider.Slider((10, 335), (270, 15), (200, 200, 255), (0, 0, 255))
        self.add_element(self.red)
        self.add_element(self.green)
        self.add_element(self.blue)
        self.rgb_label = label.Label
        self.square = None

        self.selected_color = (0, 0, 0)

    def set_color(self, new_color):
        self.selected_color = new_color

    def get_color(self):
        return self.color

    def render(self, window):
        self.surface.fill(self.color)
        super(ColorBox, self).render(window)