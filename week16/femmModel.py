from femm import *
import math
import numpy as np

class motor:

    def __init__(self):
        openfemm()
        newdocument(0)
        mi_probdef(0,"millimeters","planar","1e-008","120","30")
    
    def drawArc(self,theta,dtheta,D):
        theta = math.radians(theta)
        dtheta = math.radians(dtheta)

        points = [D*math.cos(theta),D*math.sin(theta),D*math.cos(theta+dtheta),D*math.sin(theta+dtheta)]

        mi_drawarc(points[0],points[1],points[2],points[3],math.degrees(dtheta),1)

        return points

    def drawDo(self,Do,p,D):
        if p > 1:
            dtheta = 360/p
            theta = 0
            self.drawArc(theta,dtheta,Do/2)

            mi_addnode(*self.polarToCart(360/p,D/2))
            mi_addnode(D/2,0)

            mi_addsegment(*self.polarToCart(360/p,D/2),*self.polarToCart(360/p,Do/2))
            mi_addsegment(D/2,0,Do,0)

        else:
            self.drawArc(0,180,Do/2)
            self.drawArc(180,180,Do/2)

    def polarToCart(self,theta,D):
        return D*math.cos(math.radians(theta)),D*math.sin(math.radians(theta))

    def testTeeth(self,W1,D,d1,q,WT,wTheta,Do,dB,p,g):
        Ds = Do-(dB*2)
        wTheta = math.radians(wTheta)
        slotPitch = math.radians(360/q)
        beta = math.asin(W1/D)
        a = (D/2) * math.cos(beta) + d1 - (W1*math.cos(slotPitch/2)+WT)/(2*math.sin(slotPitch/2))
        b = a * (math.sin(slotPitch/2)/math.sin(wTheta-slotPitch/2))

        points = []
        lines = []

        points.append([])

        points[0].append(np.matrix((W1/2,math.cos(beta)*D/2)))

        points[0].append(np.matrix((W1/2,d1+math.cos(beta)*D/2)))
        points[0].append(np.matrix(((W1/2)+b*math.sin(wTheta),math.cos(beta)*D/2+d1+b*math.cos(wTheta))))
        points[0].append(np.matrix((math.sin(slotPitch/2)*math.sqrt((Ds**2-WT**2))/2-math.cos(slotPitch/2)*WT/2,math.cos(slotPitch/2)*math.sqrt((Ds**2-WT**2))/2+math.sin(slotPitch/2)*WT/2)))

        x3 = (W1/2)+b*math.sin(wTheta)
        x4 = math.sin(slotPitch/2)*math.sqrt(Ds**2-WT**2)/2-math.cos(slotPitch/2)*WT/2
        x5 = math.sqrt(((x3**2)+(x4**2))/2)

        y3 = math.cos(beta)*D/2+d1+b*math.cos(wTheta)
        y4 = math.cos(slotPitch/2)*math.sqrt(Ds**2-WT**2)/2+math.sin(slotPitch/2)*WT/2
        y5 = y3 + ((y4-y3)*(x5-x3)/(x4-x3))

        points[0].insert(3,np.matrix([x5,y5]))        
        
        for i in reversed(points[0]):
            points[0].append(i*np.matrix([[-1,0],[0,1]]))

        slotPitch = math.pi*2/q
        angle = (math.pi/2)-(slotPitch/2)
        rotMatrix = np.matrix([[math.cos(angle),-math.sin(angle)],
                                       [math.sin(angle),math.cos(angle)]])

        for i in range(len(points[0])):
            points[0][i] *= rotMatrix

        for i in range(len(points[0])-1):
            lines.append(line([points[0][i],points[0][i+1]]))

        slotPitch = math.pi*2/q

        pointsLen = len(points[0])
        for i in range(1,q//p):
            points.append([])
            for j in range(pointsLen):
                angle = -i*slotPitch
                rotMatrix = np.matrix([[math.cos(angle),-math.sin(angle)],
                                       [math.sin(angle),math.cos(angle)]])
                points[i].append(points[0][j]*rotMatrix)
            
            for j in range(len(points[i])-1):
                lines.append(line([points[i][j],points[i][j+1]]))

        for i in range(len(points)-1):
            lines.append(line([points[i][-1],points[i+1][0]],curve=True))
        
        lines.append(line([np.matrix([D/2,0]),points[0][0]],curve=True))
        lines.append(line([points[-1][-1],np.matrix(self.polarToCart(360/p,D/2))],curve=True))

        group = 1

        for teeth in points:
            label1 = (teeth[3]+teeth[5])/2
            label2 = (teeth[2]+teeth[6])/2
            
            self.makeBlockLabel(label1,"Coil",group)
            group += 1
            self.makeBlockLabel(label2,"Coil",group)
            group += 1

            lines.append(line([teeth[2],teeth[7]]))
            lines.append(line([teeth[3],teeth[6]]))
            for i in teeth:
                mi_addnode(i[0,0],i[0,1])
        
        for i in lines:
            i.draw()

        self.makeBlockLabel(np.matrix(self.polarToCart(360/p/2,(Do/2)-(dB/2))),"M-15 Steel",0)
        self.makeBlockLabel(np.matrix(self.polarToCart(360/q/2,(D/2)-(g/2))),"Air",0)
        
    
    
    def drawAirGap(self,g,D,p):
        self.drawArc(0,360/p,(D/2)-g)
        mi_addsegment(D/2,0,(D/2)-g,0)
        mi_addsegment(*self.polarToCart(360/p,D/2),*self.polarToCart(360/p,(D/2)-g))



    def makeMotor(self,D,Do,WT,dB,q,p,g,W1,d1,wTheta,As,J):
        self.addMaterials()
        self.drawDo(Do,p,D)
        self.testTeeth(W1,D,d1,q,WT,wTheta,Do,dB,p,g)
        self.drawAirGap(g,D,p)

        current = J*(As/2)

        print(f"As: {As}, J: {J}")

        self.setCoils(current,q,p)

        self.calcResult(D,g,p)

    
    def addMaterials(self):
        mi_getmaterial("M-15 Steel")
        mi_addmaterial("Coil",1,1,0,0,0,0,0,0,0,0,0,0,0,0)
        mi_getmaterial("Air")

    def makeBlockLabel(self,pos,material,group):
        listPos = np.matrix.tolist(pos)[0]
        mi_addblocklabel(*listPos)
        mi_selectlabel(*listPos)
        mi_setblockprop(material,1,0,"",0,group,0)
        mi_clearselected()

    def setCoils(self,current,q,p):
        groups = (q//p)*2

        windings = self.generatePattern(q,p,1)

        mi_addcircprop("R",current,1)
        mi_addcircprop("B",-current/2,1)
        mi_addcircprop("Y",-current/2,1)

        for i in range(1,groups+1):
            mi_selectgroup(i)
            mi_setblockprop("Coil",1,0,windings[i-1][0],0,i,windings[i-1][1])
            mi_clearselected()

    def generatePattern(self,s,p,b):
        """(number of slots,number of poles,short chording)"""
        groupNum = s//(p//2)
        m = groupNum//12
        circuits = [['R',1],['B',1],['Y',1]] #circuit name, direction
        currentCir = 0
        windings = [["",0]]*groupNum

        count = 0
        for i in range(groupNum):
            count += 1

            #short chording
            if i % 2 == 0:
                slot = (i+b*2)%groupNum
                print(f"shifted slot num: {slot}")
                windings[slot] = [circuits[currentCir][0],circuits[currentCir][1]]
            else:
                print("odd")
                windings[i] = [circuits[currentCir][0],circuits[currentCir][1]]

            if count >= m*2:
                count = 0
                circuits[currentCir][1] *= -1
                currentCir += 1
                if currentCir > 2:
                    currentCir = 0


        return windings

    def calcResult(self,D,g,p):
        mi_saveas("test.FEM")

        mi_analyse(0)
        mi_loadsolution()

        dist = (D/2)-(g/2)

        end = self.polarToCart(360/p,dist)

        mo_seteditmode('contour') 
        mo_addcontour(dist,0) 
        mo_addcontour(*end) 
        mo_bendcontour(360/p,1)




class line:

    curve = False

    points = [np.matrix([0,0]),np.matrix([0,0])]

    def __init__(self, points=None, curve=None):
        if curve != None:
            self.curve = curve
        if points != None:
            self.points = points
    
    def draw(self, centre=np.matrix([0,0])):
        if self.curve:
            vector1 = self.points[0]-centre
            vector2 = self.points[1]-centre

            vector1 /= np.linalg.norm(vector1)
            vector2 /= np.linalg.norm(vector2)

            dot = 0
            for i in [0,1]:
                dot += vector1[0,i]*vector2[0,i]

            angle = math.degrees(math.acos(dot))
            mi_addarc(self.points[0][0,0],self.points[0][0,1],self.points[1][0,0],self.points[1][0,1],angle,1)
        else:
            mi_addsegment(self.points[0][0,0],self.points[0][0,1],self.points[1][0,0],self.points[1][0,1])
        




if __name__=="__main__":

    newMotor = motor()
    newMotor.testTeeth(3.3,129,1,24,9.6,70,200,9.2,2,1)
    
    input("press enter to exit")