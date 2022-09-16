from epuckfunc import *
# from scipy.io import savemat
import epuckfunc
np.set_printoptions(threshold=sys.maxsize)
CAMERA_SMP=3
TOLERANCE=5
if name=="robot(1)": print("sigma",sigma,"TOLERANCE",TOLERANCE,"VISUAL_OFFSET",VISUAL_OFFSET)

if name=='robot(1)': print('ding')
delay(1)
if name=='robot(1)': print('dong')

go()
hello()
remember_flag=False
posQR=[0,0,0]
arrows=[[0,0]]
count=0
count2=0
count3=0
last_QR='hi' # this will cause glitch if robot starts from inside the cue

QR_oc_mat=[0 for _ in range(0,QRnum)]
gab=ps[0].getValue()

tx=robot.getTime()
count_L=0
cam_count=0
trans=0
X=np.arange(-0.8,0.8,0.05)
Y=np.arange(0.4,1.8,0.05)
mat=np.zeros((len(X),len(Y),6,10))
last_x=0
last_y=0
i=0
params=np.zeros((6,10))-1
dataFlag=0
indx_x=0
indx_y=0
stop()

error_x=-1
error_y=-1
error_rot=-1

while robot.step(timestep) != -1:
            # OUT=checkQR()
            # trans=OUT[0]
            # ROT=OUT[1]
            # data=OUT[2]
            # if not(ROT is None) :
            #     ROT[2]=ROT[2]*np.sign(ROT[0])*(-1)
            #     trans=trans/10
            #     trans=[trans[1],trans[0],2-trans[2]]
    if method:
        go()
        if not TEST: logger_main()
        # scenario 2
        if not TEST:
            if check_ground():
                if detect_col():
                    if remember_flag:
                        count3+=1
                        if count3==1:
                            if vec_qr_mem[int(last_QR[1])-1,0]==0 and vec_qr_mem[int(last_QR[1])-1,1]==0:
                                arrows.append([posQR[2],ps[0].getValue()-gab])
                                vec_qr_mem[int(last_QR[1])-1]=add_arrows(arrows,posQR,last_QR,sudovec,trans)
                                if name==inspct or flag: print('I found cue after seeing \n',last_QR,"vec_qr_mem\n",vec_qr_mem)
                                gab=ps[0].getValue()
                            else:
                                if name==inspct or flag: print('I have seen',last_QR,"before","vec_qr_mem\n",vec_qr_mem)

                wait(posQR,remember_flag)

        # scenario 1
        elif TEST:
            if check_ground():
                if remember_flag:
                    count3+=1
                    if count3==1:
                        if vec_qr_mem[int(last_QR[1])-1,0]==0 and vec_qr_mem[int(last_QR[1])-1,1]==0:
                            arrows.append([posQR[2],ps[0].getValue()-gab])
                            vec_qr_mem[int(last_QR[1])-1]=add_arrows(arrows,posQR,last_QR,sudovec,trans)
                            if name==inspct or flag: print('I found cue after seeing \n',last_QR,"vec_qr_mem",vec_qr_mem)
                            gab=ps[0].getValue()
                        else:
                            if name==inspct or flag: print('I have seen',last_QR,"before","vec_qr_mem",vec_qr_mem)

                if detect_col():  wait(posQR,remember_flag)


        if not check_ground() :
            count3=0
            if detect_col():
                if remember_flag:
                    if QR_oc_mat[int(last_QR[1])-1]==1 and checkQR()==last_QR:
                        # if name==inspct or flag: print("\n 1 before gab,ps[0].getValue()",gab,ps[0].getValue())
                        avoid_col(posQR,remember_flag)
                        gab=ps[0].getValue()
                        # if name==inspct or flag: print("\n 1 after gab,ps[0].getValue()",gab,ps[0].getValue(),"\n\n")
                    else:
                        # if name==inspct or flag: print("\nbefore gab,ps[0].getValue()",gab,ps[0].getValue())
                        arrows.append([posQR[2],ps[0].getValue()-gab])
                        avoid_col(posQR,remember_flag)
                        gab=ps[0].getValue()
                        # if name==inspct or flag: print("\nafter gab,ps[0].getValue()",gab,ps[0].getValue(),"\n\n")

                else:
                    avoid_col(posQR,remember_flag)

            if cam_count>=CAMERA_SMP:
                OUT=checkQR()
                trans=OUT[0]
                ROT=OUT[1]
                QR=OUT[2]
                cam_count=0
            else: 
                cam_count+=1
                QR,ROT,trans="Q0",None,None
            if not(ROT is None) and real:
                ROT[2]+=180
                while ROT[2]>360 : ROT[2]-=360
                while ROT[2]<0: ROT[2]+=360

            if  QR != 'Q0':
                count_L+=1
                if count_L==1:
                    if name==inspct or flag: print("function out\n",QR,ROT,"\nreal rot\n",cord(),"\nerror\n",cord()-ROT[-1])
                    last_QR=QR
                    count2+=1
                    # print(name,last_QR)
                    if count2==1: QR_oc_mat[int(last_QR[1])-1]+=1
                    remember_flag=True
                    posQR=ROT
                    if name==inspct or flag: print("In QR",QR,ROT)
                    sudovec=calc_sudovec(last_QR,"add_arrow",ROT,trans)
                    arrows=[[0,0]]
                    gab=ps[0].getValue()
                    if vec_qr_mem[int(last_QR[1])-1,0]!=0 and vec_qr_mem[int(last_QR[1])-1,1]!=0:
                        if name==inspct or flag:
                            print("I remember",last_QR,"vec is",vec_qr_mem[int(last_QR[1])-1],"\nvec_qr_mem\n",vec_qr_mem)
                        go_vec(vec_qr_mem[int(last_QR[1])-1],posQR,last_QR,trans)
                        epuckfunc.STATE=str(vec_qr_mem[int(last_QR[1])-1])+"<>"+str(calc_sudovec(last_QR,"go_vec"))+"><"+last_QR

                        #DYNAMIC PART
                        while  robot.step(timestep) != -1:
                            logger_main()
                            if detect_col():
                                if w_r_recog()=="wall":
                                    epuckfunc.STATE='-'
                                    error[int(last_QR[1])-1]+=1
                                    avoid_col(posQR,remember_flag)
                                    break
                                else:
                                    epuckfunc.STATE='+'
                                    if check_ground():
                                        wait(posQR,remember_flag)
                                    else:
                                        avoid_col(posQR,remember_flag)
                                    break
                            # if check_ground():
                                # if name == inspct : print ("success")
                                # break
                        if name==inspct or flag: print("error",error)
                        for i in range(0,QRnum):
                            if error[i]>=TOLERANCE:
                                error[i]=0
                                vec_qr_mem[int(last_QR[1])-1]=[0,0]


            else : 
                count2=0
                count_L=0


######################################################################################################################################
    else:
        if check_ground():
            wait(posQR,remember_flag)



        else :
            avoid_col(posQR,remember_flag,True)
