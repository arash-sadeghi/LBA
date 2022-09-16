from controller import Robot
from controller import Motor, PositionSensor
import numpy as np
from math import sqrt,atan2,sin,cos,atan
from random import random
from os import getcwd
from time import time as Time_function
from time import ctime

import os
import sys
import cv2 as cv
####################################################################################################################
############################################
method=True                        #########
TEST= not True
cheat=False
############################################
VISUAL_OFFSET=0.1*2*2*100000
robot = Robot()
name= robot.getName()
Ftime=10000
imx=100*3
imy=100*3
SPPED_MULTP=1
if TEST:
    sd=round(int(Time_function())%1000)
    sd=84+int(name[-2])
    # sd=22+int(name[-2])
    np.random.seed(sd)
    print("TEST is ",TEST," seed for",name," ",sd)
    inspct='robot(1)'
    Wmax=120*0
else:
    inspct='robot(1x)'
    sd=round(int(Time_function())%1000)
    sd+=int(name[-2])
    np.random.seed(sd)
    print("TEST is ",TEST," seed for",name," ",sd)
    Wmax=120


real=True
sigma=0
FW=6.28

# arena config
arena_x=2
arena_y=4
Lx=2
Ly=2*Lx
c1=Ly/4
QRlocs=[(0,-(Ly/2)),(Lx/2,-c1),(Lx/2,0),(Lx/2,c1),(0,(Ly/2)),(-(Lx/2),c1),(-(Lx/2),0),(-(Lx/2),-c1)]

SEN_THRESH=470
COL_SEN_THR=200
collision_recognition=" "
flag=False
timestep = int(robot.getBasicTimeStep())
motors=[[],[]]
motors[0]=robot.getMotor("left wheel motor")
motors[1]=robot.getMotor("right wheel motor")
motors[0].setPosition(float("inf"))
motors[1].setPosition(float("inf"))
motors[0].setVelocity(0)
motors[1].setVelocity(0)

ps=[[],[]]
ps[0]=motors[0].getPositionSensor()
ps[0].enable(timestep)
ps[1]=motors[1].getPositionSensor()
ps[1].enable(timestep)

rr=robot.getDistanceSensor('rr')
rr.enable(timestep)
ll=robot.getDistanceSensor('ll')
ll.enable(timestep)

ds=[[np.nan] for _ in range(0,8)]
ds[0]= robot.getDistanceSensor('ps0')
ds[0].enable(timestep)
ds[1]= robot.getDistanceSensor('ps1')
ds[1].enable(timestep)
ds[2]= robot.getDistanceSensor('ps2')
ds[2].enable(timestep)
ds[3]= robot.getDistanceSensor('ps3')
ds[3].enable(timestep)
ds[4]= robot.getDistanceSensor('ps4')
ds[4].enable(timestep)
ds[5]= robot.getDistanceSensor('ps5')
ds[5].enable(timestep)
ds[6]= robot.getDistanceSensor('ps6')
ds[6].enable(timestep)
ds[7]= robot.getDistanceSensor('ps7')
ds[7].enable(timestep)

gps=robot.getGPS("gps")
gps.enable(timestep)

comp=robot.getCompass("compass")
comp.enable(timestep)
if real:
    cam=robot.getCamera("camera")
    cam.enable(timestep)
####################################################################################################################
def filter(strng):
    if not (name in strng) :
        if name==inspct or flag: print(name,"stoped")
        exit()
#####################################################################################################################

STATE='-'
QRnum=8
time=robot.getTime()
vec_qr_mem=np.zeros((QRnum,2))
error=[0 for _ in range(0,QRnum)]
SAMPELING_PERIOD=1 #----------------------------------------
if not TEST:
    stime=ctime(Time_function()).replace(':','_')+" "+str(method)
    stime=stime[0:16]
    fname=stime+" "+robot.getName()
    print(name," dir name ",stime)
    if name=="robot(1)": os.makedirs(stime)
    try:
        fn=open(stime+"/"+fname+".txt","a")
        fe=open(stime+"/"+fname+" errors .txt","a")
        fs=open(stime+"/"+fname+" STATES .txt","a")
    except Exception as E:
        print(E,name," dir name error ",stime)
