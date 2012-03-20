'''
Needs some major refactoring!!! want to use my development kit to run this thang!!!



Issue List:
--want to display the sprite as it's actual size on the side.
    --only issue right now is that the actual pixelArray needs to also follow
        the size of the sprite when the user changes it!!
    
--options boxes need to draw the whole screen right when they are in their input loop...
    --one option is to integrate their input loop into the main input loop, would have to do some
        checking which would be lamerskates.
    
--having troubles deciding what I want to leave up to the users as far as pixels per sprite goes.
    Primarily this is troublesome when importing pictures
    --Tkinter window to take in sprite size from the user when importing
    --maybe have the arrow keys allow the user to change the sprite size (up and down change height, left right change width)
        
--Awesome importSprite is Awesome
    --pictures that do not have a common divisor between it's dimensions (width and height)
        will throw errors when trying to import.
        -need to find some alternatives in this case, perhaps throwing out the edges of the picture and
            going from there.
    --want to try using a smarter scheme to average each pixel, Mike suggested a binomial filter
        -gives more index to pixels near the center of the chunk, less for the edges.
        -filter may cause our import to be much slower, but it is only something that needs to be
            done once, computation should not be a problem.
        
        
!!!!!!!ISSUES ON THE BACKBURNER!!!!!!!!!!!!!!!!!!!!
--displaying animation sequence on the left hand side(up to down)
    --ability to cycle through them

'''
import sys, pygame, shelve, sprite, slider, button, textBox, Image, math
import Tkinter, tkFileDialog, string
from constants import *

leftMouseHeld = False
rightMouseHeld = False
controlHeld = False
filename = None
session = None
pygame.init()
font = pygame.font.SysFont('ubuntu', 18, bold=True)
buttonFont = pygame.font.SysFont('dejavusans', 18, bold=True, italic=True)
pygame.display.set_caption('Sprite Editor')
window = pygame.display.set_mode((Width, Height))
root = Tkinter.Tk()
root.withdraw()

options = {}
options['defaultextension'] = '.spr'
options['filetypes'] = [('sprite files', '.spr'), ('all files', '.*')]
options['initialdir'] = 'C:\\'
options['initialfile'] = 'default.spr'
options['title'] = 'File Browser'

importOptions = {}
importOptions['defaultextension'] = '.jpg'
importOptions['filetypes'] = [('jpeg files', '.jpg'), ('png files', '.png'), ('all files', '.*')]
importOptions['initialdir'] = 'C:\\'
importOptions['initialfile'] = 'default.jpg'
importOptions['title'] = 'Import Browser'

def convert((xPos, yPos)):
    global blockSize, currentSprite
    if xPos < EditingPanelSize[0]:
        return (xPos/currentSprite.blockSize[0], yPos/currentSprite.blockSize[1])
    
def loadSprite(spriteName):
    global currentSprite, session, filename
    filename = tkFileDialog.askopenfilename(**options)
    
    if not filename == '':
        session = shelve.open(filename)
        if session.has_key(spriteName):
            currentSprite.pixelArray = session['array']
            currentSprite.pixelsInSprite = session['dimension']
            currentSprite.pixelSize = session['size']
        session.close()
        
def saveSprite(spriteName):
    global session, filename
    filename = tkFileDialog.asksaveasfilename(**options)
    if not filename == '':
        session = shelve.open(filename)
        session['array'] = currentSprite.pixelArray
        session['dimension'] = currentSprite.pixelsInSprite
        session['size'] = currentSprite.pixelSize
        session.close()
        
def checkRatio(width, height):
    widthDiv = []
    heightDiv = []
    for each in range(1, int(math.sqrt(width)+1)):
        temp = width/each
        if temp%1 == 0:
            widthDiv.append(temp)
            widthDiv.append(each)
    for each in range(1, int(math.sqrt(height)+1)):
        temp = height/each
        if temp%1 == 0:
            heightDiv.append(temp)
            heightDiv.append(each)
    divisors = list(set(heightDiv) & set(widthDiv))
    divisors.sort()
    print divisors
    choices = []
    for each in divisors:
        if width/each > 8 and width/each < 30:
            choices.append(each)
    return int(choices[len(choices)/2])

def binomialFilter(xStart, yStart, size):
    (red, green, blue) = (0, 0, 0)
    for x in range(xStart, xStart+size):
        for y in range(yStart, yStart+size):
            '''want to separate these into 9 blocks with different weights as well'''
            #99!/(r!(99-r)!) 
            #depending on pixel location give it more weight for the average
    
def importSprite():
    global currentSprite
    filename = tkFileDialog.askopenfilename(**importOptions)
    if not filename == '':
        filename = string.split(filename, '/')[-1]
        image = Image.open(filename)
        (width, height) = image.size
        chunkSize = checkRatio(float(width), float(height))
        '''
        if chunkSize is null, no even divisor. need to cut off a bit of the picture perhaps
        '''
        spriteDimension = (width/chunkSize, height/chunkSize)
        tempSprite = sprite.Sprite(DefaultPixelSize, spriteDimension)
        pix = image.load()
        '''
        ~~Look into!
        binomial filter for pixel averaging (will weight the center values in the block more heavily!
        resulting in a better looking picture)
        '''
        (red, green, blue) = (0, 0, 0)
        chunkSquare = chunkSize*chunkSize
        for xchunk in range(0, width-1, chunkSize):
            for ychunk in range(0, height-1, chunkSize):
                #tempSprite.setPixelColor(window, xchunk/chunkSize, ychunk/chunkSize, binomialFilter(xchunk, ychunk, chunkSize))
                (red, green, blue) =(0, 0, 0)
                for x in range(xchunk, xchunk+chunkSize):
                    for y in range(ychunk, ychunk+chunkSize):
                        
                        temp = pix[x, y]
                        #print temp
                        (red, green, blue) = (red+temp[0], green+temp[1], blue+temp[2])
                print (red/chunkSquare, green, blue)
                tempSprite.setPixelColor(window, xchunk/chunkSize, ychunk/chunkSize, (red/chunkSquare, green/chunkSquare, blue/chunkSquare))
                
        currentSprite = tempSprite
        
