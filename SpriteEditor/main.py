"""
Issue List:

--May want to think about moving the cursor after the window closes! would get rid
    of the bug I'm having with the file browser i think.
--Suggest adding a Label object to the development kit
--want to display the sprite as it's actual size on the side.
    --only issue right now is that the actual pixelArray needs to also follow
        the size of the sprite when the user changes it!!

--Still having some small problems with clicking the buttons:
    error when exporting and such, pygame reports mouse as being clicked when it isn't
    don't know if this is my problem or someone else's, suggest talking to Randy

!!!!!!!ISSUES ON THE BACKBURNER!!!!!!!!!!!!!!!!!!!!
--displaying animation sequence on the left hand side(up to down)
    --ability to cycle through them

"""
import sys
import pygame
import shelve
import sprite
import core.gui.slider as Slider
import core.gui.button as Button
import pixel
import core.gui.console as Console
import core.gui.panel as Panel
import core.gui.colorBox as ColorBox
import Image
import Tkinter
import tkFileDialog

filename = None
session = None
current_sprite = None

window = Console.Console(835, 520)
font = pygame.font.SysFont('timesnewroman', 16, bold=True)
window.set_caption("Sprite Editor")
root = Tkinter.Tk()
root.withdraw()

options = {'defaultextension': '.spr',
           'filetypes': [('sprite files', '.spr'), ('all files', '.*')],
           'initialdir': 'C:\\',
           'initialfile': 'default.spr',
           'title': 'File Browser'}

exportOptions = {'defaultextension': '.jpg',
                 'initialdir': 'C:\\',
                 'initialfile': 'default.jpg',
                 'filetypes': [('JPEG files', '.jpg'), ('PNG files', '.png'), ('all files', '.*')],
                 'title': 'Export as image'}

import_options = {'defaultextension': '.jpg',
                  'filetypes': [('jpeg files', '.jpg'), ('png files', '.png'), ('all files', '.*')],
                  'initialdir': 'C:\\',
                  'initialfile': 'default.jpg',
                  'title': 'Import Browser'}


def load_sprite():
    """Loads a .spr Sprite file as the current_sprite and is used by the Load Button."""
    global current_sprite, filename, session
    filename = tkFileDialog.askopenfilename(**options)
    if not filename == '':
        session = shelve.open(filename)
        current_sprite.pixels_in_sprite = session['dimension']
        current_sprite.pixel_size = session['size']
        for x in range(current_sprite.pixels_in_sprite[0]):
            for y in range(current_sprite.pixels_in_sprite[1]):
                current_sprite.pixelArray[x][y].change_color(session['%d %d' % (x, y)])
        session.close()
        current_sprite.generate_surface()
        pygame.event.pump()


def save_sprite():
    """Saves the current_sprite as a .spr Sprite file and is used by the Save Button."""
    global session, filename, current_sprite
    filename = tkFileDialog.asksaveasfilename(**options)
    if not filename == '':
        session = shelve.open(filename)
        session['dimension'] = current_sprite.pixelsInSprite
        session['size'] = current_sprite.pixelSize
        for x in range(current_sprite.pixelsInSprite[0]):
            for y in range(current_sprite.pixelsInSprite[1]):
                session['%d %d' % (x, y)] = current_sprite.pixelArray[x][y].save_color()
        session.close()
        pygame.event.pump()


def export_sprite():
    """Exports the current_sprite as an image and is used by the Export Button."""
    file_name = tkFileDialog.asksaveasfilename(**exportOptions)
    if not file_name == '':
        pygame.image.save(current_sprite.make_image(), file_name)
    pygame.event.pump()


