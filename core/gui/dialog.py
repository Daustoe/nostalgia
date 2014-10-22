__author__ = 'cjpowell'
from view import View
from pygame import Color
from pygame import K_ESCAPE
from signal import Signal


class DialogView(View):
    def __init__(self, x, y, width, height, color=Color('gray')):
        super(DialogView, self).__init__(x, y, width, height, color)
        self.hidden = True
        self.on_dismissed = Signal()

    def dismiss(self):
        self.on_dismissed()
        self.hidden = True

    def key_down(self, key, code):
        if key == K_ESCAPE:
            self.dismiss()