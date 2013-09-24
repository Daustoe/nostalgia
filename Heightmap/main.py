'''
Now I just need to link the button tools to the actual heightmap methods, the only problem that I
can see with this is that we need to set the variables of the methods based on values from gui
sliders. This may present a problem.

todo:
-want each history item to remember the state of the board at the time that tool is clicked.
-will allow user to change pieces in the history without rewriting data.
-need to solve the greedy cpu issues, will soak up too much.
-want to display values of the slider bars beside them.
'''

import sys
import pygame
import slider
import button
import console
import panel
import heightmap
import label

window = console.Console(960, 720)
font = pygame.font.SysFont('timesnewroman', 16, bold=True)
window.setCaption("Heightmap Generator")
myMap = heightmap.HeightMap(100, 100)
selectedPanel = None
historyElementOffset = 15
historyCount = 0
history = []
mapSquareSize = (720 / 100, 720 / 100)
backup = []
sandHeight = 0.12
grassHeight = 0.315
snowHeight = 0.785
keyIndex = [0,
            int(sandHeight * 255),
            int(sandHeight * 255) + 4,
            int(grassHeight * 255),
            int(grassHeight * 255) + 10,
            int(snowHeight * 255),
            int(snowHeight * 255) + 10,
            255]
colorKey = [(0, 0, 50),  # deep water
            (30, 30, 170),  # shallow water
            (114, 150, 71),  # sand
            (80, 120, 10),  # shrubs
            (17, 109, 7),  # grassland
            (120, 220, 120),  # snowy grass
            (208, 208, 239),  # snow
            (255, 255, 255)]


class HistoryObject:
    def __init__(self, panel, name):
        self.panel = panel
        self.name = name

    def historyAction(self):
        global infoPanel, selectedPanel, myMap
        if selectedPanel is not None:
            infoPanel.removeElement(selectedPanel)
        selectedPanel = self.panel
        infoPanel.addElement(self.panel)


def writeOut():
    global history
    filename = "hm.py"
    fileOut = open(filename, "w")
    header = "import heightmap\n\n" + "hm = heightmap.Heightmap(100,80)\n" + "def buildMap():\n"
    fileOut.write(header)
    '''
    need to be able to access elements in panel with a given name
    '''
    for each in history:
        if each.name == "change":
            fileOut.write("    hm.changeHeight({})\n".format(each.panel.heightSlider.value - .5))
        elif each.name == "valley":
            fileOut.write("    hm.addvalleys({},{},{},{})\n".format(int(
                each.panel.numberSlider.value * 50), int(each.panel.radiusSlider.value * 20),
                each.panel.radVarSlider.value, each.panel.heightSlider.value))
        elif each.name == "smooth":
            fileOut.write("    hm.smooth({},{},{})\n".format(each.panel.weightSlider.value * 20,
                each.panel.minSlider.value, each.panel.maxSlider.value * 5))
        elif each.name == "hill":
            fileOut.write("    hm.addHills({},{},{},{})\n".format(int(
                each.panel.hillNumSlider.value * 50), int(each.panel.radiusSlider.value * 20),
                each.panel.radiusVarSlider.value, each.panel.heightSlider.value))
        elif each.name == "normal":
            fileOut.write("    hm.normalize({},{})\n".format(each.panel.minSlider.value,
            each.panel.maxSlider.value))
        elif each.name == "rain":
            fileOut.write("    hm.rainErosion({},{},{})\n".format(int(
                each.panel.rainDropsSlider.value * 20000), each.panel.erosionSlider.value,
                each.panel.sedimentSlider.value))
    fileOut.close()


def doneAction():
    if selectedPanel.name == "change":
        myMap.changeHeights(selectedPanel.heightSlider.value * 2 - 1)
    elif selectedPanel.name == "valley":
        myMap.addValleys(int(selectedPanel.numberSlider.value * 50), int(
            selectedPanel.radiusSlider.value * 25), selectedPanel.radVarSlider.value,
            selectedPanel.heightSlider.value)
    elif selectedPanel.name == "hill":
        myMap.addHills(int(selectedPanel.hillNumSlider.value * 50), int(
            selectedPanel.radiusSlider.value * 25), selectedPanel.radiusVarSlider.value,
            selectedPanel.heightSlider.value)
    elif selectedPanel.name == "normal":
        myMap.normalize(selectedPanel.minSlider.value, selectedPanel.maxSlider.value)
    elif selectedPanel.name == "smooth":
        myMap.smooth(int(selectedPanel.weightSlider.value * 10), selectedPanel.minSlider.value,
            selectedPanel.maxSlider.value)
    elif selectedPanel.name == "rain":
        myMap.rainErosion(int(selectedPanel.rainDropsSlider.value * 20000),
            selectedPanel.erosionSlider.value, selectedPanel.sedimentSlider.value)


