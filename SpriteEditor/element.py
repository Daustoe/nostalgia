'''
This is the abstact class that any gui element needs to inherit from. It has the basic
definitions and variables needed by the console object to handle actionEvents and rendering.
'''
import pygame

class Element(object):
    '''
    Every element has these variables in common. 
        position (x and y position on the screen based on pixels)
        size (width and height of the surface being displayed)
        surface (pygame.Surface which is the displayable 'image' of the element)
        color (color of the surface) NOTE: not used if surface is an image, only used on creation.
        master (master controller of this element. this elements position is based of it's master)
        clicked (used for action events)
    '''
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
    Sets the surface of the element to the one given. Also adjusts the size of the element to the size
    of the new surface.
    '''
    def setSurface(self, surface):
        self.surface = surface
        self.size = self.surface.get_size()
        
    '''
    Loads the image from the filename given and converts it to an image. This elements surface is then
    set to that surface. Updates this elements size to the size of the new image.
    '''
    def setSurfaceFromImageFilename(self, filename):
        self.surface = pygame.image.load(filename)
        self.size = self.surface.get_size()
        
    '''
    Sets the master handler of this object. Master's can be panels or the main console window. 
    This updates this objects position in a way that makes the origin (0, 0) that of its masters
    (x, y) position. It takes the master object as an argument. Called by the Console or Panel object
    in which this element object was added.
    '''
    def setMaster(self, master):
        self.master=master
        self.updatePosition()
        
    '''
    The method updatePosition, sets this objects position based upon its masters position. See the setMaster
    definition for a more thorough explanation.
    '''
    def updatePosition(self):
        self.position = (self.position[0]+self.master.position[0], self.position[1]+self.master.position[1])