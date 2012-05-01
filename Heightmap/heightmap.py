'''
Created on Apr 23, 2012

@author: Claymore
'''
import random, math

class HeightMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.heightmap = [[0.0
                           for y in range(self.height)]
                                for x in range(self.width)]
        
    def normalize(self, minimum, maximum):
        (currentMin, currentMax) = self.getMinAndMax()
        if currentMax - currentMin == 0.0: invmax = 0.0
        else: invmax = (maximum-minimum)/(currentMax-currentMin)
        #now we normalize our self.heightmap
        for x in range(self.width):
            for y in range(self.height):
                self.heightmap[x][y] = minimum + (self.heightmap[x][y] - currentMin) * invmax
                
    def rainErosion(self, dropNumber, erosionCoef, agregationCoef):
        while dropNumber > 0:
            currentX = random.uniform(0, self.width-1)
            currentY = random.uniform(0, self.height-1)
            dx = {-1, 0, 1, -1, 1, -1, 0, 1}
            dy = {-1, -1, -1, 0, 0, 1, 1, 1}
            slope = 0.0
            sediment = 0.0
            while True:
                nextx = nexty = 0
                v = self.heightmap[currentX][currentY]
                #now calculate slope at x, y
                for i in range(8):
                    nx = currentX+dx[i]
                    ny = currentY+dy[i]
                    if nx >= 0 and nx < self.width and ny >= 0 and ny < self.height:
                        nslope = v - self.heightmap[nx][ny]
                        if nslope > slope:
                            slope = nslope
                            nextx = nx
                            nexty = ny
                if slope > 0.0:
                    self.heightmap[currentX][currentY] *= 1.0 - (erosionCoef * slope)
                    self.heightmap[currentX][currentY] -= erosionCoef * slope
                    currentX = nextx
                    currentY = nexty
                    sediment += slope
                else:
                    self.heightmap[currentX][currentY] *= 1.0 + (agregationCoef*sediment)
                    self.heightmap[currentX][currentY] += agregationCoef*sediment
                    break
            dropNumber -= 1
                
        
    def getMinAndMax(self):
        currentMax = currentMin = self.heightmap[0][0]
        for x in range(self.width):
            for y in range(self.height):
                value = self.heightmap[x][y]
                if value > currentMax: currentMax = value
                elif value < currentMin: currentMin = value
        return (currentMin, currentMax)
                
        
    def addHill(self, hx, hy, radius, height):
        square = radius**2
        coef = height / square
        minx = max(0, hx - radius)
        maxx = min(self.width, hx+radius)
        miny = max(0, hy-radius)
        maxy = min(self.height, hy+radius)
        for x in range(minx, maxx):
            xdist = (x-hx)**2
            for y in range(miny, maxy):
                z = square - xdist - (y - hy)**2
                if z > 0.0: self.heightmap[x][y] += z*coef
                
    def addHills(self, number, baseRadius, radiusVar, height):
        for each in range(number):
            hillMinRadius = baseRadius*(1.0-radiusVar)
            hillMaxRadius = baseRadius*(1.0+radiusVar)
            radius = random.uniform(hillMinRadius, hillMaxRadius)
            theta = random.uniform(0.0, 6.283185) #random between 0 and 2PI
            dist = random.uniform(0.0, min(self.width, self.height)/2 - radius)
            xh = (self.width/2 + math.cos(theta)*dist)
            yh = (self.height/2 + math.sin(theta)*dist)
            self.addHill(xh, yh, radius, height)