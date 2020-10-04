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

# X=[2,4,6,8,10,12,14]
# X=[2,4,6,8,10,12]
# X=[1,2,3,4,5,6,7,8]
X=[1,2,3,4,6,8,10,12]
os.chdir("FIG 2 sigma")
pltt=['royalblue','tomato','green',"pink","purple"]
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
    # tlt=['t = 20000 s','t = 30000 s','t = 80000 s']
    tlt=['(b)','(c)','(d)']
    if indx ==1: Times=[4,2.6,1]
    else: Times=[1]
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
        Etol='LBA $\sigma$ = 30 $\degrees$'
        if indx==0:
        #     Y=Y*len(X)
        #     Y1=Y1*len(X)
        #     Y3=Y3*len(X)
            Etol='BEECLUST'
            linestyle='--'

        if indx==2:
            # Y=Y*len(X)
            # Y1=Y1*len(X)
            # Y3=Y3*len(X)
            Etol='LBA with 0 $S_{total}$'
            linestyle='-.'

        ax[ii].plot(X,Y,label=Etol,color=pltt[indx],linewidth=3,linestyle=linestyle,marker='s',markersize=12)
        ax[ii].fill_between(X,Y,Y1,color=pltt[indx],alpha=0.2,linestyle=linestyle)
        ax[ii].fill_between(X,Y3,Y,color=pltt[indx],alpha=0.2,linestyle=linestyle)
        ax[ii].set_title(tlt[ii],fontsize=25,fontweight='bold')
        ax[ii].set_xlim(X[0],X[-1])
        ax[ii].set_ylim(0,1)
        plt.yticks(fontweight='bold',fontsize=25)
        ii+=1
    X=[1,2,4,6,8,10,12]
    ax[0].set_xticks(X,minor=False)
    ax[1].set_xticks(X,minor=False)
    ax[2].set_xticks(X,minor=False)

    # ax[0].set_xticks([1,2,3,4,5,6,7,8],minor=False)
    # ax[0].set_xticks([1,3,5,7,9,11,13,15],minor=False)
    # ax[0].set_xticks([0,2,4,6,8,10,12,14],minor=False)

    # ax[1].set_xticks([1,2,3,4,5,6,7,8],minor=False)
    # ax[2].set_xticks([1,2,3,4,5,6,7,8],minor=False)

    ax[0].set_xticklabels(X,fontsize=30,fontweight='bold')
    ax[1].set_xticklabels(X,fontsize=30,fontweight='bold')
    ax[2].set_xticklabels(X,fontsize=30,fontweight='bold')
    X=[1,2,3,4,6,8,10,12]

###########################################################################################################################
ax=ax10


# FolderName="0"
# lst,rownum=ten(FolderName,numel)
# plotter(POP,1)

FolderName="30"
lst,rownum=ten(FolderName,numel)
plotter(POP,1)


endtime=20000
numel=endtime//SMAPLING_PERIOD
boxnum=int(numel/tav)
FolderName="60"
lst,rownum=ten(FolderName,numel)
plotter(POP,0)

endtime=20000
numel=endtime//SMAPLING_PERIOD
boxnum=int(numel/tav)
FolderName="0"
lst,rownum=ten(FolderName,numel)
plotter(POP,2)

plt.subplots_adjust(bottom=0.17,left=0.1,right=0.96)
strng=ctime(time()).replace(':','-')+" Steup 4, Static env, shade, duration "+str(endtime)+"s, "+str(POP)+" robots"
plt.setp(ax[1].get_yticklabels(), visible=False)
plt.setp(ax[2].get_yticklabels(), visible=False)
ax[0].set_yticklabels([str(round(_,1)) for _ in np.arange(0,1.2,0.2)],fontsize=25,fontweight='bold')
ax[0].set_ylabel("Normalized aggregation size",fontweight='bold',fontsize=30)
ax[0].legend()
# fig.text(0.5, 0.01, '$\mathbf{E_{tol}}$', ha='center',fontsize=30,fontweight='bold')
# fig.text(0.55, 0.95, 'sigma 0.17', ha='center',fontsize=20,fontweight='bold')

# ax[0].set_xlabel('$\mathbf{\tau_{e}}$',fontsize=30,fontweight='bold')
ax[0].set_xlabel(r'$\mathbf{\tau_{e}}$',fontsize=30,fontweight='bold')

ax[1].set_xlabel(r'$\mathbf{\tau_{e}}$',fontsize=30,fontweight='bold')
ax[2].set_xlabel(r'$\mathbf{\tau_{e}}$',fontsize=30,fontweight='bold')

os.chdir("..")
# plt.savefig("/home/arash/Desktop/performance_vs_Etol"+ctime(time()).replace(':','_')+".pdf")
plt.savefig("/home/arash/Desktop/fig2_1 sigma 0.08 no title.pdf")

plt.show()
