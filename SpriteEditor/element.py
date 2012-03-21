'''
Created on Mar 15, 2012

@author: clayton
'''
import pygame

class Element(object):
    def __init__(self, position, (width, height), color=(200, 200, 200)):
        super(Element, self).__init__()
        self.position = position
        self.size = (self.width, self.height) = (width, height)
        self.surface = pygame.Surface(self.size)
        self.color = color
        self.surface.fill(color)
        
    def render(self, window):
        window.blit(self.surface, self.position)
        
    def lighten(self):
        '''nothing yet'''
        
    def darken(self):
        '''darken the color by some degree'''
        