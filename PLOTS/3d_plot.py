import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import datetime
from datetime import timedelta
import glob
from scipy.stats import variation

#filenames = glob.glob('/g100_scratch/userexternal/gocchipi/stoc_prova/*/result.nc')
filenames = glob.glob('/g100_scratch/userexternal/plazzari/WP6_TEST/6901772_assimilation_F3/result_*.nc')

filenames.sort(key=lambda x: int(''.join(filter(str.isdigit, x)))) #sort by number
#filenames = filenames[:3]

ref = datetime.datetime(2019, 1, 1, 0, 0, 0)
for inc,ncname in enumerate(filenames):
    print('reading file... ', inc, '/', len(filenames))
    infile=ncname 
    
    NCin=NC4.Dataset(infile,"r")
    
    depth=NCin.variables['z'][:,:,0,0].filled()
    if inc == 0:
        CHL_arr = np.zeros((len(filenames),len(NCin.variables['time'][:]),len(depth[0])))
    CHL_arr[inc,:,:]=NCin.variables['P1_Chl'][:,:,0,0].filled()+NCin.variables['P2_Chl'][:,:,0,0].filled()+NCin.variables['P3_Chl'][:,:,0,0].filled()+NCin.variables['P4_Chl'][:,:,0,0].filled()
#   CHL_arr[inc,:,:]=NCin.variables['P1_sum'][:,:,0,0].filled()
#   CHL_arr[inc,:,:]=NCin.variables['Z3_c'][:,:,0,0].filled()+NCin.variables['Z4_c'][:,:,0,0].filled()+NCin.variables['Z5_c'][:,:,0,0].filled()+NCin.variables['Z6_c'][:,:,0,0].filled()
time=NCin.variables['time'][:].filled()

CHL_mean = np.mean(CHL_arr, axis=0)
CHL_cv   = variation(CHL_arr, axis=0)


#max depth to keep in plots
maxdepth = -300
for i,dp in enumerate(depth[0]):
    if dp>maxdepth:
        imax = i
        break
CHL_mean = CHL_mean[:,imax:]
CHL_cv = CHL_cv[:,imax:]
depth = depth[:,imax:]

date_list = []

for myt in time:
    step = datetime.timedelta(seconds=int(myt))
    date_list.append(ref + step)

nT=len(date_list)
nZ=depth.shape[1]

#(time, z, lat, lon)
x=np.tile(np.arange(nT),(nZ,1))
x = np.transpose(x)
CHL_cv = - CHL_cv

#3d plot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource
fig = plt.figure()
axs = fig.gca(projection='3d')
# Create light source object.
ls = LightSource(azdeg=20, altdeg=65)
# Shade data, creating an rgb array.
#rgb = ls.shade(CHL_mean, plt.cm.RdYlBu)
rgb = ls.shade(CHL_mean, cmap=cm.viridis, vert_exag=1, blend_mode='hsv')

surf = axs.plot_surface(
   x, depth, CHL_cv, rstride=1, cstride=1,
   facecolors=rgb,
#  facecolors=cm.jet(CHL_mean),
    linewidth=0, antialiased=False, shade=False)
#plt.show()

#cax=axs.pcolor(x,y,CHLT)
#cax=axs.pcolor(x,y,CHLT,norm=LogNorm(vmin=0.1, vmax=CHLT.max()))
tpos=range(0,nT,90)
axs.set_xticks(tpos)
tick_labels=[]
for i in tpos:
   tick_labels.append(date_list[i].strftime("%Y-%m"))
axs.set_xticklabels(tick_labels,rotation=-30)
axs.zaxis.set_major_locator(plt.MaxNLocator(3))
axs.set_ylim([-300,0])
#axs.set_xlabel('Time')
axs.set_ylabel('Depth [m]')
axs.set_zlabel('CV')
axs.view_init(75, 240)

m = cm.ScalarMappable(cmap=cm.viridis)
m.set_array(CHL_mean)
plt.colorbar(m)

fileout='chl_3dplot.png'
fig.savefig(fileout, format='png',dpi=150, bbox_inches="tight")

