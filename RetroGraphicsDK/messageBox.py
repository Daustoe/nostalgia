'''
This is the messageBox object. Holds onto a list of messages sent to it sized
depending on how large the messageBox itself is. When render is called, it prints
them onto the surface of the box.
'''
import element, textwrap

class MessageBox(element.Element):
    '''
    MessageBox is constructed with a position (x, y) of where the upper left-hand corner of your
    messageBox is to be, (width,height) of the box, font of the text within, and a background color
    in the form of it's (r, g, b) values. It inherits from the Element abstract class.
    '''
    def __init__(self, position, (width, height), font, color=(0, 0, 0)):
        super(MessageBox, self).__init__(position, (width, height), color)
        self.messages = []
        self.font = font
        self.surface.fill(self.color)
        self.messageBoxHeight = self.height / self.font.size("a")[1]
    
    '''    
    The addMessage definition takes a string message and a color (defaulted to white) as arguments
    and adds it to the list of messages to be displayed. If there is no room for a new message we 
    remove the oldest message and append our new one to our list of messages. Calculation for how 
    many messages can fit into your message box is done automatically based on the font you chose.
    '''
    def addMessage(self, message, color=(255, 255, 255)):
        newMessages = textwrap.wrap(message, self.width-2)
        for line in newMessages:
            if len(self.messages) == self.messageBoxHeight:
                del self.messages[0]
            self.messages.append((line, color))
    
    '''
    The render definition takes a surface as an argument and renders all current messages in your 
    messageBox object to the screen.
    This process is handled automatically by the console.
    '''
    def render(self, window):
        super(MessageBox, self).render(window)
        messageOffset = 0
        for (message, color) in self.messages:
            window.blit(self.font.render(message, True, color), (self.position[0]+2, self.position[1]+messageOffset))
            messageOffset += self.font.size("a")[1]