"""
Now I just need to link the button tools to the actual heightmap methods, the only problem that I
can see with this is that we need to set the variables of the methods based on values from gui
sliders. This may present a problem.

todo:
-want each history item to remember the state of the board at the time that tool is clicked.
-will allow user to change pieces in the history without rewriting data.
-need to solve the greedy cpu issues, will soak up too much.
-want to display values of the slider bars beside them.
"""

import sys
import pygame
import core.gui.slider as Slider
import core.gui.button as Button
import core.gui.console as Console
import core.gui.panel as Panel
import heightmap
import core.gui.label as Label

window = Console.Console(960, 720)
font = pygame.font.SysFont('timesnewroman', 16, bold=True)
window.set_caption("Heightmap Generator")
myMap = heightmap.HeightMap(100, 100)
selected_panel = None
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

    def history_action(self):
        global infoPanel, selected_panel, myMap
        if selected_panel is not None:
            infoPanel.remove_element(selected_panel)
        selected_panel = self.panel
        infoPanel.add_element(self.panel)


def write_out():
    global history
    filename = "hm.py"
    file_out = open(filename, "w")
    header = "import heightmap\n\n" + "hm = heightmap.Heightmap(100,80)\n" + "def buildMap():\n"
    file_out.write(header)
    # need to be able to access elements in panel with a given name

    for each in history:
        if each.name == "change":
            file_out.write("    hm.changeHeight({})\n".format(each.panel.heightSlider.value - .5))
        elif each.name == "valley":
            file_out.write("    hm.addvalleys({},{},{},{})\n".format(int(
                each.panel.numberSlider.value * 50), int(each.panel.radiusSlider.value * 20),
                each.panel.radVarSlider.value, each.panel.heightSlider.value))
        elif each.name == "smooth":
            file_out.write("    hm.smooth({},{},{})\n".format(each.panel.weightSlider.value * 20,
                                                              each.panel.minSlider.value,
                                                              each.panel.maxSlider.value * 5))
        elif each.name == "hill":
            file_out.write("    hm.addHills({},{},{},{})\n".format(int(
                each.panel.hillNumSlider.value * 50), int(each.panel.radiusSlider.value * 20),
                each.panel.radiusVarSlider.value, each.panel.heightSlider.value))
        elif each.name == "normal":
            file_out.write("    hm.normalize({},{})\n".format(each.panel.minSlider.value, each.panel.maxSlider.value))
        elif each.name == "rain":
            file_out.write("    hm.rainErosion({},{},{})\n".format(int(each.panel.rainDropsSlider.value * 20000),
                                                                   each.panel.erosionSlider.value,
                                                                   each.panel.sedimentSlider.value))
    file_out.close()


def done_action():
    if selected_panel.name == "change":
        myMap.changeHeights(selected_panel.heightSlider.value * 2 - 1)
    elif selected_panel.name == "valley":
        myMap.addValleys(int(selected_panel.numberSlider.value * 50), int(
            selected_panel.radiusSlider.value * 25), selected_panel.radVarSlider.value,
                         selected_panel.heightSlider.value)
    elif selected_panel.name == "hill":
        myMap.addHills(int(selected_panel.hillNumSlider.value * 50), int(
            selected_panel.radiusSlider.value * 25), selected_panel.radiusVarSlider.value,
                       selected_panel.heightSlider.value)
    elif selected_panel.name == "normal":
        myMap.normalize(selected_panel.minSlider.value, selected_panel.maxSlider.value)
    elif selected_panel.name == "smooth":
        myMap.smooth(int(selected_panel.weightSlider.value * 10), selected_panel.minSlider.value,
                     selected_panel.maxSlider.value)
    elif selected_panel.name == "rain":
        myMap.rainErosion(int(selected_panel.rainDropsSlider.value * 20000),
                          selected_panel.erosionSlider.value, selected_panel.sedimentSlider.value)


