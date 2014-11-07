"""
Issue List:

--need a delete/remove pixel functionality enabled. We were using right click, but may want a toggle button
  to switch between draw and erase.
--want to display the sprite as it's actual size on the side.
    --can convert current_sprite to an image and display that image on the side
--move color palette to the left, shrink the width.
    --color picker should be a panel that only shows up when user clicks currently selected color
      will give the option to pick a new color. User can select colors from palette of colors as well
"""
import sys
import shelve
from Tkinter import Tk
import tkFileDialog
import pygame
from PIL import Image
from sprite import Sprite
from core.gui.button import Button
from core.gui.console import Console
from core.gui.dialog import DialogView
from core.gui.view import View
from colorPalette import ColorPalette


class SpriteEditor(Console):
    def __init__(self):
        super(SpriteEditor, self).__init__(1080, 720)
        self.sprite = Sprite(160, 50, 520, 520)
        self.font = pygame.font.Font("resources/Munro.ttf", 18)
        self.font.set_bold(True)
        self.set_caption("Sprite Editor")
        Tk().withdraw()
        self.fps_clock = pygame.time.Clock()
        self.options = {'defaultextension': '.spr',
                        'filetypes': [('sprite files', '.spr'), ('all files', '.*')],
                        'initialdir': 'C:\\',
                        'initialfile': 'default.spr',
                        'title': 'File Browser'}

        self.export_options = {'defaultextension': '.png',
                               'initialdir': 'C:\\',
                               'initialfile': 'default.png',
                               'filetypes': [('PNG files', '.png'), ('all files', '.*')],
                               'title': 'Export as image'}

        self.import_options = {'defaultextension': '.jpg',
                               'filetypes': [('jpeg files', '.jpg'), ('png files', '.png'), ('all files', '.*')],
                               'initialdir': 'C:\\',
                               'initialfile': 'default.jpg',
                               'title': 'Import Browser'}

        save_button = Button(5, 5, 65, 20, "Save", self.font)
        save_button.on_clicked.connect(self.save_sprite)
        load_button = Button(75, 5, 65, 20, "Load", self.font)
        load_button.on_clicked.connect(self.load_sprite)
        import_button = Button(145, 5, 65, 20, "Import", self.font)
        import_button.on_clicked.connect(self.import_sprite)
        export_button = Button(215, 5, 65, 20, "Export", self.font)
        export_button.on_clicked.connect(self.export_sprite)
        self.palette = ColorPalette(0, 30, 110, 690, self.font)
        self.background = View(0, 0, 1080, 720)
        self.top_menu = View(0, 0, 1080, 30, pygame.Color('0x101020'))
        self.top_menu.add(save_button)
        self.top_menu.add(load_button)
        self.top_menu.add(import_button)
        self.top_menu.add(export_button)
        self.add(self.background)
        self.add(self.palette)
        self.add(self.top_menu)
        self.sprite.set_color_box(self.palette)
        self.add(self.sprite)

        self.main_loop()

    def main_loop(self):
        controlled_view = None
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = pygame.mouse.get_pos()
                    hit_view = self.hit(mouse_pos)
                    hit_view.mouse_up(event.button, mouse_pos)
                    controlled_view = None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    hit_view = self.hit(mouse_pos)
                    controlled_view = hit_view
                    hit_view.mouse_down(event.button, mouse_pos)
                elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed != (0, 0, 0):
                    mouse_pos = pygame.mouse.get_pos()
                    hit_view = self.hit(mouse_pos)
                    if controlled_view and controlled_view.draggable:
                        controlled_view.mouse_drag(controlled_view, mouse_pos, event)
                    elif hit_view is not None:
                        hit_view.mouse_drag(controlled_view, mouse_pos, event)
            self.flip()
            self.fps_clock.tick(120)

    def load_sprite(self):
        """Loads a .spr Sprite file as the current_sprite and is used by the Load Button."""
        filename = tkFileDialog.askopenfilename(**self.options)
        if not filename == '':
            self.palette.reset()
            session = shelve.open(filename)
            self.sprite.sprite_width, self.sprite.sprite_height = session['dimension']
            self.sprite.pixel_width, self.sprite.pixel_height = session['size']
            for index in range(len(self.sprite.pixels)):
                color = session['%d' % index]
                self.sprite.pixels[index].change_color(color)
                self.sprite.color_box.add_to_history(color)
            session.close()
            pygame.event.pump()

    def save_sprite(self):
        """Saves the current_sprite as a .spr Sprite file and is used by the Save Button."""
        filename = tkFileDialog.asksaveasfilename(**self.options)
        if not filename == '':
            session = shelve.open(filename)
            session['dimension'] = self.sprite.sprite_size()
            session['size'] = self.sprite.pixel_size()
            for index in range(len(self.sprite.pixels)):
                color = self.sprite.pixels[index].get_color()
                session['%d' % index] = color
            session.close()
            pygame.event.pump()

    def export_sprite(self):
        """Exports the current_sprite as an image and is used by the Export Button."""
        filename = tkFileDialog.asksaveasfilename(**self.export_options)
        if not filename == '':
            pygame.image.save(self.sprite.make_image(), filename)
        pygame.event.pump()

    def import_sprite(self):
        """Imports an image file to the current_sprite and is used by the Import Button."""
        filename = tkFileDialog.askopenfilename(**self.import_options)
        if not filename == '':
            image = Image.open(filename).resize(self.sprite.sprite_size(), Image.BICUBIC)
            self.sprite.image_to_sprite(image)
            self.sprite.render(self.window)
            pygame.event.pump()


if __name__ == "__main__":
    SpriteEditor()