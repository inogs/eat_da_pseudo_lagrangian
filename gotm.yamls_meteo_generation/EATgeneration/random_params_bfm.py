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
 
    return parser.parse_args()

args = argument()

import numpy as np
from setting_parameters import parametersDICT
from commons.utils import addsep
from commons.utils import file2stringlist
from random import random, seed


Nfabms = int(args.nens)
OUTDIR = addsep(args.outdir)
fabm_template = args.template
ORIG = file2stringlist(fabm_template)


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
    

for pp in parametersDICT.keys():
    print(pp)

seed(1)
for nn in range(Nfabms):
    outfile = OUTDIR + '/fabm_{:04d}.yaml'.format(nn+1)
    print(nn)
    DICTsettings = {}
    for ii,pname in enumerate(parametersDICT.keys()):
        centralvalue = parametersDICT[pname][0]
        p = parametersDICT[pname][1]
        value = ((random()*2-1)*p+1) * centralvalue
        if ii==0:
            print(pname)
            print(value)
        DICTsettings[pname] = value
    dump_template(ORIG,outfile,DICTsettings)
