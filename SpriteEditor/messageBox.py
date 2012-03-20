'''
This is the messageBox object. 
'''
import element, textwrap

class MessageBox(element.Element):
    #MessageBox is constructed with a position (x, y) of where the upper left-hand corner of your
    #messageBox is to be, (width,height) of the box, font of the text within, and a background color
    #in the form of it's (r, g, b) values.
    #Note: font colors are chosen when creating the font with pygame.
    def __init__(self, position, (width, height), font, (r, g, b)):
        super(MessageBox, self).__init__(position, (width, height), (r, g, b))
        self.messages = []
        self.font = font
        self.surface.fill(self.color)
        self.messageBoxHeight = self.height / self.font.size("a")[1]
        
    #addMessage takes a message and a color (defaulted to white) and adds it to the messageBox
    #to be displayed. If there is no room for a new message we remove the oldest message and append
    #our new one to our list of messages. Calculation for how many messages can fit into your message
    #box is done automatically based on the font you chose.
    def addMessage(self, message, color=(255, 255, 255)):
        newMessages = textwrap.wrap(message, self.width-2)
        for line in newMessages:
            if len(self.messages) == self.messageBoxHeight:
                del self.messages[0]
            self.messages.append((line, color))
    
    #render takes a window and blits all current messages in your messageBox object to the screen.
    #This process is handled automatically by the console.
    def render(self, window):
        super(MessageBox, self).render(window)
        y = 0
        for (message, color) in self.messages:
            window.blit(self.font.render(message, True, color), (self.position[0]+2, self.position[1]+y))
            y += self.font.size("a")[1]