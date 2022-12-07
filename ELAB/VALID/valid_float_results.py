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

    return parser.parse_args()


args = argument()


import numpy as np
import glob
import os
import datetime
import netCDF4 as NC4
from commons.Timelist import TimeList
from commons.utils import addsep

OUTDIR = addsep(args.outdir)
INDIR = addsep(args.indir)

var = args.varname



LISTresults = [os.path.basename(ll) for ll in glob.glob(INDIR + '/result_*.nc')]
Nresults = len(LISTresults)


infile1 = LISTresults[0]
NC = NC4.Dataset(INDIR + infile1,'r')
# depth = NC.variables['z'][:,:,0,0].data
# nZ = depth.shape[1]
time = NC.variables['time'][:].data
# nT = time.shape[0]
# # var_mean = np.zeros((nZ1,nT1))
# # var_mean_2 = np.zeros((nZ1,nT1))
refstr = NC.variables['time'].units.split()[2]
ref = datetime.datetime.strptime(refstr,'%Y-%m-%d')
NC.close()

date_list = []
date_list.append(ref)
for myt in time:
    step = datetime.timedelta(seconds=myt)
    date_list.append(ref + step)
TLmod = TimeList(date_list)
TImod = TLmod.timeinterval


# RSTfile = INDIR + '/OUTNC/DAout.nc'

# NC = NC4.Dataset(RSTfile,'r')
# timeDA = NC.variables['time'][:].data
# varvaluesBEF = NC.variables[var][:,0,:,:,0,0].data
# zmodel = NC.variables['z'][:,0,0,:,0,0].data #depth does not change among ensemble members
# varvaluesAFT = NC.variables[var][:,:,:,:,0,0].data
# nT_DA = time.shape[0]
# # varvalues = NC.variables[var][:,:,:,:,0,0].data
# refstrDA = NC.variables['time'].units.split()[2]
# refhourDA = NC.variables['time'].units.split()[3]
# NC.close()

# refDA = datetime.datetime.strptime(refstrDA + '-' + refhourDA,'%Y-%m-%d-%H:%M:%S')
# ListTimeDA = TimeList([refDA+datetime.timedelta(seconds=ll) for ll in timeDA])
# TI_DA = ListTimeDA.timeinterval



obsfile = INDIR + '/ValidObs/profile_' + var + '.obs'
fid = open(obsfile)
LINEobs =  fid.readlines()
fid.close()

TimeObs = []
for ll in LINEobs:
    ddstr,hhstr,zz,obs,err = ll.rsplit()
    TimeObs.append(datetime.datetime.strptime(ddstr + '-' + hhstr,'%Y-%m-%d-%H:%M:%S'))
TimeObs = list(set(TimeObs))
ListTimeObs = TimeList(TimeObs)


TLmod_obs = []
for dd in ListTimeObs.Timelist:
    if (not(TImod.contains(dd))) & (not(TImod.contains(dd-datetime.timedelta(seconds=1)))):
        continue
    TLmod_obs.append(dd)

Ndates = len(TLmod_obs)

dlim = [0,-50,-100,-200,-400]


MATbias = np.zeros((Ndates,len(dlim)))
MAT_RMSD = np.zeros((Ndates,len(dlim)))
# MAT_RMSDall = np.zeros(len(dateobs))
for idate,dd in enumerate(TLmod_obs):
    print(dd)
    datestr = datetime.datetime.strftime(dd,'%Y-%m-%d')
    zobs = []
    profobs = []
    for ll in LINEobs:
        ddstr,_,zz,obs,err = ll.rsplit()
        if ddstr in datestr:
            zobs.append(float(zz))
            profobs.append(float(obs))
    nZobs = len(zobs)

    jj = TLmod.find(dd)
    profmod = np.zeros((nZobs))
    for file_res in LISTresults:
        NCin=NC4.Dataset(INDIR + file_res,"r")
        varvalues = np.interp(zobs,NCin.variables['z'][jj,:,0,0],NCin.variables[var][jj,:,0,0].data)
        profmod = profmod + varvalues/Nresults
        # varmean2 = varmean2 + varvalues**2/Nresults
        NCin.close()
    bias = np.zeros(len(dlim))
    RMSD = np.zeros(len(dlim))
    for iiy,yy in enumerate(dlim[1:]):
        maskz = (np.array(zobs)<dlim[iiy]) & (np.array(zobs)>dlim[iiy+1])
        bias[iiy] = np.nanmean((profmod-profobs)[maskz])
        RMSD[iiy] = (np.nanmean( ((profmod-profobs)[maskz])**2 ))**.5
    maskz = np.array(zobs)<dlim[-1]
    bias[-1] = np.nanmean((profmod-profobs)[maskz])
    RMSD[-1] = (np.nanmean( ((profmod-profobs)[maskz])**2 ))**.5
    
    MATbias[idate,:] = bias
    MAT_RMSD[idate,:] = RMSD


import sys
sys.exit(0)

print(np.nanmean(MAT_RMSD,axis=0))


np.save(OUTDIR + '/bias_levs_' + var + '.npy',MATbias)
np.save(OUTDIR + '/RMSD_levs_' + var + '.npy',MAT_RMSD)

np.save(OUTDIR + '/dateobs_' + var + '.npy',dateobs)







