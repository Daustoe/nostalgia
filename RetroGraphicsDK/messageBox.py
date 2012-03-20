'''
Created on Mar 16, 2012

@author: clayton
'''
import element, textwrap

class MessageBox(element.Element):
    def __init__(self, position, (width, height), font, (r, g, b)):
        super(MessageBox, self).__init__(position, (width, height), (r, g, b))
        self.messages = []
        self.font = font
        self.surface.fill(self.color)
        self.messageBoxHeight = self.height / self.font.size("a")[1]
        
    def addMessage(self, message, color=(255, 255, 255)):
        newMessages = textwrap.wrap(message, self.width-2)
        for line in newMessages:
            if len(self.messages) == self.messageBoxHeight:
                del self.messages[0]
            self.messages.append((line, color))
        
    def render(self, window):
        super(MessageBox, self).render(window)
        y = 0
        for (message, color) in self.messages:
            window.blit(self.font.render(message, True, color), (self.position[0]+2, self.position[1]+y))
            y += self.font.size("a")[1]