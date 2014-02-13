import pygame
import core.gui.element as Element
from pixel import Pixel
from pygame.color import Color

#TODO We may want to change how this sprite is displayed


#noinspection PyArgumentList
class Sprite(Element.Element):
    def __init__(self, x, y, width, height, pixel_size=(2, 2), pixels_in_sprite=(20, 20), pixel_array=None):
        super(Sprite, self).__init__(x, y, width, height, Color(255, 255, 255))
        self.sprite_size = None
        if pixel_array is not None:
            self.pixels = pixel_array
        else:
            self.pixels = []
        self.pixel_size = pixel_size
        #TODO pixels in sprite should perhaps be the width and height, remove current width and height
        self.pixels_in_sprite = pixels_in_sprite
        self.block_size = (self.width / self.pixels_in_sprite[0], self.height / self.pixels_in_sprite[1])
        self.update_sprite_size()
        self.surface = pygame.Surface(self.sprite_size)
        for x in range(self.pixels_in_sprite[0]):
            self.pixels.append([])
            for y in range(self.pixels_in_sprite[1]):
                self.pixels[x].append(Pixel((x * self.block_size[0], y * self.block_size[1]), self.block_size))
                self.pixels[x][y].set_master(self)
        self.color_box = None

    def update_pixel_size(self, dx, dy):
        self.pixel_size = (self.pixel_size[0] + dx, self.pixel_size[1] + dy)
        self.generate_surface()

    def update_sprite_size(self):
        self.sprite_size = (self.block_size[0] * self.pixels_in_sprite[0],
                            self.block_size[1] * self.pixels_in_sprite[1])

    def generate_surface(self):
        temp_array = self.pixels
        self.pixels = []
        self.update_sprite_size()
        self.surface = pygame.Surface(self.sprite_size)
        for x in range(self.pixels_in_sprite[0]):
            self.pixels.append([])
            for y in range(self.pixels_in_sprite[1]):
                self.pixels[x].append(Pixel((x * self.block_size[0], y * self.block_size[1]), self.block_size,
                                            temp_array[x][y].get_color()))
                self.pixels[x][y].set_master(self)

    #TODO need to perform this function on all values of the color. Right now we are just doing it on the tuple color
    def cubic_interpolation(self, row, value):
        """
        Performs the cubic operations with the given row of pixels (colors) need to be careful that we perform the tuple
        operations correctly down below, this may cause this function to blow up (may need to add quite a bit more code
        to get it to do what we want.)
        """
        first = value * (3.0 * (row[1] - row[2]) + row[3] - row[0])  # tuple and float operations, be careful!
        second = value * (2.0 * row[0] - 5.0 * row[1] + 4.0 * row[2] - row[3] + first)
        third = value * (row[2] - row[0] + second)
        fourth = row[1] + 0.5 * third
        return fourth
        
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

    def complex_image_to_sprite(self, image):
        """
        For the bicubic interpolation we want to draw lines through our image. Where these lines intersect we are making
        the new pixels for the downscaled image. In this function we are defining where those pixels are.

        Essentially these lines should bisect at the center of these blocks we are making.

        We may also have to perform this operation a few times to scale down our image and still retain a good quality.
        Shrinking an image too much using this method may yield poor results, so we will have to gradually bring it down
        """
        image_width, image_height = image.size
        sample_width, sample_height = (image_width / 20, image_height / 20)  # setting this to 20 by default
        pixels = image.load()
        for sample_x in range(0, image_width - 1, sample_width):
            for sample_y in range(0, image_height - 1, sample_height):
                x = sample_x + 10
                y = sample_y + 10
                print x, y

    def simple_image_to_sprite(self, image):
        """
        Performs a simple conversion of an image to a sprite set it as this sprite. Just grabs the average color of the
        entire section that will become one pixel of this sprite.
        """
        (width, height) = image.size
        chunk_size = (width / self.pixels_in_sprite[0], height / self.pixels_in_sprite[1])
        temp_array = []
        pix = image.load()
        this_block_size = self.block_size
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
        self.pixels_in_sprite = (self.pixels_in_sprite[0] + dx, self.pixels_in_sprite[1] + dy)
        self.block_size = (self.width / self.pixels_in_sprite[0], self.height / self.pixels_in_sprite[1])
        if dx == 1:
            self.pixels.append([])
            for each in range(self.pixels_in_sprite[1]):
                self.pixels[self.pixels_in_sprite[0] - 1].append(Pixel(((
                                                                            self.pixels_in_sprite[0] - 1) *
                                                                        self.block_size[0], each * self.block_size[1]),
                                                                       self.block_size))
        elif dx == -1:
            self.pixels.pop()
        if dy == 1:
            for each in range(self.pixels_in_sprite[0]):
                self.pixels[each].append(Pixel((each * self.block_size[0], (
                                                                               self.pixels_in_sprite[1] - 1) *
                                                                           self.block_size[1]), self.block_size))
        elif dy == -1:
            for each in range(self.pixels_in_sprite[0]):
                self.pixels[each].pop()
        self.generate_surface()

    def make_image(self):
        image_surface = pygame.Surface((self.pixels_in_sprite[0] * self.pixel_size[0],
                                        self.pixels_in_sprite[1] * self.pixel_size[1]))
        for x in range(self.pixels_in_sprite[0]):
            for y in range(self.pixels_in_sprite[1]):
                image_surface.blit(self.pixels[x][y].surface.subsurface(pygame.Rect(self.position, self.pixel_size)),
                                   (x * self.pixel_size[0], y * self.pixel_size[1]))
        return image_surface

    def render(self, window):
        for x in range(self.pixels_in_sprite[0]):
            for y in range(self.pixels_in_sprite[1]):
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
                    x = (mouse_position[0] - self.x) / self.block_size[0]
                    y = (mouse_position[1] - self.y) / self.block_size[1]
                    self.pixels[x][y].change_color(self.color_box.get_color())
                elif mouse_press[2] and not self.clicked:
                    self.clicked = True
                    x = (mouse_position[0] - self.x) / self.block_size[0]
                    y = (mouse_position[1] - self.y) / self.block_size[1]
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, info="right", object=self.pixels[x][y]))
        self.clicked = False

    def get_pixel_color(self, x, y):
        return self.pixels[x][y].get_color()
