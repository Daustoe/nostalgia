"""
Color Box Panel

TODO
Want to enable color wheel!!!
Need to generate the color 'ring' that will surround the triangle that lets the user select their
hue and saturation. Should switch to using Pygames built in color module, as it supports the necessary
mathematical color functions I will need for this.
enable more options besides rgb (hue, saturation, etc.)
docstrings
"""
import panel
import slider
import label


class ColorBox(panel.Panel):
    """
    The ColorBox class gives the developer a gui object that lets users select a color. As of right now this only
    supports rgb colors with no care for saturation or hue. That is something that we want to change. We also want to
    give the selector a fairly modern feel.

    As of now it includes a slider for red, green, and blue.
    """
    def __init__(self, (x, y), (width, height), color=(0, 0, 0)):
        """
        Initializes the sliders, and adds them to the ColorBox object. Sets the default color to gray.
        """
        super(ColorBox, self).__init__((x, y), (width, height), color)
        self.red = slider.Slider((-10, 275), (270, 15), (255, 200, 200), (255, 0, 0))
        self.green = slider.Slider((-10, 295), (270, 15), (200, 255, 200), (0, 255, 0))
        self.blue = slider.Slider((0, 315), (270, 15), (200, 200, 255), (0, 0, 255))
        self.add_element(self.red)
        self.add_element(self.green)
        self.add_element(self.blue)
        self.rgb_label = label.Label

    def set_color(self, new_color):
        """ Sets the selected color of the chooser, used mainly to set from a current pixel color."""
        self.color = new_color

    def get_color(self):
        """ Returns currently selected color."""
        return self.color

    def update_color(self):
        """
        Updates the color square to what the user has changed on the sliders. Done before every draw. Does not check
        to see if the user has updated.
        """
        self.color = (self.red.value * 255, self.green.value * 255, self.blue.value * 255)

    def render(self, window):
        """
        Draws the Colorbox surface (sliders and square for now) and blits it to the window.
        """
        self.update_color()
        self.surface.fill(self.color)
        super(ColorBox, self).render(window)