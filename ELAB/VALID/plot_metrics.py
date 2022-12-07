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

FTYPE = 'float_west'
INDIR = '/g100_scratch/userexternal/ateruzzi/EAT_DA/ELAB/VALID/WP4_tests/' + FTYPE + '/'



VARlist = [
    'dcm',
    'ncl',
]

OUTDIR = 'FIGURES/WP4_tests/' + FTYPE + '/No_TS_Nut/'
OUTDIR = 'FIGURES/WP4_tests/' + FTYPE + '/AllRUNS/'


for var in VARlist:
    print('--------------')
    print(var)
    mod = {}
    datelist = {}
    for run in LISTruns:
        print(run)
        INDATA = INDIR + '/' + run
        mod[run] = np.load(INDATA + '/' + var + '.npy')[:,0]
        obs = np.load(INDATA + '/' + var + '.npy')[:,1]
        if 'dcm' in var:
            datelist[run] = np.load(INDATA + '/dates_metrics_chl.npy',allow_pickle=True) 
        if 'ncl' in var:
            datelist[run] = np.load(INDATA + '/dates_metrics_nit.npy',allow_pickle=True) 

    plt.figure(figsize=[8,4])
    for irun,run in enumerate(LISTruns):
        plt.plot(datelist[run],mod[run][:],
                 label=DICTrunnames[run],
                 color=DICTruncol[run])
    plt.plot(datelist[run],obs[:],'o',
             label='float',
             color='k')
    plt.grid()
    plt.legend()
    plt.title(var)
    #plt.gcf().autofmt_xdate()
    plt.savefig(OUTDIR + '/modfloat_' + var + '.png')


