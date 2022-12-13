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

TI = TimeInterval(startTime, endTime)

Allprofiles = bio_float.FloatSelector(var, TI, Rectangle(-6,36,30,46))


errvar = {
    'TEMP': 30 ,
    'PSAL': 10,
}
errobs = errvar[var]

depths_surf = [ii/10. for ii in range(0,1000,50)]
depths_mid = [ii/10. for ii in range(1000,5000,250)]
depths_bott = [ii/10. for ii in range(5000,20000,500)]
depths_bott2 = [ii/10. for ii in range(20000,31001,1000)]
depths_bott3 = [12000]

depths = []
depths.extend(depths_surf)
depths.extend(depths_mid)
depths.extend(depths_bott)
depths.extend(depths_bott2)
depths.extend(depths_bott3)

LINES = []
for pp in Allprofiles:
    if floatid in pp.ID():
        Pres,Profile,Qc = pp.read(var)
        datestring = pp.time.strftime('%Y-%m-%d %H:%M:%S')
        ProfInterp = np.interp(depths,Pres,Profile)
        print(pp.ID())
        firstline = "%s\t%d\t%d\n" %(datestring,len(depths),2)
        LINES.append(firstline)
        for ii in range(len(depths)):
        #for ii in range(len(Pres)):
            line = "%5.3f\t%5.3f\n" %(-depths[ii],ProfInterp[ii])
            #line = "%s\t%5.3f\t%5.3f\t%5.3f\n" %(datestring,-Pres[ii],Profile[ii],errobs)
            LINES.append(line)
        # break


#fileout = OUTDIR + '/profile_' + var + '.obs'
fileout = OUTDIR + '/profile_' + var + '.nudg'
f = open(fileout,'w')

f.writelines(LINES)

f.close()
