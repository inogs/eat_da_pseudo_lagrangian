import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import datetime
from datetime import timedelta
import glob
from scipy.stats import variation
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import mpi4py

try:
    from mpi4py import MPI
    comm  = MPI.COMM_WORLD
    rank  = comm.Get_rank()
    nranks =comm.size
    isParallel = True
except:
    rank   = args.rank
    nranks = args.nranks
    isParallel = False

#date format for the plots
date_form = DateFormatter("%y-%m")
#rotation angle of xlables
angle = int(30)


def get_data_at_depth(indata,depth,delta):
    depths=indata['depthLIST']
    out_date=[]
    out_data=[]
    out0_err =[]
    out1_err =[]
    for i,d in enumerate(depths):
        if (d> (depth-delta)) and (d< (depth+delta)):
            out_date.append(indata['dateobjLIST'][i])
            out_data.append(indata['obsLIST'][i])
            out0_err.append(indata['err0LIST'][i])
            out1_err.append(indata['err1LIST'][i])
    return  out_date,out_data, out0_err, out1_err


#/g100_scratch/userexternal/plazzari/WP6_TEST/6901772_instances_P1_parameters_p_alpha_chl_assimilation_F3
a=np.loadtxt("../assimilation_F3_folder_list.txt",dtype=np.dtype('U'))

for test_dir in a[rank::nranks]:
    floatname = test_dir.split('/')[5][:7]
    prmtr_nm  = test_dir.split('/')[5][8:][:-16]
#filenames = glob.glob('/g100_scratch/userexternal/gocchipi/stoc_prova/*/result.nc')
    filenames = glob.glob( test_dir + '/result_*.nc')
    filenames.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) #sort by number
    
    obs_sat_file=test_dir + "/ToAssimilate/nrt_chlsat.obs.npz"
    data_sat = np.load(obs_sat_file,allow_pickle=True)
    
    obs_argo_file=test_dir + "/ToAssimilate/profile_CHLA.obs.npz"
    data_argo = np.load(obs_argo_file,allow_pickle=True)
    
    ref = datetime.datetime(2019, 1, 1, 0, 0, 0)
    for inc,ncname in enumerate(filenames):
        infile=ncname 
        print(infile)
        NCin=NC4.Dataset(infile,"r")
        if inc == 0:
            nTframes=len(NCin.variables['time'][:])
            time=NCin.variables['time'][:].filled()
        nTframes=min(nTframes,len(NCin.variables['time'][:]))
        depth=NCin.variables['z'][:,:,0,0].filled()
        NCin.close()
    print(nTframes)
    CHL_arr = np.zeros((len(filenames),nTframes,len(depth[0])))

    for inc,ncname in enumerate(filenames):
        infile=ncname 
        NCin=NC4.Dataset(infile,"r")
        CHL_arr[inc,0:nTframes,:]=NCin.variables['P1_Chl'][0:nTframes,:,0,0].filled()+NCin.variables['P2_Chl'][0:nTframes,:,0,0].filled()+NCin.variables['P3_Chl'][0:nTframes,:,0,0].filled()+NCin.variables['P4_Chl'][0:nTframes,:,0,0].filled()
        NCin.close()
    
    CHL_mean = np.mean(CHL_arr, axis=0)
    CHL_std  = np.std(CHL_arr, axis=0)
    CHL_cv   = variation(CHL_arr, axis=0)
    
    date_list = []
    
    for myt in time[0:nTframes]:
        step = datetime.timedelta(seconds=int(myt))
        date_list.append(ref + step)
    
    nT=len(date_list)
    nZ=depth.shape[1]
    
    fig,axs = plt.subplots(1,figsize=(9, 6),gridspec_kw = {'wspace':1.5, 'hspace':1.5})
    x = np.arange(nT)
    
    #select depths
    sdepth = [  0,-10,-50,-100]
    id_dep = np.zeros(len(sdepth),dtype=int)
    for i,d in enumerate(depth[0]):
        for j,select in enumerate(sdepth):
            if d > select-2. and d < select+2.:
                id_dep[j] = i
    
    tick_labels=[]
    tpos=range(0,nT,30)
    for i in tpos:
       tick_labels.append(date_list[i].strftime("%Y %m"))
    
    fig,axs = plt.subplots(2,2,figsize=(9, 6),gridspec_kw = {'wspace':0.5, 'hspace':0.35}, sharex=True, sharey=True)
    axs = axs.ravel()
    for iax,ax in enumerate(axs):
        if iax == 0:
    #dateobjLIST=dateobjLIST, obsLIST=obsLIST,errLIST=errLIST
            ln_sat=ax.plot(data_sat['dateobjLIST'],data_sat['obsLIST'],label='CHL_sat',c='red')
        lns1 = ax.plot(date_list,CHL_mean[:,id_dep[iax]],label='CHL_model',c='black')
        ax.plot(date_list,CHL_arr[:,:,id_dep[iax]].T,alpha=0.1)
        axT=ax.twinx()
        lns_std=axT.plot(date_list,CHL_std[:,id_dep[iax]],c='magenta',alpha=0.5, label='CHL_mod_std')
        argo_date, argo_obs, argo_err0, argo_err1 = get_data_at_depth(data_argo,sdepth[iax],5)
        ln_argo = ax.plot(argo_date,argo_obs,label='CHL_argo',c='green')
#       ax.set_xticks(tpos)
#       ax.set_xticklabels(tick_labels,rotation=90)
        ax.set_xticklabels(ax.get_xticks(), rotation = angle)
        ax.set_xlabel('Time')
        axT.set_ylabel(r'chl [$mgchlm^{-3}$]')
        ax.set_ylim([0.01, 1.0])
        ax.set_xlim([datetime.date(2019, 1, 1), datetime.date(2020, 1, 1)])
        ax.set_yscale('log')
        axT.set_yscale('log')
        axT.set_ylabel(r'$\sigma_{CHL-a}$ [$mg$ $m^{-3}$]')
        title = 'depth ' + str(sdepth[iax]) + ' m'
        ax.set_title(title,fontsize=9)
        ax.xaxis.set_major_formatter(date_form) #set the date format
    
    lns = lns1+lns_std+ln_sat+ln_argo
    labels = [l.get_label() for l in lns]
    fig.legend(lns,labels,ncol=4, loc='upper center')
    fig.text(0.04, 0.5, 'CHL-a Concentration [$mg$ $m^{-3}$]', va='center', rotation='vertical')
    floatname = test_dir.split('/')[5][:7]
    prmtr_nm  = test_dir.split('/')[5][8:][:-16]
    fileout='chl_' + floatname  + '_' + prmtr_nm  + '.png'
    fig.savefig(fileout, format='png',dpi=150, bbox_inches="tight")
    plt.close(fig)