else: filter("robot(1)")
####################################################################################################################
def logger_main():
    global time,STATE
    if robot.getTime()-time>SAMPELING_PERIOD/2 and not round(robot.getTime())%SAMPELING_PERIOD and not TEST:
        time=robot.getTime()
        fn.write("\n"+str(round(robot.getTime()))+"\n"+str(vec_qr_mem)+"\n")
        fe.write(str(round(robot.getTime()))+" "+str(error)+"\n")
        fs.write(str(round(robot.getTime()))+" "+STATE+"\n")

    if robot.getTime()>=Ftime and not TEST:
        fn.close()
        fe.close()
        fs.close()

        print("ready to exit")
        exit(0)
####################################################################################################################
#.....................................................................................................................
def Noise():
    global sigma
    noise= (1-2*np.random.random())*180
    return noise*sigma
#####################################################################################################################
class clr:
    HEADER = '\033[95m'
    B = '\033[94m'
    G = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
####################################################################################################################
def wait(posQR,remember_flag):
    global Wmax
    dsval=[ds[_].getValue() for _ in range(0,8)]
    detect=list(map(lambda x: x>COL_SEN_THR,dsval))
    if detect.count(True)>0:         
        stop()
        Ws=Wmax*((avrg(True)**2)/(avrg(True)**2 + 5000))
        delay(Ws)
        avoid_col(posQR,remember_flag)
        go()
####################################################################################################################
def rotate(posQR,remember_flag,dir,angle):
    global FW,SPPED_MULTP
    # print("FW",FW)
    EQ_THR=0.1
    FW=FW/SPPED_MULTP
    # print("rot",posQR)
    if name==inspct or flag: print("rotate ",posQR,remember_flag,dir,angle)
    rot_coeff=2.65
    # rot_coeff*=1.57/1.81
    if dir=='r':
        motors[0].setVelocity(-FW)
        motors[1].setVelocity(FW)

        if angle==0: rnd=180*rot_coeff/90#rnd=(((np.random.random()*100)%90+90)%180)*rot_coeff/90
        else: rnd=angle*rot_coeff/90
 
        if remember_flag:

            posQR[2]=posQR[2]+90*rnd/rot_coeff
            
            if posQR[2]>360: posQR[2]-=360
            elif posQR[2]<0: posQR[2]+=360
        # rnd=rot_coeff
        mem=ps[0].getValue()-rnd
        while robot.step(timestep) != -1:
            logger_main()
            if abs(ps[0].getValue()-mem)<EQ_THR: break

    elif dir=='l':
        motors[0].setVelocity(FW)
        motors[1].setVelocity(-FW)

        if angle==0: rnd=180*rot_coeff/90 #rnd=(((np.random.random()*100)%90+90)%180)*rot_coeff/90
        else: rnd=angle*rot_coeff/90


        if remember_flag:        
            posQR[2]=posQR[2]-90*rnd/rot_coeff
            if posQR[2]>360: posQR[2]-=360
            elif posQR[2]<0: posQR[2]+=360
        # rnd=rot_coeff
        mem=ps[0].getValue()+rnd
        while robot.step(timestep) != -1: 
            logger_main()
            if abs(ps[0].getValue()-mem)<EQ_THR: break

    elif dir=='f':
        motors[0].setVelocity(FW)
        motors[1].setVelocity(FW)
        mem=ps[0].getValue()+angle
        while robot.step(timestep) != -1: 
            logger_main()
            if abs(ps[0].getValue()-mem)<EQ_THR: break
    if name==inspct or flag: print("POSQR at then end for rot",posQR)
    FW*=SPPED_MULTP
####################################################################################################################
def detect_col():
    global collision_recognition
    dsval=[ds[_].getValue() for _ in range(0,8)]
    detect=list(map(lambda x: x>COL_SEN_THR,dsval))
    if detect.count(True)>0: 
        return True
    else : return False
