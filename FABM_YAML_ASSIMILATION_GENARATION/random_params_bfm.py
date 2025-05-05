import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    to prepare fabm .yaml with random numbers on selected parameters
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(   '--template',"-t",
                                type = str,
                                required = True,
                                help = 'path and name of the template yaml file')
    parser.add_argument(   '--outdir','-o',
                                type = str,
                                required = True,
                                help = '/some/path')
    parser.add_argument(   '--nens','-n',
                                type = str,
                                required = True,
                                help = 'numer of gotm .yaml files to be prepared')
    parser.add_argument(   '--param','-p',
                                type = str,
                                required = True,
                                help = 'parameter to be assimilated')
 
    return parser.parse_args()

args = argument()

import sys
import numpy as np
#from setting_parameters import parametersDICT
from bitsea.commons.utils import addsep
from bitsea.commons.utils import file2stringlist
from random import random, seed


Nfabms = int(args.nens)
OUTDIR = addsep(args.outdir)
fabm_template = args.template
ORIG = file2stringlist(fabm_template)

perturb_param=args.param


def dump_template(ORIG,outfile,DICTsettings):
    LISTparameters = list(DICTsettings.keys())
    LINES=[]
    for line in ORIG:
        newline=line
        for pp in LISTparameters:
            str_subst = "@@" + pp + "@@"
            str_value = '{0:.5g}'.format(DICTsettings[pp])
            if (line.find(str_subst) != -1):  newline=line.replace(str_subst,str_value)
        LINES.append(newline + "\n")
    fid=open(outfile,"w")
    fid.writelines(LINES)
    fid.close()
    

range0 = 0.
range1 = 0.2
list_params=['instances_light_parameters_EPS0r',      #  100.   Background shortwave attenuation                            [1/m]                [21]
             'instances_Z5_parameters_p_pu',          #   67.   Assimilation efficiency, microzooplankton                   [-]                  [13]
             'instances_light_parameters_pEIR_eow',   #   54.   Photosynthetically active fraction of shortwave radiation   [-]                  [6]
             'instances_P1_parameters_p_sum',         #         maximum specific productivity at reference temperature (1/d)
             'instances_Z5_parameters_p_sum',         #   47.   Potential growth rate, microzooplankton                     [1/d]                [13]
             'instances_P1_parameters_p_qlcPPY',      #   42.   Reference Chla:C quotum, diatoms                            [mgChla/mgC]         [1]
             'instances_P1_parameters_p_qup',         #   41.   Membrane affinity for P, diatoms                            [m3/mgC/d]           [4]
             'instances_Z5_parameters_p_pu_ea',       #   36.   Fraction of activity excretion, microzooplankton            [-]                  [14]
             'instances_P1_parameters_p_alpha_chl',   #   35.   Initial slope of the P-E curve, diatoms                     [mgC s m2/mgChl/uE]  [1]
             'instances_P1_parameters_p_qplc',        #   33.   Minimum phosphorus to carbon ratio, diatoms                 [mmol P/mg C]        [4]
             'instances_P1_parameters_p_srs']         #   33.   Respiration rate at 10 degrees C, diatoms                   [1/d]                [2]
#list_param=['light.EPS0r', 'Z5.p_pu', 'light.pEIR_eow', 'Z5.p_sum', 'P1.p_qlcPPY', 'P1.p_qup', 'Z5.p_pu_ea', 'P1.p_alpha_chl', 'P1.p_qplc', 'P1.p_srs' ]

list_nominal=[0.04,      #  100.   Background shortwave attenuation                            [1/m]                [21]
              0.5,       #   67.   Assimilation efficiency, microzooplankton                   [-]                  [13]
              0.4,       #   54.   Photosynthetically active fraction of shortwave radiation   [-]                  [6]
              2.5,       #   maximum specific productivity at reference temperature (1/d)
              2.71,      #   47.   Potential growth rate, microzooplankton                     [1/d]                [13]
              0.026,     #   42.   Reference Chla:C quotum, diatoms                            [mgChla/mgC]         [1]
              0.0025,    #   41.   Membrane affinity for P, diatoms                            [m3/mgC/d]           [4]
              0.5,       #   36.   Fraction of activity excretion, microzooplankton            [-]                  [14]
              0.0000261, #   35.   Initial slope of the P-E curve, diatoms                     [mgC s m2/mgChl/uE]  [1]
              0.00057,   #   33.   Minimum phosphorus to carbon ratio, diatoms                 [mmol P/mg C]        [4]
              0.076]     #   33.   Respiration rate at 10 degrees C, diatoms                   [1/d]                [2]
 

list_range=[ range1, range1, range1, range1, range1, range1, range1, range1, range1, range1, range1]

N_params= len(list_params)

list_range=[]
ipert = -1
for i,param in enumerate(list_params):
    if param  == perturb_param:
        list_range.append([list_nominal[i],range1])
        print('perturbed: ' + param)
        ipert = i
    else:
        list_range.append([list_nominal[i],range0])


if ipert == -1:
    print('error on perturbed: ' + perturb_param)
    sys.exit()

keys=list_params
values=list_range

parametersDICT=dict(zip(keys, values))

for pp in parametersDICT.keys():
    print(pp)

seed(1)

for nn in range(Nfabms):
    outfile = OUTDIR + '/fabm_{:04d}.yaml'.format(nn+1)
    print(nn)
    DICTsettings = {}
    for ii,pname in enumerate(parametersDICT.keys()):
        nominalvalue = parametersDICT[pname][0]
        deltav = parametersDICT[pname][1]*0.5
#       value = ((random()*2-1)*p+1) * centralvalue
#       valuenp = ((np.random.uniform(0,1)*2-1)*p+1) * centralvalue
        valuenp = np.random.uniform(low=nominalvalue-deltav, high=nominalvalue+deltav)
        if ii==ipert:
            print(pname)
            print(nominalvalue)
            print(valuenp)
        DICTsettings[pname] = valuenp
    dump_template(ORIG,outfile,DICTsettings)