def getInput():
    global mpress, mpos, mrel, leftMouseHeld, rightMouseHeld
    global currentSprite, controlHeld, redSlider, greenSlider, blueSlider, r, g, b
    mpress = pygame.mouse.get_pressed()
    mpos = pygame.mouse.get_pos()
    mrel = pygame.mouse.get_rel()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if mpos[0] < RightPanelX:
                xPixel, yPixel = convert(mpos)
                if event.button == 1:
                    if controlHeld:
                        (r, g, b) = currentSprite.getPixelColor(xPixel, yPixel)
                        redSlider.index = r
                        greenSlider.index = g
                        blueSlider.index = b
                    else:
                        leftMouseHeld = True
                        currentSprite.setPixelColor(window, xPixel, yPixel, (r, g, b))
                else:
                    rightMouseHeld = True
                    currentSprite.setPixelColor(window, xPixel, yPixel, (None, None, None))
        elif event.type == pygame.MOUSEMOTION:
            if mpos[0] < RightPanelX:
                xPixel, yPixel = convert(mpos)
                if leftMouseHeld == True:
                    leftMouseHeld = True
                    currentSprite.setPixelColor(window, xPixel, yPixel, (r, g, b))
                elif rightMouseHeld == True:
                    rightMouseHeld = True
                    currentSprite.setPixelColor(window, xPixel, yPixel, (None, None, None))
        elif event.type == pygame.MOUSEBUTTONUP:
            leftMouseHeld = False
            rightMouseHeld = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 115: #key 's'
                saveSprite("testSprite")
            elif event.key == 108: #key 'l'
                loadSprite("testSprite")
            elif event.key == 306 or event.key == 305: #key 'Ctrl'
                controlHeld = True
        elif event.type == pygame.KEYUP:
            if event.key == 306 or event.key == 305:
                controlHeld = False
                
def draw():
    global redSlider, blueSlider, greeSlider, loadButton, saveButton, importButton
    global currentSprite, pixelBox, spriteSizeBox, r, g, b
    pygame.draw.rect(window, RightPanelColor, (RightPanelX, 0, Width, Height))
    redSlider.update(mpos, mpress, mrel)
    blueSlider.update(mpos, mpress, mrel)
    greenSlider.update(mpos, mpress, mrel)
    if spriteSizeBox.update(mpos, mpress):
        temp = string.strip(spriteSizeBox.ask(window))
        temp = string.replace(temp[1:-1], " ", "")
        temp = string.split(temp, ',')
        currentSprite.pixelsInSprite = (int(temp[0]), int(temp[1]))
        currentSprite.drawSpriteMain(window)
        currentSprite.drawSpriteRepresentation(window)
    if pixelBox.update(mpos, mpress):
        temp = int(pixelBox.ask(window))
        currentSprite.pixelSize = (temp, temp)
        currentSprite.drawSpriteMain(window)
        currentSprite.drawSpriteRepresentation(window)
    if saveButton.update(mpos, mpress):
        saveSprite("testSprite")
    if loadButton.update(mpos, mpress):
        loadSprite("testSprite")
    if importButton.update(mpos, mpress):
        importSprite()
    currentSprite.drawSpriteMain(window)
    r, g, b = redSlider.index, greenSlider.index, blueSlider.index
    pygame.draw.rect(window, (r, g, b), (RightPanelX + 75, 10, 150, 150), 0)
    window.blit(font.render("RGB: (%s, %s, %s)" % (r, g, b), True, (0, 0, 0)), (RightPanelX + 85, 160))
    window.blit(font.render("Sprite Representation!!", True, (0, 0, 0)), (RightPanelX + 11, 245))
    currentSprite.drawSpriteRepresentation(window)
    pixelBox.drawBox(window, str(currentSprite.pixelSize[0]))
    spriteSizeBox.drawBox(window, str(currentSprite.pixelsInSprite))
    redSlider.render(window, 75, 20, 1)
    greenSlider.render(window, 75, 20, 2)
    blueSlider.render(window, 75, 20, 3)
    saveButton.render(window)
    loadButton.render(window)
    importButton.render(window)
    pygame.display.flip()

def main():
    global redSlider, blueSlider, greenSlider, loadButton, saveButton, importButton
    global currentSprite, pixelBox, spriteSizeBox
    redSlider = slider.Slider((255, 0, 0))
    greenSlider = slider.Slider((0, 255, 0))
    blueSlider = slider.Slider((0, 0, 255))
    saveButton = button.Button("Save", buttonFont, 350, 5, 1)
    loadButton = button.Button("Load", buttonFont, 350, 5, 2)
    importButton = button.Button("Import", buttonFont, 350, 5, 3)
    currentSprite = sprite.Sprite(DefaultPixelSize, DefaultSpriteDimension)
    pixelBox = textBox.TextBox("Pixel Size", RightPanelX + 10, 380)
    spriteSizeBox = textBox.TextBox("PPS", RightPanelX + 10, 400)
    while True:
        while pygame.event.peek():
            window.fill((255, 255, 255))
            getInput()
            draw()
    session.close()
        
if __name__ == "__main__": main()
    
    