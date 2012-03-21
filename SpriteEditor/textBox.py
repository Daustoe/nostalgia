
import pygame, element, sys

class TextBox(element.Element):
    
    def __init__(self, position, (width, height), font, defaultText="", fontColor=(0,0,0), color=(200, 200, 200)):
        super(TextBox, self).__init__(position, (width, height), (0, 0, 0))
        self.font = font
        self.fontColor = fontColor
        self.text = defaultText
        self.textSurface = pygame.Surface((width-2, height-2))
        self.textSurface.fill(color)
        self.surface.blit(self.textSurface, (self.position[0]+1, self.position[1]+1))
        
    def render(self, window):
        super(TextBox, self).render(window)
        window.blit(self.textSurface, (self.position[0]+1, self.position[1]+1))
        window.blit(self.font.render(self.text, True, self.fontColor), (self.position[0]+1, self.position[1]+1))
        
    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        if mousePosition[0] > self.position[0] and mousePosition[0] < self.position[0] + self.size[0]:
            if mousePosition[1] > self.position[1] and mousePosition[1] < self.position[1]+self.size[1]:
                if mousePress[0] and not self.clicked:
                    #post a new event that this object is the active Element
                    #event asks for control of event queue until it is not
                    #the active element any longer.
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, object=self))
                    return True
        return False
            
    def becomeActive(self, window):
        quit = False
        while not quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == 8:
                        self.text = self.text[:-1]
                    elif event.key == 13:
                        quit = True
                    else:
                        self.text += event.unicode
                    self.render(window.window)
                    pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] < self.position[0] or event.pos[0] > self.position[0] + self.size[0]:
                        if event.pos[1] < self.position[1] or event.pos[1] > self.position[1]+self.size[1]:
                            quit = True
                   
    def update(self, event):
        if event.type == pygame.KEYDOWN:
            print event
        
        