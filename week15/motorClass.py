from matplotlib import pyplot as plt
import math
import numpy as np
from femm import *

def generatePattern(s,p,b):
    m = s/p/3
    circuits = [['R',1],['B',1],['Y',1]] #circuit name, direction
    currentCir = 0
    windings = [["",0]]*s
    count = 0
    for i in range(s):
        count += 1

        #short chording
        if i % 2 == 0:
            slot = (i+b*2)%60
            windings[slot] = [circuits[currentCir][0],circuits[currentCir][1]]
        else:
            windings[i] = [circuits[currentCir][0],circuits[currentCir][1]]

        if count >= m*2:
            count = 0
            circuits[currentCir][1] *= -1
            currentCir += 1
            if currentCir > 2:
                currentCir = 0
    return windings


class motor():
    """class to hold all the info needed to setup a motor"""    
    def __init__(self,file,windings,turns):
        self.windings = windings
        self.turns = turns

    def assignWindings(self):
        opendocument(self.file)

        for i in range(len(self.windings)):
            mi_selectgroup(i+1)
            mi_setblockprop("Coil",1,0,self.windings[i][0],0,i+1,self.windings[i]*self.turns)
            mi_clearselected()

print(generatePattern(60,4,0))