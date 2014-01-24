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
        self.rgb_label = label.Label
        self.square = None

    def update_colors(self, r, g, b):
        self.color = (r, g, b)
        self.surface.fill(self.color)

    def get_color(self):
        return self.color