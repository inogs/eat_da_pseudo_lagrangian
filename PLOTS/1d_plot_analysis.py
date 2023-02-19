import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import datetime
from datetime import timedelta
import glob
from scipy.stats import variation

#/g100_scratch/userexternal/plazzari/WP6_TEST/6901772_instances_P1_parameters_p_alpha_chl_assimilation_F3
a=np.loadtxt("../assimilation_F3_folder_list.txt",dtype=np.dtype('U'))
for test_dir in a:     
    filename  = test_dir + '/analysis.nc'
    floatname = test_dir.split('/')[5][:7]
    prmtr_nm  = test_dir.split('/')[5][8:][:-16]
    
    ref = datetime.datetime(2019, 1, 1, 0, 0, 0)
      
    NCin=NC4.Dataset(filename,"r")
    #    (time, da_step, member, lat, lon)   
    PARAM=NCin.variables[prmtr_nm][:,1,:,0,0].filled()
    time=NCin.variables['time'][:].filled()
    
    date_list = []
    
    for myt in time:
        step = datetime.timedelta(seconds=int(myt))
        date_list.append(ref + step)
    
    nT=len(date_list)
    nM=np.shape(PARAM)[1]
    
    x = np.arange(nT)
    
    tick_labels=[]
    tpos=range(0,nT,4)
    for i in tpos:
       tick_labels.append(date_list[i].strftime("%m"))
    
    fig,axs = plt.subplots(2,2,figsize=(9, 6),gridspec_kw = {'wspace':0.5, 'hspace':0.35})
    #ig,axs = plt.subplots(2,2,figsize=(9, 6),gridspec_kw = {'wspace':0.5, 'hspace':0.35}, sharex=True, sharey=True)
    ax=axs[0,0]
    lns1 = ax.plot(x,PARAM,label='parameters')
    ax.set_xticks(tpos)
    ax.set_xticklabels(tick_labels,rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel(r'$param $')
    ax=axs[0,1]
    lns2 = ax.errorbar(x,np.mean(PARAM,axis=1),yerr=np.std(PARAM,axis=1),c='k',label='parameters')
    ax.set_xticks(tpos)
    ax.set_xticklabels(tick_labels,rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel(r'$<param> \pm \sigma $')
    ax=axs[1,0]
    lns3 = ax.plot(x,np.std(PARAM,axis=1),c='k',label='parameters')
    ax.set_xticks(tpos)
    ax.set_xticklabels(tick_labels,rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel(r'$\sigma $')
    ax=axs[1,1]
    lns3 = ax.plot(x,np.std(PARAM,axis=1)/np.mean(PARAM,axis=1),c='k',label='parameters')
    ax.set_xticks(tpos)
    ax.set_xticklabels(tick_labels,rotation=45)
    ax.set_xlabel('Time')
    ax.set_ylabel(r'$CV  [-]$')
    #title = 'depth ' + str(sdepth[iax]) + ' m'
    #ax.set_title(title,fontsize=9)
    #fig.text(0.04, 0.5, 'CHL-a Concentration [$mg/m^3$]', va='center', rotation='vertical')
    plt.suptitle(floatname + '_' + prmtr_nm)
    fileout= floatname + '_' + prmtr_nm + '.png'
    fig.savefig(fileout, format='png',dpi=150, bbox_inches="tight")
    
