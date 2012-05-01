'''
This is the abstact class that any gui element needs to inherit from. It has the basic
definitions and variables needed by the console object to handle actionEvents and rendering.
'''
import pygame, time

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
        
    '''
    The render definition takes a surface as an argument and blits its surface to the one given.
    '''
    def render(self, window):
        window.blit(self.surface, self.position)
        
    '''
    Sets the master handler of this object. Master's can be panels or the main console window. 
    This updates this objects position in a way that makes the origin (0, 0) that of its masters
    (x, y) position. It takes the master object as an argument.
    '''
    def setMaster(self, master):
        self.master=master
        
    '''
    The method updatePosition, sets this objects position based upon its masters position. See the setMaster
    definition for a more thorough explanation.
    '''
    def updatePosition(self):
        self.position = (self.position[0]+self.master.position[0], self.position[1]+self.master.position[1])