import random
import math


class HeightMap(object):
    """
    The HeightMap class holds all the functions needed to modify a two dimensional grid that represents heights on the
    ground. The grid can be of any size the user wishes.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.heightmap = [[0.0
                          for y in range(self.height)]
                          for x in range(self.width)]
        self.dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
        self.dy = [-1, -1, -1, 0, 0, 0, 1, 1, 1]

    def noise(self, x, y):
        return 0

    def normalize(self, minimum, maximum):
        """
        Normalizes the values of the HeightMap. Lowers extremely high values and raises low values.
        """
        (current_min, current_max) = self.get_min_and_max()
        if current_max - current_min == 0.0:
            inv_max = 0.0
        else:
            inv_max = (maximum - minimum) / (current_max - current_min)
            #now we normalize our self.heightmap
        for x in range(self.width):
            for y in range(self.height):
                self.heightmap[x][y] = minimum + (self.heightmap[x][y] - current_min) * inv_max

    def change_height(self, change):
        """
        Modifies the height of all values of the HeightMap by the given amount.
        """
        for x in range(self.width):
            for y in range(self.height):
                self.heightmap[x][y] += change

    def rain_erosion(self, drop_number, erosion_coefficient, aggregation_coefficient):
        """
        Simulates the erosion of rain on the Heightmap by pulling 'sediment' from the higher locations and moving it
        along the lowest neighbors for some distance. Pulls higher values to lower values. Acts like a more natural
        normalizer of the Heightmap.
        """
        while drop_number > 0:
            current_x = int(random.uniform(0, self.width - 1))
            current_y = int(random.uniform(0, self.height - 1))
            sediment = 0.0
            while True:
                next_x = next_y = 0
                height = self.heightmap[current_x][current_y]
                #now calculate slope at x, y
                slope = 0.0
                for neighbor in range(8):
                    neighbor_x = current_x + self.dx[neighbor]
                    neighbor_y = current_y + self.dy[neighbor]
                    if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:
                        neighbor_slope = height - self.heightmap[neighbor_x][neighbor_y]
                        if neighbor_slope > slope:
                            slope = neighbor_slope
                            next_x = neighbor_x
                            next_y = neighbor_y
                if slope > 0.0:
                    self.heightmap[current_x][current_y] *= 1.0 - (erosion_coefficient * slope)
                    self.heightmap[current_x][current_y] -= erosion_coefficient * slope
                    current_x = next_x
                    current_y = next_y
                    sediment += slope
                else:
                    self.heightmap[current_x][current_y] *= 1.0 + (aggregation_coefficient * sediment)
                    self.heightmap[current_x][current_y] += aggregation_coefficient * sediment
                    break
            drop_number -= 1

    def get_min_and_max(self):
        """
        Returns the minimum and maximum height in the Heightmap.
        """
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
        """
        Adds the given number of valleys with their sizes randomized around the given proportions. The user can set
        'about' how large the valleys are. The key is to make this random so it generates unique landscapes.
        """
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
        """
        Adds a 'valley' or inverse dome to the heightmap at the given location and with the given size.
        """
        square_radius = radius * radius
        coefficient = height / square_radius
        min_x = int(max(0, hx - radius))
        max_x = int(min(self.width, hx + radius))
        min_y = int(max(0, hy - radius))
        max_y = int(min(self.height, hy + radius))
        for x in range(min_x, max_x):
            x_distance = (x - hx) * (x - hx)
            for y in range(min_y, max_y):
                distance = x_distance + (y - hy) * (y - hy)
                if distance < square_radius:
                    z = (square_radius - distance) * coefficient
                    if height > 0.0:
                        if self.heightmap[x][y] < z:
                            self.heightmap[x][y] = z
                    else:
                        if self.heightmap[x][y] > z:
                            self.heightmap[x][y] = z

    def add_hill(self, hx, hy, radius, height):
        """
        Adds a hill or a dome to the HeightMap at the given location and size.
        """
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
        """
        Adds a number of hills with semi-randomized sizes as set by the parameters.
        """
        for each in range(number):
            min_hill_radius = base_radius * (1.0 - radius_var)
            max_hill_radius = base_radius * (1.0 + radius_var)
            radius = random.uniform(min_hill_radius, max_hill_radius)
            theta = random.uniform(0.0, 6.283185)  # random between 0 and 2PI
            distance = random.uniform(0.0, min(self.width, self.height) / 2 - radius)
            x_height = (self.width / 2 + math.cos(theta) * distance)
            y_height = (self.height / 2 + math.sin(theta) * distance)
            self.add_hill(x_height, y_height, radius, height)