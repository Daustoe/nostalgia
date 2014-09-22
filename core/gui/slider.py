from element import Element
from pygame import Surface, Rect
from signal import Signal


class Slider(Element):
    """
    This is the Slider class. It is an interface object which has a value tied to a movable slider so that the user can
    change that value. Inherits from the Element class. The constructor takes a position (x, y), size (width, height),
    barColor(r,g,b), sliderColor (r,g,b), and a value which defaults to 0. Index becomes value (pixel index based on
    background surface). The actual value that this object holds onto is a float from 0 to 1.
    """
    def __init__(self, x, y, width, height, bar_color, slider_color, value=0):
        super(Slider, self).__init__(x, y, width, height, bar_color)
        self.slider_frame = Rect(x, y, 20, self.frame.h)
        self.slider = Surface(self.slider_frame.size)
        self.slider_color = slider_color
        self.slider.fill(self.slider_color)
        self.value = 1.0 * value / width
        self.draggable = True
        self.on_mouse_drag = Signal()
        self.on_value_changed = Signal()

    def hit(self, mouse_pos):
        if not self.slider_frame.collidepoint(mouse_pos):
            return None
        else:
            return self

    def mouse_drag(self, view, position, event):
        if view == self:
            delta = event.rel
            self.slider_frame.x = min(self.slider_frame.x + delta[0], self.frame.x + self.frame.w - 20)
            self.slider_frame.x = max(self.slider_frame.x, self.frame.x)
            self.value = 1.0 * (self.slider_frame.x - self.frame.x) / (+ self.frame.w - 20)
            self.on_mouse_drag(position, delta)
            self.on_value_changed()

    def update_position(self):
        super(Slider, self).update_position()
        self.slider_frame = Rect(self.frame.x, self.frame.y, 20, self.frame.h)

    def set_slider(self, index):
        """
        The setIndex definition is self explanatory. It takes a new index, sets it, and updates this objects value.
        """
        self.slider_frame.x = self.frame.x + index
        self.value = 1.0 * self.slider_frame.x / (self.frame.w - 20)
        if self.value > 1.0:
            self.value = 1.0

    def render(self, window):
        """
        The render method draws this object's surface to the window. The super class draws the background while this
        object draws the slider at the correct position.
        """
        super(Slider, self).render(window)
        window.blit(self.slider, self.slider_frame)