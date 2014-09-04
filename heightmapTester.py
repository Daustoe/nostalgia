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
from core.tools import heightmap
import core.gui.slider as Slider
import core.gui.button as Button
import core.gui.console as Console
import core.gui.view as Panel
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
        global info_panel, selected_panel, myMap
        if selected_panel is not None:
            info_panel.remove_child(selected_panel)
        selected_panel = self.panel
        info_panel.add_child(self.panel)


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
            file_out.write("    hm.addvalleys({},{},{},{})\n".format(int(each.panel.numberSlider.value * 50),
                                                                     int(each.panel.radiusSlider.value * 20),
                                                                     each.panel.radVarSlider.value,
                                                                     each.panel.heightSlider.value))
        elif each.name == "smooth":
            file_out.write("    hm.smooth({},{},{})\n".format(each.panel.weightSlider.value * 20,
                                                              each.panel.minSlider.value,
                                                              each.panel.maxSlider.value * 5))
        elif each.name == "hill":
            file_out.write("    hm.addHills({},{},{},{})\n".format(int(each.panel.hillNumSlider.value * 50),
                                                                   int(each.panel.radiusSlider.value * 20),
                                                                   each.panel.radiusVarSlider.value,
                                                                   each.panel.heightSlider.value))
        elif each.name == "normal":
            file_out.write("    hm.normalize({},{})\n".format(each.panel.minSlider.value, each.panel.maxSlider.value))
        elif each.name == "rain":
            file_out.write("    hm.rainErosion({},{},{})\n".format(int(each.panel.rainDropsSlider.value * 20000),
                                                                   each.panel.erosionSlider.value,
                                                                   each.panel.sedimentSlider.value))
    file_out.close()


def done_action():
    if selected_panel.name == "change":
        myMap.change_height(selected_panel.heightSlider.value * 2 - 1)
    elif selected_panel.name == "valley":
        myMap.add_valleys(int(selected_panel.numberSlider.value * 50), int(selected_panel.radiusSlider.value * 25),
                          selected_panel.radVarSlider.value, selected_panel.heightSlider.value)
    elif selected_panel.name == "hill":
        myMap.add_hills(int(selected_panel.hillNumSlider.value * 50), int(selected_panel.radiusSlider.value * 25),
                        selected_panel.radiusVarSlider.value, selected_panel.heightSlider.value)
    elif selected_panel.name == "normal":
        myMap.normalize(selected_panel.minSlider.value, selected_panel.maxSlider.value)
    elif selected_panel.name == "smooth":
        myMap.smooth(int(selected_panel.weightSlider.value * 10), selected_panel.minSlider.value,
                     selected_panel.maxSlider.value)
    elif selected_panel.name == "rain":
        myMap.rain_erosion(int(selected_panel.rainDropsSlider.value * 20000), selected_panel.erosionSlider.value,
                           selected_panel.sedimentSlider.value)


