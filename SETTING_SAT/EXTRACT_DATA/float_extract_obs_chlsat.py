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

#   parser.add_argument(   '--lon', '-ln',
#                           type = str,
#                           required =True,
#                           help = ''' point longitude'''
#                           )

#   parser.add_argument(   '--lat', '-lt',
#                           type = str,
#                           required =True,
#                           help = ''' point latitude'''
#                           )

    parser.add_argument(   '--maskfile', '-m',
                            type = str,
                            required =True,
                            help = ''' maskfile'''
                            )

    parser.add_argument(   '--float_name', '-fln',
                                type = str,
                                required = True,
                                default = '',
                                help = 'float name to extract trajectory')

    return parser.parse_args()

args = argument()


import numpy as np

from commons.mask import Mask
from commons.utils import addsep
from commons.Timelist import TimeList, TimeInterval
from Sat import SatManager as Sat
from instruments.superfloat import FloatSelector
from instruments.var_conversions import SUPERFLOAT_VARS
from basins.region import Rectangle
from scipy import spatial


INOBS = addsep(args.indir)
OUTDIR = addsep(args.outdir)

maskfile = args.maskfile
TheMask = Mask(maskfile)


lonB = 0.
latB = 0.



#iP,jP = TheMask.convert_lon_lat_to_indices(lonB,latB)


TI = TimeInterval("2018","2022",'%Y')

TL = TimeList.fromfilenames(TI,INOBS,"*v02.nc",prefix='',dateformat='%Y%m%d')

#import float

floatname=args.float_name

DATESTART = '20180101'
DATE__END = '20220101'


T_INT = TimeInterval(DATESTART,DATE__END, '%Y%m%d')

var_mod = 'P_l'
#var_mod = 'N3n'
ALL_PROFILES = FloatSelector(SUPERFLOAT_VARS[var_mod],T_INT, Rectangle(-6,36,30,46))

nprofs = 0
LONprofs = []
LATprofs = []
DATEprofs = []
NAMEprofs = []

for iip,p in enumerate(ALL_PROFILES):
    print('%9d of %9d' %(iip+1,len(ALL_PROFILES)),flush=True)
    kk = p.read(SUPERFLOAT_VARS[var_mod])
    if kk[0].shape[0]>0:
        if p.name() == floatname :  #get data only for the interested float
            nprofs += 1
            LONprofs.append(p.lon)
            LATprofs.append(p.lat)
            DATEprofs.append(p.time)
            NAMEprofs.append(p.name())

FLOATlist = np.unique(NAMEprofs)

FLOATlon = {}
FLOATlat = {}
FLOATtimes = {}
for ff in FLOATlist:
    indices = [i for i,x in enumerate(NAMEprofs) if x==ff]
    FLOATlon[ff] = [LONprofs[i] for i in indices]
    FLOATlat[ff] = [LATprofs[i] for i in indices]
    FLOATtimes[ff] = [DATEprofs[i] for i in indices]




##########

err0 = 5 #mult %
err1 = .03 #add concentraione

dateobsLIST = []
dateobjLIST = []
obsLIST = []
errLIST = []
for ii,filein in enumerate(TL.filelist):
    datefile = TL.Timelist[ii]
    try:
        CHL = Sat.readfromfile(filein)
    except:
        continue
    for ift,ft in enumerate(FLOATtimes[floatname]):
        if ft.date() == datefile.date():
            lonB = FLOATlon[floatname][ift]
            latB = FLOATlat[floatname][ift]
            iP,jP = TheMask.convert_lon_lat_to_indices(lonB,latB)
    if lonB==0. and latB==0. : continue #in this data the float was not operating
    if (CHL[jP,iP]<0) | (CHL[jP,iP]>1.e+19): continue
    print(datefile)
    obsLIST.append(CHL[jP,iP])
    dateobsLIST.append(datefile.strftime('%Y-%m-%d %H:%M:%S'))
    dateobjLIST.append(TL.Timelist[ii])
    errstr = CHL[jP,iP]*0.1
#   errstr = np.log10(1.0+0.3)
#   errstr = "0.01"
#   errstr = "1%06d"  %(int(err0*1000)) + "%06d" %(err1*1000)
    errLIST.append(errstr)


lenD = len(dateobsLIST)
lenO = len(obsLIST)
lenE = len(errLIST)

if not((lenD==lenO) & (lenO==lenE)):
#if not((lenD==lenO)):
    print('not equal lenght of outputs. Exiting')
    import sys
    sys.exit(1)


fileout = OUTDIR + '/nrt_chlsat.obs'

f = open(fileout,'w')
LINES = []
for ll in range(lenO):
    line = "%s\t%5.3f\t%s\n" %(dateobsLIST[ll],obsLIST[ll],errLIST[ll])
    LINES.append(line)

f.writelines(LINES)

f.close()

fileout = OUTDIR + '/nrt_chlsat.obs'
np.savez(fileout, allow_pickle=True, dateobjLIST=dateobjLIST, obsLIST=obsLIST, errLIST=errLIST)
