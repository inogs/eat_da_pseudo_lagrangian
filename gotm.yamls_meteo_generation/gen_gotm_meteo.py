import argparse
def argument():
    parser = argparse.ArgumentParser(description = '''
    to prepare gotm .yaml with explicit fabm .yaml file names
    ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(   '--template',"-t",
                                type = str,
                                required = True,
                                help = 'path of the template yaml file')
    parser.add_argument(   '--outdir','-o',
                                type = str,
                                required = True,
                                help = '/some/path')
    parser.add_argument(   '--ngotm','-n',
                                type = str,
                                required = True,
                                help = 'numer of gotm .yaml files to be prepared')
    parser.add_argument(   '--prange','-p',
                                type = str,
                                required = True,
                                help = 'numer of gotm .yaml files to be prepared')
    return parser.parse_args()

args = argument()

from commons.utils import file2stringlist
from commons.utils import addsep
import numpy as np

def dump_template(ORIG, outfile, scalef):
    LINES=[]
    str_scalef = '{:4.4}'.format(scalef)
    for line in ORIG:
        newline=line
        if (line.find("@@scalef@@") != -1):  newline=line.replace("@@scalef@@",str_scalef)
        LINES.append(newline + "\n")
    fid=open(outfile,"w")
    fid.writelines(LINES)
    fid.close()

ngotm = int(args.ngotm)
OUTDIR = addsep(args.outdir)
gotm_template = args.template
ORIG = file2stringlist(gotm_template)
prange = float(args.prange)


SCALEFACTORS = np.random.rand(ngotm)/(50/prange)+(1-prange/100.)


for ii in range(1,ngotm+1):
    outfile = OUTDIR + 'gotm_{:04d}.yaml'.format(ii)
    scalef = SCALEFACTORS[ii-1]
    print(outfile)
    print(scalef)
    dump_template(ORIG,outfile,scalef)
