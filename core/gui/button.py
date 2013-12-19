"""
Created on Mar 15, 2012

@author: clayton

To Do:
    Give buttons a visual for when they are clicked.
    add doc strings
"""

import core.gui.element


class Button(core.gui.element.Element):
    def __init__(self, position, (width, height), title, font, action, font_color=(100, 0, 0), color=(200, 200, 200)):
        super(Button, self).__init__(position, (width, height), color)
        self.font = font
        self.title = title
        self.action = action
        self.font_color = font_color
        self.clicked = False
        (xPos, yPos) = self.calculate_position()
        self.title_position = (xPos, yPos)

    def change_color(self, (r, g, b)):
        self.color = (r, g, b)
        self.surface.fill(self.color)

    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        if mousePress[0] and not self.clicked:
            mouseLeft = mousePosition[0] > self.position[0]
            mouseRight = mousePosition[0] < self.position[0] + self.size[0]
            if mouseLeft and mouseRight:
                mouseUp = mousePosition[1] > self.position[1]
                mouseDown = mousePosition[1] < self.position[1] + self.size[1]
                if mouseUp and mouseDown:
                    self.clicked = True  # self.darken()
                    self.action()
        #if not mousePress[0] and self.clicked: self.lighten()
        elif not mousePress[0]:
            self.clicked = False

    def set_master(self, master):
        super(Button, self).set_master(master)

    def update_position(self):
        super(Button, self).update_position()
        self.title_position = self.calculate_position()

    def render(self, window):
        super(Button, self).render(window)
        window.blit(self.font.render(self.title, True, self.font_color), self.title_position)

    def calculate_position(self):
        """ Calculates actual position of the button on the Panel. """
        xPos = (self.position[0] + self.width / 2)
        xPos -= self.font.size(self.title)[0] / 2
        yPos = (self.position[1] + self.height / 2)
        yPos -= self.font.size(self.title)[1] / 2
        return (xPos, yPos)