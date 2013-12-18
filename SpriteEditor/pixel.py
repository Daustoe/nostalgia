'''
Pixel object.
'''
import pygame
import element


class Pixel(element.Element):
    """
    Some notes!!!
    perhaps we want render() to draw the outline of each pixel, instead of relying on
    separatePixels() in our sprite object.
    It would make it simpler to manage each 'pixel' of a sprite, and make it easier to see.
    We are also going to want to add actionEvents for each pixel if it is clicked on, in order
    to change the pixels mouse clicks
    """
    def __init__(self, (x, y), (width, height), color=(200, 200, 200)):
        super(Pixel, self).__init__((x, y), (width, height), color)
        self.surface.set_alpha(255)
        self.nullPixel = pygame.Surface(self.size)
        self.nullPixel.fill((255, 255, 255))
        pygame.draw.line(self.nullPixel, (150, 0, 0), (0, 0), self.size, 2)
        pygame.draw.line(self.nullPixel, (150, 0, 0), (self.width, 0), (0, self.height), 2)
        self.clicked = False
        if self.color == (200, 200, 200):
            self.isNull = True
        else:
            self.isNull = False

    def saveColor(self):
        if self.isNull:
            return None
        else:
            return self.color

    def changeColor(self, color):
        if color is None:
            self.isNull = True
        else:
            self.isNull = False
            self.color = color
            self.surface = pygame.Surface(self.size)
            self.surface.fill(self.color)

    def setMaster(self, master):
        super(Pixel, self).set_master(master)

    def updatePosition(self):
        super(Pixel, self).update_position()

    def getColor(self):
        return self.color

    def render(self, window):
        if self.isNull:
            window.blit(self.nullPixel, self.position)
        else:
            window.blit(self.surface, self.position)