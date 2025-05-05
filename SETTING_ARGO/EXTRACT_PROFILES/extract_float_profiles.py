import argparse

def argument():
    parser = argparse.ArgumentParser(description = '''
    Extract profiles of var form a float
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--outdir', '-o',
                            type = str,
                            required =True,
                            help = ''' Outputdir'''
                            )

    parser.add_argument(   '--floatid', '-f',
                            type = str,
                            required = True,
                            help = 'float id number'
                            )

    parser.add_argument(   '--var', '-v',
                            type = str,
                            required = True,
                            help = 'float id number'
                            )

    parser.add_argument(   '--starttime', '-s',
                            type = str,
                            required = True,
                            help = 'start time %Y$m%d'
                            )

    parser.add_argument(   '--endtime', '-e',
                            type = str,
                            required = True,
                            help = 'end time %Y$m%d'
                            )

    parser.add_argument(   '--depth', '-d',
                            type = float,
                            required = False,
                            help = 'max depth of observations'
                            )

    return parser.parse_args()

args = argument()

import numpy as np

from bitsea.commons.Timelist import TimeInterval
from bitsea.instruments import superfloat as bio_float
from bitsea.basins.region import Rectangle
from bitsea.commons.utils import addsep


startTime = args.starttime
endTime = args.endtime
var = args.var
floatid = args.floatid
OUTDIR = addsep(args.outdir)

if args.depth is not None:
    depthLIM =  args.depth
else:
    depthLIM = 5000

TI = TimeInterval(startTime, endTime)

Allprofiles = bio_float.FloatSelector(var, TI, Rectangle(-6,36,30,46))


errvar = {
    'TEMP': [0.5,0.5,.5] ,
    'PSAL': [0.1,0.1,0.1],
    'NITRATE': [np.nan,np.nan,np.nan],
    'CHLA': [.15,.15,.15],
}
err_bound = [0,20,400]
errobs = errvar[var]

depths_surf = [ii/10. for ii in range(25,2500,50)]
depths_mid = [ii/10. for ii in range(2500,5000,100)]
depths_bott = [ii/10. for ii in range(5000,18001,100)]

depths = []
depths.extend(depths_surf)
depths.extend(depths_mid)
depths.extend(depths_bott)

LINES = []
date__vector=[]
depth_vector=[]
obs___vector=[]
err0__vector=[]
err1__vector=[]
for pp in Allprofiles:
    if floatid in pp.ID():
        print(pp.ID())
        Pres,Profile,Qc = pp.read(var)
        datestring = pp.time.strftime('%Y-%m-%d %H:%M:%S')
        ProfInterp = np.interp(depths,Pres,Profile)
        errprof = np.zeros(len(ProfInterp)) 
        for iib,bb in enumerate(err_bound):
            errprof[np.array(depths)>bb] = errobs[iib]
        ProfInterp = ProfInterp[np.array(depths)<depthLIM]
        for ii in range(len(ProfInterp)):
        #for ii in range(len(Pres)):
            line = "%s\t%5.3f\t%5.3f\t%5.3f\n" %(datestring,-depths[ii],ProfInterp[ii],errprof[ii])
            #line = "%s\t%5.3f\t%5.3f\t%5.3f\n" %(datestring,-Pres[ii],Profile[ii],errobs)
            LINES.append(line)
            date__vector.append(datestring)
            depth_vector.append(-depths[ii])
            obs___vector.append(ProfInterp[ii])
            err0__vector.append(errprof[ii])
            err1__vector.append(errprof[ii])
        # break


fileout = OUTDIR + '/profile_' + var + '.obs'
f = open(fileout,'w')

f.writelines(LINES)

f.close()
np.savez(fileout, allow_pickle=True, dateobjLIST=date__vector, depthLIST=depth_vector, obsLIST=obs___vector, err0LIST=err0__vector, err1LIST=err1__vector)
