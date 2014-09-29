__author__ = 'cjpowell'
from core.gui.view import View
import pygame


class ImageView(View):
    def __init__(self, x, y, width, height, img):
        super(ImageView, self).__init__(x, y, width, height)
        self.surface = pygame.transform.scale(img, (width, height))