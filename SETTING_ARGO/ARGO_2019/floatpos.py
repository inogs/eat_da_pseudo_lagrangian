import numpy as np

from instruments.superfloat import FloatSelector
from instruments.var_conversions import SUPERFLOAT_VARS

from commons.mask import Mask
from commons.time_interval import TimeInterval
from basins.region import Rectangle


DATESTART = '20190101'
DATE__END = '20191231'


T_INT = TimeInterval(DATESTART,DATE__END, '%Y%m%d')

var_mod = 'P_l'
var_mod = 'N3n'
ALL_PROFILES = FloatSelector(SUPERFLOAT_VARS[var_mod],T_INT, Rectangle(-6,36,30,46))


nprofs = 0
LONprofs = []
LATprofs = []
DATEprofs = []
NAMEprofs = []

for iip,p in enumerate(ALL_PROFILES):
    print('%9d of %9d' %(iip+1,len(ALL_PROFILES)))
    kk = p.read(SUPERFLOAT_VARS[var_mod])
    if kk[0].shape[0]>0:
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



#LIST = [ii for ii in range(5)]

#LIST[0] = nprofs
#LIST[1] = LONprofs
#LIST[2] = LATprofs
#LIST[3] = DATEprofs
#LIST[4] = NAMEprofs


import matplotlib.pyplot as plt

maskfile = '/g100_scratch/userexternal/ateruzzi/MASK24_REA/meshmask.nc'
TheMask = Mask(maskfile)
_,jpj,jpi = TheMask.shape

maskcoast = np.zeros((jpj,jpi))
maskcoast[TheMask.mask_at_level(0)==False] = 1

plt.close('all')

sfig = 10
plt.figure(figsize=[sfig,sfig*16./42.])

levels = [-1,0,1]
colors = ['white','grey']
plt.contourf(TheMask.xlevels,TheMask.ylevels,maskcoast,
            levels,colors=colors)
plt.ylabel(u'\u00b0 N')
plt.xlabel(u'\u00b0 E')



for ff in FLOATlist:
    print(ff)
    plt.plot(FLOATlon[ff],FLOATlat[ff],
        'o',#color='orange',
        markersize=2.3,
        alpha=1,
        label='{:}_{:5.5}_{:5.5}'.format(ff,np.nanmean(FLOATlon[ff]),np.nanmean(FLOATlat[ff])),
        )
    print('lon %5.5f' %(np.nanmean(FLOATlon[ff])))
    print('lat %5.5f' %(np.nanmean(FLOATlat[ff])))


plt.legend(ncol=3,fontsize='xx-small')

plt.show(block=False)


plt.savefig('float_' + var_mod + '_2019.png')



