
import pygame
from pixel import Pixel

class Sprite():
    def __init__(self, pixelSize, pixelsInSprite):
        self.pixelArray = []
        self.pixelSize = pixelSize
        self.pixelsInSprite = pixelsInSprite
        self.blockSize = (540/self.pixelsInSprite[0], 520/self.pixelsInSprite[1])

        for x in range(self.pixelsInSprite[0]):
            self.pixelArray.append([])
            for y in range(self.pixelsInSprite[1]):
                self.pixelArray[x].append(Pixel())
    
    def drawSpriteMain(self, window):
        self.blockSize = (540/self.pixelsInSprite[0], 520/self.pixelsInSprite[1])
        for x in range(self.pixelsInSprite[0]):
            for y in range(self.pixelsInSprite[1]):
                self.pixelArray[x][y].drawMain(window, x, y, self.blockSize)
        self.separatePixels(window)
        
    def drawSpriteRepresentation(self, window):
        xx = self.pixelsInSprite[0]*self.pixelSize[0]
        yy = self.pixelsInSprite[1]*self.pixelSize[1]
        pygame.draw.rect(window, (0, 0, 0), (545-1, RepLocation[1]-1, xx+2,yy+2))
        for x in range(self.pixelsInSprite[0]):
            for y in range(self.pixelsInSprite[1]):
                self.pixelArray[x][y].drawRepresentation(window, x*self.pixelSize[0], y*self.pixelSize[1], self.pixelSize)
        
    def setPixelColor(self, window, x, y, (r, g, b)):
        self.pixelArray[x][y].setColor(r, g, b)
        
    def getPixelColor(self, x, y):
        return self.pixelArray[x][y].getColor()
        
    def separatePixels(self, window):
        for x in range(1, self.pixelsInSprite[0] + 1):
            pygame.draw.line(window, (0, 0, 0), (x*self.blockSize[0], 0), (x*self.blockSize[0], 520))
        for y in range(1, self.pixelsInSprite[1]):
            pygame.draw.line(window, (0, 0, 0), (0, y*self.blockSize[1]), (540, y*self.blockSize[1]))
