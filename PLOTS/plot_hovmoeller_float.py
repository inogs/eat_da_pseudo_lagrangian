import argparse

def argument():
    parser = argparse.ArgumentParser(description = '''
    Plot profiles of var form a float
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

    parser.add_argument(   '--vmin', '-mn',
                            type = str,
                            required = True,
                            help = 'end time %Y$m%d'
                            )

    parser.add_argument(   '--vmax', '-mx',
                            type = str,
                            required = True,
                            help = 'end time %Y$m%d'
                            )

    parser.add_argument(   '--depth', '-d',
                            type = str,
                            required = True,
                            help = 'end time %Y$m%d'
                            )

    return parser.parse_args()

args = argument()

import numpy as np
import matplotlib.pyplot as plt

from bitsea.commons.Timelist import TimeInterval
from bitsea.instruments import superfloat as bio_float
from bitsea.basins.region import Rectangle
from bitsea.commons.utils import addsep
import sys


startTime = args.starttime
endTime = args.endtime
var = args.var
deplim = float(args.depth)
floatid = args.floatid
OUTDIR = addsep(args.outdir)

vmin = float(args.vmin)
vmax = float(args.vmax)

TI = TimeInterval(startTime, endTime)

Allprofiles = bio_float.FloatSelector(var, TI, Rectangle(-6,36,30,46))

print("Number of  " + var + " profiles: " + str(len(Allprofiles)) )

if len(Allprofiles) == 0:
    print("no profiles with " + var )

depths_surf = [ii/10. for ii in range(25,2500,50)]
depths_mid = [ii/10. for ii in range(2500,5000,100)]
depths_bott = [ii/10. for ii in range(5000,18001,100)]

depths = []
depths.extend(depths_surf)
depths.extend(depths_mid)
depths.extend(depths_bott)

plt.close('all')

MATP = []
dates = []

plt.figure(figsize=[7,12])
for pp in Allprofiles:
    if floatid in pp.ID():
        Pres,Profile,Qc = pp.read(var)
        datestring = pp.time.strftime('%Y-%m-%d %H:%M:%S')
        ProfInterp = np.interp(depths,Pres,Profile)
        MATP.append(ProfInterp)
        dates.append(pp.time)
        #print(pp.ID())
        plt.plot(ProfInterp,depths,':',color='grey')

print("Number of  " + var + " profiles: " + str(len(MATP)) + " with float " + str(floatid))

if len(MATP) > 0:
   plt.plot(np.nanmean(np.array(MATP),axis=0),depths,'-',color='blue')
   plt.grid()
   plt.ylim(deplim,0)
   plt.title(var + ' ' + floatid)

   plt.tight_layout()
   plt.savefig(OUTDIR + '/allprofiles_' + var + floatid + '.png')

   plt.figure(figsize=[11,5])

   xd, yd = np.meshgrid(dates,depths)
   plt.pcolormesh(xd,yd,np.array(MATP).T,vmin=vmin,vmax=vmax,shading='auto')
   plt.ylim(deplim,0)
   plt.colorbar()

   plt.gcf().autofmt_xdate()
   plt.title(var + ' ' + floatid)

   plt.tight_layout()

   plt.savefig(OUTDIR + '/hovm_' + var + '_' + floatid + '.png')



