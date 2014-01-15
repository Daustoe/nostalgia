"""
Testing module for all of the Game Engine
"""

import sys

import pygame

from core.gui import *
from core.gameDev.heightmap import HeightMap


def game_loop(window):
    user_quit = False
    while not user_quit:
        window.draw_elements()
        window.handle_element_actions()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                user_quit = True
                sys.exit()


def main():
    window = console.Console(1100, 720)
    window.set_caption("Test Game!!1!")
    font = pygame.font.SysFont('timesnewroman', 16)
    game_map = HeightMap(100, 100)
    game_map_square_size = (1100 / 100, 720 / 100)
    sand_height = 0.12
    grass_height = 0.315
    snow_height = 0.785
    key_index = [0,
                 int(sand_height * 255),
                 int(sand_height * 255) + 4,
                 int(grass_height * 255),
                 int(grass_height * 255) + 10,
                 int(snow_height * 255),
                 int(snow_height * 255) + 10,
                 255]
    color_key = [(0, 0, 50),  # deep water
                 (30, 30, 170),  # shallow water
                 (114, 150, 71),  # sand
                 (80, 120, 10),  # shrubs
                 (17, 109, 7),  # grassland
                 (120, 220, 120),  # snowy grass
                 (208, 208, 239),  # snow
                 (255, 255, 255)]
    game_loop(window)


if __name__ == "__main__":
    main()