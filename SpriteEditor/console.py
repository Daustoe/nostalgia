'''
Console object, built upon pygames console and modified just a bit. Takes the width, 
height, and isFullscreen boolean as arguments. 
The main benefit of this object is that it is set up to automatically handle rendering
and actionEvent handling of gui objects which inherit from the Element object.
'''

import pygame
from pygame.locals import FULLSCREEN

class Console(object):
    def __init__(self, width, height, isFullscreen=False):
        pygame.init()
        self.size = (width, height)
        self.isFullscreen = isFullscreen
        self.activeElement = None
        self.position = (0, 0)
        self.window = pygame.display.set_mode(self.size)
        self.elements = []
    
    '''
    Renders all of the consoles elements to the screen in the elements list to the
    window
    '''
    def drawElements(self):
        for each in self.elements:
            if hasattr(each, 'render'):
                each.render(self.window)
        
    '''
    For elements that have actions (i.e. buttons, sliders, things you can click)
    call the actionEvent method (inherited from the Element object) on that object
    and send it all current relevent mouse information.
    '''
    def handleElementActions(self):        
        if pygame.event.peek():
            mousePress = pygame.mouse.get_pressed()
            mousePosition = pygame.mouse.get_pos()
            mouseMovement = pygame.mouse.get_rel()
            for each in self.elements:
                if hasattr(each, 'actionEvent'):
                    each.action_event(mousePress, mousePosition, mouseMovement)
                        
    '''
    Adds an element to the consoles list of elements to draw.
    '''
    def addElement(self, element):
        if element.__module__ == "messageBox":
            self.messageBoxList.append(element)
        else:
            self.elements.append(element)
        element.set_master(self)
        
    '''
    Sets the caption of the window.
    '''
    def setCaption(self, caption):
        pygame.display.set_caption(caption)
        
    '''
    Removes element from the list of console elements to draw.
    '''
    def removeElement(self, element):
        self.elements.remove(element)
        element.set_master(None)
        
    '''
    Changes the dimensions of the window
    '''
    def changeDimensions(self, width, height):
        self.size = (width, height)
        self.window = pygame.display.set_mode(self.size)
        
    '''
    Toggles between fullscreen and windowed mode for our window, depending on how you set
    up your gui, this has the potential to blow things around on the screen.
    '''
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
        