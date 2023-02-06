from femm import *
import math
import numpy as np
from matplotlib import pyplot as plt 


openfemm()

opendocument("Winding_with_1.5_slots_per_pole_per_phase.FEM")

groupCircuits = "RRRBBBYYYRRRBBBYYY"
groupDirs = [1,1,1,-1,-1,-1,1,1,1,-1,-1,-1,1,1,1,-1,-1,-1]

Turns = 10

for i in range(len(groupCircuits)):
    mi_selectgroup(i+1)
    mi_setblockprop("Coil",1,0,groupCircuits[i],0,i+1,groupDirs[i]*Turns)
    mi_clearselected()

mi_analyse(0)
mi_loadsolution()

AG_radius = 48.5
x_end = AG_radius*math.sin(0.995*math.pi/3)
y_end = AG_radius*math.cos(0.995*math.pi/3)

mo_seteditmode('contour') 
mo_addcontour( x_end, y_end) 
mo_addcontour(-x_end, y_end) 
mo_bendcontour(120,1) 
mo_makeplot(2,361,'Bgap.txt',1)

flux = np.loadtxt("Bgap.txt")


# plt.plot(flux[:,0],flux[:,1])


plt.plot(np.abs(np.fft.fft(flux[:,1])[:]))

plt.show()

input("Press enter to exit")