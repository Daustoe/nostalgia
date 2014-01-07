import random
import math


class HeightMap(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.heightmap = [[0.0
                          for y in range(self.height)]
                          for x in range(self.width)]
        self.dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
        self.dy = [-1, -1, -1, 0, 0, 0, 1, 1, 1]

    def normalize(self, minimum, maximum):
        (current_min, current_max) = self.get_min_and_max()
        if current_max - current_min == 0.0:
            invmax = 0.0
        else:
            invmax = (maximum - minimum) / (current_max - current_min)
            #now we normalize our self.heightmap
        for x in range(self.width):
            for y in range(self.height):
                self.heightmap[x][y] = minimum + (self.heightmap[x][y] - current_min) * invmax

    def change_height(self, change):
        for x in range(self.width):
            for y in range(self.height):
                self.heightmap[x][y] += change

    def rain_erosion(self, drop_number, erosion_coefficient, agregation_coefficient):
        while drop_number > 0:
            current_x = int(random.uniform(0, self.width - 1))
            current_y = int(random.uniform(0, self.height - 1))
            slope = 0.0
            sediment = 0.0
            while True:
                next_x = next_y = 0
                v = self.heightmap[current_x][current_y]
                #now calculate slope at x, y
                slope = 0.0
                for i in range(8):
                    nx = current_x + self.dx[i]
                    ny = current_y + self.dy[i]
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        n_slope = v - self.heightmap[nx][ny]
                        if n_slope > slope:
                            slope = n_slope
                            next_x = nx
                            next_y = ny
                if slope > 0.0:
                    self.heightmap[current_x][current_y] *= 1.0 - (erosion_coefficient * slope)
                    self.heightmap[current_x][current_y] -= erosion_coefficient * slope
                    current_x = next_x
                    current_y = next_y
                    sediment += slope
                else:
                    self.heightmap[current_x][current_y] *= 1.0 + (agregation_coefficient * sediment)
                    self.heightmap[current_x][current_y] += agregation_coefficient * sediment
                    break
            drop_number -= 1

    def get_min_and_max(self):
        current_max = current_min = self.heightmap[0][0]
        for x in range(self.width):
            for y in range(self.height):
                value = self.heightmap[x][y]
                if value > current_max:
                    current_max = value
                elif value < current_min:
                    current_min = value
        return current_min, current_max

    def smooth(self, weight, minimum, maximum):
        weight = [1.0, 2.0, 1.0, 2.0, 20.0, 2.0, 1.0, 2.0, 1.0]
        for x in range(self.width):
            for y in range(self.height):
                if minimum <= self.heightmap[x][y] <= maximum:
                    value = 0.0
                    total_weight = 0.0
                    for i in range(9):
                        nx = x + self.dx[i]
                        ny = y + self.dy[i]
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            value += weight[i] * self.heightmap[nx][ny]
                            total_weight += weight[i]
                    self.heightmap[x][y] = value / total_weight

    def add_valleys(self, number, base_radius, radius_var, height):
        for each in range(number):
            min_hill_radius = base_radius * (1.0 - radius_var)
            max_hill_radius = base_radius * (1.0 + radius_var)
            radius = random.uniform(min_hill_radius, max_hill_radius)
            theta = random.uniform(0.0, 6.283185)  # random between 0 and 2PI
            dist = random.uniform(0.0, min(self.width, self.height) / 2 - radius)
            xh = (self.width / 2 + math.cos(theta) * dist)
            yh = (self.height / 2 + math.sin(theta) * dist)
            self.add_hill(xh, yh, radius, height)

    def add_valley(self, hx, hy, radius, height):
        square_radius = radius * radius
        coefficient = height / square_radius
        min_x = int(max(0, hx - radius))
        max_x = int(min(self.width, hx + radius))
        miny = int(max(0, hy - radius))
        maxy = int(min(self.height, hy + radius))
        for x in range(min_x, max_x):
            x_dist = (x - hx) * (x - hx)
            for y in range(miny, maxy):
                dist = x_dist + (y - hy) * (y - hy)
                if dist < square_radius:
                    z = (square_radius - dist) * coefficient
                    if height > 0.0:
                        if self.heightmap[x][y] < z:
                            self.heightmap[x][y] = z
                    else:
                        if self.heightmap[x][y] > z:
                            self.heightmap[x][y] = z

    def add_hill(self, hx, hy, radius, height):
        square = radius ** 2
        coefficient = height / square
        min_x = int(max(0, hx - radius))
        max_x = int(min(self.width, hx + radius))
        miny = int(max(0, hy - radius))
        maxy = int(min(self.height, hy + radius))
        for x in range(min_x, max_x):
            x_dist = (x - hx) ** 2
            for y in range(miny, maxy):
                z = square - x_dist - (y - hy) ** 2
                if z > 0.0:
                    self.heightmap[x][y] += z * coefficient

    def add_hills(self, number, base_radius, radius_var, height):
        for each in range(number):
            min_hill_radius = base_radius * (1.0 - radius_var)
            max_hill_radius = base_radius * (1.0 + radius_var)
            radius = random.uniform(min_hill_radius, max_hill_radius)
            theta = random.uniform(0.0, 6.283185)  # random between 0 and 2PI
            dist = random.uniform(0.0, min(self.width, self.height) / 2 - radius)
            x_height = (self.width / 2 + math.cos(theta) * dist)
            y_height = (self.height / 2 + math.sin(theta) * dist)
            self.add_hill(x_height, y_height, radius, height)