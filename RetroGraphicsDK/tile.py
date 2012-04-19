'''
Created on Apr 18, 2012

@author: Claymore
'''
import pygame, gameObject

class Tile(gameObject.GameObject):
    def __init__(self, (x, y), (width, height), block, color=(200,200,200), sprite=None, blockSight=None):
        if sprite == None: 
            sprite = pygame.Surface((width, height))
            self.color = color
            sprite.fill(self.color)
        self.size = sprite.get_size()
        super(Tile, self).__init__((x*self.size[0], y*self.size[1]), sprite, block, blockSight)
        self.explored = False
        
    def setColor(self, (r,g,b)):
        self.color = (r,g,b)
        self.surface.fill(self.color)
                
    def isBlocked(self):
        return self.blocked