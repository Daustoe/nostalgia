'''
Created on Mar 21, 2012

@author: clpowell
'''
import element


class Panel(element.Element):
    def __init__(self, position, (width, height), color=(200, 200, 200)):
        super(Panel, self).__init__(position, (width, height), color)
        self.elements = []

    def addElement(self, element):
        self.elements.append(element)
        element.setMaster(self)

    def removeElement(self, element):
        self.elements.remove(element)
        element.setMaster(None)

    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        for element in self.elements:
            if hasattr(element, 'actionEvent'):
                element.actionEvent(mousePress, mousePosition, mouseMovement)

    def render(self, window):
        super(Panel, self).render(window)
        for element in self.elements:
            if hasattr(element, 'render'):
                element.render(window)