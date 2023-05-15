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

    def drawDo(self,Do,p):
        if p > 2:
            dtheta = 360/(p/2)
            theta = (180-dtheta)/2
            self.drawArc(theta,dtheta,Do)
        else:
            self.drawArc(0,180,Do)
            self.drawArc(180,180,Do)

    def polarToCart(self,theta,D):
        return D*math.cos(math.radians(theta)),D*math.sin(math.radians(theta))

    def testTeeth(self,W1,D,d1,q,WT,wTheta,Do,dB,p):
        Ds = Do-dB
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
        points[0].append(np.matrix((math.sin(slotPitch/2)*math.sqrt(Ds**2-WT**2)/2-math.cos(slotPitch/2)*WT/2,math.cos(slotPitch/2)*math.sqrt(Ds**2-WT**2)/2+math.sin(slotPitch/2)*WT/2)))

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

        for teeth in points:
            for i in teeth:
                mi_addnode(i[0,0],i[0,1])
        
        for i in lines:
            i.draw()

        
    
    
    def drawAirGap(self,g,D,p):
        self.drawDo(D-g,p)
        if p > 2:
            p1 = self.polarToCart((180-(360/(p/2)))/2,D)
            p2 = self.polarToCart((180-(360/(p/2)))/2,D-g)
            mi_addsegment(p1[0],p1[1],p2[0],p2[1])
            p1 = self.polarToCart(((180-(360/(p/2)))/2)+(360/(p/2)),D)
            p2 = self.polarToCart(((180-(360/(p/2)))/2)+(360/(p/2)),D-g)
            mi_addsegment(p1[0],p1[1],p2[0],p2[1])

    def makeMotor(self,D,Do,WT,dB,q,p,g,W1,d1,wTheta):
        self.testTeeth(W1,D,d1,q,WT,wTheta,Do,dB,p)

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
    newMotor.testTeeth(3.3,129,1,24,9.6,70,200,9.2,2)
    
    input("press enter to exit")