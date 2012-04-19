'''
Created on Apr 18, 2012

@author: Claymore
'''
from tile import *
import random
class Room:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.center = self.center()
        
    def center(self):
        centerX = (self.x1 + self.x2)/2
        centerY = (self.y1 + self.y2)/2
        return (centerX, centerY)
    
    def intersect(self, other):
        #returns true if this room intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class DungeonGenerator(object):
    def __init__(self, maxRooms, minRoomSize, maxRoomSize, mapWidth, mapHeight):
        self.maxRooms = maxRooms
        self.minRoomSize = minRoomSize
        self.maxRoomSize = maxRoomSize
        self.width = mapWidth
        self.height = mapHeight
        self.map = []
        self.rooms = []
        
    def createRoom(self, room):
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2):
                self.map[x][y].blocked = False
                self.map[x][y].blockSight = False
                
    def carveHTunnel(self, xStart, xEnd, y):
        for x in range(min(xStart, xEnd), max(xStart, xEnd)+1):
            self.map[x][y].blocked = False
            self.map[x][y].blockSight = False
        
    def carveVTunnel(self, yStart, yEnd, x):
        for y in range(min(yStart, yEnd), max(yStart, yEnd)+1):
            self.map[x][y].blocked = False
            self.map[x][y].blockSight = False
            
    def makeMap(self):
        self.map = [[Tile((x, y), (10, 13), True)
                for y in range(self.height)]
                    for x in range(self.width) ]
        roomCount = 0
        
        for room in range(self.maxRooms):
            #random width and height chosen
            width = random.randint(self.minRoomSize, self.maxRoomSize)
            height = random.randint(self.minRoomSize, self.maxRoomSize)
            #random position without going out of boundaries
            x = random.randint(0, self.width - width - 1)
            y = random.randint(0, self.height - height - 1)
            
            newRoom = Room(x, y, width, height)
            
            #Check all other rooms to see if they intersect with this new one
            failed = False
            for otherRoom in self.rooms:
                if newRoom.intersect(otherRoom):
                    failed = True
                    break
            
            if not failed:
                self.createRoom(newRoom)
                #now we connect this room to others with tunnels
                if roomCount > 0:
                    (prevX, prevY) = self.rooms[roomCount-1].center
                    (thisX, thisY) = newRoom.center
                    if random.randint(0, 1) == 1:
                        self.carveHTunnel(prevX, thisX, prevY)
                        self.carveVTunnel(prevY, thisY, thisX)
                    else:
                        self.carveHTunnel(prevX, thisX, thisY)
                        self.carveVTunnel(prevY, thisY, prevX)
                self.rooms.append(newRoom)
                roomCount += 1
        return self.map
                    
                