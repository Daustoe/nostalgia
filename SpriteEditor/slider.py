'''
Created on Mar 16, 2012

@author: clayton
'''

import element, pygame

class Slider(element.Element):
    def __init__(self, position, (width, height), barColor, sliderColor, value=0):
        super(Slider, self).__init__(position, (width, height), barColor)
        self.slider = pygame.Surface((20, self.height))
        self.sliderColor = sliderColor
        self.slider.fill(self.sliderColor)
        self.index = value
        self.value = 1.0*value/width
        self.action = True
        
    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        if mousePress[0]:
            if (mousePosition[0] > (self.position[0]+self.index)) and (mousePosition[0] < (self.position[0]+self.index)+20):
                if mousePosition[1] > self.position[1] and mousePosition[1] < self.position[1] + self.height:
                    self.clicked = True
        elif not mousePress[0]:
            self.clicked = False
        if self.clicked:
            self.index += mouseMovement[0]
            self.value = 1.0*self.index/(self.width-20)
        if self.index < 0: 
            self.index = 0
            self.value = 0.0
        if self.index > self.width-20: 
            self.index = self.width-20
            self.value = 1.0
            
    def setIndex(self, index):
        self.index = index
        self.value = 1.0*self.index/(self.width-20)
        if self.value > 1.0:
            self.value = 1.0
        
    def render(self, window):
        super(Slider, self).render(window)
        window.blit(self.slider, (self.position[0]+self.index, self.position[1]))
