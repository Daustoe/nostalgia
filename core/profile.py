'''
Created on November 5, 2013

@author: Claymore
'''
import time


class Profile(object):
    def __init__(self, name):
        self.name = name
        self.isValid = True
        self.totalTime = 0.0
        self.childTime = 0.0

    def start(self):
        return time.clock()