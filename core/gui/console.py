import pygame
from pygame.locals import FULLSCREEN
#TODO themes for objects. All element objects will have stylize() method to set current them settings to it


class Console(object):
    """
    Console object, wraps the pygame Console object. Takes the width, height, and fullscreen boolean as arguments. The
    main benefit of this object is that it is set up to automatically handle rendering and the events of gui objects
    which inherit from the Element object of the gui.
    """
    def __init__(self, width, height, is_fullscreen=False):
        pygame.init()
        self.size = (width, height)
        self.is_fullscreen = is_fullscreen
        self.active_element = None
        self.position = (0, 0)
        self.window = pygame.display.set_mode(self.size)
        self.children = []
        self.message_box_list = []

    def draw_children(self):
        """
        Renders all of the consoles elements to the screen in the elements list to
        the window
        """
        self.window.fill((0, 0, 0))
        for each in self.children:
            if hasattr(each, 'render'):
                each.render(self.window)

    def handle_element_actions(self):
        """
        For elements that have actions (i.e. buttons, sliders, things you can click) call the actionEvent method
        (inherited from the Element object) on that object and send it all current relevant mouse information.

        Note: may need to change how we think about events on gui elements.
        """
        if pygame.event.peek():
            mouse_press = pygame.mouse.get_pressed()
            mouse_position = pygame.mouse.get_pos()
            mouse_movement = pygame.mouse.get_rel()
            for element in self.children:
                if hasattr(element, 'action_event'):
                    element.action_event(mouse_press, mouse_position, mouse_movement)

    def add(self, element):
        """
        Adds an element to the consoles list of elements to draw.
        """
        if element.__module__ == "messageBox":
            self.message_box_list.append(element)
        else:
            self.children.append(element)
        element.set_parent(self)

    @staticmethod
    def set_caption(caption):
        """ Sets the caption of the window."""
        pygame.display.set_caption(caption)

    def remove_element(self, element):
        """ Removes element from the list of console elements to draw. """
        self.children.remove(element)
        element.set_parent(None)

    def change_dimensions(self, width, height):
        """ Changes the dimensions of the window. """
        self.size = (width, height)
        self.window = pygame.display.set_mode(self.size)

    def toggle_fullscreen(self):
        """
        Toggles between fullscreen and windowed mode for our window, depending on how you set up your gui, this has the
        potential to blow things around on the screen.
        """
        screen = pygame.display.get_surface()
        tmp = screen.convert()
        caption = pygame.display.get_caption()
        cursor = pygame.mouse.get_cursor()

        size = (screen.get_width(), screen.get_height())
        flags = screen.get_flags()
        bits = screen.get_bitsize()

        pygame.display.quit()
        pygame.display.init()

        screen = pygame.display.set_mode(size, flags ^ FULLSCREEN, bits)
        screen.blit(tmp, (0, 0))
        pygame.display.set_caption(*caption)

        pygame.key.set_mods(0)
        pygame.mouse.set_cursor(*cursor)
        self.window = screen
        return self.window
