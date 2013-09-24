'''
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

'''
import sys
import pygame
import shelve
import sprite
import slider
import button
import pixel
import console
import panel
import colorBox
import Image
import Tkinter
import tkFileDialog

filename = None
session = None

window = console.Console(835, 520)
font = pygame.font.SysFont('timesnewroman', 16, bold=True)
window.setCaption("Sprite Editor")
root = Tkinter.Tk()
root.withdraw()

options = {}
options['defaultextension'] = '.spr'
options['filetypes'] = [('sprite files', '.spr'), ('all files', '.*')]
options['initialdir'] = 'C:\\'
options['initialfile'] = 'default.spr'
options['title'] = 'File Browser'

exportOptions = {}
exportOptions['defaultextension'] = '.jpg'
exportOptions['initialdir'] = 'C:\\'
exportOptions['initialfile'] = 'default.jpg'
exportOptions['filetypes'] = [('JPEG files', '.jpg'), ('PNG files', '.png'), ('all files', '.*')]
exportOptions['title'] = 'Export as image'

importOptions = {}
importOptions['defaultextension'] = '.jpg'
importOptions['filetypes'] = [('jpeg files', '.jpg'), ('png files', '.png'), ('all files', '.*')]
importOptions['initialdir'] = 'C:\\'
importOptions['initialfile'] = 'default.jpg'
importOptions['title'] = 'Import Browser'


def loadSprite():
    global currentSprite, filename
    filename = tkFileDialog.askopenfilename(**options)
    if not filename == '':
        session = shelve.open(filename)
        currentSprite.pixelsInSprite = session['dimension']
        currentSprite.pixelSize = session['size']
        for x in range(currentSprite.pixelsInSprite[0]):
            for y in range(currentSprite.pixelsInSprite[1]):
                currentSprite.pixelArray[x][y].changeColor(session['%d %d' % (x, y)])
        session.close()
        currentSprite.generateSurface()
        pygame.event.pump()


def saveSprite():
    global session, filename
    filename = tkFileDialog.asksaveasfilename(**options)
    if not filename == '':
        session = shelve.open(filename)
        session['dimension'] = currentSprite.pixelsInSprite
        session['size'] = currentSprite.pixelSize
        for x in range(currentSprite.pixelsInSprite[0]):
            for y in range(currentSprite.pixelsInSprite[1]):
                session['%d %d' % (x, y)] = currentSprite.pixelArray[x][y].saveColor()
        session.close()
        pygame.event.pump()


def exportSprite():
    filename = tkFileDialog.asksaveasfilename(**exportOptions)
    if not filename == '':
        pygame.image.save(currentSprite.makeImage(), filename)
    pygame.event.pump()


def importSprite():
    global currentSprite
    filename = tkFileDialog.askopenfilename(**importOptions)
    if not filename == '':
        image = Image.open(filename)
        (width, height) = image.size
        chunkSize = (width / currentSprite.pixelsInSprite[0], height / currentSprite.pixelsInSprite[1])
        temparray = []
        pix = image.load()
        (red, green, blue) = (0, 0, 0)
        thisBlockSize = currentSprite.blockSize
        chunktotal = 0
        for xchunk in range(0, width - 1, chunkSize[0]):
            temparray.append([])
            for ychunk in range(0, height - 1, chunkSize[1]):
                (red, green, blue) = (0, 0, 0)
                for x in range(xchunk, xchunk + chunkSize[0]):
                    for y in range(ychunk, ychunk + chunkSize[1]):
                        if x < width and y < height:
                            temp = pix[x, y]
                            (red, green, blue) = (red + temp[0], green + temp[1], blue + temp[2])
                            chunktotal += 1
                temparray[xchunk / chunkSize[0]].append(pixel.Pixel((xchunk / chunkSize[0] * thisBlockSize[0], ychunk / chunkSize[1] * thisBlockSize[1]), thisBlockSize, (red / chunktotal, green / chunktotal, blue / chunktotal)))
                chunktotal = 0;
        currentSprite.pixelArray = temparray
        currentSprite.render(window.window)
        pygame.event.pump()


def main():
    global currentSprite
    currentSprite = sprite.Sprite((0, 0), (540, 520))
    currentSprite.setColorBox(chooserBox)
    window.addElement(currentSprite)
    control = False
    while True:
        window.drawElements()
        window.handleElementActions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                break
            elif event.type == pygame.USEREVENT:
                if event.info == 'right':
                    if control:
                        color = event.object.getColor()
                        redSlider.setIndex(color[0])
                        greenSlider.setIndex(color[1])
                        blueSlider.setIndex(color[2])
                    else:
                        event.object.changeColor(None)
            elif event.type == pygame.KEYDOWN:
                if event.key == 306:
                    control = True
            elif event.type == pygame.KEYUP:
                #print event
                if event.key == 273:
                    #up arrow
                    if event.mod == 1:
                        currentSprite.updatePixelSize(0, 1)
                    else:
                        currentSprite.updatePixelCount(0, -1)
                elif event.key == 274:
                    #down arrow
                    if event.mod == 1:
                        currentSprite.updatePixelSize(0, -1)
                    else:
                        currentSprite.updatePixelCount(0, 1)
                elif event.key == 275:
                    #right arrow
                    if event.mod == 1:
                        currentSprite.updatePixelSize(1, 0)
                    else:
                        currentSprite.updatePixelCount(1, 0)
                elif event.key == 276:
                    #left arrow
                    if event.mod == 1:
                        currentSprite.updatePixelSize(-1, 0)
                    else:
                        currentSprite.updatePixelCount(-1, 0)
                elif event.key == 306:
                    control = False

        chooserBox.updateColors((int(redSlider.value*255), int(greenSlider.value*255), int(blueSlider.value*255)))
        window.window.blit(font.render("RGB: (%s, %s, %s)" % chooserBox.color, True, (0, 0, 0)), (625, 355))
        window.window.blit(font.render("Sprite Dimensions: (%d,%d)" % (currentSprite.pixelsInSprite[0], currentSprite.pixelsInSprite[1]), True, (0, 0, 0)), (540+5, 400))
        window.window.blit(font.render("Pixel Dimension: (%d,%d)" % (currentSprite.pixelSize[0], currentSprite.pixelSize[1]), True, (0, 0, 0)), (540+5, 420))
        pygame.display.flip()

infoPanel = panel.Panel((540, 0), (295, 520), (255, 255, 255))
redSlider = slider.Slider((10, 295), (270, 15), (255, 200, 200), (255, 0, 0))
greenSlider = slider.Slider((10, 315), (270, 15), (200, 255, 200), (0, 255, 0))
blueSlider = slider.Slider((10, 335), (270, 15), (200, 200, 255), (0, 0, 255))
saveButton = button.Button((5, 375), (65, 20), "Save", font, saveSprite)
loadButton = button.Button((75, 375), (65, 20), "Load", font, loadSprite)
importButton = button.Button((145, 375), (65, 20), "Import", font, importSprite)
exportButton = button.Button((215, 375), (65, 20), "Export", font, exportSprite)
chooserBox = colorBox.ColorBox((10, 10), (275, 275))
window.addElement(infoPanel)
infoPanel.addElement(saveButton)
infoPanel.addElement(loadButton)
infoPanel.addElement(importButton)
infoPanel.addElement(exportButton)
infoPanel.addElement(chooserBox)
infoPanel.addElement(redSlider)
infoPanel.addElement(greenSlider)
infoPanel.addElement(blueSlider)

if __name__ == "__main__":
    main()