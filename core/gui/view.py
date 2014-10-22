from element import Element
from pygame import Color


class View(Element):
    """
    The View object is a more basic object of the nostalgia gui. It merely holds onto a list of elements which belong
    to it. It sets the position of it's containing elements to be based off of the panel.
    """
    def __init__(self, x, y, width, height, color=Color('gray')):
        super(View, self).__init__(x, y, width, height, color)
        self.children = []

    def add(self, element):
        """
        Adds an element to a View. The element is now drawn with its position relative to this panel.
        """
        self.children.append(element)
        element.set_parent(self)

    def remove(self, element):
        """
        Removes the element from this View.
        """
        self.children.remove(element)
        element.set_parent(None)

    def action_event(self, mouse_press, mouse_position, mouse_movement):
        """
        If there is an action event within this View, we hand down that event to all gui elements that belong to this
        View.
        """
        for element in self.children:
            if hasattr(element, 'action_event'):
                element.action_event(mouse_press, mouse_position, mouse_movement)

    def hit(self, mouse_pos):
        if self.hidden:
            return None
        if not self.frame.collidepoint(mouse_pos):
            return None

        for child in reversed(self.children):   # front to back
            hit_view = child.hit(mouse_pos)
            if hit_view is not None:
                return hit_view

        return self

    def set_parent(self, parent):
        """
        Elements that belong to a View need to also update their position to follow their parent
        """
        super(View, self).set_parent(parent)
        for element in self.children:
            element.update_position()

    def render(self, window):
        """
        We render this View, it may or may not have it's own surface, and then render all elements that belong to this
        View.
        """
        super(View, self).render(window)
        for element in self.children:
            if hasattr(element, 'render'):
                element.render(window)