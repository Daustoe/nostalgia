"""
Issue List:

--May want to think about moving the cursor after the window closes! would get rid
    of the bug I'm having with the file browser I think.
--want to display the sprite as it's actual size on the side.
    --can convert current_sprite to an image and display that image on the side
"""
import sys
import shelve
import Tkinter
import tkFileDialog
import pygame
from PIL import Image
from sprite import Sprite
from core.gui.button import Button
from core.gui.console import Console
from core.gui.view import View
from core.gui.label import Label
from colorBox import ColorBox


class SpriteEditor(Console):
    def __init__(self):
        super(SpriteEditor, self).__init__(835, 520)
        self.current_sprite = Sprite(0, 0, 540, 520)
        self.font = pygame.font.Font("Munro.ttf", 18)
        self.font.set_bold(True)
        self.set_caption("Sprite Editor")
        Tkinter.Tk().withdraw()
        self.fps_clock = pygame.time.Clock()
        self.options = {'defaultextension': '.spr',
                        'filetypes': [('sprite files', '.spr'), ('all files', '.*')],
                        'initialdir': 'C:\\',
                        'initialfile': 'default.spr',
                        'title': 'File Browser'}

        self.export_options = {'defaultextension': '.jpg',
                               'initialdir': 'C:\\',
                               'initialfile': 'default.jpg',
                               'filetypes': [('JPEG files', '.jpg'), ('PNG files', '.png'), ('all files', '.*')],
                               'title': 'Export as image'}

        self.import_options = {'defaultextension': '.jpg',
                               'filetypes': [('jpeg files', '.jpg'), ('png files', '.png'), ('all files', '.*')],
                               'initialdir': 'C:\\',
                               'initialfile': 'default.jpg',
                               'title': 'Import Browser'}

        info_panel = View(540, 0, 295, 520, pygame.Color('0xffffff'))
        color_label = Label(85, 535, 80, 20, self.font, "RGB: ")
        save_button = Button(5, 375, 65, 20, "Save", self.font)
        save_button.on_clicked.connect(self.save_sprite)
        load_button = Button(75, 375, 65, 20, "Load", self.font)
        load_button.on_clicked.connect(self.load_sprite)
        import_button = Button(145, 375, 65, 20, "Import", self.font)
        import_button.on_clicked.connect(self.import_sprite)
        export_button = Button(215, 375, 65, 20, "Export", self.font)
        export_button.on_clicked.connect(self.export_sprite)
        self.color_box = ColorBox(0, 0, 295, 350)
        self.add(info_panel)
        info_panel.add(save_button)
        info_panel.add(load_button)
        info_panel.add(import_button)
        info_panel.add(export_button)
        info_panel.add(self.color_box)
        # TODO fix below command, we shouldn't have to pass the current sprite the color box
        self.current_sprite.set_color_box(self.color_box)
        self.add(self.current_sprite)

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
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    hit_view = self.hit(mouse_pos)
                    if controlled_view and controlled_view.draggable:
                        controlled_view.mouse_drag(controlled_view, mouse_pos, event)
                    else:
                        hit_view.mouse_drag(controlled_view, mouse_pos, event)
            # TODO make GUI Labels out of these three font renders. That way the flip method handles them.
            self.window.blit(self.font.render("RGB: " + str(self.color_box.get_color()), True, (0, 0, 0)), (625, 355))
            self.window.blit(self.font.render("Sprite Dimensions: (%d,%d)" % (self.current_sprite.sprite_width,
                                                                              self.current_sprite.sprite_height),
                                              True, (0, 0, 0)), (540 + 5, 400))
            self.window.blit(self.font.render("Pixel Dimension: (%d,%d)" % (self.current_sprite.pixel_width,
                                                                            self.current_sprite.pixel_height),
                                              True, (0, 0, 0)), (540 + 5, 420))
            self.flip()
            self.fps_clock.tick(60)

    def load_sprite(self):
        """Loads a .spr Sprite file as the current_sprite and is used by the Load Button."""
        filename = tkFileDialog.askopenfilename(**self.options)
        if not filename == '':
            session = shelve.open(filename)
            self.current_sprite.sprite_size = session['dimension']
            self.current_sprite.pixel_size = session['size']
            for index in range(len(self.current_sprite.pixels)):
                self.current_sprite.pixels[index].change_color(session['%d' % index])
            session.close()
            self.current_sprite.generate_surface()
            pygame.event.pump()

    def save_sprite(self):
        """Saves the current_sprite as a .spr Sprite file and is used by the Save Button."""
        filename = tkFileDialog.asksaveasfilename(**self.options)
        if not filename == '':
            session = shelve.open(filename)
            session['dimension'] = (self.current_sprite.sprite_width, self.current_sprite.sprite_height)
            session['size'] = (self.current_sprite.pixel_width, self.current_sprite.pixel_height)
            for index in range(len(self.current_sprite.pixels)):
                session['%d' % index] = self.current_sprite.pixels[index].get_color()
            session.close()
            pygame.event.pump()

    def export_sprite(self):
        """Exports the current_sprite as an image and is used by the Export Button."""
        filename = tkFileDialog.asksaveasfilename(**self.export_options)
        if not filename == '':
            pygame.image.save(self.current_sprite.make_image(), filename)
        pygame.event.pump()

    def import_sprite(self):
        """Imports an image file to the current_sprite and is used by the Import Button."""
        filename = tkFileDialog.askopenfilename(**self.import_options)
        if not filename == '':
            self.current_sprite.image_to_sprite(Image.open(filename))
            self.current_sprite.render(self.window)
            pygame.event.pump()


if __name__ == "__main__":
    SpriteEditor()