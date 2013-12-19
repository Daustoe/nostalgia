"""
Created on Apr 11, 2012

@author: Claymore
"""
import core.gui.element
import pygame
import sys


class Menu(core.gui.element.Element):
    def __init__(self, (x, y), (width, height), font, font_color=(255, 255, 255), title="", color=(100, 100, 100)):
        super(Menu, self).__init__((x, y), (width, height), color)
        self.font = font
        self.title = title
        self.font_color = font_color
        self.is_open = False
        self.title_position = ((self.position[0] + self.width / 2) -
                               self.font.size(self.title)[0] / 2, 2)
        self.title_size = self.font.size(self.title)
        self.option_list = None
        self.reset_surface()

    def open(self, option_list):
        """
        we want to blit the option_list strings to the surface of the window! in
        some order that makes sense visually. Also want to send a message to the
        console to give all input data (keyboard mouse and such) to this object.
        Should block out all other elements data handling. (much the same as the
        textbox).
        """
        self.option_list = option_list
        header_height = self.title_size[1]  # height of our title

        letter_index = ord('a')
        index = 0
        for option in option_list:
            text = '(' + chr(letter_index) + ')' + option
            self.surface.blit(self.font.render(text, True, self.font_color),
                              (15, header_height + index * self.font.size(text)[1]))
            letter_index += 1
            index += 1
        self.is_open = True
        super(Menu, self).render(self.master.window)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if 97 <= event.key <= 122:
                        index = event.key - 97
                        if 0 <= index < len(self.option_list):
                            self.is_open = False
                            self.reset_surface()
                            return index

    def render(self, window):
        return None

    def reset_surface(self):
        self.surface = pygame.Surface(self.size)
        self.surface.blit(self.font.render(self.title, True, self.font_color),
                          self.title_position)
        point_list = [(self.title_position[0] - 2, self.title_size[1] / 2),
                      (self.title_size[1] / 2, self.title_size[1] / 2),
                      (self.title_size[1] / 2, self.height - self.title_size[1] / 2),
                      (self.width - self.title_size[1] / 2, self.height - self.title_size[1] / 2),
                      (self.width - self.title_size[1] / 2, self.title_size[1] / 2),
                      (self.title_position[0] + self.title_size[0] + 2, self.title_size[1] / 2)]
        pygame.draw.lines(self.surface, self.font_color, False, point_list, 3)