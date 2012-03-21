'''
Created on Mar 21, 2012

@author: clpowell
'''
import element

class Panel(element.Element):
    def __init__(self, position, (width, height), color=(200,200,200)):
        super(Panel, self).__init__(position, (width, height), color)
        #need to figure out what I want to do with this!!