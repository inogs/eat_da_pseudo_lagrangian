import argparse

def argument():
    parser = argparse.ArgumentParser(description = '''
    Extract profiles of var from a float
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

from commons.Timelist import TimeInterval
from instruments import superfloat as bio_float
from basins.region import Rectangle
from commons.utils import addsep


startTime = args.starttime
endTime = args.endtime
var = args.var
floatid = args.floatid
OUTDIR = addsep(args.outdir)

if args.depth is not None:
    depthLIM =  np.float(args.depth)
else:
    depthLIM = 5000

TI = TimeInterval(startTime, endTime)

Allprofiles = bio_float.FloatSelector(var, TI, Rectangle(-6,36,30,46))


errvar = {
    # 'TEMP': [0.5,0.5,.5] ,
    # 'PSAL': [0.1,0.1,0.1],
    # 'NITRATE': [np.nan,np.nan,np.nan],
    'CHLA': [(1.2,0.02),(1.2,0.02),(1.2,0.02)],
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
for pp in Allprofiles:
    if floatid in pp.ID():
        print(pp.ID())
        Pres,Profile,Qc = pp.read(var)
        datestring = pp.time.strftime('%Y-%m-%d %H:%M:%S')
        ProfInterp = np.interp(depths,Pres,Profile)
        errprof = np.zeros(len(ProfInterp),dtype=object) 
        for iib,bb in enumerate(err_bound):
            #errprof[np.array(depths)>bb] = errobs[iib][0]*1000 + errobs[iib][1]*1.e+9 + 1.e+12
            if ((errobs[iib][0]>=1000) | (errobs[iib][1]>=1000)):
                print('err >= 1000 not implemented - exit')
                import sys
                sys.exit('exiting')
            errprof[np.array(depths)>bb] = "1%06d"  %(int(errobs[iib][0]*1000)) + "%06d" %(int(errobs[iib][1]*1000))
        ProfInterp = ProfInterp[np.array(depths)<depthLIM]
        for ii in range(len(ProfInterp)):
        #for ii in range(len(Pres)):
            line = "%s\t%5.3f\t%5.3f\t%s\n" %(datestring,-depths[ii],ProfInterp[ii],errprof[ii])
            #line = "%s\t%5.3f\t%5.3f\t%5.3f\n" %(datestring,-Pres[ii],Profile[ii],errobs)
            LINES.append(line)


fileout = OUTDIR + '/profile_' + var + '.obs'
f = open(fileout,'w')

f.writelines(LINES)

f.close()
