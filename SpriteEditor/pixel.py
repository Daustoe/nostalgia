
import pygame
from constants import RepLocation

class Pixel():
    def __init__(self):
        self.r, self.g, self.b = (None, None, None)
        
    def isNull(self):
        if (self.r, self.g, self.b) == (None, None, None):
            return True
        else:
            return False
        
    def setColor(self, r, g, b):
        self.r, self.g, self.b = (r, g, b)
        
    def getColor(self):
        if self.isNull():
            return (0, 0, 0)
        else:
            return (self.r, self.g, self.b)
    
    def drawMain(self, window, x, y, blockSize):
        if self.isNull():
            nullPixel = pygame.Surface(blockSize)
            nullPixel.fill((255, 255, 255))
            pygame.draw.line(nullPixel, (150, 0, 0), (0, 0), blockSize, 2)
            pygame.draw.line(nullPixel, (150, 0, 0), (blockSize[0], 0), (0, blockSize[1]), 2)
            window.blit(nullPixel, (x*blockSize[0], y*blockSize[1]))
        else:
            window.fill(self.getColor(), (x*blockSize[0], y*blockSize[1], blockSize[0], blockSize[1]))
    
    def drawRepresentation(self, window, x, y, pixelSize):
        if not self.isNull():
            window.fill(self.getColor(), (x+RepLocation[0], y+RepLocation[1], pixelSize[0], pixelSize[1]))
        else:
            nullPixel = pygame.Surface(pixelSize)
            nullPixel.fill((255, 255, 255))
            pygame.draw.line(nullPixel, (150, 0, 0), (0, 0), pixelSize)
            window.blit(nullPixel, (x+RepLocation[0], y+RepLocation[1]))