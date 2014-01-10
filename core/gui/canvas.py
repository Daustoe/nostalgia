"""
The Canvas object can be thought of as the actual game board that represents
actual characters and the environment of your game. Inherits from the Element
object.
"""
import element


class Canvas(element.Element):
    """
    Constructor takes position (x, y) and (width, height). (x, y) is the upper
    left-hand corner display is an array of items to be displayed on our canvas,
    it makes up the background. DisplayType holds onto if
    """
    def __init__(self, position, (width, height), (r, g, b)=(0, 0, 0), display_type=True, display=[]):
        super(Canvas, self).__init__(position, (width, height), (r, g, b))
        self.display = display
        self.display_type = display_type

    def render(self, window):
        """ render() is used to display the canvas on the screen. Automated by the Console object. """
        super(Canvas, self).render(window)
        for each in self.display:
            self.surface.blit(each.surface, each.position)
        window.blit(self.surface, self.position)