"""
This is the abstract class that any gui element needs to inherit from. It has the
basic definitions and variables needed by the console object to handle
actionEvents and rendering.
"""
import pygame


class Element(object):
    def __init__(self, position, (width, height), color=(200, 200, 200)):
        super(Element, self).__init__()
        self.position = (self.x, self.y) = position
        self.size = (self.width, self.height) = (width, height)
        self.surface = pygame.Surface(self.size)
        self.color = color
        self.surface.fill(color)
        self.master = None
        self.clicked = False

    def render(self, window):
        """
        The render definition takes a surface as an arugement and blits its surface to the one given.
        """
        window.blit(self.surface, self.position)

    def set_master(self, master):
        """
        Sets the master handler of this object. Master's can be panels or the main
        console window. This updates this objects position in a way that makes the
        origin (0, 0) that of its masters (x, y) position. It takes the master
        object as an argument.
        """
        self.master = master
        self.update_position()

    def update_position(self):
        """
        The method updatePosition, sets this objects position based upon its masters
        position. See the setMaster definition for a more thorough explanation.
        """
        x = self.position[0] + self.master.position[0]
        y = self.position[1] + self.master.position[1]
        self.position = (x, y)