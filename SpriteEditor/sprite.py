import pygame
from pygame.color import Color

import core.gui.element as Element
from pixel import Pixel


#TODO We may want to change how this sprite is displayed


#noinspection PyArgumentList
class Sprite(Element.Element):
    def __init__(self, x, y, width, height, sprite_dimension=(20, 20), pixels=None):
        super(Sprite, self).__init__(x, y, width, height, Color(255, 255, 255))
        self.size = None
        if pixels is not None:
            self.pixels = pixels
        else:
            self.pixels = []
        #TODO we can calculate pixel w/h using sprite Dim and w/h of sprite surface
        self.pixel_width = 2
        self.pixel_height = 2
        #TODO pixels in sprite should perhaps be the width and height, remove current width and height
        self.sprite_width, self.sprite_height = sprite_dimension
        self.block_width, self.block_height = (self.width / self.sprite_width, self.height / self.sprite_height)
        self.update_sprite_size()
        self.surface = pygame.Surface(self.size)
        #TODO self.pixels does not need to be a double array. Pixel objects know their location once set so we only need
        #ToDo a list of them
        for x in range(self.sprite_width):
            self.pixels.append([])
            for y in range(self.sprite_height):
                self.pixels[x].append(Pixel(x * self.block_width, y * self.block_height, self.block_width, self.block_height))
                self.pixels[x][y].set_master(self)
        self.color_box = None

    def update_pixel_size(self, dx, dy):
        self.pixel_width = self.pixel_width + dx
        self.pixel_height = self.pixel_height + dy
        self.generate_surface()

    def update_sprite_size(self):
        self.size = (self.block_width * self.sprite_width, self.block_height * self.sprite_height)

    def generate_surface(self):
        temp_array = self.pixels
        self.pixels = []
        self.update_sprite_size()
        self.surface = pygame.Surface(self.size)
        for x in range(self.sprite_width):
            self.pixels.append([])
            for y in range(self.sprite_height):
                self.pixels[x].append(Pixel(x * self.block_width, y * self.block_height, self.block_width, self.block_height,
                                            temp_array[x][y].get_color()))
                self.pixels[x][y].set_master(self)

    @staticmethod
    def cubic_interpolation(row, value):
        """
        Performs the cubic operations with the given row of pixels (colors) need to be careful that we perform the tuple
        operations correctly down below, this may cause this function to blow up (may need to add quite a bit more code
        to get it to do what we want.)
        """
        interpolated_color = [0, 0, 0]
        for color in range(3):
            first = value * (3.0 * (row[1][color] - row[2][color]) + row[3][color] - row[0][color])
            second = value * (2.0 * row[0][color] - 5.0 * row[1][color] + 4.0 * row[2][color] - row[3][color] + first)
            third = value * (row[2][color] - row[0][color] + second)
            fourth = row[1][color] + 0.5 * third
            interpolated_color[color] = fourth
        return tuple(interpolated_color)

    def bicubic_interpolation(self, cube, x, y):
        """
        Here we are handed a cube of pixels 4x4 and we need to take their r, g, b values and perform this function
        on them to get a weighted average. Performs the normal cubic interpolation on the rows, then again on the
        results to get our bicubic weighted value.
        """
        temp = [self.cubic_interpolation(cube[0], y),
                self.cubic_interpolation(cube[1], y),
                self.cubic_interpolation(cube[2], y),
                self.cubic_interpolation(cube[3], y)]
        return self.cubic_interpolation(temp, x)

    def interpolation_step(self, pixels):
        new_pixels = []
        old_width, old_height = pixels.size
        print pixels.index()
        new_width, new_height = (old_width / 4, old_height / 4)
        for sample_x in range(0, old_width - 1, new_width):
            temp_row = []
            for sample_y in range(0, old_height - 1, new_height):
                x_mid = sample_x + new_width / 2
                y_mid = sample_y + new_height / 2
                cube = [[pixels[x, y] for x in range(x_mid - 1, x_mid + 3, 1)] for y in range(y_mid - 1, y_mid + 3, 1)]
                temp_row.append(self.bicubic_interpolation(cube, 1, 1))
            new_pixels.append(temp_row)
        if len(new_pixels) >= 30:
            new_pixels = self.interpolation_step(new_pixels)
        return new_pixels

    def image_to_sprite(self, image):
        """
        For the bicubic interpolation we want to draw lines through our image. Where these lines intersect we are making
        the new pixels for the downscaled image. In this function we are defining where those pixels are.

        Essentially these lines should bisect at the center of these blocks we are making.

        We may also have to perform this operation a few times to scale down our image and still retain a good quality.
        Shrinking an image too much using this method may yield poor results, so we will have to gradually bring it down
        """
        colors = self.interpolation_step(image)

    def color_array_to_pixel_array(self, colors):
        #ToDo currently new_pixels is an array of colors, not Pixel objects. Need to convert and set locations
        pixels = []
        for row in colors:
            pixels.append([])
            for col in colors:
                pixels[row].append(Pixel((20, 20), colors[row][col]))

    def simple_image_to_sprite(self, image):
        """
        Performs a simple conversion of an image to a sprite set it as this sprite. Just grabs the average color of the
        entire section that will become one pixel of this sprite.

        deprecated
        """
        (width, height) = image.size
        chunk_size = (width / self.sprite_width, height / self.sprite_height)
        temp_array = []
        pix = image.load()
        this_block_size = (self.block_width, self.block_height)
        chunk_total = 0
        for x_chunk in range(0, width - 1, chunk_size[0]):
            temp_array.append([])
            for y_chunk in range(0, height - 1, chunk_size[1]):
                (red, green, blue) = (0, 0, 0)
                for x in range(x_chunk, x_chunk + chunk_size[0]):
                    for y in range(y_chunk, y_chunk + chunk_size[1]):
                        if x < width and y < height:
                            temp = pix[x, y]
                            (red, green, blue) = (red + temp[0], green + temp[1], blue + temp[2])
                            chunk_total += 1
                temp_array[x_chunk / chunk_size[0]].append(Pixel((x_chunk / chunk_size[0] * this_block_size[0],
                                                                  y_chunk / chunk_size[1] * this_block_size[1]),
                                                                 this_block_size,
                                                                 (red / chunk_total, green / chunk_total,
                                                                  blue / chunk_total)))
                chunk_total = 0
        self.pixels = temp_array

    def update_pixel_count(self, dx, dy):
        self.sprite_width = self.sprite_width + dx
        self.sprite_height = self.sprite_height + dy
        self.block_width = self.width / self.sprite_width
        self.block_height = self.height / self.sprite_height
        if dx == 1:
            self.pixels.append([])
            for each in range(self.sprite_height):
                self.pixels[self.sprite_width - 1].append(
                    Pixel((self.sprite_width - 1) * self.block_width, each * self.block_height, self.block_width, self.block_height))
        elif dx == -1:
            self.pixels.pop()
        if dy == 1:
            for each in range(self.sprite_width):
                self.pixels[each].append(
                    Pixel(each * self.block_width, (self.sprite_height - 1) * self.block_height, self.block_width, self.block_height))
        elif dy == -1:
            for each in range(self.sprite_width):
                self.pixels[each].pop()
        self.generate_surface()

    def make_image(self):
        image_surface = pygame.Surface((self.sprite_width * self.pixel_width, self.sprite_height * self.pixel_height))
        for x in range(self.sprite_width):
            for y in range(self.sprite_height):
                image_surface.blit(self.pixels[x][y].surface.subsurface(pygame.Rect(self.position, (self.pixel_width, self.pixel_height))),
                                   (x * self.pixel_width, y * self.pixel_height))
        return image_surface

    def render(self, window):
        for x in range(self.sprite_width):
            for y in range(self.sprite_height):
                self.pixels[x][y].render(self.surface)
        super(Sprite, self).render(window)

    def set_color_box(self, color_box):
        self.color_box = color_box

    def set_master(self, master):
        super(Sprite, self).set_master(master)
        for row in self.pixels:
            for each in row:
                each.set_master(self)

    def action_event(self, mouse_press, mouse_position, mouse_movement):
        if self.color_box is not None and self.x < mouse_position[0] < self.x + self.width:
            if self.y < mouse_position[1] < self.y + self.height:
                if mouse_press[0] and not self.clicked:
                    self.clicked = True
                    x = (mouse_position[0] - self.x) / self.block_width
                    y = (mouse_position[1] - self.y) / self.block_height
                    self.pixels[x][y].change_color(self.color_box.get_color())
                elif mouse_press[2] and not self.clicked:
                    self.clicked = True
                    x = (mouse_position[0] - self.x) / self.block_width
                    y = (mouse_position[1] - self.y) / self.block_height
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, info="right", object=self.pixels[x][y]))
        self.clicked = False

    def get_pixel_color(self, x, y):
        return self.pixels[x][y].get_color()
