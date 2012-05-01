'''
This is the base Class GameObject, from which all objects (living or environmental) inherit from.
Should be considered an abstract class, as instances of it can usually be better represented
by one of the classes that inherit from this one.
'''

from math import sqrt

class GameObject(object):
    '''
    Constructor takes position (x, y), a sprite image(pygame.Surface), a boolean on whether or not
    the object blocks movement, and a boolean on whether or not the object blocks sight.
    '''
    def __init__(self, (x, y), sprite, block=None, blockSight=None):
        self.position = (self.x, self.y) = (x, y)
        self.size = sprite.get_size()
        self.surface = sprite
        self.block = block
        if blockSight is None: blockSight = block
        self.blockSight = blockSight
        
    '''
    The draw definition draws the sprite surface of this object to the given surface
    '''
    def render(self, surface):
        surface.blit(self.surface, self.position)
            
    '''
    Moves the object by adding changes in x and y.
    '''
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    '''
    Returns the distance from the (x, y) location to this objects location.
    this is all relative to the board blocks, not the pixel locations.
    '''
    def distance(self, x, y):
        return sqrt((x-self.x)**2 + (y-self.y)**2)