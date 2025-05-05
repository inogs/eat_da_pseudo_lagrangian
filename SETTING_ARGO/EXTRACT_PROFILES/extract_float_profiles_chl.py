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
                            type = str,
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
    depthLIM =  float(args.depth)
else:
    depthLIM = 5000

TI = TimeInterval(startTime, endTime)

Allprofiles = bio_float.FloatSelector(var, TI, Rectangle(-6,36,30,46))


 
err_bound = [0,20,400]
errobs = [0.0690, 0.0969, 0.0997, 0.0826, 0.0660, 0.0500, 0.0360, 0.0140, 0.0320, 0.0390, 0.0340, 0.0490]

depths_surf = [ii/10. for ii in range(25,2500,50)]
depths_mid = [ii/10. for ii in range(2500,5000,100)]
depths_bott = [ii/10. for ii in range(5000,18001,100)]

depths = []
depths.extend(depths_surf)
depths.extend(depths_mid)
depths.extend(depths_bott)

LINES = []
for pp in Allprofiles:
    if floatid in pp.ID():
        print(pp.ID())
        iim = pp.time.month - 1
        Pres,Profile,Qc = pp.read(var)
        datestring = pp.time.strftime('%Y-%m-%d %H:%M:%S')
        ProfInterp = np.interp(depths,Pres,Profile)
        errprof = np.zeros(len(ProfInterp)) 
        errprof[:] = errobs[iim]
        ProfInterp = ProfInterp[np.array(depths)<depthLIM]
        for ii in range(len(ProfInterp)):
        #for ii in range(len(Pres)):
            line = "%s\t%5.3f\t%5.3f\t%5.3f\n" %(datestring,-depths[ii],ProfInterp[ii],errprof[ii])
            #line = "%s\t%5.3f\t%5.3f\t%5.3f\n" %(datestring,-Pres[ii],Profile[ii],errobs)
            LINES.append(line)
        # break


fileout = OUTDIR + '/profile_' + var + '.obs'
f = open(fileout,'w')

f.writelines(LINES)

f.close()
