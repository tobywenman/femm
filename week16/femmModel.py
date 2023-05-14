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


    def drawTeeth(self,q,WT,dB,p,D,Do,W1,d1):
        startAngle = (180-(360/(p/2)))/2

        slotPitch = 360/q
        gapAngle = math.degrees(W1/D)

        self.drawArc(startAngle,(slotPitch/2)-(gapAngle/2),D)

        p1 = self.polarToCart(startAngle+(slotPitch/2),D)
        p2 = self.polarToCart(startAngle+(slotPitch/2),Do)

        toothVector = np.array([p2[0]-p1[0],p2[1]-p1[1]])

        toothVector = toothVector / np.linalg.norm(toothVector)
        toothVector = toothVector * d1

        perpVector = np.array([1,-toothVector[0]/toothVector[1]])
        perpVector = perpVector / np.linalg.norm(perpVector) 
        perpVector = perpVector * (W1/2)

        toothVector = toothVector+perpVector

        mi_addnode(p1[0]+toothVector[0],p1[1]+toothVector[1])
        p3 = self.polarToCart(startAngle+(slotPitch/2)-(gapAngle/2),D)
        mi_addsegment(p3[0],p3[1],p1[0]+toothVector[0],p1[1]+toothVector[1])

    def testTeeth(self,W1,D,d1,q,WT,wTheta,Do,dB,p):
        Ds = Do-dB
        wTheta = math.radians(wTheta)
        slotPitch = math.radians(360/q)
        beta = math.asin(W1/D)
        a = (D/2) * math.cos(beta) + d1 - (W1*math.cos(slotPitch/2)+WT)/(2*math.sin(slotPitch/2))
        b = a * (math.sin(slotPitch/2)/math.sin(wTheta-slotPitch/2))

        points = []

        points.append(np.matrix((W1/2,math.cos(beta)*D/2)))

        points.append(np.matrix((W1/2,d1+math.cos(beta)*D/2)))
        points.append(np.matrix(((W1/2)+b*math.sin(wTheta),math.cos(beta)*D/2+d1+b*math.cos(wTheta))))
        points.append(np.matrix((math.sin(slotPitch/2)*math.sqrt(Ds**2-WT**2)/2-math.cos(slotPitch/2)*WT/2,math.cos(slotPitch/2)*math.sqrt(Ds**2-WT**2)/2+math.sin(slotPitch/2)*WT/2)))



        for i in reversed(points):
            points.append(i*np.matrix([[-1,0],[0,1]]))

        slotPitch = math.pi*2/q

        pointsLen = len(points)
        for i in range(1,q//p):
            for j in range(pointsLen):
                angle = -i*slotPitch
                rotMatrix = np.matrix([[math.cos(angle),-math.sin(angle)],
                                       [math.sin(angle),math.cos(angle)]])
                points.append(points[j]*rotMatrix)
       
        mi_addnode(points[0][0,0],points[0][0,1])
        prevPoint = points[0]

        for i in points[1:]:
            mi_addnode(i[0,0],i[0,1])
            mi_addsegment(i[0,0],i[0,1],prevPoint[0,0],prevPoint[0,1])
            prevPoint = i

        
    


        
        
    
    
    def drawAirGap(self,g,D,p):
        self.drawDo(D-g,p)
        if p > 2:
            p1 = self.polarToCart((180-(360/(p/2)))/2,D)
            p2 = self.polarToCart((180-(360/(p/2)))/2,D-g)
            mi_addsegment(p1[0],p1[1],p2[0],p2[1])
            p1 = self.polarToCart(((180-(360/(p/2)))/2)+(360/(p/2)),D)
            p2 = self.polarToCart(((180-(360/(p/2)))/2)+(360/(p/2)),D-g)
            mi_addsegment(p1[0],p1[1],p2[0],p2[1])

    def makeMotor(self,D,Do,WT,dB,q,p,g,W1,d1):
        self.drawDo(Do,p)
        self.drawTeeth(q,WT,dB,p,D,Do,W1,d1)
        self.drawAirGap(g,D,p)

    
        





if __name__=="__main__":

    newMotor = motor()
    newMotor.testTeeth(3.3,129,1,24,9.6,70,200,9.2,4)
    
    input("press enter to exit")