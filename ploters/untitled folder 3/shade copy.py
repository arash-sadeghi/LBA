from DataFillerNA20000_shade import *
from matplotlib.patches import PathPatch
import statistics as st
from time import time,ctime
POP=20
endtime=20000
SMAPLING_PERIOD=5
numel=int(endtime/SMAPLING_PERIOD)
tav=int(500/500)
boxnum=int(numel/tav)
fig, ax10 = plt.subplots(1, 1,figsize=(18,8)) 
# cases=[0,0.02,0.04,0.08,0.17,0.35,100]
# X=[0,18,36,54,72,90,108,126,144,162,180]
X=[0,15,30,45,60,75,90,105,120,135,150,165,180]

pltt=['royalblue','tomato','green',"pink","purple"]
#....................................................................................................................................
def plotter(pop,indx):
    global rownum,numel,tav,boxnum,pltt,fig,ax,lst,cases,endtime
    rownum=20
    for c,v in enumerate(lst):
        lst[c]=np.delete(lst[c],slice(rownum,None),0)
        # print("---",c)

    lstshape=[len(lst),len(lst[0])]
    lst_av=np.zeros((lstshape[0],lstshape[1],boxnum))
    # print(len(lst[0][0]))
    for c,v in enumerate(lst):
        lst[c]=lst[c]/pop
        for i in range(0,boxnum):
            for j in range(0,rownum):
                try:
                    lst_av[c,j,i]=sum(lst[c][j][i*tav:(i+1)*tav])/len(lst[c][j][i*tav:(i+1)*tav])
                except Exception as E:
                    print(E,"<> error",c,i,j)
                    exit()

    lst_av_sh=np.shape(lst_av)
    med=np.zeros((lst_av_sh[0],lst_av_sh[2]))
    q1=np.zeros((lst_av_sh[0],lst_av_sh[2]))
    q3=np.zeros((lst_av_sh[0],lst_av_sh[2]))

    for i in range(lst_av_sh[0]):
        for k in range(lst_av_sh[2]):
            med[i,k]=np.mean(lst_av[i,:,k]) #np.percentile(lst_av[i,:,k],50)
            q1[i,k]=np.percentile(lst_av[i,:,k],25)
            q3[i,k]=np.percentile(lst_av[i,:,k],75)
    dlen=len(med[0])
    x=list(range(dlen))
    Y=[];Y1=[];Y3=[]
    for i in range(lst_av_sh[0]):
        M=np.mean(med[i,-1000:])
        Q1=np.mean(q1[i,-1000:])
        Q3=np.mean(q3[i,-1000:])
        Y.append(M)
        Y1.append(Q1)
        Y3.append(Q3)
    linestyle='-'
    Etol=r'LBA $\tau_{e}$ = 4'
    marker='s'

    if indx==0:
        Y=Y*len(X)
        Y1=Y1*len(X)
        Y3=Y3*len(X)
        Etol='BEECLUST'
        linestyle='--'
        marker='NO'
    if indx==2:
        Y=Y*len(X)
        Y1=Y1*len(X)
        Y3=Y3*len(X)
        Etol='LBA with 0 $S_{total}$'
        linestyle='-.'
    if marker=='NO':
        plt.plot(X,Y,label=Etol,color=pltt[indx],linewidth=3,linestyle=linestyle)
    else :
        plt.plot(X,Y,label=Etol,color=pltt[indx],linewidth=3,linestyle=linestyle,marker=marker,markersize=12)

    plt.fill_between(X,Y,Y1,color=pltt[indx],alpha=0.2,linestyle=linestyle)
    plt.fill_between(X,Y3,Y,color=pltt[indx],alpha=0.2,linestyle=linestyle)


    plt.xticks(X,fontweight='bold',fontsize=25)
    plt.yticks(fontweight='bold',fontsize=25)
    plt.ylim(0,1)
    plt.xlim(0,X[-1])
###########################################################################################################################
ax=ax10


FolderName="0 BEECLUST"
lst,rownum=ten(FolderName,numel)
plotter(POP,0)

# FolderName="BEECLUST_"
# lst,rownum=ten(FolderName,numel)
# plotter(POP,2)

FolderName="0"
lst,rownum=ten(FolderName,numel)
plotter(POP,1)

# plt.subplots_adjust(top=0.97,bottom=0.15,left=0.1,right=0.96)
plt.subplots_adjust(bottom=0.17,left=0.1,right=0.96)


# FolderName="Etol 6"
# lst,rownum=ten(FolderName,numel)
# plotter(POP,1)

# # FolderName="Etol 10"
# # lst,rownum=ten(FolderName,numel)
# # plotter(POP,2)

# FolderName="Etol 14"
# lst,rownum=ten(FolderName,numel)
# plotter(POP,3)

# # FolderName="Etol inf"
# # lst,rownum=ten(FolderName,numel)
# # plotter(POP,4)

# 1 Dynamic shade sigma 0_duration 40000s_20 robots_different Etols.png
strng=ctime(time()).replace(':','-')+" Steup 4, Static env, shade, duration "+str(endtime)+"s, "+str(POP)+" robots"
# plt.title(str(POP)+" robots, sigma= "+str(sigma)+", Dynamic env, Duration=40000s",fontweight='bold',fontsize=21)
# plt.title(strng,fontweight='bold',fontsize=21,pad=25)
plt.xlabel("Noise strength ($\mathbf{\sigma}$) [degree]",fontweight='bold',fontsize=30)
plt.ylabel("Normalized aggregation size",fontweight='bold',fontsize=30)
plt.legend(fontsize=30)
print(strng)
os.chdir("..")
plt.savefig("/home/arash/Desktop/performance vs noise.pdf")
plt.show()
