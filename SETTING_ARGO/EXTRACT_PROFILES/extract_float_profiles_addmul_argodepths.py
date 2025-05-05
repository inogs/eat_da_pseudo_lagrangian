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

    parser.add_argument(   '--errm', '-m',
                            type = str,
                            required = False,
                            help = 'multiplicative err ex. 1.3 for 30%'
                            )

    parser.add_argument(   '--erra', '-a',
                            type = str,
                            required = False,
                            help = 'additive err ex. 0.02 chl conc'
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

errm = float(args.errm)
erra = float(args.erra)

TI = TimeInterval(startTime, endTime)

Allprofiles = bio_float.FloatSelector(var, TI, Rectangle(-6,36,30,46))


#errvar = {
#    'TEMP': [0.5,0.5,.5] ,
#    'PSAL': [0.1,0.1,0.1],
#    'NITRATE': [(1.2,0.02),(1.2,0.02),(1.2,0.02)],
#    'CHLA': [(1.2,0.02),(1.2,0.02),(1.2,0.02)],
#}
err_bound = [0,20,400]
#errobs = errvar[var]

errobs = [(errm,erra) for ii in range(len(err_bound))]

# depths_surf = [ii/10. for ii in range(25,2500,50)]
# depths_mid = [ii/10. for ii in range(2500,5000,100)]
# depths_bott = [ii/10. for ii in range(5000,18001,100)]

# depths = []
# depths.extend(depths_surf)
# depths.extend(depths_mid)
# depths.extend(depths_bott)

LINES = []
LINESsurf = []
for pp in Allprofiles:
    if floatid in pp.ID():
        print(pp.ID())
        Pres,Profile,Qc = pp.read(var)
        dd = pp.time.replace(hour=12,minute=0,second=0)
        datestring = dd.strftime('%Y-%m-%d %H:%M:%S')
        errprof = np.zeros(len(Profile),dtype=object) 
        for iib,bb in enumerate(err_bound):
            if ((errobs[iib][0]>=1000) | (errobs[iib][1]>=1000)):
                print('err >= 1000 not implemented - exit')
                import sys
                sys.exit('exiting')
            errprof[np.array(Pres)>bb] = "1%06d"  %(int(errobs[iib][0]*1000)) + "%06d" %(int(errobs[iib][1]*1000))
        surf = np.nanmean(Profile[np.array(Pres)<5])
        line_surf = "%s\t%5.3f\n" %(datestring,surf)
        LINESsurf.append(line_surf)

        Profile = Profile[np.array(Pres)<depthLIM]
        for ii in range(len(Profile)):
            line = "%s\t%5.3f\t%5.3f\t%s\n" %(datestring,-Pres[ii],Profile[ii],errprof[ii])
            LINES.append(line)


fileout = OUTDIR + '/profile_' + var + '.obs'
f = open(fileout,'w')

f.writelines(LINES)
f.close()

fileout = OUTDIR + '/surf_' + var + '.obs'
f = open(fileout,'w')

f.writelines(LINESsurf)

f.close()