####################################################################################################################
def w_r_recog():
    if abs(cord(False)[1])>(arena_y/2-0.05) or abs(cord(False)[0])>(arena_x/2-0.05):
        if name==inspct or flag:print("\nit is wall")
        return "wall"
    else:
        if name==inspct or flag:print("it is robot")
        return "robot"
####################################################################################################################
def avoid_col(posQR,remember_flag,prt=False):
    # print("avoid",posQR)
    dsval=[ds[_].getValue() for _ in range(0,8)]
    detect=list(map(lambda x: x>COL_SEN_THR,dsval))
    if prt: 
        if name==inspct or flag: print (name," AV ",dsval,detect)
    if detect_col():
        if detect[0] or detect[1] or detect[2]:
            rotate(posQR,remember_flag,'r',0)
            motors[0].setVelocity(FW)
            motors[1].setVelocity(FW)
            delay(0.1)
        elif detect[6] or detect[7]:
            rotate(posQR,remember_flag,'l',0)
            motors[0].setVelocity(FW)
            motors[1].setVelocity(FW)
            delay(0.1)
####################################################################################################################
def check_ground():
    #510 b 90 w
    lst=[rr.getValue(),ll.getValue()]
    # if name==inspct or flag: print("lst of ground sens",lst)
    c1=list(map(lambda x: True if x<SEN_THRESH else False,lst)).count(True)
    delay(0.01)
    lst=[rr.getValue(),ll.getValue()]
    c2=list(map(lambda x: True if x<SEN_THRESH else False,lst)).count(True)
    delay(0.01)
    lst=[rr.getValue(),ll.getValue()]
    c3=list(map(lambda x: True if x<SEN_THRESH else False,lst)).count(True)
    delay(0.01)
    c=[c1,c2,c3]
    
    if c.count(0)>1:
        return False
    else: 
        return True
####################################################################################################################
def delay(x):
    if x=='inf':
        while robot.step(timestep) != -1: pass
        
    t=robot.getTime()
    while robot.step(timestep) != -1:
        logger_main() 
        if robot.getTime()-t>x: return 1
####################################################################################################################
def hello():
    print (name, "xxxxxxx")
####################################################################################################################
def clear():
    if name==inspct or flag: print (name, '\f')
####################################################################################################################
def go():
    motors[0].setVelocity(FW)
    motors[1].setVelocity(FW)      
####################################################################################################################
def stop():
    motors[1].setVelocity(0)
    motors[0].setVelocity(0)
####################################################################################################################
def stnd_cue():
    val=np.array([rr.getValue(),ll.getValue()])
    valstnd = 520 - val
    valstnd=valstnd*255.0/430.0
    return valstnd
####################################################################################################################
def avrg(f=False):
    if f : stnd=stnd_cue(); return abs(stnd[0]+stnd[1])/2
    else : return (rr.getValue()+ll.getValue())/2.0 
#.....................................................................................................................
def make0_360(x):
    while x>360: x-=360
    while x<0: x+=360
    return x
#.....................................................................................................................
def cord(rot_f=True):
    pos=gps.getValues()
    rotx=np.array(comp.getValues())
    # rot=atan2(rotx[0],rotx[2])/np.pi*180-90#zaviyeye xatte abi
    rot=atan2(rotx[2],rotx[0])
    # rot=(rot-1.5708)*180/np.pi
    rot=rot*180/np.pi
    rot+=180
    if rot<0.0: rot+=360.0
    if rot>360.0: rot-=360.0

    if rot_f==True: return rot
    else: return [pos[0],pos[2],rot]
