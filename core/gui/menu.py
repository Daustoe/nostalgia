from element import Element
import pygame
import sys


class Menu(Element):
    """
    The Menu object pulls up a panel with options given. It then waits for the user to make a selection before
    continuing the flow of the game.
    """
    def __init__(self, x, y, width, height, font, font_color=(255, 255, 255), title="", color=(100, 100, 100)):
        super(Menu, self).__init__(x, y, width, height, color)
        self.font = font
        self.title = title
        self.font_color = font_color
        self.is_open = False
        self.title_position = ((self.frame.x + self.frame.w / 2) - self.font.size(self.title)[0] / 2, 2)
        self.title_size = self.font.size(self.title)
        self.option_list = None
        self.reset_surface()

    def open(self, option_list):
        """
        Opens the menu, renders a surface with an options list (string list) and starts a loop that waits for user
        input. Once a selection is made (user event that is valid) the menu returns the index of the selected item from
        the option_list.
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
        super(Menu, self).render(self.parent.window)
        pygame.display.update()

        # Starting loop that waits for user input
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
        """
        Render function should never be called, once the open function has been called this menu seizes control of the
        program flow and waits for user input.
        """
        return None

    def reset_surface(self):
        """
        Need to find out exactly what this does, I believe that it is drawing lines using this point list to show
        which item from the option_list is currently selected.
        """
        self.surface = pygame.Surface(self.size())
        self.surface.blit(self.font.render(self.title, True, self.font_color), self.title_position)
        point_list = [(self.title_position[0] - 2, self.title_size[1] / 2),
                      (self.title_size[1] / 2, self.title_size[1] / 2),
                      (self.title_size[1] / 2, self.frame.h - self.title_size[1] / 2),
                      (self.frame.w - self.title_size[1] / 2, self.frame.h - self.title_size[1] / 2),
                      (self.frame.w - self.title_size[1] / 2, self.title_size[1] / 2),
                      (self.title_position[0] + self.title_size[0] + 2, self.title_size[1] / 2)]
        pygame.draw.lines(self.surface, self.font_color, False, point_list, 3)