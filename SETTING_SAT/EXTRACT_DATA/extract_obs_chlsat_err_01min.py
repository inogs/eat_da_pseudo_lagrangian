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

    parser.add_argument(   '--invar', '-v',
                            type = str,
                            required =True,
                            help = ''' dir var sat'''
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
    
    parser.add_argument(   '--merr', '-em',
                            type = str,
                            required =True,
                            help = ''' multiplicative error'''
                            )

    return parser.parse_args()

args = argument()


import numpy as np

from commons.mask import Mask
from commons.utils import addsep
from commons.Timelist import TimeList, TimeInterval
from Sat import SatManager as Sat

INOBS = addsep(args.indir)
VARSATDIR = addsep(args.invar)
OUTDIR = addsep(args.outdir)

maskfile = args.maskfile
TheMask = Mask(maskfile)


lonB = float(args.lon)
latB = float(args.lat)



iP,jP = TheMask.convert_lon_lat_to_indices(lonB,latB)


TI = TimeInterval("2018","2022",'%Y')

TL = TimeList.fromfilenames(TI,INOBS,"*v02.nc",prefix='',dateformat='%Y%m%d')


err0 = float(args.merr) #mult
#err1 = .03 #add
err1 = np.zeros(12)
err1[:] = np.nan

for im in range(12):
    varfile = VARSATDIR + "/var2D.%02d.nc" %(im+1)
    varsat = Sat.readfromfile(varfile,'variance')
    varsat_p = varsat[jP,iP]
    if (np.isnan(varsat_p)) | (varsat_p>1.e+19): continue
    err1[im] = varsat_p**.5
    if err1[im]<0.01:
        err1[im] = 0.01
    print(varsat_p**.5)

# import sys
# sys.exit(0)

dateobsLIST = []
obsLIST = []
errLIST = []
for ii,filein in enumerate(TL.filelist):
    datefile = TL.Timelist[ii]
    im = datefile.month-1
    try:
        CHL = Sat.readfromfile(filein)
    except:
        continue
    if (CHL[jP,iP]<0) | (CHL[jP,iP]>1.e+19) | (np.isnan(err1[im])): continue
    print(datefile)
    obsLIST.append(CHL[jP,iP])
    dateobsLIST.append(datefile.strftime('%Y-%m-%d %H:%M:%S'))
    errstr = "1%06d"  %(round(err0*1000)) + "%06d" %(round(err1[im]*1000))
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


