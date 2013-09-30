'''
This is the Bar Class. It creates bars that represent information such as
health, or mana.  It paints a filled bar corresponding to a maximum value that
it is given. Inherits from the Element class.
'''
import element
import pygame


class Bar(element.Element):
    '''
    The constructor takes a position (x, y), size (width, height), a maximum
    value (upper bounds of the bar), a foreground color(filled bar), and a
    background color(empty bar).
    '''
    def __init__(self, (x, y), (width, height), maxValue,
            foreground=(200, 0, 0), background=(200, 200, 200)):
        super(Bar, self).__init__((x, y), (width, height), background)
        self.maximum = maxValue
        self.value = maxValue
        self.percentage = 1.0
        self.fillColor = foreground
        self.filledBar = pygame.Surface(
            (self.width * self.percentage, self.height))
        self.filledBar.fill(self.fillColor)

    '''
    Sets the maximum value (upper bounds) to be maximum.
    '''
    def setMaximum(self, maximum):
        self.maximum = maximum
        if self.value > self.maximum:
            self.value = self.maximum

    '''
    Updates the value of the of the bar with valueChange. valueChange should be
     a change such as dx would be.
    '''
    def updateValue(self, valueChange):
        self.value += valueChange
        if self.value > self.maximum:
            self.value = self.maximum
        elif self.value < 0:
            self.value = 0
        self.percentage = self.value * 1.0 / self.maximum
        self.filledBar = pygame.Surface(
            (self.width * self.percentage, self.height))
        self.filledBar.fill(self.fillColor)

    '''
    Blits this object to the window. The super class render draws the background
    surface while this render draws only the filled portion of the bar.
    '''
    def render(self, window):
        super(Bar, self).render(window)
        window.blit(self.filledBar, self.position)
