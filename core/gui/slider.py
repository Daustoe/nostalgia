from element import Element
import pygame


class Slider(Element):
    """
    This is the Slider class. It is an interface object which has a value tied to a movable slider so that the user can
    change that value. Inherits from the Element class. The constructor takes a position (x, y), size (width, height),
    barColor(r,g,b), sliderColor (r,g,b), and a value which defaults to 0. Index becomes value (pixel index based on
    background surface). The actual value that this object holds onto is a float from 0 to 1.
    """
    def __init__(self, x, y, width, height, bar_color, slider_color, value=0):
        super(Slider, self).__init__(x, y, width, height, bar_color)
        self.slider = pygame.Surface((20, self.frame.h))
        self.slider_color = slider_color
        self.slider.fill(self.slider_color)
        self.index = value
        self.value = 1.0 * value / width
        self.action = True

    def action_event(self, mouse_press, mouse_position, mouse_movement):
        """
        actionEvent is the definition that handles what to do if the user interacts with this object with the mouse.
        This method should only be called by the console object.
        """
        if mouse_press[0]:
            mouse_left = mouse_position[0] > self.frame.x + self.index
            mouse_right = mouse_position[0] < self.frame.x + self.index + 20
            if mouse_left and mouse_right:
                mouse_up = mouse_position[1] > self.frame.y
                mouse_down = mouse_position[1] < self.frame.y + self.frame.h
                if mouse_up and mouse_down:
                    self.clicked = True
        elif not mouse_press[0]:
            self.clicked = False
        if self.clicked:
            self.index += mouse_movement[0]
            self.value = 1.0 * self.index / (self.frame.w - 20)
        if self.index < 0:
            self.index = 0
            self.value = 0.0
        if self.index > self.frame.w - 20:
            self.index = self.frame.w - 20
            self.value = 1.0

    def set_value(self, value):
        """
        Sets the value of the bar location. Float between 0 and 1, 1 representing full and 0 empty.
        """
        if value >= 1.0:
            self.value = 1.0
        elif value <= 0.0:
            self.value = 0.0
        else:
            self.value = value

    def set_index(self, index):
        """
        The setIndex definition is self explanatory. It takes a new index, sets it, and updates this objects value.
        """
        self.index = index
        self.value = 1.0 * self.index / (self.frame.w - 20)
        if self.value > 1.0:
            self.value = 1.0

    def render(self, window):
        """
        The render method draws this object's surface to the window. The super class draws the background while this
        object draws the slider at the correct position.
        """
        super(Slider, self).render(window)
        position = (self.frame.x + self.index, self.frame.y)
        window.blit(self.slider, position)