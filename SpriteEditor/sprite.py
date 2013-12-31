import pygame
import element
from pixel import Pixel


class Sprite(element.Element):
    def __init__(self, (x, y), (width, height), pixel_size=(2, 2), pixels_in_sprite=(20, 20), pixel_array=[]):
        super(Sprite, self).__init__((x, y), (width, height), (255, 255, 255))
        self.sprite_size = None
        self.pixels = pixel_array
        self.pixel_size = pixel_size
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

    def update_pixel_count(self, dx, dy):
        self.pixels_in_sprite = (self.pixels_in_sprite[0] + dx, self.pixels_in_sprite[1] + dy)
        self.block_size = (self.width / self.pixels_in_sprite[0], self.height / self.pixels_in_sprite[1])
        if dx == 1:
            self.pixels.append([])
            for each in range(self.pixels_in_sprite[1]):
                self.pixels[self.pixels_in_sprite[0] - 1].append(Pixel(((
                    self.pixels_in_sprite[0] - 1) * self.block_size[0], each * self.block_size[1]),
                    self.block_size))
        elif dx == -1:
            self.pixels.pop()
        if dy == 1:
            for each in range(self.pixels_in_sprite[0]):
                self.pixels[each].append(Pixel((each * self.block_size[0], (
                    self.pixels_in_sprite[1] - 1) * self.block_size[1]), self.block_size))
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
                                   (x*self.pixel_size[0], y*self.pixel_size[1]))
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
        if self.color_box is not None and self.position[0] < mouse_position[0] < self.position[0] + self.size[0]:
            if self.position[1] < mouse_position[1] < self.position[1] + self.size[1]:
                if mouse_press[0] and not self.clicked:
                    self.clicked = True
                    x = (mouse_position[0] - self.position[0]) / self.block_size[0]
                    y = (mouse_position[1] - self.position[1]) / self.block_size[1]
                    self.pixels[x][y].change_color(self.color_box.get_color())
                elif mouse_press[2] and not self.clicked:
                    self.clicked = True
                    x = (mouse_position[0] - self.position[0]) / self.block_size[0]
                    y = (mouse_position[1] - self.position[1]) / self.block_size[1]
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, info="right", object=self.pixels[x][y]))
        self.clicked = False

    def update_position(self):
        super(Sprite, self).update_position()

    def get_pixel_color(self, x, y):
        return self.pixels[x][y].get_color()