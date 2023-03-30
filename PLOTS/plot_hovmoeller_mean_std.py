import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    Produce Hovmoeller plot of a variable or
    an aggregate variable
    from results of FABM-GOTM 1D
    ''',
#    (adding a line of a constant variable)
    formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(   '--varname', '-v',
                                type = str,
                                required = False,
                                help = 'Variable to be plotted in the Hovmoeller')

    parser.add_argument(   '--varagg', '-g',
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

#    parser.add_argument(   '--varline', '-l',
#                                type = str,
#                                required = False,
#                                help = 'variable to plot a line')

#    parser.add_argument(   '--linevalue', '-k',
#                                type = str,
#                                required = False,
#                                help = 'constant value for the line')

    parser.add_argument(   '--depth', '-d',
                                type = str,
                                required = False,
                                default = '300',
                                help = 'depth limit')

    parser.add_argument(   '--varmin', '-vl',
                                type = str,
                                required = False,
                                default = None,
                                help = 'var limit')

    parser.add_argument(   '--varmax', '-vm',
                                type = str,
                                required = False,
                                default = None,
                                help = 'var limit')

    return parser.parse_args()


args = argument()



# import os,sys
import netCDF4 as NC4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as pltdates
import datetime
import glob
import os
from matplotlib.colors import LogNorm
from datetime import timedelta
from commons.utils import addsep
from commons.Timelist import TimeList


#ref = datetime.datetime(2016, 1, 1, 0, 0, 0)

OUTDIR = addsep(args.outdir)
INDIR = addsep(args.indir)

# infile=args.infile
if (not (args.varname is None)) & (not (args.varagg is None)):
    raise ValueError("Both aggregate and normal variable cannot be assigned: choose one")
var = None
aggvar = False
if not (args.varname is None):
    var = args.varname
if not (args.varagg is None):
    var = args.varagg
    aggvar = True


if var is None:
    raise ValueError("Assign one variable (or simple -v or aggragate -g)")


doline = False
#if (not (args.varline is None)) & (not (args.linevalue is None)):
#    varline = args.varline
#    linevalue = args.linevalue
#    doline = True
#if (not (args.varline is None)) & (args.linevalue is None):
#    raise ValueError('value to plot line not assigned ')

deplim = float(args.depth)
varmin = args.varmin
if not(varmin==None):
   varmin = float(args.varmin)
varmax = args.varmax
if not(varmax==None):
   varmax = float(args.varmax)


LISTresults = [os.path.basename(ll) for ll in glob.glob(INDIR + '/result_*.nc')]
Nresults = len(LISTresults)

#Naxs = 6
#Nfigs = int(np.ceil(Nresults/Naxs))

plt.close('all')

infile1 = LISTresults[0]
NC1 = NC4.Dataset(INDIR + infile1,'r')
depth1 = NC1.variables['z'][:,:,0,0].data
nZ1 = depth1.shape[1]
time1=NC1.variables['time'][:].data
nT1 = time1.shape[0]
var_mean = np.zeros((nZ1,nT1))
var_mean_2 = np.zeros((nZ1,nT1))


#for iif in range(Nfigs):
#    print(iif)
#    fig,avaxs = plt.subplots(Naxs,1,sharex=True,sharey=True,figsize=[8,9])

#    ind_start = Naxs*iif
#    ind_end = Naxs*(iif+1)
#    if ind_end>Nresults:
#        ind_end = Nresults

#    for iix,infile in enumerate(LISTresults[ind_start:ind_end]):
for iix,infile in enumerate(LISTresults):
    #print(infile)
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
    if ((not(nT==nT1)) | (not(nZ==nZ1))):
        print('ignoring this result...')
        continue

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
       

#    if doline==True:
#        var2plot_lines = {}
#        LISTvarlines = []
#        varGroupL = varline.split('_')[0]
#        lenGroupL = len(varGroupL)
#        varElementListL = varline.split('_')[1:]
#        varElementL = ('_').join(varElementListL)
#        lenElementL = len(varElementL)
#        for vv in AllVars:
#            if varGroupL in vv[:lenGroupL]:
#                vvElementListL = vv.split('_')[1:]
#                vvElementL = ('_').join(vvElementListL)
#                if len(vvElementL)==lenElementL:
#                    if varElementL in vv[-lenElementL:]:
#                        LISTvarlines.append(vv)

#        if len(LISTvarlines)<1:
#            raise ValueError('Variables for line not found in %s for %s' %(infile,varline))
#        for vg in LISTvarlines:
#            print ('Plotting contour for %s' %(vg,))
#            var2plot_lines[vg] = NCin.variables[vg][:,:,0,0].data


    NCin.close()



        #axs = avaxs[iix]
        #plt.sca(axs)
    var2plotT = np.transpose(var2plot)
    var_mean += var2plotT
    var_mean_2 += var2plotT**2
    x,y = np.meshgrid(pltdates.date2num(date_list),depth[0,:])
        #if (varmin==None) & (varmax==None):
        #    cax=axs.pcolormesh(x,y,var2plotT,shading='auto')
        #else:
        #    if varmin==None:
        #       cax=axs.pcolormesh(x,y,var2plotT,vmax=varmax,shading='auto')
        #    elif varmax==None:
        #       cax=axs.pcolormesh(x,y,var2plotT,vmin=varmin,shading='auto')
        #    else:
        #       cax=axs.pcolormesh(x,y,var2plotT,vmin=varmin,vmax=varmax,shading='auto')

        #if doline:
        #    for vv in LISTvarlines:
        #        var2plot_linesT = np.transpose(var2plot_lines[vv])
        #        caxl = axs.contour(x,y,var2plot_linesT,[float(linevalue)],colors='w')

        #axs.xaxis_date()

        #axs.set_ylim([-deplim,0])
        #axs.set_xlim([x[0,0],x[0,365]])
        #if iix==Naxs-1:
        #    axs.set_xlabel('Time')
        #if iix==int(Naxs/2):
        #    axs.set_ylabel('Depth [m]')
        #cbar = fig.colorbar(cax)
        #plt.colorbar(cax)

        #iiens = iix+ind_start
        #if doline:
        #    plt.title('%s - line is %s at %s - %s' %(var,varline,linevalue,iiens),fontsize=8)
        #else:
        #    plt.title('%s - %s ' %(var,iiens),fontsize=8)
    #fig.autofmt_xdate()
    #plt.tight_layout()

#fileout='prova.png'
    #if doline:
    #    nomefile = 'Hov_' + var + '_' + varline + args.depth + np.str(iif) + '.png'
    #else:
    #    nomefile = 'Hov_' + var + args.depth + np.str(iif) + '.png'
    #fileout = OUTDIR + '/' + nomefile
    #fig.savefig(fileout, format='png',dpi=150, bbox_inches="tight")


var_mean = var_mean/Nresults
var_mean_2 = var_mean_2/Nresults

var_std = (var_mean_2-var_mean**2)**.5

fig,axss = plt.subplots(3,1,sharex=True,sharey=True,figsize=[8,7])
plt.sca(axss[0])
axs = axss[0]
if (varmin==None) & (varmax==None):
    plt.pcolormesh(x,y,var_mean,shading='auto')
else:
    if varmin==None:
        plt.pcolormesh(x,y,var_mean,vmax=varmax,shading='auto')
    elif varmax==None:
        plt.pcolormesh(x,y,var_mean,vmin=varmin,shading='auto')
    else:
        print('here')
        plt.pcolormesh(x,y,var_mean,vmin=varmin,vmax=varmax,shading='auto')

axs.xaxis_date()
axs.set_ylim([-deplim,0])
plt.title('%s - mean ' %(var))
plt.colorbar()


plt.sca(axss[1])
axs = axss[1]
if varmax==None:
    cax=plt.pcolormesh(x,y,var_std,shading='auto')
else:
    cax=plt.pcolormesh(x,y,var_std,vmin=0.,vmax=varmax/3.,shading='auto')

axs.xaxis_date()
axs.set_ylim([-deplim,0])
axs.set_ylabel('Depth [m]')
plt.title('%s - std ' %(var))
plt.colorbar()


plt.sca(axss[2])
axs = axss[2]
cax=plt.pcolormesh(x,y,var_std/var_mean,vmin=0.,vmax=2.5,shading='auto')

axs.xaxis_date()
axs.set_ylim([-deplim,0])
axs.set_xlabel('Time')
plt.title('%s - CV ' %(var))
plt.colorbar()

fig.autofmt_xdate()
plt.tight_layout()

nomefile = 'Hov_' + var + args.depth + '.mean.png'
fileout = OUTDIR + '/' + nomefile
fig.savefig(fileout, format='png',dpi=150)#, bbox_inches="tight")


#plt.show(block=False)
