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

var = "total_chlorophyll_calculator_result"



RSTfile = INDIR + '/OUTNC/DAout.nc'

NC = NC4.Dataset(RSTfile,'r')
timeDA = NC.variables['time'][:].data
varvaluesBEF = NC.variables[var][:,0,:,:,0,0].data
zmodel = NC.variables['z'][:,0,0,:,0,0].data #depth does not change among ensemble members
# varvaluesAFT = NC.variables[var][:,:,:,:,0,0].data
# nT_DA = time.shape[0]
# # varvalues = NC.variables[var][:,:,:,:,0,0].data
refstrDA = NC.variables['time'].units.split()[2]
refhourDA = NC.variables['time'].units.split()[3]
NC.close()

refDA = datetime.datetime.strptime(refstrDA + '-' + refhourDA,'%Y-%m-%d-%H:%M:%S')
ListTimeDA = TimeList([refDA+datetime.timedelta(seconds=ll) for ll in timeDA])
TI_DA = ListTimeDA.timeinterval



obsfile = INDIR + '/ValidObs/surf_' + var + '.obs'
fid = open(obsfile)
LINEobs =  fid.readlines()
fid.close()

TimeObs = []
for ll in LINEobs:
    ddstr,hhstr,obs,err = ll.rsplit()
    TimeObs.append(datetime.datetime.strptime(ddstr + '-' + hhstr,'%Y-%m-%d-%H:%M:%S'))
TimeObs = list(set(TimeObs))
ListTimeObs = TimeList(TimeObs)

dlim = [0,-5]


MATbias = np.zeros((12))
MAT_RMSD = np.zeros((12))
# MAT_RMSDall = np.zeros(len(dateobs))
Lobs = {}
Lmod = {}
for im in range(12):
    Lobs[im] = []
    Lmod[im] = []


for idate,dd in enumerate(ListTimeObs.Timelist):
    if (not(TI_DA.contains(dd))) & (not(TI_DA.contains(dd-datetime.timedelta(seconds=1)))):
        continue
    print(dd)
    datestr = datetime.datetime.strftime(dd,'%Y-%m-%d')
    im = dd.month-1
    for ll in LINEobs:
        ddstr,_,obs,err = ll.rsplit()
        if ddstr in datestr:
            obssat = float(obs)
    Lobs[im].append(obssat)

    jj = ListTimeDA.find(dd)
    ensdate = varvaluesBEF[jj,:,:] #[time,Nens,depth]
    ensmean = np.mean(ensdate,axis=0)
    maskz = (np.array(zmodel[jj,:])<dlim[0]) & (np.array(zmodel[jj,:])>dlim[1])
    chlmod = np.mean(ensmean[maskz])
    Lmod[im].append(chlmod)

for im in range(12):
    print(im) 
    diff = np.array(Lmod[im]) - np.array(Lobs[im])
    MATbias[im] = np.nanmean(diff)
    MAT_RMSD[im] = (np.nanmean(diff**2))**.5
    # bias = np.zeros(len(dlim))
    # RMSD = np.zeros(len(dlim))
    # bias[iiy] = np.nanmean((profmod-profobs)[maskz])
    # RMSD[iiy] = (np.nanmean( ((profmod-profobs)[maskz])**2 ))**.5
    # maskz = np.array(zobs)<dlim[-1]
    # bias[-1] = np.nanmean((profmod-profobs)[maskz])
    # RMSD[-1] = (np.nanmean( ((profmod-profobs)[maskz])**2 ))**.5

    # MATbias[idate,:] = bias
    # MAT_RMSD[idate,:] = RMSD
    # varmean = np.zeros((nZobs))
    # varmean2 = np.zeros((nZobs))
    # for file_res in LISTresults:
    #     NCin=NC4.Dataset(INDIR + file_res,"r")
    #     varvalues = np.interp(zobs,NCin.variables['z'][jj,:,0,0],NCin.variables[var][jj,:,0,0].data)
    #     varmean = varmean + varvalues/Nresults
    #     varmean2 = varmean2 + varvalues**2/Nresults
    
    # bias = np.zeros(len(dlim))
    # RMSD = np.zeros(len(dlim))
    #     # bias[iiy] = np.nanmean((varmean-profobs)[maskz])
    #     # RMSD[iiy] = (np.nanmean(((varmean-profobs)[maskz])**2)**.5)**.5
    # maskz = np.array(zobs)<dlim[-1]
    # bias[-1] = np.nanmean((varmean-profobs)[maskz])
    # RMSD[-1] = (np.nanmean(((varmean-profobs)[maskz])**2)**.5)**.5
    # print(bias)

import sys
sys.exit(0)


print(np.nanmean(MAT_RMSD,axis=0))


np.save(OUTDIR + '/bias_levs_' + var + '.npy',MATbias)
np.save(OUTDIR + '/RMSD_levs_' + var + '.npy',MAT_RMSD)

np.save(OUTDIR + '/dateobs_' + var + '.npy',dateobs)







