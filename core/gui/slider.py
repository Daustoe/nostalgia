"""
This is the Slider class. It is an interface object which has a value tied to a
movable slider so that the user can change that value. Inherits from the Element
class.
"""

import core.gui.element
import pygame


class Slider(core.gui.element.Element):
    """
    The constructor takes a position (x, y), size (width, height), barColor(r,g,b), sliderColor (r,g,b), and a value
    which defaults to 0. Index becomes value (pixel index based on background surface). The actual value that this
    object holds onto is a float from 0 to 1.
    """

    def __init__(self, position, (width, height), bar_color, slider_color, value=0):
        super(Slider, self).__init__(position, (width, height), bar_color)
        self.slider = pygame.Surface((20, self.height))
        self.slider_color = slider_color
        self.slider.fill(self.slider_color)
        self.index = value
        self.value = 1.0 * value / width
        self.action = True

    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        """
        actionEvent is the definition that handles what to do if the user interacts with this object with the mouse.
        This method should only be called by the console object.
        """
        if mousePress[0]:
            mouseLeft = mousePosition[0] > self.position[0] + self.index
            mouseRight = mousePosition[0] < self.position[0] + self.index + 20
            if mouseLeft and mouseRight:
                mouseUp = mousePosition[1] > self.position[1]
                mouseDown = mousePosition[1] < self.position[1] + self.height
                if mouseUp and mouseDown:
                    self.clicked = True
        elif not mousePress[0]:
            self.clicked = False
        if self.clicked:
            self.index += mouseMovement[0]
            self.value = 1.0 * self.index / (self.width - 20)
        if self.index < 0:
            self.index = 0
            self.value = 0.0
        if self.index > self.width - 20:
            self.index = self.width - 20
            self.value = 1.0

    '''
    The setIndex definition is self explanatory. It takes a new index, sets it,
    and updates this objects value.
    '''

    def setIndex(self, index):
        self.index = index
        self.value = 1.0 * self.index / (self.width - 20)
        if self.value > 1.0:
            self.value = 1.0

    '''
    The render method blits this object's surface to the window. The super class
    draws the background while this object draws the slider at the correct
    position.
    '''

    def render(self, window):
        super(Slider, self).render(window)
        position = (self.position[0] + self.index, self.position[1])
        window.blit(self.slider, position)
