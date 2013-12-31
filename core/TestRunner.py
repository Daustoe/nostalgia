"""
Created on Mar 15, 2012

@author: clayton

Issue List for whole of development kit

--TOP::: add setup.py file and get it functional so we can add the development
    kit to python environment.
--Look into PyQt4 to replace TkInter as the main gui board for our dev kit
--some classes may need more inheritance(i.e. blockableGameObjects or something)
--make mouseReporter (mouseover reporter for elements on our console)
--make pathfinding algorithm
--make field of view algorithm
    -perhaps a few of these
--random dungeon generator
--basic class structures of game Objects
--heightmap stuff for above ground map generation
--make gameCanvas (main display of game)
"""
import gui.console as Console
import pygame
import sys
import gui.button as Button
# import messageBox
import core.gui.slider as Slider
import core.gui.menu as Menu
import core.gameDev.dungeonGenerator as Dungeon
import core.gameDev.pathfinder as PathFinder
import gui.panel as Panel
import gui.bar as Bar
import core.gameDev.gameObject as gameObject
import random
import time


def button_action():
    print "Button works"


window = Console.Console(1100, 720)
font = pygame.font.SysFont('timesnewroman', 16, bold=True)
firstButton = Button.Button((10, 10), (80, 20), "Hello", font, button_action)
slider = Slider.Slider((10, 300), (275, 15), (255, 200, 200), (255, 0, 0))
menu = Menu.Menu((10, 10), (580, 580), font, title="Test Menu")
window.add_element(menu)
player = gameObject.GameObject((0, 0), pygame.image.load("player.png"))
bottomPanel = Panel.Panel((0, 560), (1100, 180), (20, 20, 20))
health_bar = Bar.Bar((10, 20), (200, 10), 100, (200, 0, 0), (100, 20, 20))
mana_bar = Bar.Bar((10, 40), (200, 10), 100, (0, 0, 200), (20, 20, 100))
bottomPanel.add_element(mana_bar)
bottomPanel.add_element(health_bar)
window.add_element(bottomPanel)

mapmaker = Dungeon.DungeonGenerator(30, 6, 13, 85, 40)

myMap = mapmaker.makeMap()
finder = PathFinder.PathFinder(myMap)

while myMap[player.position[0]][player.position[1]].blockSight:
    x = random.randint(0, 84)
    y = random.randint(0, 39)
    player.position = (x, y)

menu_options = ["test1", "test2"]

pauseOptions = ["Save Game", "Load Game", "Quit to Desktop"]

lightWall = (130, 110, 50)
lightGround = (200, 180, 50)


def color_map():
    global myMap, lightWall, lightGround
    for y in range(40):
        for x in range(85):
            wall = myMap[x][y].blockSight
            if wall:
                myMap[x][y].setColor(lightWall)
            else:
                myMap[x][y].setColor(lightGround)

userQuit = False
color_map()
while not userQuit:
    window.draw_elements()
    window.handle_element_actions()
    for y in range(40):
        for x in range(85):
            myMap[x][y].render(window.window)
    window.window.blit(player.surface, player.position)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            userQuit = True
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == 115:  # hit 's' testing out dijkstra's algorithm
                start_y = random.randint(0, 42)
                start_x = random.randint(0, 79)
                end_y = random.randint(0, 42)
                end_x = random.randint(0, 79)
                while myMap[start_x][start_y].blockSight is True:
                    start_y = random.randint(0, 42)
                    start_x = random.randint(0, 79)
                while myMap[end_x][end_y].blockSight is True:
                    end_y = random.randint(0, 42)
                    end_x = random.randint(0, 79)
                myMap[start_x][start_y].setColor((255, 0, 255))
                myMap[end_x][end_y].setColor((0, 255, 0))
                myMap[start_x][start_y].render(window.window)
                myMap[end_x][end_y].render(window.window)
                pygame.display.flip()
                print finder.dijkstra((start_x, start_y), (end_x, end_y))
            elif event.key == 27:  # escape key hit
                value = menu.open(pauseOptions)
                if value == 2:
                    sys.exit()
    pygame.display.flip()
    time.sleep(0.0001)