def import_sprite():
    """Imports an image file to the current_sprite and is used by the Import Button."""
    global current_sprite
    file_name = tkFileDialog.askopenfilename(**import_options)
    if not file_name == '':
        image = Image.open(file_name)
        (width, height) = image.size
        chunk_size = (width / current_sprite.pixels_in_sprite[0], height / current_sprite.pixels_in_sprite[1])
        temp_array = []
        pix = image.load()
        this_block_size = current_sprite.block_size
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
                temp_array[x_chunk / chunk_size[0]].append(pixel.Pixel((x_chunk / chunk_size[0] * this_block_size[0],
                                                                       y_chunk / chunk_size[1] * this_block_size[1]),
                                                                       this_block_size,
                                                                       (red / chunk_total, green / chunk_total,
                                                                       blue / chunk_total)))
                chunk_total = 0
        current_sprite.pixels = temp_array
        current_sprite.render(window.window)
        pygame.event.pump()


def main():
    """Main loop of the Sprite Editor.

    Loops through and draws the surface and handles user actions every iteration.
    """
    global current_sprite
    current_sprite = sprite.Sprite((0, 0), (540, 520))
    current_sprite.set_color_box(chooser_box)
    window.add_element(current_sprite)
    control = False
    while True:
        window.draw_elements()
        window.handle_element_actions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.USEREVENT:
                if event.info == 'right':
                    if control:
                        color = event.object.get_color()
                        redSlider.set_index(color[0])
                        greenSlider.set_index(color[1])
                        blueSlider.set_index(color[2])
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
                        current_sprite.update_pixel_size(0, 1)
                    else:
                        current_sprite.update_pixel_count(0, -1)
                elif event.key == 274:
                    #down arrow
                    if event.mod == 1:
                        current_sprite.update_pixel_size(0, -1)
                    else:
                        current_sprite.update_pixel_count(0, 1)
                elif event.key == 275:
                    #right arrow
                    if event.mod == 1:
                        current_sprite.update_pixel_size(1, 0)
                    else:
                        current_sprite.update_pixel_count(1, 0)
                elif event.key == 276:
                    #left arrow
                    if event.mod == 1:
                        current_sprite.update_pixel_size(-1, 0)
                    else:
                        current_sprite.update_pixel_count(-1, 0)
                elif event.key == 306:
                    control = False

        chooser_box.update_colors(
            (int(redSlider.value * 255), int(greenSlider.value * 255), int(blueSlider.value * 255)))
        window.window.blit(font.render("RGB: (%s, %s, %s)" % chooser_box.color, True, (0, 0, 0)), (625, 355))
        window.window.blit(font.render(
            "Sprite Dimensions: (%d,%d)" % (current_sprite.pixels_in_sprite[0], current_sprite.pixels_in_sprite[1]),
            True, (0, 0, 0)), (540 + 5, 400))
        window.window.blit(
            font.render("Pixel Dimension: (%d,%d)" % (current_sprite.pixel_size[0], current_sprite.pixel_size[1]), True,
                        (0, 0, 0)), (540 + 5, 420))
        pygame.display.flip()


info_panel = Panel.Panel((540, 0), (295, 520), (255, 255, 255))
redSlider = Slider.Slider((10, 295), (270, 15), (255, 200, 200), (255, 0, 0))
greenSlider = Slider.Slider((10, 315), (270, 15), (200, 255, 200), (0, 255, 0))
blueSlider = Slider.Slider((10, 335), (270, 15), (200, 200, 255), (0, 0, 255))
saveButton = Button.Button((5, 375), (65, 20), "Save", font, save_sprite)
loadButton = Button.Button((75, 375), (65, 20), "Load", font, load_sprite)
importButton = Button.Button((145, 375), (65, 20), "Import", font, import_sprite)
exportButton = Button.Button((215, 375), (65, 20), "Export", font, export_sprite)
chooser_box = ColorBox.ColorBox((10, 10), (275, 275))
window.add_element(info_panel)
info_panel.add_element(saveButton)
info_panel.add_element(loadButton)
info_panel.add_element(importButton)
info_panel.add_element(exportButton)
info_panel.add_element(chooser_box)
info_panel.add_element(redSlider)
info_panel.add_element(greenSlider)
info_panel.add_element(blueSlider)

if __name__ == "__main__":
    main()