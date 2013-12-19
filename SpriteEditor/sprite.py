'''
Sprite object.
'''

import pygame
import element
from pixel import Pixel


class Sprite(element.Element):
    def __init__(self, (x, y), (width, height), pixelSize=(2, 2), pixelsInSprite=(20, 20), pixelArray=[]):
        super(Sprite, self).__init__((x, y), (width, height), (255, 255, 255))
        self.spriteSize = None
        self.pixelArray = pixelArray
        self.pixelSize = pixelSize
        self.pixelsInSprite = pixelsInSprite
        self.blockSize = (self.width / self.pixelsInSprite[0], self.height / self.pixelsInSprite[1])
        self.updateSpriteSize()
        self.surface = pygame.Surface(self.spriteSize)
        for x in range(self.pixelsInSprite[0]):
            self.pixelArray.append([])
            for y in range(self.pixelsInSprite[1]):
                self.pixelArray[x].append(Pixel((x * self.blockSize[0], y * self.blockSize[1]),
                    self.blockSize))
                self.pixelArray[x][y].set_master(self)
        self.colorBox = None

    def updatePixelSize(self, dx, dy):
        self.pixelSize = (self.pixelSize[0] + dx, self.pixelSize[1] + dy)
        self.generateSurface()

    def updateSpriteSize(self):
        self.spriteSize = (self.blockSize[0] * self.pixelsInSprite[0], self.blockSize[1] *
            self.pixelsInSprite[1])

    def generateSurface(self):
        temparray = self.pixelArray
        self.pixelArray = []
        self.updateSpriteSize()
        self.surface = pygame.Surface(self.spriteSize)
        for x in range(self.pixelsInSprite[0]):
            self.pixelArray.append([])
            for y in range(self.pixelsInSprite[1]):
                self.pixelArray[x].append(Pixel((x * self.blockSize[0], y * self.blockSize[1]),
                    self.blockSize, temparray[x][y].get_color()))
                self.pixelArray[x][y].set_master(self)

    def updatePixelCount(self, dx, dy):
        self.pixelsInSprite = (self.pixelsInSprite[0] + dx, self.pixelsInSprite[1] + dy)
        self.blockSize = (self.width / self.pixelsInSprite[0], self.height / self.pixelsInSprite[1])
        if dx == 1:
            self.pixelArray.append([])
            for each in range(self.pixelsInSprite[1]):
                self.pixelArray[self.pixelsInSprite[0] - 1].append(Pixel(((
                    self.pixelsInSprite[0] - 1) * self.blockSize[0], each * self.blockSize[1]),
                    self.blockSize))
        elif dx == -1:
            self.pixelArray.pop()
        if dy == 1:
            for each in range(self.pixelsInSprite[0]):
                self.pixelArray[each].append(Pixel((each * self.blockSize[0], (
                    self.pixelsInSprite[1] - 1) * self.blockSize[1]), self.blockSize))
        elif dy == -1:
            for each in range(self.pixelsInSprite[0]):
                self.pixelArray[each].pop()
        self.generateSurface()

    def makeImage(self):
        imageSurface = pygame.Surface((self.pixelsInSprite[0] * self.pixelSize[0],
            self.pixelsInSprite[1] * self.pixelSize[1]))
        for x in range(self.pixelsInSprite[0]):
            for y in range(self.pixelsInSprite[1]):
                imageSurface.blit(self.pixelArray[x][y].surface.subsurface(pygame.Rect(self.position, self.pixelSize)), (x*self.pixelSize[0], y*self.pixelSize[1]))
        return imageSurface

    def render(self, window):
        for x in range(self.pixelsInSprite[0]):
            for y in range(self.pixelsInSprite[1]):
                self.pixelArray[x][y].render(self.surface)
        super(Sprite, self).render(window)

    def setColorBox(self, colorBox):
        self.colorBox = colorBox

    def setMaster(self, master):
        super(Sprite, self).set_master(master)
        for row in self.pixelArray:
            for each in row:
                each.set_master(self)

    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        if self.colorBox is not None and mousePosition[0] > self.position[0] and mousePosition[0] < self.position[0] + self.size[0]:
            if mousePosition[1] > self.position[1] and mousePosition[1] < self.position[1] + self.size[1]:
                if mousePress[0] and not self.clicked:
                    self.clicked = True
                    x = (mousePosition[0] - self.position[0]) / self.blockSize[0]
                    y = (mousePosition[1] - self.position[1]) / self.blockSize[1]
                    self.pixelArray[x][y].change_color(self.colorBox.get_color())
                elif mousePress[2] and not self.clicked:
                    self.clicked = True
                    x = (mousePosition[0] - self.position[0]) / self.blockSize[0]
                    y = (mousePosition[1] - self.position[1]) / self.blockSize[1]
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, info="right",
                        object=self.pixelArray[x][y]))
        self.clicked = False

    def updatePosition(self):
        super(Sprite, self).update_position()

    def getPixelColor(self, x, y):
        return self.pixelArray[x][y].get_color()