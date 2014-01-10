"""
To Do:
    Give buttons a visual for when they are clicked.
    add doc strings
"""

import element


class Button(element.Element):
    def __init__(self, position, (width, height), title, font, action, font_color=(100, 0, 0), color=(200, 200, 200)):
        super(Button, self).__init__(position, (width, height), color)
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
            mouse_left = mouse_position[0] > self.position[0]
            mouse_right = mouse_position[0] < self.position[0] + self.size[0]
            if mouse_left and mouse_right:
                mouse_up = mouse_position[1] > self.position[1]
                mouse_down = mouse_position[1] < self.position[1] + self.size[1]
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
        x_pos = (self.position[0] + self.width / 2)
        x_pos -= self.font.size(self.title)[0] / 2
        y_pos = (self.position[1] + self.height / 2)
        y_pos -= self.font.size(self.title)[1] / 2
        return x_pos, y_pos