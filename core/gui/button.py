"""
To Do:
    Give buttons a visual for when they are clicked.
    add doc strings
"""

from element import Element
from pygame.color import Color


class Button(Element):
    def __init__(self, x, y, width, height, title, font, action, font_color=Color('black'), color=Color('gray')):
        super(Button, self).__init__(x, y, width, height, color)
        self.font = font
        self.title = title
        self.action = action
        self.font_color = font_color
        self.clicked = False
        (x_pos, y_pos) = self.calculate_position()
        self.title_position = (x_pos, y_pos)

    def change_color(self, (r, g, b)):
        self.color = (r, g, b)
        self.surface.fill(self.color)

    def action_event(self, mouse_press, mouse_position, mouse_movement):
        if mouse_press[0] and not self.clicked:
            mouse_left = mouse_position[0] > self.x
            mouse_right = mouse_position[0] < self.x + self.width
            if mouse_left and mouse_right:
                mouse_up = mouse_position[1] > self.y
                mouse_down = mouse_position[1] < self.y + self.height
                if mouse_up and mouse_down:
                    self.clicked = True  # self.darken()
                    self.action()
        #if not mouse_press[0] and self.clicked: self.lighten()
        elif not mouse_press[0]:
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
        x_pos = (self.x + self.width / 2)
        x_pos -= self.font.size(self.title)[0] / 2
        y_pos = (self.y + self.height / 2)
        y_pos -= self.font.size(self.title)[1] / 2
        return x_pos, y_pos