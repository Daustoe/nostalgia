'''
Created on May 14, 2013

@author: Claymore

I want to make a menu sphere, similar to LOL ping spheres for menus. When started as long as the user is holding the inital
start key down, they may move their mouse to select a menu item, when released will select that item. Can also have it stay up after 
activation and have a deactivation key for the menu. Starting with the second idea would most likely be the best idea.

Do I want to have each element hold onto its own sphere menu?? Probably the most efficient way to do it, so if menu element is null,
nothing happens. If that element has a sphere it will display it. Cheers

So, right clicking an element gives us a menu ok. Do I still want an action Event for my menu? I think I do

'''

import element

class Sphere(element.Element):
    def __init__(self):
        super(Sphere, self).__init__()
        
    def actionEvent(self, mousePress, mouseEvent, mouseMovement):
        

