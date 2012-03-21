'''
Created on Mar 20, 2012

@author: clpowell
'''

'''
Created on Mar 15, 2012

@author: clayton

Issue List for whole of development kit

--make mouseReporter (mouseover reporter for elements on our console)
--make textBox
--make pathfinding algorithm
--make field of view algorithm
    -perhaps a few of these
--random dungeon generator
--basic class structures of game Objects
--heightmap stuff for above ground map generation
--make gameCanvas (main display of game)
'''
import console, pygame, sys, button, messageBox, slider
from pygame.locals import *

def buttonAction():
    print "Button works"
    

window = console.Console(600, 600)
font = pygame.font.SysFont('ubuntu', 18, bold=True)
firstButton = button.Button((10, 10), (80, 20), "Hello World", font, buttonAction)
slider = slider.Slider((10, 300), (275, 15), (255, 200, 200), (255, 0, 0))
messageBox = messageBox.MessageBox((10, 50), (200, 150), font, (0, 255, 0))
window.addElement(firstButton)
window.addElement(messageBox)
window.addElement(slider)



quit = False
while not quit:
    window.drawElements()
    window.handleElementActions()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            sys.exit()
            break
        elif event.type == pygame.KEYDOWN: #hit any keystroke
            if event.key == 115: #hit 's'
                window.toggleFullscreen()
            else:
                messageBox.addMessage("Hello World!", (0, 0, 255))
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()