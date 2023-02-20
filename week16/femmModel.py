from femm import *
import math

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


    def drawTeeth(self,q,WT,dB,p,D,Do):
        slotPitch = 360/q
        toothAngle = math.degrees(WT/D)
        backIronAngle = slotPitch-toothAngle
        backIronDepth = Do-dB

        startAngle = (180-(360/(p/2)))/2

        frontPoints = self.drawArc(startAngle,toothAngle/2,D)
        
        if p > 2:
            p1 = self.polarToCart(startAngle,Do)
            mi_drawline(frontPoints[0],frontPoints[1],p1[0],p1[1])

        for i in range(q//(p//2)-1):
            backPoints = self.drawArc(i*slotPitch+startAngle+toothAngle/2,backIronAngle,backIronDepth)
            mi_addsegment(backPoints[0],backPoints[1],frontPoints[2],frontPoints[3])
            frontPoints = self.drawArc(i*slotPitch+startAngle+(toothAngle/2)+backIronAngle,toothAngle,D)
            mi_addsegment(backPoints[2],backPoints[3],frontPoints[0],frontPoints[1])
        
        backPoints = self.drawArc((q//(p//2)-1)*slotPitch+startAngle+toothAngle/2,backIronAngle,backIronDepth)
        mi_addsegment(backPoints[0],backPoints[1],frontPoints[2],frontPoints[3])
        frontPoints = self.drawArc((q//(p//2)-1)*slotPitch+startAngle+(toothAngle/2)+backIronAngle,toothAngle/2,D)
        mi_addsegment(backPoints[2],backPoints[3],frontPoints[0],frontPoints[1])
        if p > 2:
            mi_drawline(frontPoints[2],frontPoints[3],Do*math.cos(math.radians(startAngle+360/(p/2))),Do*math.sin(math.radians(startAngle+360/(p/2))))
        
        for i in range(q//(p//2)):
            p1 = self.polarToCart((startAngle)+(toothAngle/2)+slotPitch*i,D)
            p2 = self.polarToCart(backIronAngle+(startAngle)+(toothAngle/2)+slotPitch*i,D) 
            mi_addarc(p1[0],p1[1],p2[0],p2[1],backIronAngle,1)

    def makeMotor(self,D,Do,WT,dB,q,p):
        self.drawDo(Do,p)
        self.drawTeeth(q,WT,dB,p,D,Do)
        





if __name__=="__main__":
    openfemm()
    newdocument(0)
    
    newMotor = motor()
    newMotor.drawDo(200,2)
    newMotor.drawTeeth(24,8.7,16.5,2,116,200)
    
    input("press enter to exit")