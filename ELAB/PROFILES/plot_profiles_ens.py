import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Produce Hovmoeller plot of a variable or
    an aggregate variable
    from results of FABM-GOTM 1D
    (adding a line of a constant variable)
    ''',
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--varname', '-v',
                                type = str,
                                required = False,
                                help = 'Variable to be plotted in the Hovmoeller')

    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                required = True,
                                default = '',
                                help = 'Output Images directory')
    
    parser.add_argument(   '--indir', '-i',
                                type = str,
                                required = True,
                                help = 'indir with result.nc from ensemble')

    parser.add_argument(   '--depth', '-d',
                                type = str,
                                required = False,
                                default = '300',
                                help = 'depth limit')

    return parser.parse_args()


args = argument()



# import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
import datetime
import glob
import os
#from matplotlib.colors import LogNorm
#from datetime import timedelta
from commons.utils import addsep
#from commons.Timelist import TimeList


#ref = datetime.datetime(2016, 1, 1, 0, 0, 0)

OUTDIR = addsep(args.outdir)
INDIR = addsep(args.indir)

var = args.varname

deplim = float(args.depth)



LISTresults = [os.path.basename(ll) for ll in glob.glob(INDIR + '/result_*.nc')]
Nresults = len(LISTresults)

infile1 = LISTresults[0]
NC1 = NC4.Dataset(INDIR + infile1,'r')
depths = NC1.variables['z'][:,:,0,0].data
nZ = depths.shape[1]
times = NC1.variables['time'][:].data
nT = times.shape[0]
profiles = np.zeros((Nresults,nT,nZ))

refstr = NC1.variables['time'].units.split()[2]
ref = datetime.datetime.strptime(refstr,'%Y-%m-%d')

NC1.close()

for iix,infile in enumerate(LISTresults):
    NC = NC4.Dataset(INDIR + infile,'r')

    varvalues = NC.variables[var][:,:,0,0].data
    profiles[iix,:,:] = varvalues

    NC.close()


for idate in range(0,nT,30):
    print(idate)
    plt.close('all')
    plt.figure(figsize=[5,8])

    step = datetime.timedelta(seconds=times[idate])
    datenow = ref + step
    datestr = datenow.strftime('%Y-%m-%d')

    plt.plot(profiles[:,idate,:].T,-depths[idate,:],':',color='grey')
    pstd = np.std(profiles[:,idate,:],axis=0)
    pmean = np.mean(profiles[:,idate,:],axis=0)
    plt.plot(pmean,-depths[idate,:],'-',color='blue')
    plt.plot(pmean+pstd,-depths[idate,:],'-',color='green')
    plt.plot(pmean-pstd,-depths[idate,:],'-',color='green')
    plt.grid()
    plt.ylim(deplim,0)
    plt.title(var + ' ' + datestr)

    plt.show(block=False)

    plt.savefig(OUTDIR + '/ens_profiles.' + datestr + '.' + var + '.png')


import sys
sys.exit(0)
for iif in range(Nfigs):
    print(iif)
    fig,avaxs = plt.subplots(Naxs,1,sharex=True,sharey=True,figsize=[8,9])

    ind_start = Naxs*iif
    ind_end = Naxs*(iif+1)
    if ind_end>Nresults:
        ind_end = Nresults

    for iix,infile in enumerate(LISTresults[ind_start:ind_end]):
        print(infile)
        NCin=NC4.Dataset(INDIR + infile,"r")

        depth=NCin.variables['z'][:,:,0,0].data

        time=NCin.variables['time'][:].data

        refstr = NCin.variables['time'].units.split()[2]
        ref = datetime.datetime.strptime(refstr,'%Y-%m-%d')


        date_list = []

        for myt in time:
            step = datetime.timedelta(seconds=myt)
            date_list.append(ref + step)


        nT=len(date_list)
        nZ=depth.shape[1]

        AllVars = NCin.variables.keys()

        if aggvar==False:
            if var in AllVars:
                var2plot = NCin.variables[var][:,:,0,0].data
            else:
                raise ValueError('%s variable not in %s' %(var,infile))

        else:
            LISTvars = []
            varGroup = var.split('_')[0]
            lenGroup = len(varGroup)
            varElementList = var.split('_')[1:]
            varElement = ('_').join(varElementList)
            lenElement = len(varElement)
            for vv in AllVars:
                if varGroup in vv[:lenGroup]:
                    vvElementList = vv.split('_')[1:]
                    vvElement = ('_').join(vvElementList)
                    if len(vvElement)==lenElement:
                        if varElement in vv[-lenElement:]:
                            print(vv)
                            LISTvars.append(vv)

            var2plot = np.zeros((nT,nZ))

            if len(LISTvars)<1:
                raise ValueError('Variables for aggregation not found in %s for %s' %(infile,var))
            for vg in LISTvars:
                var2plot = var2plot + NCin.variables[vg][:,:,0,0].data
       
#LISTvarn = ['B1_n','P1_n','P2_n','P3_n','P4_n',
#            'Z4_n','Z5_n','Z3_n','Z6_n',
#            'N3_n','N4_n',
#            'R1_n','R6_n',
#           ]
#var2plot = np.zeros((nT,nZ))
#for vv in LISTvarn:
#    var2plot = var2plot + NCin.variables[vv][:,:,0,0].data


        if doline==True:
            var2plot_lines = {}
            LISTvarlines = []
            varGroupL = varline.split('_')[0]
            lenGroupL = len(varGroupL)
            varElementListL = varline.split('_')[1:]
            varElementL = ('_').join(varElementListL)
            lenElementL = len(varElementL)
            for vv in AllVars:
                if varGroupL in vv[:lenGroupL]:
                    vvElementListL = vv.split('_')[1:]
                    vvElementL = ('_').join(vvElementListL)
                    if len(vvElementL)==lenElementL:
                        if varElementL in vv[-lenElementL:]:
                            LISTvarlines.append(vv)

            if len(LISTvarlines)<1:
                raise ValueError('Variables for line not found in %s for %s' %(infile,varline))
            for vg in LISTvarlines:
                print ('Plotting contour for %s' %(vg,))
                var2plot_lines[vg] = NCin.variables[vg][:,:,0,0].data


        NCin.close()



#(time, z, lat, lon)
#CHL=NCin.variables['P1_Chl'][:,:,0,0].filled()+NCin.variables['P2_Chl'][:,:,0,0].filled()+NCin.variables['P3_Chl'][:,:,0,0].filled()+NCin.variables['P4_Chl'][:,:,0,0].filled()

#plt.close('all')

#fig,axs = plt.subplots(1,figsize=(9, 6))#,gridspec_kw = {'wspace':1.5, 'hspace':1.5})
#fig,axs = plt.subplots(1, gridspec_kw = {'wspace':0.5, 'hspace':0.35})
        axs = avaxs[iix]
        plt.sca(axs)
        var2plotT = np.transpose(var2plot)
        var_mean += var2plotT
        var_mean_2 += var2plotT**2
        x,y = np.meshgrid(pltdates.date2num(date_list),depth[0,:])
        if (varmin==None) & (varmax==None):
            cax=axs.pcolormesh(x,y,var2plotT,shading='auto')
        else:
            if varmin==None:
               cax=axs.pcolormesh(x,y,var2plotT,vmax=varmax,shading='auto')
            elif varmax==None:
               cax=axs.pcolormesh(x,y,var2plotT,vmin=varmin,shading='auto')
            else:
               cax=axs.pcolormesh(x,y,var2plotT,vmin=varmin,vmax=varmax,shading='auto')

        if doline:
            for vv in LISTvarlines:
                var2plot_linesT = np.transpose(var2plot_lines[vv])
                caxl = axs.contour(x,y,var2plot_linesT,[float(linevalue)],colors='w')

        axs.xaxis_date()
#cax=axs.pcolor(x,y,CHLT,norm=LogNorm(vmin=0.1, vmax=CHLT.max()))
#tpos=range(0,nT,30)
#axs.set_xticks(tpos)
#tick_labels=[]
#for i in tpos:
#   tick_labels.append(date_list[i].strftime("%Y %m"))
#axs.set_xticklabels(tick_labels,rotation=90)

        axs.set_ylim([-deplim,0])
        #axs.set_xlim([x[0,0],x[0,365]])
        if iix==Naxs-1:
            axs.set_xlabel('Time')
        if iix==int(Naxs/2):
            axs.set_ylabel('Depth [m]')
        #cbar = fig.colorbar(cax)
        plt.colorbar(cax)

        iiens = iix+ind_start
        if doline:
            plt.title('%s - line is %s at %s - %s' %(var,varline,linevalue,iiens),fontsize=8)
        else:
            plt.title('%s - %s ' %(var,iiens),fontsize=8)
    fig.autofmt_xdate()
    plt.tight_layout()

#fileout='prova.png'
    if doline:
        nomefile = 'Hov_' + var + '_' + varline + args.depth + np.str(iif) + '.png'
    else:
        nomefile = 'Hov_' + var + args.depth + np.str(iif) + '.png'
    fileout = OUTDIR + '/' + nomefile
    fig.savefig(fileout, format='png',dpi=150, bbox_inches="tight")


var_mean = var_mean/Nresults
var_mean_2 = var_mean_2/Nresults

var_std = (var_mean_2-var_mean**2)**.5

fig,axss = plt.subplots(3,1,sharex=True,sharey=True,figsize=[8,9])
plt.sca(axss[0])
axs = axss[0]
if (varmin==None) & (varmax==None):
    plt.pcolormesh(x,y,var_mean,shading='auto')
else:
    if varmin==None:
        cax=axs.pcolormesh(x,y,var_mean,vmax=varmax,shading='auto')
    elif varmax==None:
        cax=axs.pcolormesh(x,y,var_mean,vmin=varmin,shading='auto')
    else:
        cax=axs.pcolormesh(x,y,var_mean,vmin=varmin,vmax=varmax,shading='auto')

axs.xaxis_date()
axs.set_ylim([-deplim,0])
plt.title('%s - mean ' %(var))
plt.colorbar(cax)


plt.sca(axss[1])
axs = axss[1]
cax=plt.pcolormesh(x,y,var_std,shading='auto')

axs.xaxis_date()
axs.set_ylim([-deplim,0])
axs.set_ylabel('Depth [m]')
plt.title('%s - std ' %(var))
plt.colorbar(cax)


plt.sca(axss[2])
axs = axss[2]
cax=plt.pcolormesh(x,y,var_std/var_mean,shading='auto')

axs.xaxis_date()
axs.set_ylim([-deplim,0])
axs.set_xlabel('Time')
plt.title('%s - CV ' %(var))
plt.colorbar(cax)

fig.autofmt_xdate()
plt.tight_layout()

nomefile = 'Hov_' + var + args.depth + '.mean.png'
fileout = OUTDIR + '/' + nomefile
fig.savefig(fileout, format='png',dpi=150)#, bbox_inches="tight")


plt.show(block=False)
