'''
Created on November 5, 2013

@author: Claymore
'''


class Profile(object):
    def __init__(self, name):
        self.name = name
        self.isValid = True
        self.totalTime = 0.0
        self.childTime = 0.0