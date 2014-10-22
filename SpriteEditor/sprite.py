import pygame
from core.gui.imageView import ImageView
from pixel import Pixel


#TODO We may want to change how this sprite is displayed


#noinspection PyArgumentList
class Sprite(ImageView):
    def __init__(self, x, y, width, height):
        super(Sprite, self).__init__(x, y, width, height, pygame.image.load('resources/checkered.png'))
        self.pixels = []
        #TODO we can calculate pixel w/h using sprite Dim and w/h of sprite surface
        self.pixel_width = 2
        self.pixel_height = 2
        #TODO pixels in sprite should perhaps be the width and height, remove current width and height
        self.sprite_width = 20
        self.sprite_height = 20
        self.block_width, self.block_height = (self.frame.w / self.sprite_width, self.frame.h / self.sprite_height)
        #TODO self.pixels does not need to be a double array. Pixel objects know their location once set so we only need
        #ToDo a list of them
        for y in range(self.sprite_width):
            for x in range(self.sprite_height):
                pixel = Pixel(x * self.block_width, y * self.block_height, self.block_width, self.block_height)
                pixel.set_parent(self)
                self.add(pixel)
                self.pixels.append(pixel)
        self.color_box = None

    def sprite_size(self):
        return self.sprite_width, self.sprite_height

    def pixel_size(self):
        return self.pixel_width, self.pixel_height

    def image_to_sprite(self, image):
        pixels = image.getdata()
        for index in range(len(pixels)):
            r, g, b = pixels[index][:3]
            alpha = pixels[index][3]
            alpha = min(alpha, 1) * 255
            self.pixels[index].change_color(pygame.Color(r, g, b))
            self.pixels[index].set_alpha(alpha)

    def make_image(self):
        size = (self.sprite_width * self.pixel_width, self.sprite_height * self.pixel_height)
        image_surface = pygame.Surface(size, pygame.SRCALPHA)
        for index in range(len(self.pixels)):
            surface = pygame.transform.scale(self.pixels[index].surface, (self.pixel_width, self.pixel_height))
            x = index % self.sprite_width
            y = index / self.sprite_width
            image_surface.blit(surface, (x * self.pixel_width, y * self.pixel_height))
        return image_surface

    def set_color_box(self, color_box):
        self.color_box = color_box

    def set_parent(self, parent):
        super(Sprite, self).set_parent(parent)
        for pixel in self.pixels:
            pixel.set_parent(self)