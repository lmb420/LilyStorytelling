from IPC import *
from nitepy import *
import threading
import thread
import sys

#conditions for determining a pose using standard parameters
#all distances specified in terms of torso to neck distance. 
#c is core distance
#shoulder to elbow distance should be approximately 1.2c
#hand to elbow should be approximately 1.2c
#knee to hip should be approximately 2c


#poses ignore some body parts
#poses define relative positioning of limbs in terms of c
#a transition between poses requires that all factors approach their new values monotonically (approximately)
#a gesture is a series of poses

#Other thought: larger modes of behavior (ie running, jumping, walking, sitting, etc) cannot be defined by a FSM since they can be performed
#in many ways, (see ministery of silly walks).  Therefore, other key aspects must be monitored such as movement speed and activity levels of #different limbs in addition to their apporoximate locations relative to the torso.

class poses:
    def RightArmExtRight(self,user):
        #get distance to exact pose
        dist = (lib.getUserSkeletonR_HandX(track,user)-lib.getUserSkeletonR_ShX(track,user))-2*(lib.getUserSkeletonNeckY(track,user)-lib.getUserSkeletonTorsoY(track,user))
        return dist
    
    def LeftArmExtLeft(self,user):
        dist = (-lib.getUserSkeletonL_HandX(track,user)+lib.getUserSkeletonL_ShX(track,user))-2*(lib.getUserSkeletonNeckY(track,user)-lib.getUserSkeletonTorsoY(track,user))
        return dist

    def LeftArmAboveLeftSh(self,user):
        dist = abs((lib.getUserSkeletonL_HandY(track,user)-lib.getUserSkeletonL_ShY(track,user))-0.5*(lib.getUserSkeletonNeckY(track,user)-lib.getUserSkeletonTorsoY(track,user)))+abs(lib.getUserSkeletonL_HandX(track,user)-lib.getUserSkeletonL_ShX(track,user))
        return dist
        
    def RightArmAboveRightSh(self,user):
        dist = abs((lib.getUserSkeletonR_HandY(track,user)-lib.getUserSkeletonR_ShY(track,user))-0.5*(lib.getUserSkeletonNeckY(track,user)-lib.getUserSkeletonTorsoY(track,user)))+abs(lib.getUserSkeletonR_HandX(track,user)-lib.getUserSkeletonR_ShX(track,user))
        return dist
    def RightArmExtFront(self,user):
        dist = (-lib.getUserSkeletonR_HandZ(track,user)+lib.getUserSkeletonR_ShZ(track,user))-2.4*(lib.getUserSkeletonNeckY(track,user)-lib.getUserSkeletonTorsoY(track,user))
        return dist
    def LeftArmExtFront(self,user):
        dist = (-lib.getUserSkeletonL_HandZ(track,user)+lib.getUserSkeletonL_ShZ(track,user))-2.4*(lib.getUserSkeletonNeckY(track,user)-lib.getUserSkeletonTorsoY(track,user))
        return dist
        
