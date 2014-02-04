import element
import pygame.color


class Label(element.Element):
    """
    Label inherits from Element. It takes position (x, y), size (width, height) font (pygame.font), text (String),
    fontColor (red, green, blue) defaults to black.
    """
    def __init__(self, x, y, width, height, font, text, red=0, green=0, blue=0):
        super(Label, self).__init__(x, y, width, height)
        self.font = font
        self.text = text
        self.font_color = pygame.color.Color(red, green, blue)

    def render(self, window):
        """
        Overrides the render function of the Element class. Draws the text to the screen.
        """
        window.blit(self.font.render(self.text, True, self.font_color), self.position)

    def set_master(self, master):
        """
        Calls the Element set_master function.
        """
        super(Label, self).set_master(master)