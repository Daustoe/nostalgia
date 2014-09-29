__author__ = 'cjpowell'
from core.gui.view import View
from pygame.transform import scale


class ImageView(View):
    def __init__(self, x, y, width, height, img):
        super(ImageView, self).__init__(x, y, width, height)
        self.surface = scale(img, (width, height))