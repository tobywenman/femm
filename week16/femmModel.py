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

    def drawTeeth(self,q,WT,dB,p,D,Do):
        slotPitch = 360/q
        toothAngle = math.degrees(WT/D)
        backIronAngle = slotPitch-toothAngle
        backIronDepth = Do-dB

        startAngle = (180-(360/(p/2)))/2

        frontPoints = self.drawArc(startAngle,toothAngle/2,D)
        mi_addsegment(frontPoints[0],frontPoints[1],Do*math.cos(startAngle),Do*math.sin(startAngle))

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
            mi_addsegment(frontPoints[2],frontPoints[3],Do*math.cos(math.radians(startAngle+360/(p/2))),Do*math.sin(math.radians(startAngle+360/(p/2))))





if __name__=="__main__":
    openfemm()
    newdocument(0)
    
    newMotor = motor()
    newMotor.drawDo(200,2)
    newMotor.drawTeeth(24,8.7,16.5,2,116,200)
    
    input("press enter to exit")