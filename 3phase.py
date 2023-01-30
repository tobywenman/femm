from femm import *
import math

openfemm()

opendocument("Primative_3ph(1).FEM")

currentMag = 100

angle = input("Enter phase angle: ")

angle = math.radians(float(angle))

circuits = {"R":math.sin(angle)*currentMag,
            "Y":math.sin(angle+(2/3)*math.pi)*currentMag,
            "B":math.sin(angle+(4/3)*math.pi)*currentMag}

for i in circuits.keys():
    print(circuits[i])
    print(i)
    mi_setcurrent(i,circuits[i])

mi_analyse(0)
mi_loadsolution()

mo_addcontour( 48, 0)
mo_addcontour(-48, 0)
mo_bendcontour(180,1)
mo_addcontour(-48, 0)
mo_addcontour( 48, 0)
mo_bendcontour(180,1)

mo_makeplot(2,1500)

input("Press enter to exit")