def change_button_action():
    global selected_panel, historyElementOffset, font, history, myMap
    if selected_panel is not None:
        info_panel.remove_child(selected_panel)
    change_panel = Panel.View((5, 210), (230, 80), (10, 10, 50))
    change_label = Label.Label((5, 2), (230, 8), font, "------valleys------", (230, 230, 230))
    change_panel.add_child(change_label)
    height_label = Label.Label((0, 15), (80, 8), font, "height", (230, 230, 230))
    height_slider = Slider.Slider((80, 15), (140, 8), (50, 50, 50), (230, 230, 230))
    change_panel.add_child(height_label)
    change_panel.add_child(height_slider)
    done_button = Button.Button((5, 80), (100, 10), "done", font, myMap.change_height, (230, 230, 230), (10, 10, 50))
    change_panel.add_child(done_button)
    change_panel.name = "change"
    height_slider.set_value(.55)
    selected_panel = change_panel
    change_panel.height_slider = height_slider
    info_panel.add_child(change_panel)
    history.append(HistoryObject(change_panel, "change"))
    historyPanel.add_child(Button.Button((5, historyElementOffset), (220, 10), "change z", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.changeHeights(.1)


def valley_button_action():
    global selected_panel, historyElementOffset, font, history, myMap
    if selected_panel is not None:
        info_panel.remove_child(selected_panel)
    valley_panel = Panel.View((5, 210), (230, 80), (10, 10, 50))
    valley_label = Label.Label((5, 2), (230, 8), font, "------valleys------", (230, 230, 230))
    valley_panel.add_child(valley_label)
    number_label = Label.Label((0, 15), (80, 8), font, "number", (230, 230, 230))
    number_slider = Slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    radius_slider = Slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    radius_label = Label.Label((0, 30), (80, 8), font, "radius", (230, 230, 230))
    valley_panel.add_child(number_label)
    valley_panel.add_child(number_slider)
    valley_panel.add_child(radius_slider)
    valley_panel.add_child(radius_label)
    rad_var_label = Label.Label((0, 45), (80, 8), font, "radVar", (230, 230, 230))
    rad_var_slider = Slider.Slider((80, 45), (140, 8), (50, 50, 50), (230, 230, 230))
    valley_panel.add_child(rad_var_label)
    valley_panel.add_child(rad_var_slider)
    height_label = Label.Label((0, 60), (80, 8), font, "height", (230, 230, 230))
    height_slider = Slider.Slider((80, 60), (140, 8), (50, 50, 50), (230, 230, 230))
    valley_panel.add_child(height_label)
    valley_panel.add_child(height_slider)
    selected_panel = valley_panel
    valley_panel.number_slider = number_slider
    valley_panel.radius_slider = radius_slider
    valley_panel.rad_var_slider = rad_var_slider
    valley_panel.height_slider = height_slider
    valley_panel.name = "valley"
    info_panel.add_child(valley_panel)
    history.append(HistoryObject(valley_panel, "valley"))
    historyPanel.add_child(Button.Button((5, historyElementOffset), (220, 10), "valleys", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.addValleys(25, 10, .5, .5)


def smooth_button_action():
    global selected_panel, historyElementOffset, font, history, myMap
    if selected_panel is not None:
        info_panel.remove_child(selected_panel)
    smooth_panel = Panel.View((5, 210), (230, 80), (10, 10, 50))
    smooth_label = Label.Label((5, 2), (230, 8), font, "------smooth------", (230, 230, 230))
    smooth_panel.add_child(smooth_label)
    min_label = Label.Label((0, 15), (80, 8), font, "min", (230, 230, 230))
    min_slider = Slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    max_slider = Slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    max_label = Label.Label((0, 30), (80, 8), font, "max", (230, 230, 230))
    smooth_panel.add_child(min_label)
    smooth_panel.add_child(min_slider)
    smooth_panel.add_child(max_slider)
    smooth_panel.add_child(max_label)
    weight_label = Label.Label((0, 45), (80, 8), font, "weight", (230, 230, 230))
    weight_slider = Slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    smooth_panel.add_child(weight_label)
    smooth_panel.add_child(weight_slider)
    selected_panel = smooth_panel
    smooth_panel.min_slider = min_slider
    smooth_panel.max_slider = max_slider
    smooth_panel.weight_slider = weight_slider
    smooth_panel.name = "smooth"
    info_panel.add_child(smooth_panel)
    history.append(HistoryObject(smooth_panel, "smooth"))
    historyPanel.add_child(Button.Button((5, historyElementOffset), (220, 10), "smooth", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.smooth(2, 0, 1.95)


def normal_button_action():
    global selected_panel, historyElementOffset, font, history, myMap
    if selected_panel is not None:
        info_panel.remove_child(selected_panel)
    norm_panel = Panel.View((5, 210), (230, 80), (10, 10, 50))
    norm_label = Label.Label((5, 2), (230, 8), font, "------normalize------", (230, 230, 230))
    norm_panel.add_child(norm_label)
    min_label = Label.Label((0, 15), (80, 8), font, "min", (230, 230, 230))
    min_slider = Slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    max_slider = Slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    max_label = Label.Label((0, 30), (80, 8), font, "max", (230, 230, 230))
    norm_panel.add_child(min_label)
    norm_panel.add_child(min_slider)
    norm_panel.add_child(max_slider)
    norm_panel.add_child(max_label)
    selected_panel = norm_panel
    norm_panel.min_slider = min_slider
    norm_panel.max_slider = max_slider
    info_panel.add_child(norm_panel)
    norm_panel.name = "normal"
    history.append(HistoryObject(norm_panel, "normal"))
    historyPanel.add_child(Button.Button((5, historyElementOffset), (220, 10), "normalize", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.normalize(0, 1)


def hill_button_action():
    global selected_panel, font, history, historyElementOffset, myMap
    if selected_panel is not None:
        info_panel.remove_child(selected_panel)
    hill_panel = Panel.View((5, 210), (230, 80), (10, 10, 50))
    hill_label = Label.Label((5, 2), (230, 8), font, "------hills------", (230, 230, 230))
    hill_panel.add_child(hill_label)
    hill_num_slider = Slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    hill_num_label = Label.Label((0, 15), (80, 8), font, "hillnum", (230, 230, 230))
    hill_panel.add_child(hill_num_label)
    hill_panel.add_child(hill_num_slider)
    height_slider = Slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    height_label = Label.Label((0, 30), (80, 8), font, "height", (230, 230, 230))
    hill_panel.add_child(height_label)
    hill_panel.add_child(height_slider)
    radius_slider = Slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    radius_label = Label.Label((0, 45), (80, 8), font, "radius", (230, 230, 230))
    hill_panel.add_child(radius_label)
    hill_panel.add_child(radius_slider)
    radius_var_slider = Slider.Slider((80, 60), (140, 8), (50, 50, 50), (150, 150, 150))
    radius_var_label = Label.Label((0, 60), (80, 8), font, "radiusVar", (230, 230, 230))
    hill_panel.add_child(radius_var_label)
    hill_panel.add_child(radius_var_slider)
    hill_panel.hill_num_slider = hill_num_slider
    hill_panel.radius_slider = radius_slider
    hill_panel.radius_var_slider = radius_var_slider
    hill_panel.height_slider = height_slider
    selected_panel = hill_panel
    hill_panel.name = "hill"
    info_panel.add_child(hill_panel)
    history.append(HistoryObject(hill_panel, "hill"))
    historyPanel.add_child(Button.Button((5, historyElementOffset), (220, 10), "hills", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.addHills(25, 10, .5, .5)


def rain_button_action():
    global selected_panel, font, history, historyElementOffset
    if selected_panel is not None:
        info_panel.remove_child(selected_panel)
    rain_panel = Panel.View((5, 210), (230, 80), (10, 10, 50))
    rain_label = Label.Label((5, 2), (230, 8), font, "------rain------", (230, 230, 230))
    rain_panel.add_child(rain_label)
    raindrop_slider = Slider.Slider((80, 15), (140, 8), (50, 50, 50), (150, 150, 150))
    raindrop_label = Label.Label((0, 15), (80, 8), font, "drops", (230, 230, 230))
    rain_panel.add_child(raindrop_slider)
    rain_panel.add_child(raindrop_label)
    erosion_slider = Slider.Slider((80, 30), (140, 8), (50, 50, 50), (150, 150, 150))
    erosion_label = Label.Label((0, 30), (80, 8), font, "erosion", (230, 230, 230))
    rain_panel.add_child(erosion_slider)
    rain_panel.add_child(erosion_label)
    sediment_slider = Slider.Slider((80, 45), (140, 8), (50, 50, 50), (150, 150, 150))
    sediment_label = Label.Label((0, 45), (80, 8), font, "sediment", (230, 230, 230))
    rain_panel.add_child(sediment_slider)
    rain_panel.add_child(sediment_label)
    rain_panel.raindrop_slider = raindrop_slider
    rain_panel.erosion_slider = erosion_slider
    rain_panel.sediment_slider = sediment_slider
    selected_panel = rain_panel
    rain_panel.name = "rain"
    info_panel.add_child(rain_panel)
    history.append(HistoryObject(rain_panel, "rain"))
    historyPanel.add_child(Button.Button((5, historyElementOffset), (220, 10), "rain", font,
                                           history[-1].history_action, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    #myMap.rainErosion(1000, .05, .05)


def main():
    global myMap, mapSquareSize, colorKey
    while True:
        window.draw_elements()
        window.handle_element_actions()
        #need to perform all the operations
        color = None
        for x in range(myMap.width):
            for y in range(myMap.height):
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
        pygame.display.flip()


info_panel = Panel.View((720, 0), (240, 720), (200, 200, 200))
tool_panel = Panel.View((5, 5), (230, 200), (10, 10, 50))
tool_panel_label = Label.Label((5, 2), (230, 8), font, "------tools------", (230, 230, 230))
tool_panel.add_child(tool_panel_label)

norm_button = Button.Button((5, 20), (220, 10), "normalize", font, normal_button_action, (230, 230, 230), (10, 10, 50))
tool_panel.add_child(norm_button)

hill_button = Button.Button((5, 50), (220, 10), "hills", font, hill_button_action, (230, 230, 230), (10, 10, 50))
tool_panel.add_child(hill_button)

rain_button = Button.Button((5, 65), (220, 10), "rain", font, rain_button_action, (230, 230, 230), (10, 10, 50))
tool_panel.add_child(rain_button)

valley_button = Button.Button((5, 35), (220, 10), "valleys", font, valley_button_action, (230, 230, 230), (10, 10, 50))
tool_panel.add_child(valley_button)

smooth_button = Button.Button((5, 80), (220, 10), "smooth", font, smooth_button_action, (230, 230, 230), (10, 10, 50))
tool_panel.add_child(smooth_button)

change_button = Button.Button((5, 95), (220, 10), "change z", font, change_button_action, (230, 230, 230), (10, 10, 50))
tool_panel.add_child(change_button)

write_button = Button.Button((5, 110), (220, 10), "write to file", font, write_out, (230, 230, 230), (10, 10, 50))
tool_panel.add_child(write_button)

done_button = Button.Button((5, 295), (230, 15), "done", font, done_action, (230, 230, 230), (10, 10, 50))
info_panel.add_child(done_button)

info_panel.add_child(tool_panel)

historyPanel = Panel.View((5, 315), (230, 400), (10, 10, 50))
historyLabel = Label.Label((5, 2), (230, 8), font, "------history------", (230, 230, 230))
historyPanel.add_child(historyLabel)
info_panel.add_child(historyPanel)
window.add_element(info_panel)
write_out()
if __name__ == "__main__":
    main()