#.....................................................................................................................
def checkQR():
    global VISUAL_OFFSET,imx,imy
    pos=cord(False)
    if real:
        Im=cam.getImage()

        im=list(Im)
        imlen=len(im)
        img=np.zeros((1,int(imlen/4)))[0]
        i=0;j=0

        indx=range(0,int(imlen),4)
        for i in indx:
            img[int(i/4)]=im[i]
        imgar_=np.zeros((imy,imx))
        i=0;j=0

        for i in range(imx-1):
            imgar_[i,:]=img[i*imx:(i+1)*imx]
        imgar_=np.uint8(imgar_)

        # imgar=cv.resize(imgar_,(200,200))
        imgar=imgar_

        detector = cv.QRCodeDetector()
        try:
            data, bbox, straight_qrcode = detector.detectAndDecode(imgar)
        except Exception as E:
            print(" an error has encountered", name,E)
            return None,None,"Q0"
        if (not (bbox is None)) and (not (data is None)):
            bboxar=np.zeros((4,2))
            bboxar[0,0]=int(bbox[0][0][0]);bboxar[0,1]=int(bbox[0][0][1])
            bboxar[1,0]=int(bbox[1][0][0]);bboxar[1,1]=int(bbox[1][0][1])
            bboxar[2,0]=int(bbox[2][0][0]);bboxar[2,1]=int(bbox[2][0][1])
            bboxar[3,0]=int(bboxar[0,0]);bboxar[3,1]=int(bboxar[2,1])
            s=np.sign(atan2((bboxar[0,1]-bboxar[1,1]),(bboxar[0,0]-bboxar[1,0])))
            ss=atan2((bboxar[0,1]-bboxar[1,1]),(bboxar[0,0]-bboxar[1,0]))*180/np.pi
            im=imgar
            size = im.shape
            image_points = np.array([
                                    (bboxar[0,0], bboxar[0,1]),     # right
                                    (bboxar[3,0], bboxar[3,1]),     # middle
                                    (bboxar[2,0],bboxar[2,1]),     # down
                                    (bboxar[1,0], bboxar[1,1]),     # Right eye right corne
                                    # (345, 465),     # Left Mouth corner
                                    # (453, 469)      # Right mouth corner

                                ], dtype="double")

            model_points = np.array([
                                    (-1, -1, 0),             # Nose tip
                                    (1, -1, 0),        # Chin
                                    (1, 1, 0),     # Left eye left corner
                                    (-1, 1.0, 0),      # Right eye right corne
                                    # (-150.0, -150.0, -125.0),    # Left Mouth corner
                                    # (150.0, -150.0, -125.0)      # Right mouth corner
                                
                                ])

            focal_length = size[1]
            center = (size[1]/2, size[0]/2)
            camera_matrix = np.array(
                                    [[focal_length, 0, center[0]],
                                    [0, focal_length, center[1]],
                                    [0, 0, 1]], dtype = "double"
                                    )

            dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
            (success, rotation_vector, translation_vector) = cv.solvePnP(model_points, image_points, camera_matrix, dist_coeffs,flags=cv.SOLVEPNP_P3P)

            if success and (not (rotation_vector is None)) and (not (translation_vector is None)) and (not (data is '')):
                rotation_matrix, jacobian = cv.Rodrigues(rotation_vector)
                C = np.matmul(-rotation_matrix.transpose(), translation_vector) # position coordinate
                O = np.matmul(rotation_matrix.T, np.array([0, 0, 1]).T)*180/np.pi
                C[1]=abs(C[1])
                C[1]*=s*(-1)
                trans=C
                trans=trans/10
                trans=[trans[1],trans[0],2-trans[2]]
                try : 
                    data=data[0]+data[-1]
                except Exception as E:
                    print(E,data)
                    exit(0)
                return trans,rotation_vector*180/np.pi,data
            else:
                return None,None,"Q0"
        else:
            return None,None,"Q0"

