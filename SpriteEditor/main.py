"""
Issue List:

--May want to think about moving the cursor after the window closes! would get rid
    of the bug I'm having with the file browser i think.
--want to display the sprite as it's actual size on the side.
    --can convert current_sprite to an image and display that image on the side

--Still having some small problems with clicking the buttons:
    error when exporting and such, pygame reports mouse as being clicked when it isn't
    don't know if this is my problem or someone else's, suggest talking to Randy
"""
import sys
import pygame
import shelve
import sprite
import core.gui.button as Button
import core.gui.console as Console
import core.gui.panel as Panel
import core.gui.colorBox as ColorBox
from PIL import Image
import Tkinter
import tkFileDialog


class SpriteEditor(Console.Console):
    def __init__(self):
        super(SpriteEditor, self).__init__(835, 520)
        self.current_sprite = sprite.Sprite(0, 0, 540, 520)
        self.font = pygame.font.SysFont('timesnewroman', 16, bold=True)
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

        info_panel = Panel.Panel(540, 0, 295, 520, pygame.Color(255, 255, 255))
        save_button = Button.Button(5, 375, 65, 20, "Save", self.font, self.save_sprite)
        load_button = Button.Button(75, 375, 65, 20, "Load", self.font, self.load_sprite)
        import_button = Button.Button(145, 375, 65, 20, "Import", self.font, self.import_sprite)
        export_button = Button.Button(215, 375, 65, 20, "Export", self.font, self.export_sprite)
        self.color_box = ColorBox.ColorBox(0, 0, 295, 350)
        self.add_element(info_panel)
        info_panel.add_element(save_button)
        info_panel.add_element(load_button)
        info_panel.add_element(import_button)
        info_panel.add_element(export_button)
        info_panel.add_element(self.color_box)
        self.current_sprite.set_color_box(self.color_box)
        self.add_element(self.current_sprite)

        self.main_loop()

    def main_loop(self):
        #may want to add a list of keys down to track what keyboard keys are currently being held down.
        #this will let us remove the control variable and just check our list of keys for 'Ctrl' and so on.
        control = False
        while True:
            self.draw_elements()
            self.handle_element_actions()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.USEREVENT:
                    if event.info == 'right':
                        if control:
                            self.color_box.set_color(event.object.get_color())
                        else:
                            event.object.change_color(None)
                elif event.type == pygame.KEYDOWN:
                    if event.key == 306:
                        control = True
                elif event.type == pygame.KEYUP:
                    #print event
                    if event.key == 273:
                        #up arrow
                        if event.mod == 1:
                            self.current_sprite.update_pixel_size(0, 1)
                        else:
                            self.current_sprite.update_pixel_count(0, -1)
                    elif event.key == 274:
                        #down arrow
                        if event.mod == 1:
                            self.current_sprite.update_pixel_size(0, -1)
                        else:
                            self.current_sprite.update_pixel_count(0, 1)
                    elif event.key == 275:
                        #right arrow
                        if event.mod == 1:
                            self.current_sprite.update_pixel_size(1, 0)
                        else:
                            self.current_sprite.update_pixel_count(1, 0)
                    elif event.key == 276:
                        #left arrow
                        if event.mod == 1:
                            self.current_sprite.update_pixel_size(-1, 0)
                        else:
                            self.current_sprite.update_pixel_count(-1, 0)
                    elif event.key == 306:
                        control = False
            self.window.blit(self.font.render("RGB: " + str(self.color_box.get_color()), True, (0, 0, 0)), (625, 355))
            self.window.blit(self.font.render("Sprite Dimensions: (%d,%d)" % (self.current_sprite.pixels_in_sprite[0],
                                                                              self.current_sprite.pixels_in_sprite[1]),
                                              True, (0, 0, 0)), (540 + 5, 400))
            self.window.blit(self.font.render("Pixel Dimension: (%d,%d)" % (self.current_sprite.pixel_size[0],
                                                                            self.current_sprite.pixel_size[1]),
                                              True, (0, 0, 0)), (540 + 5, 420))
            pygame.display.flip()
            self.fps_clock.tick(30)

    def load_sprite(self):
        """Loads a .spr Sprite file as the current_sprite and is used by the Load Button."""
        filename = tkFileDialog.askopenfilename(**self.options)
        if not filename == '':
            session = shelve.open(filename)
            self.current_sprite.pixels_in_sprite = session['dimension']
            self.current_sprite.pixel_size = session['size']
            for x in range(self.current_sprite.pixels_in_sprite[0]):
                for y in range(self.current_sprite.pixels_in_sprite[1]):
                    self.current_sprite.pixels[x][y].change_color(session['%d %d' % (x, y)])
            session.close()
            self.current_sprite.generate_surface()
            pygame.event.pump()

    def save_sprite(self):
        """Saves the current_sprite as a .spr Sprite file and is used by the Save Button."""
        filename = tkFileDialog.asksaveasfilename(**self.options)
        #perhaps do something here to prevent key from sticking in gui and reopening
        if not filename == '':
            session = shelve.open(filename)
            session['dimension'] = self.current_sprite.pixels_in_sprite
            session['size'] = self.current_sprite.pixel_size
            for x in range(self.current_sprite.pixels_in_sprite[0]):
                for y in range(self.current_sprite.pixels_in_sprite[1]):
                    session['%d %d' % (x, y)] = self.current_sprite.pixels[x][y].save_color()
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