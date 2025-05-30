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

    parser.add_argument(   '--errmul', '-em',
                            type = str,
                            required =True,
                            help = ''' multiplicative errro, ex. 1.35'''
                            )

    parser.add_argument(   '--erradd', '-ea',
                            type = str,
                            required =True,
                            help = ''' additive errro, ex. 0.02 conc chl'''
                            )

    return parser.parse_args()

args = argument()


import numpy as np

from bitsea.commons.mask import Mask
from bitsea.commons.utils import addsep
from bitsea.commons.Timelist import TimeList, TimeInterval
from bitsea.Sat import SatManager as Sat
from bitsea.instruments.superfloat import FloatSelector
from bitsea.instruments.var_conversions import SUPERFLOAT_VARS
from bitsea.basins.region import Rectangle
from scipy import spatial


INOBS = addsep(args.indir)
OUTDIR = addsep(args.outdir)

maskfile = args.maskfile
TheMask = Mask.from_file(maskfile)


lonB = 0.
latB = 0.



#iP,jP = TheMask.convert_lon_lat_to_indices(lon=lonB,lat=latB)


TI = TimeInterval("2018","2022",'%Y')

TL = TimeList.fromfilenames(TI,INOBS,"*P1D.nc",prefix='',dateformat='%Y%m%d')

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
    print(len(indices))




##########

err0 = float(args.errmul)
err1 = float(args.erradd)

dateobsLIST = []
dateobjLIST = []
obsLIST = []
errLIST = []
for ii,filein in enumerate(TL.filelist):
    lonB = 0
    latB = 0
    datefile = TL.Timelist[ii]
    try:
        CHL = Sat.readfromfile(filein)
    except:
        continue
    for ift,ft in enumerate(FLOATtimes[floatname]):
        if (ft.date() >= datefile.date()) & (ft.date()<=TL.Timelist[-1].date()):
            lonB = FLOATlon[floatname][ift]
            latB = FLOATlat[floatname][ift]
            iP,jP = TheMask.convert_lon_lat_to_indices(lon=lonB,lat=latB)
            break
    if lonB==0: continue
    if (CHL[jP,iP]<0) | (CHL[jP,iP]>1.e+19): continue
    print(datefile)
    obsLIST.append(CHL[jP,iP])
    pp = datefile.replace(hour=12,minute=0,second=0)
    dateobsLIST.append(pp.strftime('%Y-%m-%d %H:%M:%S'))
    dateobjLIST.append(TL.Timelist[ii])
#   errstr = CHL[jP,iP]*0.1
#   errstr = np.log10(1.0+0.3)
#   errstr = "0.01"
#   errstr = "1%06d"  %(int(err0*1000)) + "%06d" %(err1*1000)
    errstr = "1%06d"  %(round(err0*1000)) + "%06d" %(round(err1*1000))
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
