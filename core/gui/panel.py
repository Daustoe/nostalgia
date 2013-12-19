"""
Created on Mar 21, 2012

@author: clpowell
"""
import core.gui.element


class Panel(core.gui.element.Element):
    def __init__(self, position, (width, height), color=(200, 200, 200)):
        super(Panel, self).__init__(position, (width, height), color)
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)
        element.set_master(self)

    def remove_element(self, element):
        self.elements.remove(element)
        element.set_master(None)

    def action_event(self, mouse_press, mouse_position, mouse_movement):
        for element in self.elements:
            if hasattr(element, 'actionEvent'):
                element.action_event(mouse_press, mouse_position, mouse_movement)

    def render(self, window):
        super(Panel, self).render(window)
        for element in self.elements:
            if hasattr(element, 'render'):
                element.render(window)