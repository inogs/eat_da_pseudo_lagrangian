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




LISTresults = [os.path.basename(ll) for ll in glob.glob(INDIR + '/result_*.nc')]
Nresults = len(LISTresults)


infile1 = LISTresults[0]
NC = NC4.Dataset(INDIR + infile1,'r')
depth = NC.variables['z'][:,:,0,0].data
nZ = depth.shape[1]
time = NC.variables['time'][:].data
nT = time.shape[0]
refstr = NC.variables['time'].units.split()[2]
ref = datetime.datetime.strptime(refstr,'%Y-%m-%d')
NC.close()

date_list = []
for myt in time:
    step = datetime.timedelta(seconds=myt)
    date_list.append(ref + step)

deltaz = 5
zinterp = np.arange(-200,1,deltaz)
nzinterp = len(zinterp)
maskz = zinterp>=-200

varMat = np.zeros((nT,Nresults))

for iir,file_res in enumerate(LISTresults):
    print(iir)
    NCin=NC4.Dataset(INDIR + file_res,"r")
    values = np.zeros((nT,nZ))
    for pp in range(4):
        ppstr = 'Z' + np.str(pp+3) + '_c'
        values = values + NCin.variables[ppstr][:,:,0,0].data
    for jj in range(nT):
        valinterp = np.interp(zinterp,NCin.variables['z'][jj,:,0,0].data,values[jj,:])
        Z_c = np.nansum(valinterp[maskz]*deltaz)
        varMat[jj,iir] = Z_c  #gC/m2/y

    NCin.close()


Z_cmean = varMat.mean(axis=1)
Z_cstd = varMat.std(axis=1)

LIST = []
LIST.append(Z_cmean)
LIST.append(Z_cstd)

outfile = OUTDIR + '/Z_c200.npy'
np.save(outfile,LIST)

outfile = OUTDIR + '/Z_c200.txt'
np.savetxt(outfile,LIST)








