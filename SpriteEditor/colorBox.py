"""
Created on Mar 22, 2012

@author: Claymore

@todo
    add doc strings
"""
import core.gui.element


class ColorBox(core.gui.element.Element):
    def __init__(self, (x, y), (width, height), color=(0, 0, 0)):
        super(ColorBox, self).__init__((x, y), (width, height), color)

    def update_colors(self, (r, g, b)):
        self.color = (r, g, b)
        self.surface.fill(self.color)

    def set_master(self, master):
        super(ColorBox, self).set_master(master)

    def render(self, window):
        super(ColorBox, self).render(window)

    def get_color(self):
        return self.color