"""
TODO
Want to enable color wheel!!!
Need to generate the color 'ring' that will surround the triangle that lets the user select their
hue and saturation. Should switch to using Pygames built in color module, as it supports the necessary
mathematical color functions I will need for this.
enable more options besides rgb (hue, saturation, etc.)
"""
import view
import slider
import label
import element
import pygame.color as Color


class ColorBox(view.View):
    """
    The ColorBox class gives the developer a gui object that lets users select a color. As of right now this only
    supports rgb colors with no care for saturation or hue. That is something that we want to change. We also want to
    give the selector a fairly modern feel.

    As of now it includes a slider for red, green, and blue.
    """
    def __init__(self, x, y, width, height, color=Color.Color('0x323232')):
        """
        Initializes the sliders, and adds them to the ColorBox object. Default background color is rgb=505050
        """
        super(ColorBox, self).__init__(x, y, width, height, color)
        self.red = slider.Slider(10, 290, 275, 15, Color.Color('0xffc8c8'), Color.Color('red'))
        self.green = slider.Slider(10, 310, 275, 15, Color.Color('0xc8ffc8'), Color.Color('green'))
        self.blue = slider.Slider(10, 330, 275, 15, Color.Color('0xc8c8ff'), Color.Color('blue'))
        self.square = element.Element(10, 10, 275, 275)
        self.add_child(self.red)
        self.add_child(self.green)
        self.add_child(self.blue)
        self.add_child(self.square)
        self.rgb_label = label.Label

    def set_color(self, new_color):
        """ Sets the selected color of the chooser, used mainly to set from a current pixel color."""
        self.color = new_color

    def get_color(self):
        """ Returns currently selected color."""
        return self.square.color

    def update_color(self):
        """
        Updates the color square to what the user has changed on the sliders. Done before every draw. Does not check
        to see if the user has updated.
        """
        self.square.color = Color.Color(int(self.red.value * 255), int(self.green.value * 255), int(self.blue.value * 255))
        self.square.surface.fill(self.square.color)

    def render(self, window):
        """
        Draws the Colorbox surface (sliders and square for now) and blits it to the window.
        """
        self.update_color()
        super(ColorBox, self).render(window)