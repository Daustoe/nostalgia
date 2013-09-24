'''
Created on Apr 4, 2012

@author: Claymore
'''
import gameObject


class Item(gameObject.GameObject):
    def __init__(self, use_function=None):
        self.use_function = use_function
