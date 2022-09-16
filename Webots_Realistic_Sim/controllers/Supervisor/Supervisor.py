from controller import Supervisor,Display, ImageRef
from time import time,ctime 
from numpy.random import random
import numpy as np
from math import sqrt
import os
TEST=not True
############################################
if TEST : ROBN= 1 #1 #5                      #########
else: ROBN=5*2
############################################
# Ftime=5002
# Htime=Ftime/2
Ftime=10000
Htime=Ftime
print("Htime",Htime,"Ftime",Ftime)
if TEST:
    sd=round(int(time())%1000)
    sd=764
    np.random.seed(sd)
    print("supervisor seed", sd)

sup=Supervisor()
SAMPELING_PERIOD=1
static=True
timestep = int(sup.getBasicTimeStep())
strs=["_"+str(_) for _ in range(1,ROBN+1)]
defs=[sup.getFromDef(_) for _ in strs]
fld=[_.getField("translation") for _ in defs]  
rfld=[_.getField("rotation") for _ in defs]
Time=sup.getTime()
tottime=sup.getTime()
data=[]
count=0
####################################################################################################################
def determine_method():
    # p=os.getcwd()
    p='/home/arash/Desktop/ph4/15 x/controllers/epuck'
    fm=open(p+"/counterr.txt",'r')
    cnt=int(fm.read())-1
    fm.close()
    if cnt>5: return True
    else: return False  
####################################################################################################################
def check_cue(static):
    if static :
    	return list(map(lambda x: True if abs(x[0])<0.4 and x[1]>-1.4 and x[1]<-0.6 else False,pos))
    else:
        return list(map(lambda x: True if abs(x[0])<0.4 and x[1]>0.6 and x[1]<1.4 else False,pos))

####################################################################################################################
def dist(x,y):
    return sqrt((x[0]-y[0])**2+(x[2]-y[2])**2)
####################################################################################################################
def distribute():
    fault_flag=False
    mem=[]    
    x=np.random.uniform(-0.8,0.8,20)
    y=np.random.uniform(-1.35,1.35,20)
    i=0
    while i <ROBN:
        for j in range(0,min(len(mem),20)):
            if dist([x[i],0,y[i]],mem[j])<0.3:
                x[i]=np.random.uniform(-0.8,0.8)
                y[i]=np.random.uniform(-1.35,1.35)
                fault_flag=True
                break

        if dist([x[i],0,y[i]],[0,0,-0.8])<0.6:
            x[i]=np.random.uniform(-0.8,0.8)
            y[i]=np.random.uniform(-1.35,1.35)
            fault_flag=True

        if fault_flag:
            fault_flag=False
            continue
        mem.append([x[i],0,y[i]])

        pv=[x[i],0,y[i]]

        fld[i].setSFVec3f(pv)
        rot=[0,1,0,random()*6.28] 

        rfld[i].setSFRotation(rot)
        i+=1
####################################################################################################################
def getPos(defs):
    return [[_.getPosition()[0],_.getPosition()[2]] for _ in defs] 
####################################################################################################################
def delay(x):
    t=sup.getTime()
    while sup.step(timestep) != -1: 
        if sup.getTime()-t>x: break
####################################################################################################################
def change_background():
    delay(0.1)
    im=dis.imageLoad("Secondary_background.png")
    # im=dis.imageLoad("Initial_background.png")
    # im=dis.imageLoad("Initial_background_x.png")

    dis.imagePaste(im,0,0,False)
    delay(0.1)
#----------------------------------------------------------------------------------------------------------------------------------------
stime=ctime(time()).replace(':','_')
logname=stime+" position log.txt"
stime=stime+str(True)
print("sup stime",stime)
if not TEST:
    distribute()
    os.makedirs(stime)
    ff=open(stime+"/"+logname,"a")
dis=sup.getDisplay('display')
im=dis.imageLoad("Initial_background.png")
dis.imagePaste(im,0,0,False)        
if TEST: exit(0)
while sup.step(timestep) != -1:
    pos=getPos(defs)

    if sup.getTime()-Time>SAMPELING_PERIOD/2 and not round(sup.getTime())%SAMPELING_PERIOD:
        incue=check_cue(static)
        c=incue.count(True)
        data.append(c)
        Time=round(sup.getTime())
        for i in range(0,ROBN):    
            strng=str(Time)+" "+\
                str(i)+" "+\
                str(defs[i].getPosition()[0])+" "+\
                str(defs[i].getPosition()[2])+" "+\
                str(rfld[i].getSFRotation()[3])+" "+\
                str(incue[i])+"\n"

            ff.write(strng)
 
    if sup.getTime()-tottime>SAMPELING_PERIOD*10:
        tottime=sup.getTime()
        print('.',round(sup.getTime()))

    if sup.getTime()>=Htime and static and Htime!=Ftime:
        print(sup.getTime())
        print("\n----------------static done-----------------\n")
        change_background()
        static=False

    if sup.getTime()>=Ftime:
        print("\n----------------dynamic done-----------------\n")
        f = open(stime+"/"+stime+".txt", "w")
        f.write(str(data))
        f.close()
        ff.close()
        delay(10)
        print("\n----------------reseting-----------------\n")
        sup.simulationReset()
