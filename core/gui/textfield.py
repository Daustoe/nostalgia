import pygame
import element
import sys


class TextField(element.Element):
    """
    This is a work in progress, it needs a major refactoring.
    """
    def __init__(self, x, y, width, height, font, default_text="", font_color=(0, 0, 0), color=(200, 200, 200)):
        super(TextField, self).__init__(x, y, width, height, (0, 0, 0))
        self.font = font
        self.font_color = font_color
        self.text = default_text
        self.text_surface = pygame.Surface((width - 2, height - 2))
        self.text_surface.fill(color)
        self.surface.blit(self.text_surface, self.position())

    def render(self, window):
        """
        Calls the super Element's render and then draws the text on top of that surface.
        """
        super(TextField, self).render(window)
        window.blit(self.text_surface, self.position())
        window.blit(self.font.render(self.text, True, self.font_color), self.position())

    def action_event(self, mouse_press, mouse_position, mouse_movement):
        """
        Action event for this object
        """
        mouse_left = mouse_position[0] > self.x
        mouse_right = mouse_position[0] < self.x + self.width
        if mouse_left and mouse_right:
            mouse_up = mouse_position[1] > self.y
            mouse_down = mouse_position[1] < self.y + self.height
            if mouse_up and mouse_down:
                if mouse_press[0]:
                    #post a new event that this object is the active Element
                    #event asks for control of event queue until it is not
                    #the active element any longer.
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, object=self))
                    return True
        return False

    def become_active(self, window):
        stop = False
        while not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == 8:
                        self.text = self.text[:-1]
                    elif event.key == 13:
                        stop = True
                    else:
                        self.text += event.unicode
                    self.render(window.window)
                    pygame.display.flip()
                #I feel like this can be refactored to be better
                if event.type == pygame.MOUSEBUTTONDOWN:
                    left = event.pos[0] < self.x
                    right = event.pos[0] > self.x + self.width
                    if left or right:
                        up = event.pos[1] < self.y
                        down = event.pos[1] > self.y + self.height
                        if up or down:
                            stop = True

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            print event