import iRobotCreate
import numpy as np
import time

r = iRobotCreate.iRobotCreate(1)
dist = 0.2
r.trajectory()
r.set_trail_size(100)
x = 5
y = 2

xobst = np.zeros(4)
yobst = np.zeros(4)
xobst[0] = 3
yobst[0] = 1
xobst[1] = 3
yobst[1] = 0.6
xobst[2] = 3
yobst[2] = 0.2
xobst[3] = 3
yobst[3] = 0

time = 0
d=10000
r.forward(0.1)
print d
while dist<d and time<100:
    [rx,ry,rt] = r.get_pose()
    xt = x-rx
    yt = y-ry
    d = ((xt)**2+(yt)**2)**0.5
    theta = np.arctan2(yt,xt)
    xt = d*np.cos(theta - rt*3.1415/180)
    yt = d*np.sin(theta - rt*3.1415/180)
    
    xto = xobst-rx
    yto = yobst-ry
    d = ((xto)**2+(yto)**2)**0.5
    theta = np.arctan2(yto,xto)
    xto = d*np.cos(theta - rt*3.1415/180)
    yto = d*np.sin(theta - rt*3.1415/180)
    
    r.goToGoal(xt,yt,[xto,yto])
    r.distance_sensor()
    r.angle_sensor()
    d = ((rx-x)**2+(ry-y)**2)**0.5
    print xt,yt,rx,ry,rt,d
    time+=1
obst = [xobst,yobst]
r.sim(obst)

    
