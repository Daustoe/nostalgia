import core.gui.element


class Label(core.gui.element.Element):
    """
    Label inherits from Element. It takes position (x, y), size (width, height) font (pygame.font), text (String),
    fontColor (red, green, blue) defaults to black.
    """
    def __init__(self, (x, y), (width, height), font, text, color=(0, 0, 0)):
        super(Label, self).__init__((x, y), (width, height))
        self.font = font
        self.text = text
        self.font_color = color

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