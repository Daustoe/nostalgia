
import pygame, string, sys

class TextBox(object):
    
    def __init__(self, query, x, y):
        self.query = query + ": "
        self.x = x
        self.y = y
        pygame.font.init()
        self.font = pygame.font.Font(None, 18)
        
    def drawBox(self, window, message):
        pygame.draw.rect(window, (255,255,255), (self.x, self.y, 200, 20), 0)
        pygame.draw.rect(window, (0,0,0), (self.x-2, self.y-2, 204, 24), 1)
        if len(self.query) != 0:
            window.blit(self.font.render(self.query + message, 1, (0,0,0)),(self.x, self.y))
        
    def ask(self, window):
        "ask(screen) -> answer"
        currentString = []
        while True:
            inkey, shift = self.getKey()
            if inkey == pygame.K_BACKSPACE:
                currentString = currentString[0:-1]
            elif inkey == pygame.K_RETURN:
                break
            elif inkey <= 127:
                if shift == True:
                    if inkey == 48:
                        currentString.append(chr(41))
                    elif inkey == 57:
                        currentString.append(chr(40))
                    else:
                        currentString.append(string.upper(chr(inkey)))
                else:
                    currentString.append(chr(inkey))
            self.drawBox(window, string.join(currentString,""))
            pygame.display.flip()
        return string.join(currentString, "")
            
    def getKey(self):
        shift = False
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == 304 or event.key == 303:
                    shift = True
                else:
                    return event.key, shift
            elif event.type == pygame.KEYUP:
                if event.key == 304 or event.key == 303:
                    shift = False
            else:
                pass
            
    def update(self, mpos, mpress):
        if mpos[0] > self.x and mpos[0] < self.x+200:
            if mpos[1] > self.y and mpos[1] < self.y+20:
                if mpress[0]:
                    return True
        