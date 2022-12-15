import os,sys
import subprocess
os.environ['ONLINE_REPO']='/g100_work/IscrB_3DSBM/FLOAT_GUIDO/'

def release_list(a):
   del a[:]
   del a
import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    extract forcings for meteo.dat adn precip.dat for gotm
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

#    parser.add_argument(   '--infile', '-i',
#                                type = str,
#                                required = True,
#                                help = 'floatname')

   # parser.add_argument(   '--inprec', '-p',
   #                             type = str,
   #                             required = True,
   #                             help = 'In .nc file with precipitation data extracted from ERA5')

    # parser.add_argument(   '--startdate', '-s',
    #                             type = str,
    #                             required = True,
    #                             help = 'start date , format YYYYMMDD')

    # parser.add_argument(   '--enddate', '-e',
    #                             type = str,
    #                             required = True,
    #                             help = 'end date , format YYYYMMDD')


#   parser.add_argument(   '--outdir', '-o',
#                               type = str,
#                               required = True,
#                               default = '',
#                               help = 'Output dir')

    parser.add_argument(   '--float_name', '-fln',
                                type = str,
                                required = True,
                                default = '',
                                help = 'float name to extract trajectory')

#   parser.add_argument(   '--lon', '-n',
#                               type = str,
#                               required = True,
#                               default = '',
#                               help = 'longitude of the point')

#   parser.add_argument(   '--lat', '-t',
#                               type = str,
#                               required = True,
#                               default = '',
#                               help = 'latitude of the point')
    parser.add_argument(   '--datestart', '-d_s',
                                type = str,
                                required = True,
                                default = '',
                                help = 'date forma YYYYMMDD')
    parser.add_argument(   '--dateend', '-d_e',
                                type = str,
                                required = True,
                                default = '',
                                help = 'date forma YYYYMMDD')

    return parser.parse_args()


args = argument()

import numpy as np
import datetime
import netCDF4 as NC
from commons import netcdf4
from commons.utils import addsep

#### import float data

from instruments.superfloat import FloatSelector
from instruments.var_conversions import SUPERFLOAT_VARS

from commons.mask import Mask
from commons.time_interval import TimeInterval
from basins.region import Rectangle
from scipy import spatial

DATESTART = args.datestart
DATE__END = args.dateend


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
        if p.name() == args.float_name :  #get data only for the interested float
            nprofs += 1
            LONprofs.append(p.lon)
            LATprofs.append(p.lat)
            DATEprofs.append(p.time)
            NAMEprofs.append(p.name())
            break

FLOATlist = np.unique(NAMEprofs)

FLOATlon = {}
FLOATlat = {}
FLOATtimes = {}
for ff in FLOATlist:
    indices = [i for i,x in enumerate(NAMEprofs) if x==ff]
    FLOATlon[ff] = [LONprofs[i] for i in indices]
    FLOATlat[ff] = [LATprofs[i] for i in indices]
    FLOATtimes[ff] = [DATEprofs[i] for i in indices]



for ff in FLOATlist:
    if ff == args.float_name:
        with open('lat.txt', 'w') as f:
            f.write('LAT='+str(FLOATlat[ff][0]))
        with open('lon.txt', 'w') as f:
            f.write('LON='+str(FLOATlon[ff][0]))
