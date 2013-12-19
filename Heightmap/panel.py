'''
Created on Mar 21, 2012

@author: clpowell
'''
import element

class Panel(element.Element):
    def __init__(self, position, (width, height), color=(200,200,200)):
        super(Panel, self).__init__(position, (width, height), color)
        self.elements = []
        
    def addElement(self, element):
        self.elements.append(element)
        element.set_master(self)
        
    def removeElement(self, element):
        self.elements.remove(element)
        element.set_master(None)
        
    def actionEvent(self, mousePress, mousePosition, mouseMovement):
        for element in self.elements:
            if hasattr(element, 'actionEvent'):
                newMouse = (mousePosition[0]-self.position[0], mousePosition[1]-self.position[1])
                element.action_event(mousePress, newMouse, mouseMovement)
                
    def setMaster(self, master):
        self.master = master
        
    def updatePosition(self):
        super(Panel, self).update_position()
        for element in self.elements:
            element.update_position()
                
    def render(self, window):
        for element in self.elements:
            if hasattr(element, 'render'):
                element.render(self.surface)
        super(Panel, self).render(window)