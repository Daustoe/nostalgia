'''
Created on Mar 15, 2012

@author: clayton

Console object, built upon pygames console and modified just a bit.
'''

import pygame
from pygame.locals import FULLSCREEN

class Console(object):
    
    #Constructor method
    def __init__(self, width, height, isFullscreen=False):
        pygame.init()
        '''size is the size of our window'''
        self.size = (width, height)
        self.isFullscreen = isFullscreen
        self.activeElement = None
        
        '''this initializes our window with size whatever options the user has set.'''
        self.window = pygame.display.set_mode(self.size)
        
        '''elements is the list of GUI elements that are being drawn onto our window'''
        self.elements = []
    
    '''blits all of the consoles elements to the screen'''
    def drawElements(self):
        for each in self.elements:
            if hasattr(each, 'render'):
                each.render(self.window)
        pygame.display.flip()
        
    '''for elements that have actions (i.e. buttons, sliders, things you can click
    check mouse information to see if said element needs to perform its action!
    '''
    def handleElementActions(self):
        mousePress = pygame.mouse.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        mouseMovement = pygame.mouse.get_rel()
        for each in self.elements:
            if hasattr(each, 'actionEvent'):
                each.actionEvent(mousePress, mousePosition, mouseMovement)
                        
    '''adds an element to the consoles list of elements to draw.'''
    def addElement(self, element):
        self.elements.append(element)
        
    def setCaption(self, caption):
        pygame.display.set_caption(caption)
        
    '''Removes element from the consoles, list of elements to draw.'''
    def removeElement(self, element):
        self.elements.remove(element)
        
    '''changes the dimensions of the window'''
    def changeDimensions(self, width, height):
        self.size = (width, height)
        self.window = pygame.display.set_mode(self.size)
        
    '''Set's the window to be fullscreen'''
    def toggleFullscreen(self):
        screen = pygame.display.get_surface()
        tmp = screen.convert()
        caption = pygame.display.get_caption()
        cursor = pygame.mouse.get_cursor()
        
        width, height = screen.get_width(), screen.get_height()
        flags = screen.get_flags()
        bits = screen.get_bitsize()
        
        pygame.display.quit()
        pygame.display.init()
        
        screen = pygame.display.set_mode((width, height), flags^FULLSCREEN, bits)
        screen.blit(tmp, (0,0))
        pygame.display.set_caption(*caption)
        
        pygame.key.set_mods(0)
        pygame.mouse.set_cursor(*cursor)
        self.window = screen
        return self.window
        