'''
Created on Apr 11, 2012

@author: Claymore
'''
import element
import pygame
import sys


class Menu(element.Element):
    def __init__(self, (x, y), (width, height), font, fontColor=(255, 255, 255),
            title="", color=(100, 100, 100)):
        super(Menu, self).__init__((x, y), (width, height), color)
        self.font = font
        self.title = title
        self.fontColor = fontColor
        self.isOpen = False
        self.titlePosition = ((self.position[0] + self.width / 2) -
                               self.font.size(self.title)[0] / 2, 2)
        self.titleSize = self.font.size(self.title)
        self.optionList = None
        self.resetSurface()

    def open(self, optionList):
        '''
        we want to blit the optionList strings to the surface of the window! in
        some order that makes sense visually. Also want to send a message to the
        console to give all input data (keyboard mouse and such) to this object.
        Should block out all other elements data handling. (much the same as the
        textbox).
        '''
        self.optionList = optionList
        headerHeight = self.titleSize[1]  # height of our title

        letterIndex = ord('a')
        index = 0
        for each in optionList:
            text = '(' + chr(letterIndex) + ')' + each
            self.surface.blit(self.font.render(text, True, self.fontColor),
                (15, headerHeight + index * self.font.size(text)[1]))
            letterIndex += 1
            index += 1
        self.isOpen = True
        super(Menu, self).render(self.master.window)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    break
                if event.type == pygame.KEYUP:
                    if event.key >= 97 and event.key <= 122:
                        index = event.key - 97
                        if index >= 0 and index < len(self.optionList):
                            self.isOpen = False
                            self.resetSurface()
                            return index

    def render(self, window):
        return None

    def resetSurface(self):
        self.surface = pygame.Surface(self.size)
        self.surface.blit(self.font.render(self.title, True, self.fontColor),
            self.titlePosition)
        pointList = [(self.titlePosition[0] - 2, self.titleSize[1] / 2)]
        pointList.append((self.titleSize[1] / 2, self.titleSize[1] / 2))
        pointList.append((self.titleSize[1] / 2,
                          self.height - self.titleSize[1] / 2))
        pointList.append((self.width - self.titleSize[1] / 2,
                          self.height - self.titleSize[1] / 2))
        pointList.append((self.width - self.titleSize[1] / 2,
                          self.titleSize[1] / 2))
        pointList.append((self.titlePosition[0] + self.titleSize[0] + 2,
                          self.titleSize[1] / 2))
        pygame.draw.lines(self.surface, self.fontColor, False, pointList, 3)