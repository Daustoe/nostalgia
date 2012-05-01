'''
Created on Apr 23, 2012

@author: Claymore
'''

import sys, pygame, slider, button, console, panel, heightmap, label

window = console.Console(960, 720)
font = pygame.font.SysFont('timesnewroman', 16, bold=True)
window.setCaption("Heightmap Generator")
map = heightmap.HeightMap(30, 30)
selectedPanel = None
historyElementOffset = 15

def normalButtonAction():
    global selectedPanel, historyElementOffset, font
    if selectedPanel != None:
        infoPanel.removeElement(selectedPanel)
    selectedPanel = normPanel
    infoPanel.addElement(normPanel)
    '''
    consider adding an array that holds onto the history, each element in the array is a Panel object
    when we click a button in the tools panel, we actually create a new panel object to display, which
    gets added to the history array. Clicking the history button returns the object at that index.
    '''
    historyPanel.addElement(button.Button((5, historyElementOffset), (220, 10), "normalize", font, normalButtonAction, (230, 230, 230), (10, 10, 50)))
    historyElementOffset += 15
    
def hillButtonAction():
    global selectedPanel
    if selectedPanel != None:
        infoPanel.removeElement(selectedPanel)
    selectedPanel = hillPanel
    infoPanel.addElement(hillPanel)
    
def rainButtonAction():
    global selectedPanel
    if selectedPanel != None:
        infoPanel.removeElement(selectedPanel)
    selectedPanel = rainPanel
    infoPanel.addElement(rainPanel)

def main():
    while True:
        window.drawElements()
        window.handleElementActions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                break
        pygame.display.flip()
        
infoPanel = panel.Panel((720, 0), (240, 720), (200, 200, 200))
toolPanel = panel.Panel((5, 5), (230, 200), (10, 10, 50))
toolPanelLabel = label.Label((5, 2), (230, 8), font, "------tools------", (230, 230, 230))
toolPanel.addElement(toolPanelLabel)

normButton = button.Button((5, 20), (220, 10), "normalize", font, normalButtonAction, (230, 230, 230), (10, 10, 50))
toolPanel.addElement(normButton)

hillButton = button.Button((5, 35), (220, 10), "hills", font, hillButtonAction, (230, 230, 230), (10, 10, 50))
toolPanel.addElement(hillButton)

rainButton = button.Button((5, 50), (220, 10), "rain", font, rainButtonAction, (230, 230, 230), (10, 10, 50))
toolPanel.addElement(rainButton)

infoPanel.addElement(toolPanel)

hillPanel = panel.Panel((5, 210), (230, 100), (10, 10, 50))
hillLabel = label.Label((5, 2), (230, 8), font, "------hills------", (230, 230, 230))
hillPanel.addElement(hillLabel)
hillNumSlider = slider.Slider((50, 15), (140, 8), (50, 50, 50), (150, 150, 150))
hillPanel.addElement(hillNumSlider)
heightSlider = slider.Slider((50, 25), (140, 8), (50, 50, 50), (150, 150, 150))
hillPanel.addElement(heightSlider)
radiusSlider = slider.Slider((50, 35), (140, 8), (50, 50, 50), (150, 150, 150))
hillPanel.addElement(radiusSlider)
radiusVarSlider = slider.Slider((50, 45), (140, 8), (50, 50, 50), (150, 150, 150))
hillPanel.addElement(radiusVarSlider)

normPanel = panel.Panel((5, 210), (230, 100), (10, 10, 50))
normLabel = label.Label((5, 2), (230, 8), font, "------normalize------", (230, 230, 230))
normPanel.addElement(normLabel)

rainPanel = panel.Panel((5, 210), (230, 100), (10, 10, 50))
rainLabel = label.Label((5, 2), (230, 8), font, "------rain------", (230, 230, 230))
rainPanel.addElement(rainLabel)

historyPanel = panel.Panel((5, 315), (230, 400), (10, 10, 50))
historyLabel = label.Label((5, 2), (230, 8), font, "------history------", (230, 230, 230))
historyPanel.addElement(historyLabel)
infoPanel.addElement(historyPanel)
window.addElement(infoPanel)
if __name__ == "__main__": main()