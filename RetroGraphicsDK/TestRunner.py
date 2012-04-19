'''
Created on Mar 15, 2012

@author: clayton

Issue List for whole of development kit

--make mouseReporter (mouseover reporter for elements on our console)
--make pathfinding algorithm
--make field of view algorithm
    -perhaps a few of these
--random dungeon generator
--basic class structures of game Objects
--heightmap stuff for above ground map generation
--make gameCanvas (main display of game)
'''
import console, pygame, sys, button, messageBox, slider, menu, dungeonGenerator
from pygame.locals import *

def buttonAction():
    print "Button works"
    

window = console.Console(1100, 720)
font = pygame.font.SysFont('timesnewroman', 16, bold=True)
firstButton = button.Button((10, 10), (80, 20), "Hello World", font, buttonAction)
slider = slider.Slider((10, 300), (275, 15), (255, 200, 200), (255, 0, 0))
menu = menu.Menu((10, 10), (580, 580), font, title="Test Menu")
#window.addElement(firstButton)
#window.addElement(slider)
window.addElement(menu)

mapmaker = dungeonGenerator.DungeonGenerator(30, 6, 10, 80, 43)

myMap = mapmaker.makeMap()
print myMap

menuOptions = []
menuOptions.append("test1")
menuOptions.append("test2")

pauseOptions = ["Save Game", "Load Game", "Quit to Desktop"]

lightWall = (130, 110, 50)
lightGround = (200, 180, 50)
tilesize = (8, 12)
def drawMap():
    global myMap, lightWall, lightGround, tilesize
    
    for y in range(43):
        for x in range(80):
            wall = myMap[x][y].blockSight
            if wall:
                myMap[x][y].setColor(lightWall)
            else:
                myMap[x][y].setColor(lightGround)
            myMap[x][y].render(window.window)
            
quit = False
while not quit:
    window.drawElements()
    window.handleElementActions()
    drawMap()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            sys.exit()
            break
        elif event.type == pygame.KEYDOWN: #hit any keystroke
            if event.key == 115: #hit 's'
                window.toggleFullscreen()
            elif event.key == 114:
                print menu.open(pauseOptions)
    pygame.display.flip()