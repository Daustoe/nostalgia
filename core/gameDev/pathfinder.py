'''
Created on Apr 19, 2012

@author: Claymore
'''


class PathFinder(object):
    def __init__(self, amap):
        self.map = amap
        self.size = self.map

    def dijkstra(self, (startX, startY), (endX, endY)):
        '''
        1) create our graph out of the map(moveable spaces)
        2) assign to every node a distance value:
            zero for our initial node and infinity for all other nodes.
        3) mark all nodes unvisited. set initial node as current.
        4) for the current node, consider all of its unvisited neighbors
            and calculate their distances. If this distance is less than
            the previously recorded distance the overwrite it.
        5)when we are done considering all of the neighbors of the current node,
            mark the current node as visited.
        6) if the destination node has been marked visited or if the smallest
            distance among the nodes in the unvisited set is inifinity then stop
        7) set the unvisited node marked with the smallest tentative distance as
        the next current node then go back to step three
        '''
        visited = []
        distance = []
        checked = []

        for x in range(len(self.map)):
            visited.append([])
            distance.append([])
            checked.append([])
            for y in range(len(self.map[0])):
                visited[x].append(self.map[x][y].block)
                distance[x].append(10000)
                checked[x].append(False)
        nodeQueue = []
        nodeQueue.append((startX, startY))
        print visited[startX][startY]
        print distance[startX][startY]
        distance[startX][startY] = 0
        currentNode = (startX, startY)
        endNode = (endX, endY)
        print currentNode
        while currentNode != endNode and len(nodeQueue) > 0:
            #check left, right, up, down, and diags to see if they are viable
            currentNode = nodeQueue.pop()
            visited[currentNode[0]][currentNode[1]] = True
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 or dy != 0:
                        if currentNode[0]+dx >= 0 and currentNode[0]+dx < len(self.map[0]) and currentNode[1]+dy >= 0 and currentNode[1]+dy < len(self.map[0]):
                            if not visited[currentNode[0]+dx][currentNode[1]+dy]:
                                if distance[currentNode[0]+dx][currentNode[1]+dy] > distance[currentNode[0]][currentNode[1]]:
                                    distance[currentNode[0]+dx][currentNode[1]+dy] = distance[currentNode[0]][currentNode[1]]+1
                                if nodeQueue.count((currentNode[0]+dx, currentNode[1]+dy)) == 0:
                                    nodeQueue.append((currentNode[0]+dx, currentNode[1]+dy))

        currentNode = (endX, endY)
        path = []

        print "past calc"
        while currentNode != (startX, startY):
            smallest = 100000
            (nextX, nextY) = currentNode
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 or dy != 0:
                        if currentNode[0]+dx >= 0 and currentNode[0]+dx < len(self.map[0]) and currentNode[1]+dy >= 0 and currentNode[1]+dy < len(self.map[0]) and checked[currentNode[0]+dx][currentNode[1]+dy] == False:
                            #print "checking neighbor"
                            checked[currentNode[0]+dx][currentNode[1]+dy] = True
                            print not self.map[currentNode[0]+dx][currentNode[1]+dy].block
                            if distance[currentNode[0]+dx][currentNode[1]+dy] < smallest and not self.map[currentNode[0]+dx][currentNode[1]+dy].block:
                                smallest = distance[currentNode[0]+dx][currentNode[1]+dy]
                                print smallest
                                (nextX, nextY) = (currentNode[0]+dx, currentNode[1]+dy)
            if currentNode == (nextX, nextY):
                break
            currentNode = (nextX, nextY)
            path.append(currentNode)
        return path


class Node():
    def __init__(self):
        self.neighbors = []
        self.visited = False
        self.distance = 10000

    def addNeighbor(self, node):
        self.neighbors.append(node)