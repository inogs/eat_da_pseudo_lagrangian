import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    extract variable profiles for ICs
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--indir', '-i',
                                type = str,
                                required = True,
                                help = 'indir')

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


    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                required = True,
                                default = '',
                                help = 'Output dir')

    parser.add_argument(   '--lon', '-n',
                                type = str,
                                required = True,
                                default = '',
                                help = 'longitude of the point')

    parser.add_argument(   '--lat', '-t',
                                type = str,
                                required = True,
                                default = '',
                                help = 'latitude of the point')

    parser.add_argument(   '--depth', '-p',
                                type = str,
                                required = True,
                                default = '',
                                help = 'depth used in gotm.yaml')

    parser.add_argument(   '--date', '-d',
                                type = str,
                                required = True,
                                default = '',
                                help = 'date forma YYYYMMDD')

    parser.add_argument(   '--maskfile', '-m',
                                type = str,
                                required = True,
                                default = '',
                                help = 'maskfile meshmask.nc')

    parser.add_argument(   '--zfile', '-z',
                                type = str,
                                required = True,
                                default = '',
                                help = 'file with gotm vertical discretization gird.dat')

    return parser.parse_args()


args = argument()

import numpy as np
import datetime
#import netCDF4 as NC
#from commons import netcdf4
from commons.utils import addsep
from commons.dataextractor import DataExtractor
from commons.mask import Mask
import matplotlib.pylab as plt

INDIR = addsep(args.indir)

lonP = float(args.lon)
latP = float(args.lat)

OUTDIR = addsep(args.outdir)

datestr = args.date
TheMask = Mask(args.maskfile)
zfile = args.zfile
depth = float(args.depth)


datet = datetime.datetime.strptime(datestr,'%Y%m%d')
datestrgotm = datet.strftime('%Y-%m-%d %H:%M:%S')

varLIST = ['O2o','O3h','O3c',
    'N1p','N3n','N4n','N5s',
    'P1c','P1l','P1n','P1p','P1s',
    'P2c','P2l','P2n','P2p',
    'P3c','P3l','P3n','P3p',
    'P4c','P4l','P4n','P4p',
    'R1c','R1n','R1p',
    'R2c',
    'R3c','R3l',
    'R6c','R6p','R6n','R6s']

print(varLIST)
DICTvar = {}
for var in varLIST:
    DICTvar[var] = []


ff = open(zfile,'r')
lines = ff.readlines()[1:]
ff.close()

dzLIST = [float(ll.rstrip('\n'))*depth for ll in lines]
depthLIST = []
depthLIST.append(dzLIST[0])
for k in range(len(dzLIST)-1):
    depthLIST.append(dzLIST[k+1] +depthLIST[k])

indlon,indlat = TheMask.convert_lon_lat_to_indices(lonP,latP)
for var in varLIST:
#for var in [varLIST[0]]:
    print(var)
    infile = INDIR + '/RST.' + datestr + '-00:00:00.' + var + '.nc'
    De = DataExtractor(TheMask,filename=infile,varname='TRN' + var)
    profile_zmodel = De.filled_values[:,indlat,indlon]
    maskp = ((profile_zmodel>1.e+19) | np.isnan(profile_zmodel))==False
    profile_zmodel = profile_zmodel[maskp]
    profile_zgotm = np.interp(depthLIST,TheMask.zlevels[maskp],profile_zmodel)
    if np.any(np.isnan(profile_zgotm)):
        print('nan!!!')
        import sys
        sys.exit(0)
    else: print('   this variable OK')
    if np.any(profile_zgotm==0):
        print('zero!!!')
        import sys
        sys.exit(0)
    else: print('   this variable OK - zero')
    nZ = len(profile_zgotm)
    LINES = []
    LINES.append("%s\t%6i\t%6i\n" %(datestrgotm,nZ,2))
    for kk in range(nZ):
        line = "%8.6f\t%8.6f\n" %(depthLIST[kk]*-1,profile_zgotm[kk])
        line = "{:8.6f}".format(depthLIST[kk]*(-1)) + "\t{:10.5e}\n".format(profile_zgotm[kk])
        LINES.append(line)

    fileout = OUTDIR + '/' + var + '.prof'
    print(fileout)
    f = open(fileout,'w')
    f.writelines(LINES)
    f.close()

    plt.plot(profile_zgotm,depthLIST)
    plt.title(var)
    plt.grid()
    plt.ylim(depthLIST[-1],depthLIST[0])
    plt.savefig(OUTDIR + '/fig' + var + '.png')
        
    plt.close('all')

