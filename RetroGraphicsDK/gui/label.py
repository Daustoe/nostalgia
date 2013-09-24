'''
This is the Label object. It just sets text to the screen with no background.
'''
import element

class Label(element.Element):
    '''
    Label inherits from Element. It takes position (x, y), size (width, height)
    font (pygame.font), text (String), fontColor (red, green, blue) defaults to black.
    '''
    def __init__(self, (x, y), (width, height), font, text, fontColor=(0,0,0)):
        super(Label, self).__init__((x, y), (width, height))
        self.font = font
        self.text = text
        self.fontColor = fontColor
        
    def render(self, window):
        window.blit(self.font.render(self.text, True, self.fontColor), self.position)
        
    def setMaster(self, master):
        super(Label, self).setMaster(master)