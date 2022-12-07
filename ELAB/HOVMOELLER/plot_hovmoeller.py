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

    parser.add_argument(   '--varagg', '-g',
                                type = str,
                                required = False,
                                help = 'Variable to be plotted in the Hovmoeller')

    parser.add_argument(   '--outdir', '-o',
                                type = str,
                                required = True,
                                default = '',
                                help = 'Output Images directory')
    
    parser.add_argument(   '--infile', '-i',
                                type = str,
                                required = True,
                                help = '.nc infile (typically result.nc)')

    parser.add_argument(   '--varline', '-l',
                                type = str,
                                required = False,
                                help = 'variable to plot a line')

    parser.add_argument(   '--linevalue', '-k',
                                type = str,
                                required = False,
                                help = 'constant value for the line')

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
from matplotlib.colors import LogNorm
import datetime
from datetime import timedelta


#ref = datetime.datetime(2016, 1, 1, 0, 0, 0)

OUTDIR = args.outdir

infile=args.infile
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
if (not (args.varline is None)) & (not (args.linevalue is None)):
    varline = args.varline
    linevalue = args.linevalue
    doline = True
if (not (args.varline is None)) & (args.linevalue is None):
    raise ValueError('value to plot line not assigned ')

deplim = float(args.depth)
varmin = args.varmin
if not(varmin==None):
   varmin = float(args.varmin)
varmax = args.varmax
if not(varmax==None):
   varmax = float(args.varmax)


NCin=NC4.Dataset(infile,"r")

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

plt.close('all')

fig,axs = plt.subplots(1,figsize=(9, 6))#,gridspec_kw = {'wspace':1.5, 'hspace':1.5})
#fig,axs = plt.subplots(1, gridspec_kw = {'wspace':0.5, 'hspace':0.35})
var2plotT = np.transpose(var2plot)
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
axs.set_xlabel('Time')
axs.set_ylabel('Depth [m]')
cbar = fig.colorbar(cax)

if doline:
    plt.title('%s - line is %s at %s' %(var,varline,linevalue))
else:
    plt.title(var)
fig.autofmt_xdate()

plt.show(block=False)
#fileout='prova.png'
if doline:
    nomefile = 'Hov_' + var + '_' + varline + args.depth +  '.png'
else:
    nomefile = 'Hov_' + var + args.depth + '.png'
fileout = OUTDIR + '/' + nomefile
fig.savefig(fileout, format='png',dpi=150, bbox_inches="tight")

