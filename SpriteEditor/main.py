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
import sys, pygame, shelve, sprite, slider, button, textBox, math, console
import Tkinter, tkFileDialog, string

leftMouseHeld = False
rightMouseHeld = False
controlHeld = False
filename = None
session = None

window = console.Console(835, 520)
font = pygame.font.SysFont('dejavusans', 18, bold=True, italic=True)
window.setCaption("Sprite Editor")
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
    if xPos < 540:
        return (xPos/currentSprite.blockSize[0], yPos/currentSprite.blockSize[1])
    
def loadSprite():
    global currentSprite, session, filename
    filename = tkFileDialog.askopenfilename(**options)
    
    if not filename == '':
        session = shelve.open(filename)
        if session.has_key("testSprite"):
            currentSprite.pixelArray = session['array']
            currentSprite.pixelsInSprite = session['dimension']
            currentSprite.pixelSize = session['size']
        session.close()
        
def saveSprite():
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
        image = open(filename)
        (width, height) = image.size
        chunkSize = checkRatio(float(width), float(height))
        '''
        if chunkSize is null, no even divisor. need to cut off a bit of the picture perhaps
        '''
        spriteDimension = (width/chunkSize, height/chunkSize)
        tempSprite = sprite.Sprite((2, 2), spriteDimension)
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

'''        
def draw():
    global redSlider, blueSlider, greeSlider, loadButton, saveButton, importButton
    global currentSprite, pixelBox, spriteSizeBox, r, g, b
    pygame.draw.rect(window, (237, 246, 193), (540, 0, 835, 520))
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
        saveSprite()
    if loadButton.update(mpos, mpress):
        loadSprite()
    if importButton.update(mpos, mpress):
        importSprite()
    currentSprite.drawSpriteMain(window)
    r, g, b = redSlider.index, greenSlider.index, blueSlider.index
    pygame.draw.rect(window, (r, g, b), (540 + 75, 10, 150, 150), 0)
    window.blit(font.render("RGB: (%s, %s, %s)" % (r, g, b), True, (0, 0, 0)), (540 + 85, 160))
    window.blit(font.render("Sprite Representation!!", True, (0, 0, 0)), (540 + 11, 245))
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
    '''

def main():
    currentSprite = sprite.Sprite((2, 2), (20, 20))
    while True:
        window.drawElements()
        window.handleElementActions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                break
            elif event.type == pygame.USEREVENT:
                event.object.becomeActive(window)
            elif event.type == pygame.KEYDOWN: #hit any keystroke
                if event.key == 115: #hit 's'
                    window.toggleFullscreen()
    session.close()
        
pixelBox = textBox.TextBox((550, 200), (270, 20), font, "Pixel Size")
spriteSizeBox = textBox.TextBox((550, 250), (270, 20), font, "PPS")
saveButton = button.Button((540, 300), (80, 20), "Save", font, saveSprite)
redSlider = slider.Slider((540, 100), (270, 15), (255, 200, 200), (255, 0, 0))
greenSlider = slider.Slider((540, 120), (270, 15), (200, 255, 200), (0, 255, 0))
blueSlider = slider.Slider((540, 140), (270, 15), (200, 200, 255), (0, 0, 255))
loadButton = button.Button((540, 400), (80, 20), "Load", font, loadSprite)
importButton = button.Button((540, 350), (80, 20), "Import", font, importSprite)
window.addElement(saveButton)
window.addElement(loadButton)
window.addElement(importButton)
window.addElement(redSlider)
window.addElement(greenSlider)
window.addElement(blueSlider)
window.addElement(pixelBox)
window.addElement(spriteSizeBox)
if __name__ == "__main__": main()
    
    