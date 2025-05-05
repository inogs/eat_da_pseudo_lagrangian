import numpy as np
import pandas as pd

from bitsea.commons.mask import Mask
from bitsea.commons.utils import addsep
from bitsea.commons.Timelist import TimeList, TimeInterval
from bitsea.Sat import SatManager as Sat
from bitsea.instruments.superfloat import FloatSelector
from bitsea.instruments.var_conversions import SUPERFLOAT_VARS
from bitsea.basins.region import Rectangle
from scipy import spatial



floatname=[ '6901772','6901774','6901775','6902898','6902902','6902903','6902904','6903247','6903250']
#floatname='6901772'

params_list={'instances_light_parameters_EPS0r':    [ 0., 1.],      #  100.   Background shortwave attenuation                            [1/m]                [21]
             'instances_Z5_parameters_p_pu':        [ 0., 1.],      #   67.   Assimilation efficiency, microzooplankton                   [-]                  [13]
             'instances_light_parameters_pEIR_eow': [ 0., 1.],      #   54.   Photosynthetically active fraction of shortwave radiation   [-]                  [6]
             'instances_P1_parameters_p_sum':       [ 2., 4.],      #         maximum specific productivity at reference temperature (1/d)
             'instances_Z5_parameters_p_sum':       [ 2., 5.],      #   47.   Potential growth rate, microzooplankton                     [1/d]                [13]
             'instances_P1_parameters_p_qlcPPY':    [ 0., 1.],      #   42.   Reference Chla:C quotum, diatoms                            [mgChla/mgC]         [1]
             'instances_P1_parameters_p_qup':       [ 0., 0.5],     #   41.   Membrane affinity for P, diatoms                            [m3/mgC/d]           [4]
             'instances_Z5_parameters_p_pu_ea':     [ 0., 1.],      #   36.   Fraction of activity excretion, microzooplankton            [-]                  [14]
             'instances_P1_parameters_p_alpha_chl': [ 0., 5e-5],    #   35.   Initial slope of the P-E curve, diatoms                     [mgC s m2/mgChl/uE]  [1]
             'instances_P1_parameters_p_qplc':      [ 0., 1.],      #   33.   Minimum phosphorus to carbon ratio, diatoms                 [mmol P/mg C]        [4]
             'instances_P1_parameters_p_srs':       [ 0., 0.5 ], }  #   33.   Respiration rate at 10 degrees C, diatoms                   [1/d]                [2]

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
#   print('%9d of %9d' %(iip+1,len(ALL_PROFILES)),flush=True)
    kk = p.read(SUPERFLOAT_VARS[var_mod])
    if kk[0].shape[0]>0:
        if p.name() in floatname :  #get data only for the interested float
#       if p.name() == floatname :  #get data only for the interested float
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

# get data from assimilation
#data = np.random.uniform(0,1,len(FLOATtimes[ff])) #fake data to give colors to each point

for pp in params_list.keys():
#### plot map
        pvmin=params_list[pp][0]
        pvmax=params_list[pp][1]
        import matplotlib.pyplot as plt
        
        maskfile = '/g100_scratch/userexternal/ateruzzi/MASK24_REA/meshmask.nc'
        TheMask = Mask.from_file(maskfile)
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
            filein='PARAMETERS_TXT/' + ff + '_' + pp + '.txt'
            try:
               df = pd.read_csv(filein, sep="\t",skiprows = 0, engine='python')
            except:
                print("input file not found or corrupted " + filein)
                continue
            #yyyy	mm	dd	HH	MM	SS	AVE	STD
            ave  = df['AVE'].values
            yyyy = df['yyyy'].values
            mm   = df['mm'].values
            dd   = df['dd'].values
            lon=[]
            lat=[]
            data=[]
            for i,val in  enumerate(ave):
                for j,date_time_obj in enumerate(FLOATtimes[ff]):

                    if int(date_time_obj.year) == yyyy[i]:
                        if int(date_time_obj.month)== mm[i]:
#                          if int( date_time_obj.day)== dd[i]:
#                              print([ FLOATlon[ff][j] + ' ' +  FLOATlat[ff][j]  + ' ' + ave[i]] )
                               lon.append(FLOATlon[ff][j])
                               lat.append(FLOATlat[ff][j])
                               data.append(ave[i])

            if data :  #  false if list is empty 
               sc=plt.scatter(lon,lat,s=2.3,c=data,cmap='YlGnBu',vmin=pvmin,vmax=pvmax)
               my_offset=(30, 30)
               if  ff =='6901775':
                   my_offset=(-30,-30)
               if ff == '6903247' :
                   my_offset=(-10,-20)
               if ff == '6902904' :
                   my_offset=(50,50)
               plt.annotate( ff,
                                xy=(lon[0], lat[0]), xytext=my_offset,
                                textcoords='offset points', ha='right', va='bottom',
                                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
                              )
            else:
                print(" assimilated data not matching float data " + filein)
                continue

            print('lon %5.5f' %(np.nanmean(FLOATlon[ff])))
            print('lat %5.5f' %(np.nanmean(FLOATlat[ff])))
        
        plt.title(pp) 
        plt.colorbar(sc)
        plt.savefig('float_' + pp + '_2019_interpolated.png')
        
        
        
        