def changeButtonAction():
    global selectedPanel, historyElementOffset, font, history, myMap
    if selectedPanel is not None:
        infoPanel.removeElement(selectedPanel)
    changePanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    changeLabel = label.Label((5, 2), (230, 8), font, "------valleys------", (230, 230, 230))
    changePanel.addElement(changeLabel)
    heightLabel = label.Label((0, 15), (80, 8), font, "height", (230, 230, 230))
    heightSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (230, 230, 230))
    changePanel.addElement(heightLabel)
    changePanel.addElement(heightSlider)
    doneButton = button.Button((5, 80), (100, 10), "done", font, myMap.changeHeights, (230, 230,
        230), (10, 10, 50))
    changePanel.addElement(doneButton)
    changePanel.name = "change"
    heightSlider.setValue(.55)
    selectedPanel = changePanel
    changePanel.heightSlider = heightSlider
    infoPanel.addElement(changePanel)
    history.append(HistoryObject(changePanel, "change"))
    historyPanel.addElement(button.Button((5, historyElementOffset), (220, 10), "change z", font,
        history[-1].historyAction, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.changeHeights(.1)


def valleyButtonAction():
    global selectedPanel, historyElementOffset, font, history, myMap
    if selectedPanel is not None:
        infoPanel.removeElement(selectedPanel)
    valleyPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    valleyLabel = label.Label((5, 2), (230, 8), font, "------valleys------", (230, 230, 230))
    valleyPanel.addElement(valleyLabel)
    numberLabel = label.Label((0, 15), (80, 8), font, "number", (230, 230, 230))
    numberSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    radiusSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    radiusLabel = label.Label((0, 30), (80, 8), font, "radius", (230, 230, 230))
    valleyPanel.addElement(numberLabel)
    valleyPanel.addElement(numberSlider)
    valleyPanel.addElement(radiusSlider)
    valleyPanel.addElement(radiusLabel)
    radVarLabel = label.Label((0, 45), (80, 8), font, "radVar", (230, 230, 230))
    radVarSlider = slider.Slider((80, 45), (140, 8), (50, 50, 50), (230, 230, 230))
    valleyPanel.addElement(radVarLabel)
    valleyPanel.addElement(radVarSlider)
    heightLabel = label.Label((0, 60), (80, 8), font, "height", (230, 230, 230))
    heightSlider = slider.Slider((80, 60), (140, 8), (50, 50, 50), (230, 230, 230))
    valleyPanel.addElement(heightLabel)
    valleyPanel.addElement(heightSlider)
    selectedPanel = valleyPanel
    valleyPanel.numberSlider = numberSlider
    valleyPanel.radiusSlider = radiusSlider
    valleyPanel.radVarSlider = radVarSlider
    valleyPanel.heightSlider = heightSlider
    valleyPanel.name = "valley"
    infoPanel.addElement(valleyPanel)
    history.append(HistoryObject(valleyPanel, "valley"))
    historyPanel.addElement(button.Button((5, historyElementOffset), (220, 10), "valleys", font,
        history[-1].historyAction, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.addValleys(25, 10, .5, .5)


def smoothButtonAction():
    global selectedPanel, historyElementOffset, font, history, myMap
    if selectedPanel is not None:
        infoPanel.removeElement(selectedPanel)
    smoothPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    smoothLabel = label.Label((5, 2), (230, 8), font, "------smooth------", (230, 230, 230))
    smoothPanel.addElement(smoothLabel)
    minLabel = label.Label((0, 15), (80, 8), font, "min", (230, 230, 230))
    minSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    maxSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    maxLabel = label.Label((0, 30), (80, 8), font, "max", (230, 230, 230))
    smoothPanel.addElement(minLabel)
    smoothPanel.addElement(minSlider)
    smoothPanel.addElement(maxSlider)
    smoothPanel.addElement(maxLabel)
    weightLabel = label.Label((0, 45), (80, 8), font, "weight", (230, 230, 230))
    weightSlider = slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    smoothPanel.addElement(weightLabel)
    smoothPanel.addElement(weightSlider)
    selectedPanel = smoothPanel
    smoothPanel.minSlider = minSlider
    smoothPanel.maxSlider = maxSlider
    smoothPanel.weightSlider = weightSlider
    smoothPanel.name = "smooth"
    infoPanel.addElement(smoothPanel)
    history.append(HistoryObject(smoothPanel, "smooth"))
    historyPanel.addElement(button.Button((5, historyElementOffset), (220, 10), "smooth", font,
        history[-1].historyAction, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.smooth(2, 0, 1.95)


def normalButtonAction():
    global selectedPanel, historyElementOffset, font, history, myMap
    if selectedPanel is not None:
        infoPanel.removeElement(selectedPanel)
    normPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    normLabel = label.Label((5, 2), (230, 8), font, "------normalize------", (230, 230, 230))
    normPanel.addElement(normLabel)
    minLabel = label.Label((0, 15), (80, 8), font, "min", (230, 230, 230))
    minSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    maxSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    maxLabel = label.Label((0, 30), (80, 8), font, "max", (230, 230, 230))
    normPanel.addElement(minLabel)
    normPanel.addElement(minSlider)
    normPanel.addElement(maxSlider)
    normPanel.addElement(maxLabel)
    selectedPanel = normPanel
    normPanel.minSlider = minSlider
    normPanel.maxSlider = maxSlider
    infoPanel.addElement(normPanel)
    normPanel.name = "normal"
    history.append(HistoryObject(normPanel, "normal"))
    historyPanel.addElement(button.Button((5, historyElementOffset), (220, 10), "normalize", font,
        history[-1].historyAction, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.normalize(0, 1)


def hillButtonAction():
    global selectedPanel, font, history, historyElementOffset, myMap
    if selectedPanel is not None:
        infoPanel.removeElement(selectedPanel)
    hillPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    hillLabel = label.Label((5, 2), (230, 8), font, "------hills------", (230, 230, 230))
    hillPanel.addElement(hillLabel)
    hillNumSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    hillNumLabel = label.Label((0, 15), (80, 8), font, "hillnum", (230, 230, 230))
    hillPanel.addElement(hillNumLabel)
    hillPanel.addElement(hillNumSlider)
    heightSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    heightLabel = label.Label((0, 30), (80, 8), font, "height", (230, 230, 230))
    hillPanel.addElement(heightLabel)
    hillPanel.addElement(heightSlider)
    radiusSlider = slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    radiusLabel = label.Label((0, 45), (80, 8), font, "radius", (230, 230, 230))
    hillPanel.addElement(radiusLabel)
    hillPanel.addElement(radiusSlider)
    radiusVarSlider = slider.Slider((80, 60), (140, 8), (50, 50, 50), (150, 150, 150))
    radiusVarLabel = label.Label((0, 60), (80, 8), font, "radiusVar", (230, 230, 230))
    hillPanel.addElement(radiusVarLabel)
    hillPanel.addElement(radiusVarSlider)
    hillPanel.hillNumSlider = hillNumSlider
    hillPanel.radiusSlider = radiusSlider
    hillPanel.radiusVarSlider = radiusVarSlider
    hillPanel.heightSlider = heightSlider
    selectedPanel = hillPanel
    hillPanel.name = "hill"
    infoPanel.addElement(hillPanel)
    history.append(HistoryObject(hillPanel, "hill"))
    historyPanel.addElement(button.Button((5, historyElementOffset), (220, 10), "hills", font,
        history[-1].historyAction, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.addHills(25, 10, .5, .5)


def rainButtonAction():
    global selectedPanel, font, history, historyElementOffset
    if selectedPanel is not None:
        infoPanel.removeElement(selectedPanel)
    rainPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    rainLabel = label.Label((5, 2), (230, 8), font, "------rain------", (230, 230, 230))
    rainPanel.addElement(rainLabel)
    rainDropsSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    rainDropsLabel = label.Label((0, 15), (80, 8), font, "drops", (230, 230, 230))
    rainPanel.addElement(rainDropsSlider)
    rainPanel.addElement(rainDropsLabel)
    erosionSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    erosionLabel = label.Label((0, 30), (80, 8), font, "erosion", (230, 230, 230))
    rainPanel.addElement(erosionSlider)
    rainPanel.addElement(erosionLabel)
    sedimentSlider = slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    sedimentLabel = label.Label((0, 45), (80, 8), font, "sediment", (230, 230, 230))
    rainPanel.addElement(sedimentSlider)
    rainPanel.addElement(sedimentLabel)
    rainPanel.rainDropsSlider = rainDropsSlider
    rainPanel.erosionSlider = erosionSlider
    rainPanel.sedimentSlider = sedimentSlider
    selectedPanel = rainPanel
    rainPanel.name = "rain"
    infoPanel.addElement(rainPanel)
    history.append(HistoryObject(rainPanel, "rain"))
    historyPanel.addElement(button.Button((5, historyElementOffset), (220, 10), "rain", font,
        history[-1].historyAction, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.rainErosion(1000, .05, .05)


def main():
    global myMap, mapSquareSize, colorKey
    while True:
        window.drawElements()
        window.handleElementActions()
        #need to perform all the operations
        for x in range(myMap.width):
            for y in range(myMap.height):
                color = None
                if myMap.heightmap[x][y] <= 0.08:
                    color = colorKey[0]
                elif myMap.heightmap[x][y] < 0.12:
                    color = colorKey[1]
                elif myMap.heightmap[x][y] < 0.21:
                    color = colorKey[2]
                elif myMap.heightmap[x][y] < 0.315:
                    color = colorKey[3]
                elif myMap.heightmap[x][y] < 0.6:
                    color = colorKey[4]
                elif myMap.heightmap[x][y] < 0.785:
                    color = colorKey[5]
                elif myMap.heightmap[x][y] < 0.9:
                    color = colorKey[6]
                else:
                    color = colorKey[7]
                temp = pygame.Surface(mapSquareSize)
                temp.fill(color)
                window.window.blit(temp, (x * mapSquareSize[0], y * mapSquareSize[1]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                break
        pygame.display.flip()

infoPanel = panel.Panel((720, 0), (240, 720), (200, 200, 200))
toolPanel = panel.Panel((5, 5), (230, 200), (10, 10, 50))
toolPanelLabel = label.Label((5, 2), (230, 8), font, "------tools------", (230, 230, 230))
toolPanel.addElement(toolPanelLabel)

normButton = button.Button((5, 20), (220, 10), "normalize", font, normalButtonAction, (230, 230,
    230), (10, 10, 50))
toolPanel.addElement(normButton)

hillButton = button.Button((5, 50), (220, 10), "hills", font, hillButtonAction, (230, 230, 230),
    (10, 10, 50))
toolPanel.addElement(hillButton)

rainButton = button.Button((5, 65), (220, 10), "rain", font, rainButtonAction, (230, 230, 230),
    (10, 10, 50))
toolPanel.addElement(rainButton)

valleyButton = button.Button((5, 35), (220, 10), "valleys", font, valleyButtonAction, (230, 230,
    230), (10, 10, 50))
toolPanel.addElement(valleyButton)

smoothButton = button.Button((5, 80), (220, 10), "smooth", font, smoothButtonAction, (230, 230,
    230), (10, 10, 50))
toolPanel.addElement(smoothButton)

changeButton = button.Button((5, 95), (220, 10), "change z", font, changeButtonAction, (230, 230,
    230), (10, 10, 50))
toolPanel.addElement(changeButton)

writeButton = button.Button((5, 110), (220, 10), "write to file", font, writeOut, (230, 230, 230),
    (10, 10, 50))
toolPanel.addElement(writeButton)

doneButton = button.Button((5, 295), (230, 15), "done", font, doneAction, (230, 230, 230),
    (10, 10, 50))
infoPanel.addElement(doneButton)

infoPanel.addElement(toolPanel)

historyPanel = panel.Panel((5, 315), (230, 400), (10, 10, 50))
historyLabel = label.Label((5, 2), (230, 8), font, "------history------", (230, 230, 230))
historyPanel.addElement(historyLabel)
infoPanel.addElement(historyPanel)
window.addElement(infoPanel)
writeOut()
if __name__ == "__main__":
    main()