def changeButtonAction():
    global selected_panel, historyElementOffset, font, history, myMap
    if selected_panel is not None:
        infoPanel.remove_element(selected_panel)
    changePanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    changeLabel = label.Label((5, 2), (230, 8), font, "------valleys------", (230, 230, 230))
    changePanel.add_element(changeLabel)
    heightLabel = label.Label((0, 15), (80, 8), font, "height", (230, 230, 230))
    heightSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (230, 230, 230))
    changePanel.add_element(heightLabel)
    changePanel.add_element(heightSlider)
    doneButton = button.Button((5, 80), (100, 10), "done", font, myMap.changeHeights, (230, 230,
                                                                                       230), (10, 10, 50))
    changePanel.add_element(doneButton)
    changePanel.name = "change"
    heightSlider.setValue(.55)
    selected_panel = changePanel
    changePanel.heightSlider = heightSlider
    infoPanel.add_element(changePanel)
    history.append(HistoryObject(changePanel, "change"))
    historyPanel.add_element(button.Button((5, historyElementOffset), (220, 10), "change z", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.changeHeights(.1)


def valleyButtonAction():
    global selected_panel, historyElementOffset, font, history, myMap
    if selected_panel is not None:
        infoPanel.remove_element(selected_panel)
    valleyPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    valleyLabel = label.Label((5, 2), (230, 8), font, "------valleys------", (230, 230, 230))
    valleyPanel.add_element(valleyLabel)
    numberLabel = label.Label((0, 15), (80, 8), font, "number", (230, 230, 230))
    numberSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    radiusSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    radiusLabel = label.Label((0, 30), (80, 8), font, "radius", (230, 230, 230))
    valleyPanel.add_element(numberLabel)
    valleyPanel.add_element(numberSlider)
    valleyPanel.add_element(radiusSlider)
    valleyPanel.add_element(radiusLabel)
    radVarLabel = label.Label((0, 45), (80, 8), font, "radVar", (230, 230, 230))
    radVarSlider = slider.Slider((80, 45), (140, 8), (50, 50, 50), (230, 230, 230))
    valleyPanel.add_element(radVarLabel)
    valleyPanel.add_element(radVarSlider)
    heightLabel = label.Label((0, 60), (80, 8), font, "height", (230, 230, 230))
    heightSlider = slider.Slider((80, 60), (140, 8), (50, 50, 50), (230, 230, 230))
    valleyPanel.add_element(heightLabel)
    valleyPanel.add_element(heightSlider)
    selected_panel = valleyPanel
    valleyPanel.numberSlider = numberSlider
    valleyPanel.radiusSlider = radiusSlider
    valleyPanel.radVarSlider = radVarSlider
    valleyPanel.heightSlider = heightSlider
    valleyPanel.name = "valley"
    infoPanel.add_element(valleyPanel)
    history.append(HistoryObject(valleyPanel, "valley"))
    historyPanel.add_element(button.Button((5, historyElementOffset), (220, 10), "valleys", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.addValleys(25, 10, .5, .5)


def smoothButtonAction():
    global selected_panel, historyElementOffset, font, history, myMap
    if selected_panel is not None:
        infoPanel.remove_element(selected_panel)
    smoothPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    smoothLabel = label.Label((5, 2), (230, 8), font, "------smooth------", (230, 230, 230))
    smoothPanel.add_element(smoothLabel)
    minLabel = label.Label((0, 15), (80, 8), font, "min", (230, 230, 230))
    minSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    maxSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    maxLabel = label.Label((0, 30), (80, 8), font, "max", (230, 230, 230))
    smoothPanel.add_element(minLabel)
    smoothPanel.add_element(minSlider)
    smoothPanel.add_element(maxSlider)
    smoothPanel.add_element(maxLabel)
    weightLabel = label.Label((0, 45), (80, 8), font, "weight", (230, 230, 230))
    weightSlider = slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    smoothPanel.add_element(weightLabel)
    smoothPanel.add_element(weightSlider)
    selected_panel = smoothPanel
    smoothPanel.minSlider = minSlider
    smoothPanel.maxSlider = maxSlider
    smoothPanel.weightSlider = weightSlider
    smoothPanel.name = "smooth"
    infoPanel.add_element(smoothPanel)
    history.append(HistoryObject(smoothPanel, "smooth"))
    historyPanel.add_element(button.Button((5, historyElementOffset), (220, 10), "smooth", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.smooth(2, 0, 1.95)


def normalButtonAction():
    global selected_panel, historyElementOffset, font, history, myMap
    if selected_panel is not None:
        infoPanel.remove_element(selected_panel)
    normPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    normLabel = label.Label((5, 2), (230, 8), font, "------normalize------", (230, 230, 230))
    normPanel.add_element(normLabel)
    minLabel = label.Label((0, 15), (80, 8), font, "min", (230, 230, 230))
    minSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    maxSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    maxLabel = label.Label((0, 30), (80, 8), font, "max", (230, 230, 230))
    normPanel.add_element(minLabel)
    normPanel.add_element(minSlider)
    normPanel.add_element(maxSlider)
    normPanel.add_element(maxLabel)
    selected_panel = normPanel
    normPanel.minSlider = minSlider
    normPanel.maxSlider = maxSlider
    infoPanel.add_element(normPanel)
    normPanel.name = "normal"
    history.append(HistoryObject(normPanel, "normal"))
    historyPanel.add_element(button.Button((5, historyElementOffset), (220, 10), "normalize", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.normalize(0, 1)


def hillButtonAction():
    global selected_panel, font, history, historyElementOffset, myMap
    if selected_panel is not None:
        infoPanel.remove_element(selected_panel)
    hillPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    hillLabel = label.Label((5, 2), (230, 8), font, "------hills------", (230, 230, 230))
    hillPanel.add_element(hillLabel)
    hillNumSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    hillNumLabel = label.Label((0, 15), (80, 8), font, "hillnum", (230, 230, 230))
    hillPanel.add_element(hillNumLabel)
    hillPanel.add_element(hillNumSlider)
    heightSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    heightLabel = label.Label((0, 30), (80, 8), font, "height", (230, 230, 230))
    hillPanel.add_element(heightLabel)
    hillPanel.add_element(heightSlider)
    radiusSlider = slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    radiusLabel = label.Label((0, 45), (80, 8), font, "radius", (230, 230, 230))
    hillPanel.add_element(radiusLabel)
    hillPanel.add_element(radiusSlider)
    radiusVarSlider = slider.Slider((80, 60), (140, 8), (50, 50, 50), (150, 150, 150))
    radiusVarLabel = label.Label((0, 60), (80, 8), font, "radiusVar", (230, 230, 230))
    hillPanel.add_element(radiusVarLabel)
    hillPanel.add_element(radiusVarSlider)
    hillPanel.hillNumSlider = hillNumSlider
    hillPanel.radiusSlider = radiusSlider
    hillPanel.radiusVarSlider = radiusVarSlider
    hillPanel.heightSlider = heightSlider
    selected_panel = hillPanel
    hillPanel.name = "hill"
    infoPanel.add_element(hillPanel)
    history.append(HistoryObject(hillPanel, "hill"))
    historyPanel.add_element(button.Button((5, historyElementOffset), (220, 10), "hills", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.addHills(25, 10, .5, .5)


def rainButtonAction():
    global selected_panel, font, history, historyElementOffset
    if selected_panel is not None:
        infoPanel.remove_element(selected_panel)
    rainPanel = panel.Panel((5, 210), (230, 80), (10, 10, 50))
    rainLabel = label.Label((5, 2), (230, 8), font, "------rain------", (230, 230, 230))
    rainPanel.add_element(rainLabel)
    rainDropsSlider = slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    rainDropsLabel = label.Label((0, 15), (80, 8), font, "drops", (230, 230, 230))
    rainPanel.add_element(rainDropsSlider)
    rainPanel.add_element(rainDropsLabel)
    erosionSlider = slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    erosionLabel = label.Label((0, 30), (80, 8), font, "erosion", (230, 230, 230))
    rainPanel.add_element(erosionSlider)
    rainPanel.add_element(erosionLabel)
    sedimentSlider = slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    sedimentLabel = label.Label((0, 45), (80, 8), font, "sediment", (230, 230, 230))
    rainPanel.add_element(sedimentSlider)
    rainPanel.add_element(sedimentLabel)
    rainPanel.rainDropsSlider = rainDropsSlider
    rainPanel.erosionSlider = erosionSlider
    rainPanel.sedimentSlider = sedimentSlider
    selected_panel = rainPanel
    rainPanel.name = "rain"
    infoPanel.add_element(rainPanel)
    history.append(HistoryObject(rainPanel, "rain"))
    historyPanel.add_element(button.Button((5, historyElementOffset), (220, 10), "rain", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.rainErosion(1000, .05, .05)


def main():
    global myMap, mapSquareSize, colorKey
    while True:
        window.draw_elements()
        window.handle_element_actions()
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
toolPanel.add_element(toolPanelLabel)

normButton = button.Button((5, 20), (220, 10), "normalize", font, normalButtonAction, (230, 230,
                                                                                       230), (10, 10, 50))
toolPanel.add_element(normButton)

hillButton = button.Button((5, 50), (220, 10), "hills", font, hillButtonAction, (230, 230, 230),
                           (10, 10, 50))
toolPanel.add_element(hillButton)

rainButton = button.Button((5, 65), (220, 10), "rain", font, rainButtonAction, (230, 230, 230),
                           (10, 10, 50))
toolPanel.add_element(rainButton)

valleyButton = button.Button((5, 35), (220, 10), "valleys", font, valleyButtonAction, (230, 230,
                                                                                       230), (10, 10, 50))
toolPanel.add_element(valleyButton)

smoothButton = button.Button((5, 80), (220, 10), "smooth", font, smoothButtonAction, (230, 230,
                                                                                      230), (10, 10, 50))
toolPanel.add_element(smoothButton)

changeButton = button.Button((5, 95), (220, 10), "change z", font, changeButtonAction, (230, 230,
                                                                                        230), (10, 10, 50))
toolPanel.add_element(changeButton)

writeButton = button.Button((5, 110), (220, 10), "write to file", font, write_out, (230, 230, 230),
                            (10, 10, 50))
toolPanel.add_element(writeButton)

doneButton = button.Button((5, 295), (230, 15), "done", font, done_action, (230, 230, 230),
                           (10, 10, 50))
infoPanel.add_element(doneButton)

infoPanel.add_element(toolPanel)

historyPanel = panel.Panel((5, 315), (230, 400), (10, 10, 50))
historyLabel = label.Label((5, 2), (230, 8), font, "------history------", (230, 230, 230))
historyPanel.add_element(historyLabel)
infoPanel.add_element(historyPanel)
window.add_element(infoPanel)
write_out()
if __name__ == "__main__":
    main()