'''
Created on Mar 15, 2012

@author: clayton

also make the button look like it was clicked when mouse is pressed on it.
'''

import element

class Button(element.Element):
    def __init__(self, position, (width, height), title, font, action, fontColor=(100,0,0), color=(200, 200, 200)):
        super(Button, self).__init__(position, (width, height), color)
        self.font = font
        self.title = title
        self.action = action
        self.fontColor = fontColor
        self.clicked = False
        self.titlePosition = ((self.position[0]+self.width/2)-self.font.size(self.title)[0]/2, (self.position[1]+self.height/2)-self.font.size(self.title)[1]/2)
        
    def changeColor(self, (r, g, b)):
        self.color = (r, g, b)
        self.surface.fill(self.color)
        
    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        if mousePress[0] and not self.clicked:
            if mousePosition[0] > self.position[0] and mousePosition[0] < self.position[0] + self.size[0]:
                if mousePosition[1] > self.position[1] and mousePosition[1] < self.position[1]+self.size[1]:
                    self.clicked = True
                    #self.darken()
                    self.action()
                    return True
        #if not mousePress[0] and self.clicked: self.lighten()
        self.clicked = False
        return False
    
    def setMaster(self, master):
        super(Button, self).set_master(master)
    
    def updatePosition(self):
        super(Button, self).update_position()
        self.titlePosition = ((self.position[0]+self.width/2)-self.font.size(self.title)[0]/2, (self.position[1]+self.height/2)-self.font.size(self.title)[1]/2)
        
    def render(self, window):
        super(Button, self).render(window)
        window.blit(self.font.render(self.title, True, self.fontColor), self.titlePosition)