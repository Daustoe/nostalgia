import element


class Panel(element.Element):
    """
    The Panel object is a more basic object of the nostalgia gui. It merely holds onto a list of elements which belong
    to it. It sets the position of it's containing elements to be based off of the panel.
    """
    def __init__(self, position, (width, height), color=(200, 200, 200)):
        super(Panel, self).__init__(position, (width, height), color)
        self.elements = []

    def add_element(self, element):
        """
        Adds an element to a Panel. The element is now drawn with its position relative to this panel.
        """
        self.elements.append(element)
        element.set_master(self)

    def remove_element(self, element):
        """
        Removes the element from this Panel.
        """
        self.elements.remove(element)
        element.set_master(None)

    def action_event(self, mouse_press, mouse_position, mouse_movement):
        """
        If there is an action event within this Panel, we hand down that event to all gui elements that belong to this
        Panel.
        """
        for element in self.elements:
            if hasattr(element, 'action_event'):
                element.action_event(mouse_press, mouse_position, mouse_movement)

    def set_master(self, master):
        """
        Elements that belong to a Panel need to also update their position to follow their parent
        """
        super(Panel, self).set_master(master)
        for element in self.elements:
            element.update_position()

    def render(self, window):
        """
        We render this Panel, it may or may not have it's own surface, and then render all elements that belong to this
        Panel.
        """
        super(Panel, self).render(window)
        for element in self.elements:
            if hasattr(element, 'render'):
                element.render(window)