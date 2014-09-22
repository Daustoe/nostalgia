import pygame
from pygame.color import Color

from core.gui.view import View
from pixel import Pixel


#TODO We may want to change how this sprite is displayed


#noinspection PyArgumentList
class Sprite(View):
    def __init__(self, x, y, width, height, sprite_width=20, sprite_height=20):
        super(Sprite, self).__init__(x, y, width, height, Color(255, 255, 255))
        self.pixels = []
        #TODO we can calculate pixel w/h using sprite Dim and w/h of sprite surface
        self.pixel_width = 2
        self.pixel_height = 2
        #TODO pixels in sprite should perhaps be the width and height, remove current width and height
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.block_width, self.block_height = (self.frame.w / self.sprite_width, self.frame.h / self.sprite_height)
        #TODO self.pixels does not need to be a double array. Pixel objects know their location once set so we only need
        #ToDo a list of them
        for x in range(self.sprite_width):
            for y in range(self.sprite_height):
                pixel = Pixel(x * self.block_width, y * self.block_height, self.block_width, self.block_height)
                pixel.set_parent(self)
                self.add(pixel)
                self.pixels.append(pixel)
        self.color_box = None

    def generate_surface(self):
        temp_array = self.pixels
        self.pixels = []
        self.surface = pygame.Surface(self.size)
        for x in range(self.sprite_width):
            for y in range(self.sprite_height):
                pixel = Pixel(x * self.block_width, y * self.block_height, self.block_width, self.block_height, temp_array[x][y].get_color())
                pixel.set_parent(self)
                self.add(pixel)
                self.pixels.append(pixel)

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
        old_width, old_height = pixels.size()
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

    def make_image(self):
        image_surface = pygame.Surface((self.sprite_width * self.pixel_width, self.sprite_height * self.pixel_height))
        for pixel in self.pixels:
            pixel_surface = pixel.surface.subsurface(pygame.Rect(self.position, (self.pixel_width, self.pixel_height)))
            image_surface.blit(pixel_surface, (pixel.x * self.pixel_width, pixel.y * self.pixel_height))
        return image_surface

    def render(self, window):
        for pixel in self.pixels:
            pixel.render(self.surface)
        super(Sprite, self).render(window)

    def set_color_box(self, color_box):
        self.color_box = color_box

    def set_parent(self, parent):
        super(Sprite, self).set_parent(parent)
        for pixel in self.pixels:
            pixel.set_parent(self)