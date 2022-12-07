import numpy as np
import matplotlib.pyplot as plt
import datetime


LISTruns = [
    'ENS_n50_floatsal_p20',
    'ESTKF_n50_T_S',
    'ESTKF_n50_T_S_Nut',
    'ESTKF_n50_T_S_Nplugin',
]

DICTrunnames = {
    'ENS_n50_floatsal_p20': 'ENS',
    'ESTKF_n50_T_S': 'EnKF_TS',
    'ESTKF_n50_T_S_Nplugin': 'EnKF_TS_VarNut',
    'ESTKF_n50_T_S_Nut': 'EnKF_TS_Nut',
}

DICTruncol= {
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


FTYPE = 'float_east'
FTYPE = 'float_west'
INDIR = '/g100_scratch/userexternal/ateruzzi/EAT_DA/ELAB/VALID/WP4_tests/' + FTYPE +'/'


VARlist = ['temp']
VARlist = ['N3_n','total_chlorophyll_calculator_result','temp','salt']

OUTDIR = 'FIGURES/WP4_tests/' + FTYPE + '/No_TS_Nut/'
OUTDIR = 'FIGURES/WP4_tests/' + FTYPE + '/AllRUNS/'

plt.close('all')

for var in VARlist:
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
            plt.plot(datelist[run],bias[run][:,ll],'s',
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
        for run in LISTruns:
            plt.plot(datelist[run],rmsd[run][:,ll],'s',
                     label=DICTrunnames[run],
                     color=DICTruncol[run])
        if 'N3' in var: plt.ylim(None,2)
        plt.ylabel(DICTvarunits[var])
        plt.grid()
        plt.legend()
        plt.title(DICTvarnames[var] + ' RMSD ' + levname)
    #    plt.gcf().autofmt_xdate()
        plt.savefig(OUTDIR + '/rmsd' + DICTvarnames[var] + levname + '.png')

#plt.show(block=False)





