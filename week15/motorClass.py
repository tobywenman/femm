from matplotlib import pyplot as plt
import math
import numpy as np
from femm import *

def generatePattern(s,p,b):
    """(number of slots,number of poles,short chording)"""
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

def calcTurns(x,b,m,angle,p):
    alpha = 1-b/(3*m)
    turns = (math.sin(alpha*math.pi/2)*math.sin(m*angle/2)/(m*math.sin(angle/2)))
    turns = x/turns
    return round(turns,0)

class motor():
    """class to hold all the info needed to setup a motor"""    
    def __init__(self,file,windings,turns):
        self.file = file
        self.windings = windings
        self.turns = turns

    def assignWindings(self):
        opendocument(self.file)

        for i in range(len(self.windings)):
            mi_selectgroup(i+1)
            mi_setblockprop("Coil",1,0,self.windings[i][0],0,i+1,self.windings[i][1]*self.turns)
            mi_clearselected()
    
    def saveBgap(self,outFile):
        mi_analyse(0)
        mi_loadsolution()
        AG_radius = 78
        x_end = AG_radius*math.sin(math.pi/2)
        y_end = AG_radius*math.cos(math.pi/2)

        mo_seteditmode('contour') 
        mo_addcontour( x_end, y_end) 
        mo_addcontour(-x_end, y_end) 
        mo_bendcontour(180,1) 
        mo_makeplot(2,31,outFile,1)


openfemm()

# noShortChord = motor(r"Tesla_stator.FEM",generatePattern(60,4,1),7)

# noShortChord.assignWindings()

motors = []

fig, ax = plt.subplots()
width = 0.35

for shortChord in range(4):
    motors.append(motor(r"Tesla_stator.FEM",generatePattern(60,4,shortChord),calcTurns(15.01,shortChord,5,math.pi/15,4)))
    motors[shortChord].assignWindings()
    #motors[shortChord].saveBgap("Bgap"+str(shortChord)+".txt")

    flux = np.loadtxt("Bgap"+str(shortChord)+".txt")
    x = np.arange(len(flux[:,0])//2-1)
    rects1 = ax.bar(0.1 + x + (shortChord-2)*width/2, np.abs(np.fft.fft(flux[:,1])[1:len(flux[:,1])//2]), width/2, label="ShortChord "+str(shortChord))

ax.legend()
fig.tight_layout()
plt.show()

input("Press enter to exit")