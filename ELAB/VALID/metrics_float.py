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


# LISTvar = ['N3_n']
# LISTvar = ['total_chlorophyll_calculator_result']
LISTvar = ['total_chlorophyll_calculator_result','N3_n']

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
TLmod = TimeList(date_list)


for var in LISTvar:

    obsfile = INDIR + '/ValidObs/profile_' + var + '.obs'
    fid = open(obsfile)
    LINEobs =  fid.readlines()
    fid.close()

    alldateobs = []
    for ll in LINEobs:
        ddstr,_,zz,obs,err = ll.rsplit()
        alldateobs.append(ddstr)
    dateobs = list(set(alldateobs))
    dateobs.sort()


    metric = np.zeros((len(dateobs),2))
    metric[:,:] = np.nan
    dates_to_save = []
    for idate,datestr in enumerate(dateobs):
        datenow = datetime.datetime.strptime(datestr,'%Y-%m-%d')
        dates_to_save.append(datenow)
        if (datenow>=datetime.datetime(2019, 7, 1, 0, 0)) & (datenow<=datetime.datetime(2019, 9,30, 0, 0)):
            print(datestr)
            zobs = []
            profobs = []
            for ll in LINEobs:
                ddstr,_,zz,obs,err = ll.rsplit()
                if ddstr in datestr:
                    zobs.append(float(zz))
                    profobs.append(float(obs))
            nZobs = len(zobs)

            jj = TLmod.find(datenow)
            varmean = np.zeros((nZobs))
            for file_res in LISTresults:
                NCin=NC4.Dataset(INDIR + file_res,"r")
                varvalues = np.interp(zobs,NCin.variables['z'][jj,:,0,0],NCin.variables[var][jj,:,0,0].data)
                varmean = varmean + varvalues/Nresults
 
            if 'chlorophyll' in var:
                jkm = np.argmax(varmean)
                jko = np.argmax(profobs)
            if 'N3' in var:
                dN = np.diff(varmean)/np.diff(np.abs(zobs))
                jkm = dN.argmax()
                dNo = np.diff(profobs)/np.diff(np.abs(zobs))
                jko = dNo.argmax()
            metric[idate,0] = zobs[jkm]
            metric[idate,1] = zobs[jko]



    if 'chlorophyll' in var:
        np.save(OUTDIR + '/dcm.npy',metric)
        np.save(OUTDIR + '/dates_metrics_chl.npy',dates_to_save)
    if 'N3' in var:
        np.save(OUTDIR + '/ncl.npy',metric)
        np.save(OUTDIR + '/dates_metrics_nit.npy',dates_to_save)







