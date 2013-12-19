"""
This is the Label object. It just sets text to the screen with no background.
"""
import core.gui.element


class Label(core.gui.element.Element):
    """
    Label inherits from Element. It takes position (x, y), size (width, height)
    font (pygame.font), text (String), fontColor (red, green, blue) defaults to
    black.
    """
    def __init__(self, (x, y), (width, height), font, text, color=(0, 0, 0)):
        super(Label, self).__init__((x, y), (width, height))
        self.font = font
        self.text = text
        self.font_color = color

    def render(self, window):
        window.blit(self.font.render(self.text, True, self.font_color), self.position)

    def set_master(self, master):
        super(Label, self).set_master(master)