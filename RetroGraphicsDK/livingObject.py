'''
The LivingObject class inherits from the GameObject class. It represents any living object
'''
import gameObject

class LivingObject(gameObject.GameObject):
    '''
    Constructor takes location, sprite surface, and integers of hp, mana, defense, and power. Also takes
    booleans of blocking movement and blocking sight.
    '''
    def __init__(self, (x, y), sprite, hp, mana, defense, power, blocks=None, blocksSight=None):
        super(LivingObject, self).__init__((x, y), sprite, blocks, blocksSight)
        self.hp = hp
        self.maxMana = mana
        self.mana = mana
        self.power = power
        self.defense = defense