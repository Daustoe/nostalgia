"""
This is the Bar Class. It creates bars that represent information such as health, or mana.  It paints a filled bar
corresponding to a maximum value that it is given. Inherits from the Element class.
"""
import element
import pygame


class Bar(element.Element):
    """
    The constructor takes a position (x, y), size (width, height), a maximum
    value (upper bounds of the bar), a foreground color(filled bar), and a
    background color(empty bar).
    """
    def __init__(self, x, y, width, height, max_value, foreground=(200, 0, 0), background=(200, 200, 200)):
        super(Bar, self).__init__(x, y, width, height, background)
        self.maximum = max_value
        self.value = max_value
        self.percentage = 1.0
        self.fill_color = foreground
        self.filled_bar = pygame.Surface((self.frame.w * self.percentage, self.frame.h))
        self.filled_bar.fill(self.fill_color)

    def set_maximum(self, maximum):
        """ Sets the maximum value (upper bounds) to be maximum. """
        self.maximum = maximum
        if self.value > self.maximum:
            self.value = self.maximum

    def update_value(self, value_change):
        """
        Updates the value of the of the bar with value_change. value_change should be a change such as dx would be.
        """
        self.value += value_change
        if self.value > self.maximum:
            self.value = self.maximum
        elif self.value < 0:
            self.value = 0
        self.percentage = self.value * 1.0 / self.maximum
        self.filled_bar = pygame.Surface((self.frame.w * self.percentage, self.frame.h))
        self.filled_bar.fill(self.fill_color)

    def render(self, window):
        """
        Blits this object to the window. The super class render draws the background
        surface while this render draws only the filled portion of the bar.
        """
        super(Bar, self).render(window)
        window.blit(self.filled_bar, self.position)
