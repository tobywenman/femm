from femm import *
import math
import numpy as np
from matplotlib import pyplot as plt 

def generate_B_field(groupCircuits,groupDirs, turns, name, out):
    opendocument(name)
    for i in range(len(groupCircuits)):
        mi_selectgroup(i+1)
        mi_setblockprop("Coil",1,0,groupCircuits[i],0,i+1,groupDirs[i]*turns)
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
    mo_makeplot(2,361,out,1)

openfemm()


#1.5 slots per pole per phase
#generate_B_field("RRRBBBYYYRRRBBBYYY",[1,1,1,-1,-1,-1,1,1,1,-1,-1,-1,1,1,1,-1,-1,-1],10,"Winding_with_1.5_slots_per_pole_per_phase.FEM")

#2 slots per pole per phase
generate_B_field("RRRBBBBYYYYRRRRBBBBYYYYR",[1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1],10,"Winding_with_2_slots_per_pole_per_phase.FEM","out2_1shortchord.txt")
generate_B_field("RRRRBBBBYYYYRRRRBBBBYYYY",[1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1,1,1,1,1,-1,-1,-1,-1],10,"Winding_with_2_slots_per_pole_per_phase.FEM","out2_0shortchord.txt")

fluxs = []

fluxs.append(np.loadtxt("out2_1shortchord.txt"))
fluxs.append(np.loadtxt("out2_0shortchord.txt"))

for flux in fluxs:
    plt.plot(flux[:,0],flux[:,1])

plt.show()

for flux in fluxs:
    plt.plot(np.abs(np.fft.fft(flux[:,1])[:len(flux[:,1])//2]),'--')

plt.show()

input("Press enter to exit")