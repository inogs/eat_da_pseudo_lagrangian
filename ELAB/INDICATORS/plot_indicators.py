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
FTYPE = 'float_east'
INDIR = '/g100_scratch/userexternal/ateruzzi/EAT_DA/ELAB/INDICATORS/WP4_tests/' + FTYPE + '/'



VARlist = [
    'P_c_large200',
    'POCexp',
    'Z_c200',
    'P_c200',
    'P_c_small200',
    'ppn200',
]

DICTunits = {
    'P_c_large200': '$[mgC/m^2]$',
    'POCexp': '$[mgC/m^2/s]$',
    'Z_c200': '$[mgC/m^2]$',
    'P_c200': '$[mgC/m^2]$',
    'P_c_small200': '$[mgC/m^2]$',
    'ppn200': '$[gC/m^2/y]$',
}

OUTDIR = 'FIGURES/WP4_tests/' + FTYPE + '/No_TS_Nut/'
OUTDIR = 'FIGURES/WP4_tests/' + FTYPE + '/AllRUNS/'


for var in VARlist:
    print('--------------')
    print(var)
    mean = {}
    std = {}
    datelist = {}
    for run in LISTruns:
        print(run)
        INDATA = INDIR + '/' + run
        mean[run] = np.load(INDATA + '/' + var + '.npy')[0]
        std[run] = np.load(INDATA + '/' + var + '.npy')[1]
        datelist[run] = np.load(INDATA + '/dates.npy',allow_pickle=True) 

    plt.figure(figsize=[8,4])
    for irun,run in enumerate(LISTruns):
        plt.plot(datelist[run],mean[run][:],
                 label=DICTrunnames[run],
                 color=DICTruncol[run])
    plt.ylabel(DICTunits[var])
    plt.grid()
    plt.legend()
    plt.title(var + ' mean')
    #plt.gcf().autofmt_xdate()
    plt.savefig(OUTDIR + '/mean_' + var + '.png')

    plt.figure(figsize=[8,4])
    for irun,run in enumerate(LISTruns):
        plt.plot(datelist[run],std[run][:],
                 label=DICTrunnames[run],
                 color=DICTruncol[run])
    plt.ylabel(DICTunits[var])
    plt.grid()
    plt.legend()
    plt.title(var + ' std')
    #plt.gcf().autofmt_xdate()
    plt.savefig(OUTDIR + '/std_' + var + '.png')

