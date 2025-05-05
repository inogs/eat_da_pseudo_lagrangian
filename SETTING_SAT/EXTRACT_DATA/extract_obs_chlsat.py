import argparse

def argument():
    parser = argparse.ArgumentParser(description = '''
    Extract satellite observation
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--outdir', '-o',
                            type = str,
                            required =True,
                            help = ''' Outputdir'''
                            )

    parser.add_argument(   '--indir', '-i',
                            type = str,
                            required =True,
                            help = ''' dir daily sat'''
                            )

    parser.add_argument(   '--lon', '-ln',
                            type = str,
                            required =True,
                            help = ''' point longitude'''
                            )

    parser.add_argument(   '--lat', '-lt',
                            type = str,
                            required =True,
                            help = ''' point latitude'''
                            )

    parser.add_argument(   '--maskfile', '-m',
                            type = str,
                            required =True,
                            help = ''' maskfile'''
                            )

    return parser.parse_args()

args = argument()


import numpy as np

from bitsea.commons.mask import Mask
from bitsea.commons.utils import addsep
from bitsea.commons.Timelist import TimeList, TimeInterval
from bitsea.Sat import SatManager as Sat

INOBS = addsep(args.indir)
OUTDIR = addsep(args.outdir)

maskfile = args.maskfile
TheMask = Mask.from_file(maskfile)


lonB = float(args.lon)
latB = float(args.lat)



iP,jP = TheMask.convert_lon_lat_to_indices(lon=lonB,lat=latB)


TI = TimeInterval("2018","2022",'%Y')

TL = TimeList.fromfilenames(TI,INOBS,"*P1D.nc",prefix='',dateformat='%Y%m%d')


err0 = 5 #mult
err1 = .03 #add

dateobsLIST = []
obsLIST = []
errLIST = []
for ii,filein in enumerate(TL.filelist):
    datefile = TL.Timelist[ii]
    try:
        CHL = Sat.readfromfile(filein)
    except:
        continue
    if (CHL[jP,iP]<0) | (CHL[jP,iP]>1.e+19): continue
    print(datefile)
    obsLIST.append(CHL[jP,iP])
    dateobsLIST.append(datefile.strftime('%Y-%m-%d %H:%M:%S'))
    errstr = "1%06d"  %(int(err0*1000)) + "%06d" %(err1*1000)
    errLIST.append(errstr)


lenD = len(dateobsLIST)
lenO = len(obsLIST)
lenE = len(errLIST)

if not((lenD==lenO) & (lenO==lenE)):
#if not((lenD==lenO)):
    print('not equal lenght of outputs. Exiting')
    import sys
    sys.exit(1)


fileout = OUTDIR + '/nrt_chlsat.dat'

f = open(fileout,'w')
LINES = []
for ll in range(lenO):
    line = "%s\t%5.3f\t%s\n" %(dateobsLIST[ll],obsLIST[ll],errLIST[ll])
    LINES.append(line)

f.writelines(LINES)

f.close()


