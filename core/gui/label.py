from element import Element
from pygame.color import Color


class Label(Element):
    """
    Label inherits from Element. It takes position (x, y), size (width, height) font (pygame.font), text (String),
    fontColor (red, green, blue) defaults to black.
    """
    def __init__(self, x, y, width, height, font, text, color=Color('0xffffff'), font_color=Color('0x000000')):
        super(Label, self).__init__(x, y, width, height, color)
        self.font = font
        self.text = text
        self.font_color = font_color

    def update_text(self, text):
        self.text = text

    def render(self, window):
        """
        Overrides the render function of the Element class. Draws the text to the screen.
        """
        super(Label, self).render(window)
        window.blit(self.font.render(self.text, True, self.font_color), self.position())