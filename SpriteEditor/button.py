'''
Created on Mar 15, 2012

@author: clayton

need to add action variable to buttons! this is a method of code that is to 
be run when button is clicked
also make the button look like it was clicked when mouse is pressed on it.
'''

import element

class Button(element.Element):
    def __init__(self, position, (width, height), title, font, action, color=(200, 200, 200)):
        super(Button, self).__init__(position, (width, height), color)
        self.font = font
        self.title = title
        self.action = action
        
    def changeColor(self, (r, g, b)):
        self.color = (r, g, b)
        self.surface.fill(self.color)
        
    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        if mousePosition[0] > self.position[0] and mousePosition[0] < self.position[0] + self.size[0]:
            if mousePosition[1] > self.position[1] and mousePosition[1] < self.position[1]+self.size[1]:
                if mousePress[0] and not self.clicked:
                    self.clicked = True
                    self.darken()
                    self.action()
                    #perform action!
                    return True
        if not mousePress[0] and self.clicked: self.lighten()
        self.clicked = False
        #if we get here do not perform action!
        return False
        
    def render(self, window):
        super(Button, self).render(window)
        window.blit(self.font.render(self.title, True, (100, 0, 0)), (self.position[0]+12, self.position[1]))