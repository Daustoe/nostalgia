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
import console, pygame, sys, button, messageBox, slider, menu, dungeonGenerator, pathfinder, panel, bar
import gameObject
from pygame.locals import *
import random, time

def buttonAction():
    print "Button works"


window = console.Console(1100, 720)
font = pygame.font.SysFont('timesnewroman', 16, bold=True)
firstButton = button.Button((10, 10), (80, 20), "Hello World", font, buttonAction)
slider = slider.Slider((10, 300), (275, 15), (255, 200, 200), (255, 0, 0))
menu = menu.Menu((10, 10), (580, 580), font, title="Test Menu")
window.addElement(menu)
player = gameObject.GameObject((0, 0), pygame.image.load("player.png"))
bottomPanel = panel.Panel((0, 560), (1100, 180), (20, 20, 20))
healthbar = bar.Bar((10, 20), (200, 10), 100, (200, 0, 0), (100, 20, 20))
manabar = bar.Bar((10, 40), (200, 10), 100, (0, 0, 200), (20, 20, 100))
bottomPanel.addElement(manabar)
bottomPanel.addElement(healthbar)
window.addElement(bottomPanel)


mapmaker = dungeonGenerator.DungeonGenerator(30, 6, 13, 85, 40)

myMap = mapmaker.makeMap()
finder = pathfinder.PathFinder(myMap)

while myMap[player.position[0]][player.position[1]].blockSight:
    x = random.randint(0, 84)
    y = random.randint(0, 39)
    player.position = (x, y)

menuOptions = []
menuOptions.append("test1")
menuOptions.append("test2")

pauseOptions = ["Save Game", "Load Game", "Quit to Desktop"]

lightWall = (130, 110, 50)
lightGround = (200, 180, 50)


def colorMap():
    global myMap, lightWall, lightGround, tilesize
    for y in range(40):
        for x in range(85):
            wall = myMap[x][y].blockSight
            if wall:
                myMap[x][y].setColor(lightWall)
            else:
                myMap[x][y].setColor(lightGround)

quit = False
colorMap()
while not quit:
    window.drawElements()
    window.handleElementActions()
    for y in range(40):
        for x in range(85):
            myMap[x][y].render(window.window)
    window.window.blit(player.surface, player.position)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            sys.exit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == 115: #hit 's' testing out dijkstra's algorithm
                starty = random.randint(0, 42)
                startx = random.randint(0, 79)
                endy = random.randint(0, 42)
                endx = random.randint(0, 79)
                while myMap[startx][starty].blockSight == True:
                    starty = random.randint(0, 42)
                    startx = random.randint(0, 79)
                while myMap[endx][endy].blockSight == True:
                    endy = random.randint(0, 42)
                    endx = random.randint(0, 79)
                myMap[startx][starty].setColor((255, 0, 255))
                myMap[endx][endy].setColor((0, 255, 0))
                myMap[startx][starty].render(window.window)
                myMap[endx][endy].render(window.window)
                pygame.display.flip()
                print finder.dijkstra((startx, starty), (endx, endy))
            elif event.key == 27: #escape key hit
                value = menu.open(pauseOptions)
                if value == 2:
                    sys.exit()
    pygame.display.flip()
    time.sleep(0.0001)