"""
To Do:
    Give buttons a visual for when they are clicked.
    add doc strings
"""

from label import Label
from pygame.color import Color


class Button(Label):
    def __init__(self, x, y, width, height, text, font, action, font_color=Color('black'), color=Color('gray')):
        super(Button, self).__init__(x, y, width, height, font, text, color, font_color)
        self.action = action
        self.clicked = False

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
                    self.clicked = True
                    self.action()
        elif not mouse_press[0]:
            self.clicked = False

    def set_parent(self, master):
        super(Button, self).set_parent(master)

    def update_position(self):
        super(Button, self).update_position()