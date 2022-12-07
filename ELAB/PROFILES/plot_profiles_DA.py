import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Produce Hovmoeller plot of a variable or
    an aggregate variable
    from results of FABM-GOTM 1D
    (adding a line of a constant variable)
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--varname', '-v',
                                type = str,
                                required = False,
                                help = 'Variable to be plotted in the Hovmoeller')

    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                required = True,
                                default = '',
                                help = 'Output Images directory')
    
    parser.add_argument(   '--indir', '-i',
                                type = str,
                                required = True,
                                help = 'indir with result.nc from ensemble')

    parser.add_argument(   '--depth', '-d',
                                type = str,
                                required = False,
                                default = '300',
                                help = 'depth limit')

    return parser.parse_args()


args = argument()



# import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
import datetime
#import glob
#import os
#from matplotlib.colors import LogNorm
#from datetime import timedelta
from commons.utils import addsep
#from commons.Timelist import TimeList


#ref = datetime.datetime(2016, 1, 1, 0, 0, 0)

OUTDIR = addsep(args.outdir)
INDIR = addsep(args.indir)

var = args.varname

deplim = float(args.depth)



RSTfile = INDIR + '/OUTNC/DAout.nc'

NC = NC4.Dataset(RSTfile,'r')

depth = NC.variables['z'][:,0,0,:,0,0].data
nZ = depth.shape[1]
time = NC.variables['time'][:].data
nT = time.shape[0]
varvalues = NC.variables[var][:,:,:,:,0,0].data
if 'rho' in var:
    varvalues = varvalues - 1000
#var_mean = np.zeros((nZ1,nT1))
#var_mean_2 = np.zeros((nZ1,nT1))

refstr = NC.variables['time'].units.split()[2]
refhour = np.float(NC.variables['time'].units.split()[3][:2])
refmin = np.float(NC.variables['time'].units.split()[3][3:5])
refsec = np.float(NC.variables['time'].units.split()[3][6:8])
refstep = datetime.timedelta(hours=refhour,minutes=refmin,seconds=refsec)
ref = datetime.datetime.strptime(refstr,'%Y-%m-%d') + refstep


NC.close()


plotfloat = True
try:
    obsfile = INDIR + '/ValidObs/profile_' + var + '.obs'
    fid = open(obsfile)
    LINEobs =  fid.readlines()
    fid.close()
except:
    print('File obs not found: ' + INDIR + '/ValidObs/profile_' + var + '.obs')
    plotfloat = False

for idate in range(nT):
    step = datetime.timedelta(seconds=time[idate])
    datenow = ref + step
    datestr = datenow.strftime('%Y-%m-%d')
    if plotfloat:
        zobs = []
        profobs = []
        for ll in LINEobs:
            ddstr,_,zz,obs,err = ll.rsplit()
            if ddstr in datestr:
                zobs.append(float(zz))
                profobs.append(float(obs))


#    current_time = datetime.datetime.strptime(time[idate],'%Y-%m-%d')
    print(idate)
    plt.close('all')
    fig,axs = plt.subplots(1,4,sharey=True,figsize=[10,8])
    plt.sca(axs[0])
    plt.plot(varvalues[idate,0,:,:].T,-depth[idate,:],':',color='grey')
    plt.plot(np.mean(varvalues[idate,0,:,:],axis=0),-depth[idate,:],'-',color='blue')
    plt.grid()
    plt.ylim(deplim,0)
    plt.title('Before ' + datestr)

    plt.sca(axs[1])
    plt.plot(varvalues[idate,1,:,:].T,-depth[idate,:],':',color='grey')
    plt.plot(np.mean(varvalues[idate,1,:,:],axis=0),-depth[idate,:],'-',color='green')
    plt.grid()
    plt.ylim(deplim,0)
    plt.title('After ' + datestr)

    plt.sca(axs[2])
    plt.plot(np.mean(varvalues[idate,0,:,:],axis=0),-depth.T,'-',color='blue')
    plt.plot(np.mean(varvalues[idate,1,:,:],axis=0),-depth.T,'-',color='green')
    if plotfloat: plt.plot(np.array(profobs),np.array(zobs)*-1,'-',color='red')
    plt.grid()
    plt.ylim(deplim,0)
    plt.title('Mean and observation')

    plt.sca(axs[3])
    plt.plot(np.std(varvalues[idate,0,:,:],axis=0),-depth[idate,:],'--',color='blue')
    plt.plot(np.std(varvalues[idate,1,:,:],axis=0),-depth[idate,:],'--',color='green')
    plt.grid()
    plt.ylim(deplim,0)
    plt.title('Std ' + datestr)

#    plt.show(block=False)

    plt.savefig(OUTDIR + '/profilesDA.' + datestr + '.' + var + '.png')


