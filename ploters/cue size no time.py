from DataFillerNA20000_shade import *
from matplotlib.patches import PathPatch
import statistics as st
from time import time,ctime
import matplotlib.pylab as ply

ply.rcParams['xtick.major.pad']='18'
POP=20
endtime=20000
SMAPLING_PERIOD=5
numel=endtime//SMAPLING_PERIOD
tav=int(500/500)
boxnum=int(numel/tav)
fig, ax10 = plt.subplots(1, 1,figsize=(18,8)) 
ax10=[ax10]
X=[0.3,0.5,0.7,0.9,1.1,1.5,2,2.5,3,5,10]
pltt=['tomato','royalblue',"pink","purple"]

#....................................................................................................................................
def plotter(pop,indx):
    global rownum,numel,tav,boxnum,pltt,fig,ax,lst,cases,endtime,X
    rownum=20
    for c,v in enumerate(lst):
        lst[c]=np.delete(lst[c],slice(rownum,None),0)
        # print("---",c)

    lstshape=[len(lst),len(lst[0])]
    lst_av=np.zeros((lstshape[0],lstshape[1],boxnum))
    # print(len(lst[0][0]))
    for c,v in enumerate(lst):
        if indx>=2: pop=X[c]
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
    # Times=[4,2.6,1]
    Times=[1]

    ii=0
    # tlt=['t = 20000 s','t = 30000 s','t = 80000 s']
    tlt=['(b)','(c)','(d)']

    for v in Times:
        Y=[];Y1=[];Y3=[]
        Time=int(numel//v-1)
        for i in range(lst_av_sh[0]):
            M=np.mean(med[i,Time-3000:Time])
            Q1=np.mean(q1[i,Time-3000:Time])
            Q3=np.mean(q3[i,Time-3000:Time])
            Y.append(M)
            Y1.append(Q1)
            Y3.append(Q3)
        linestyle='-'
        Etol=r'LBA $\tau_{e}$ = 4'
        if indx==0:
            # Etol='LBA'
            linestyle='-'
            axindx=0
            marker='s'

        if indx==1:
            Etol='BEECLUST'
            linestyle='--'
            axindx=0
            marker='^'
        if indx==2:
            axindx=1
        Y.append(1)
        Y1.append(1)
        Y3.append(1)
        ax[axindx].plot(X,Y,label=Etol,color=pltt[indx],linewidth=3,linestyle=linestyle,marker=marker,markersize=12)
        ax[axindx].fill_between(X,Y,Y1,color=pltt[indx],alpha=0.2,linestyle=linestyle)
        ax[axindx].fill_between(X,Y3,Y,color=pltt[indx],alpha=0.2,linestyle=linestyle)
        # ax.set_title(tlt[ii],fontsize=25,fontweight='bold')
        ax[axindx].set_xlim(0,X[-1])
        ax[axindx].set_ylim(0,1)
        ii+=1
    tks=list(range(len(X)))
    ax[axindx].set_xticks(tks,minor=False)
    # ax[1].set_xticks(X,minor=False)
    # ax[2].set_xticks(X,minor=False)

    ax[axindx].set_xticklabels(tks,fontsize=30,fontweight='bold')
    # ax[1].set_xticklabels([1,2,3,4,6,8,10,12],fontsize=30,fontweight='bold')
    # ax[2].set_xticklabels([1,2,3,4,6,8,10,12],fontsize=30,fontweight='bold')

###########################################################################################################################
ax=ax10

FolderName="Cue size BEECLUST"
lst,rownum=ten(FolderName,numel)
plotter(POP,1)

FolderName="Cue size"
lst,rownum=ten(FolderName,numel)
plotter(POP,0)

plt.subplots_adjust(bottom=0.17,left=0.1,right=0.96)

strng=ctime(time()).replace(':','-')+" Steup 4, Static env, shade, duration "+str(endtime)+"s, "+str(POP)+" robots"
# plt.setp(ax[1].get_yticklabels(), visible=False)
# plt.setp(ax[2].get_yticklabels(), visible=False)
ax[0].set_yticklabels([str(round(_,1)) for _ in np.arange(0,1.2,0.2)],fontsize=30,fontweight='bold')
ax[0].set_ylabel("Normalized aggregation size",fontweight='bold',fontsize=30)

# fig.text(0.5, 0.01, '$\mathbf{E_{tol}}$', ha='center',fontsize=30,fontweight='bold')
# fig.text(0.55, 0.95, 'sigma 0.17', ha='center',fontsize=20,fontweight='bold')

ax[0].set_xlabel('Cue radius [m]',fontsize=30,fontweight='bold')
ax[0].legend(fontsize=30)
os.chdir("..")
# plt.savefig("/home/arash/Desktop/performance_vs_Etol"+ctime(time()).replace(':','_')+".pdf")
plt.savefig("/home/arash/Desktop/cue size.pdf")

plt.show()
