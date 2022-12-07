import numpy as np
import matplotlib.pyplot as plt
import datetime

from commons.utils import writetable
from commons.Timelist import TimeList
from commons import timerequestors as requestors
from commons import season

seasonobj = season.season()

LISTruns = [
#    'ENS_n50',
#    'ENS_n50_fabms',
#    'ENS_n50_fabmsall',
    'ENS_n50_nometeo_fabmsall',
    'ESTKF_n50_chl_float_fabmsall_nometeo',
    'ESTKF_n50_chl_float_fabmsall',
    'ESTKF_n50_chl_float_fabms',
#    'ENS_n50_floatsal_p20',
#    'ESTKF_n50_T_S',
#    'ESTKF_n50_T_S_Nut',
#    'ESTKF_n50_T_S_Nplugin',
]

DICTrunnames = {
    'ENS_n50': 'ENS',
    'ENS_n50_fabms': 'ENS_fabms',
    'ENS_n50_fabmsall': 'ENS_fabms_all',
    'ENS_n50_nometeo_fabmsall': 'ENS_fabms_nometeo_fabmsall',

    'ESTKF_n50_chl_float_fabmsall_nometeo': 'ESTKF_nometeo',
    'ESTKF_n50_chl_float_fabmsall': 'ESTKF_fabmsall',
    'ESTKF_n50_chl_float_fabms': 'ESTKF_fabms',

    'ENS_n50_floatsal_p20': 'ENS',
    'ESTKF_n50_T_S': 'EnKF_TS',
    'ESTKF_n50_T_S_Nplugin': 'EnKF_TS_VarNut',
    'ESTKF_n50_T_S_Nut': 'EnKF_TS_Nut',
}

DICTruncol= {
    'ENS_n50': 'black',
    'ENS_n50_fabms': 'blue',
    'ENS_n50_fabmsall': 'grey',
    'ENS_n50_nometeo_fabmsall': 'red',

    'ESTKF_n50_chl_float_fabmsall_nometeo': 'orange',
    'ESTKF_n50_chl_float_fabmsall': 'black',
    'ESTKF_n50_chl_float_fabms': 'cyan',

    'ENS_n50_floatsal_p20': 'grey',
    'ESTKF_n50_T_S': 'orange',
    'ESTKF_n50_T_S_Nut': 'red',
    'ESTKF_n50_T_S_Nplugin': 'green',
}

DICTvarnames = {
    'N3_n': 'Nitrate',
    'temp': 'Temperature',
    'salt': 'Salinity',
    'total_chlorophyll_calculator_result': 'Chlorophyll',
}

DICTvarunits = {
    'N3_n': '$[mmol/m^3]$',
    'temp': '[°C]',
    'salt': '[psu]',
    'total_chlorophyll_calculator_result': '$[mg/m^3]$',
}


LISTlevs = [
    '0-50 m',
    '50-100 m',
    '100-200 m',
    '200-400 m',
    '>400 m',
]


FTYPE = 'float_west'
FTYPE = 'float_east'
INDIR = '/g100_scratch/userexternal/ateruzzi/EAT_DA/ELAB/VALID/WP5_tests/' + FTYPE +'/'


VARlist = ['temp']
VARlist = ['N3_n','total_chlorophyll_calculator_result','temp','salt']
VARlist = ['N3_n','total_chlorophyll_calculator_result']

OUTDIR = 'FIGURES/WP5_tests/' + FTYPE + '/ESTKF_gen_runs_LINE/'


for var in VARlist:
    plt.close('all')
    print('--------------')
    print(var)
    bias = {}
    rmsd = {}
    datelist = {}
    for run in LISTruns:
        print(run)
        INVALID = INDIR + '/' + run
        bias[run] = np.load(INVALID + '/bias_levs_' + var + '.npy')
        rmsd[run] = np.load(INVALID + '/RMSD_levs_' + var + '.npy')
        datelist_str = np.load(INVALID + '/dateobs_' + var + '.npy')
        datelist[run] = []
        for dd in datelist_str:
            datelist[run].append(datetime.datetime.strptime(dd,'%Y-%m-%d'))



#    Ndates = len(datelist[run])
#    width = 0.85/len(LISTruns)
#    xval = np.arange(Ndates)

    for ll,levname in enumerate(LISTlevs):
        print(levname)
        plt.figure(figsize=[8,4])
        for irun,run in enumerate(LISTruns):
#            plt.bar(xval+width*((1-len(LISTruns))/2.+irun),
#                     bias[run][:,ll],width,
            plt.plot(datelist[run],bias[run][:,ll],'-',
                     label=DICTrunnames[run],
                     color=DICTruncol[run])
#        plt.gca().set_xticks(xval[0::30],datelist_str[0::30])
        plt.ylabel(DICTvarunits[var])
        plt.grid()
        plt.legend()
        plt.title(DICTvarnames[var] + ' bias ' + levname)
        #plt.gcf().autofmt_xdate()
        plt.savefig(OUTDIR + '/bias' + DICTvarnames[var] + levname + '.png')

        plt.figure(figsize=[8,4])
        matrixRMSD = np.zeros((4,len(LISTruns)))
        for irun,run in enumerate(LISTruns):
            plt.plot(datelist[run],rmsd[run][:,ll],'-',
                     label=DICTrunnames[run],
                     color=DICTruncol[run])
            TL = TimeList(datelist[run])
            for iSeas in range(4):
                m = requestors.Clim_season(iSeas,seasonobj)
                indseas,_ = TL.select(m)
                meanseas = 0
                for iis in indseas:
                    meanseas = meanseas + rmsd[run][iis,ll]/len(indseas)
                matrixRMSD[iSeas,irun] = meanseas
        if 'N3' in var: plt.ylim(None,2)
        plt.ylabel(DICTvarunits[var])
        plt.grid()
        plt.legend()
        plt.title(DICTvarnames[var] + ' RMSD ' + levname)
    #    plt.gcf().autofmt_xdate()
        plt.savefig(OUTDIR + '/rmsd' + DICTvarnames[var] + levname + '.png')

        writetable(OUTDIR + '/rmsd' + DICTvarnames[var] + levname + '.txt', 
                   matrixRMSD,['win','spr','sum','aut'],LISTruns)

#plt.show(block=False)





