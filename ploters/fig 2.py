from DataFillerNA20000_shade import *
from matplotlib.patches import PathPatch
import statistics as st
from time import time,ctime
POP=20
endtime=80000
SMAPLING_PERIOD=5
numel=endtime//SMAPLING_PERIOD
tav=int(500/500)
boxnum=int(numel/tav)
fig, ax10 = plt.subplots(1, 3,figsize=(18,8)) 
# fig, ax10 = plt.subplots(1, 1,figsize=(18,8)) 


# X=[2,4,6,8,10,12,14]
X=[2,4,6,8,10,12]

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
    Times=[4,2.6,1]
    ii=0
    tlt=['t = 20000 s','t = 40000 s','t = 80000 s']
    for v in Times:
        Y=[];Y1=[];Y3=[]
        Time=int(numel//v-1)
        for i in range(lst_av_sh[0]):
            M=np.mean(med[i,Time-1000:Time])
            Q1=np.mean(q1[i,Time-1000:Time])
            Q3=np.mean(q3[i,Time-1000:Time])
            Y.append(M)
            Y1.append(Q1)
            Y3.append(Q3)
        linestyle='-'
        Etol='LBA $E_{tol}$ = 4'
        if indx==0:
            Y=Y*len(X)
            Y1=Y1*len(X)
            Y3=Y3*len(X)
            Etol='BEECLUST'
            linestyle='--'

        if indx==2:
            Y=Y*len(X)
            Y1=Y1*len(X)
            Y3=Y3*len(X)
            Etol='LBA with 0 $S_{total}$'
            linestyle='-.'

        ax[ii].plot(X,Y,label=Etol,color=pltt[indx],linewidth=3,linestyle=linestyle)
        ax[ii].fill_between(X,Y,Y1,color=pltt[indx],alpha=0.2,linestyle=linestyle)
        ax[ii].fill_between(X,Y3,Y,color=pltt[indx],alpha=0.2,linestyle=linestyle)
        ax[ii].set_title(tlt[ii],fontsize=25,fontweight='bold')
        ax[ii].set_xlim(X[0],X[-1])
        ax[ii].set_ylim(0,1)
        plt.xticks(X,fontweight='bold',fontsize=25)
        plt.yticks(fontweight='bold',fontsize=25)
        # ax[ii].xlabel("$E_{tol}$",fontweight='bold',fontsize=30)


        ii+=1
    # data=np.transpose(lst_av[:,:,numel//1-1],)
    # ax[0].boxplot(data,showfliers=False,whis=100,patch_artist=True)


    # plt.xticks(X,fontweight='bold',fontsize=25)
    # plt.yticks(fontweight='bold',fontsize=25)
    # plt.xlabel("$E_{tol}$",fontweight='bold',fontsize=30)

    # for i in range(3):
    #     ax[i].set_yticks(fontweight='bold',fontsize=25)
    #     ax[i].set_ylim(0,1)
    #     ax[i].set_xticks([1,2,3,4,5,6,7],[2,4,6,8,10,12,14],fontweight='bold',fontsize=25)


###########################################################################################################################
ax=ax10


FolderName="2"
lst,rownum=ten(FolderName,numel)
plotter(POP,1)

# plt.subplots_adjust(top=0.97,bottom=0.15,left=0.1,right=0.96)
# plt.title("t=20000s")
plt.subplots_adjust(bottom=0.15,left=0.1,right=0.96)


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
# plt.title(strng,fontweight='bold',fontsize=21,pad=25)
# plt.title("",fontweight='bold',fontsize=21,pad=25)

# ax[0].xlabel("$E_{tol}$",fontweight='bold',fontsize=30)
# ax[1].xlabel("$E_{tol}$",fontweight='bold',fontsize=30)
# ax[2].xlabel("$E_{tol}$",fontweight='bold',fontsize=30)
# plt.xlabel("$E_{tol}$",fontweight='bold',fontsize=30)

# setp(ax[0].get_xticklabels(), visible=False)
plt.setp(ax[1].get_yticklabels(), visible=False)
plt.setp(ax[2].get_yticklabels(), visible=False)
ax[0].set_yticklabels([str(round(_,1)) for _ in np.arange(0,1.2,0.2)],fontsize=20,fontweight='bold')
ax[0].set_ylabel("Normalized aggregation size",fontweight='bold',fontsize=30)

# ax[0].set_xticklabels([str(int(_)) for _ in np.arange(2,14,2)],fontsize=25,fontweight='bold')
# ax[1].set_xticklabels([str(int(_)) for _ in np.arange(2,14,2)],fontsize=25,fontweight='bold')
ax[0].set_xticklabels(X,fontsize=25,fontweight='bold')
ax[1].set_xticklabels(X,fontsize=25,fontweight='bold')

fig.text(0.5, 0.01, '$\mathbf{E_{tol}}$', ha='center',fontsize=30,fontweight='bold')

# ax[0].ylabel("Normalized aggregation size",fontweight='bold',fontsize=30)
# plt.legend(fontsize=30)
print(strng)
os.chdir("..")
plt.savefig("/home/arash/Desktop/performance_vs_Etol"+ctime(time()).replace(':','_')+".pdf")
plt.show()