#.....................................................................................................................
def add_arrows(arrow,posQR,last_QR,sudovec,trans):
    global Lx,Ly,QRlocs
    try:
        vec=np.array(arrow[1:len(arrow)])
    except Exception as E:
        print(E,arrow[1:len(arrow)])
        exit(1)

    vecx=np.zeros((np.size(vec,0)+1,np.size(vec,1)))
    # vecx=np.zeros((np.size(vec,0),np.size(vec,1)))

    for i in range(0,np.size(vec,0)):
        vecx[i,1]=vec[i,1]*cos(vec[i,0]*np.pi/180.0)
        vecx[i,0]=vec[i,1]*sin(vec[i,0]*np.pi/180.0)
    
    vecx[i+1,:]=sudovec
    totvecx=[sum(vecx[:,0]),sum(vecx[:,1])]
    
    totvec=[0,0]
    totvec[0]=atan2(totvecx[0],totvecx[1])*180/np.pi
    totvec[0]=make0_360(totvec[0])
    totvec[1]=sqrt(totvecx[0]**2+totvecx[1]**2)
    if name==inspct or flag: print("\n<><>add arrow says vec",vec,"\n\nvecx",vecx,"\n\ntotvecx",totvecx,"\n\ntotvec",totvec,"\n\n")
    return totvec
#.....................................................................................................................

def go_vec(vec,posQR,last_QR):
    global sigma
    vec_,posQR_,last_QR_=vec,posQR,last_QR
    rev_flag=False
    #--
    sudovec=calc_sudovec(last_QR,"go_vec")
    vec_x=vec_[1]*sin(vec_[0]*np.pi/180.0)
    vec_y=vec_[1]*cos(vec_[0]*np.pi/180.0)
    totvecx=[sudovec[0]+vec_x,sudovec[1]+vec_y]
    totvecx=[vec_x,vec_y]

    vecn=atan2(totvecx[0],totvecx[1])*180/np.pi
    #--

    ####
    if sigma!=0:
        if name == inspct : print(last_QR,"vec before noise ",vec)
        vecn=vecn+Noise()
        # if name == inspct : print(last_QR,"vec after noise ",vecn)
    else: vecn=vecn
    ####
    rot=vecn-posQR_[2]
    rot=make0_360(rot)
    rot_dir='r'
    # if name==inspct or flag: print("vec[0]",vec[0] , "posQR[2]" ,posQR[2], "rot",rot, "rot_dir",rot_dir,"rev_flag",rev_flag)
    if name==inspct or flag: print("go_vec says: vecn",vecn," posQR_[2]",posQR_[2],"rot",rot, "rot_dir",rot_dir,"rev_flag",rev_flag)

    if rot!=0: rotate(0,0,rot_dir,rot)
    go()

#.....................................................................................................................
def determine_method():
    # p="/home/arash/Desktop/ph3/Ultra perfect 20 automatic/single perfect/controllers/epuck"
    p=getcwd()
    if robot.getName()=='robot(1)':
 
        fm=open(p+"/counterr.txt",'r')
        cnt=int(fm.read())
        fm.close()

        fm=open(p+"/counterr.txt",'w')
        fm.write(str(cnt+1))
        fm.close()
        
        print("cnt",cnt)

        if cnt>5: return True
        else: return False  
    else:
        fm=open(p+"/counterr.txt",'r')
        cnt=int(fm.read())-1
        fm.close()
        if cnt>5: return True
        else: return False  
#.....................................................................................................................
def calc_sudovec(last_QR,call,ROT,trans):
    global QRlocs
    if cheat:
        if call=="add_arrow":
            pos=cord(False)
            pos=[pos[0],pos[1]]
            QRpos=QRlocs[int(last_QR[-1])-1]
            sudovec=np.array([pos[0]-QRpos[0],pos[1]-QRpos[1]])

        if call=="go_vec":
            pos=cord(False)
            pos=[pos[0],pos[1]]
            QRpos=QRlocs[int(last_QR[-1])-1]
            sudovec=np.array([-pos[0]+QRpos[0],-pos[1]+QRpos[1]])
        sudovec*=20/0.4
        # print(call+"<->",pos,QRpos,last_QR,"sudovec",sudovec)
        return sudovec
    else:
        X=trans[0]
        Y=trans[2]

        if call=="add_arrow":
            sudovec=np.array([-X,-Y])
        if call=="go_vec":
            sudovec=np.array([X,Y])

    sudovec*=20/0.4
    return sudovec

    
    
    
    
    
    
    
    
    
    
        
