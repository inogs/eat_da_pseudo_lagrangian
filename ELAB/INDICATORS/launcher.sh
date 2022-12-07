#! /bin/bash

DIRNAME=float_east
DIRNAME=float_west
SETUP=ESTKF_n50_T_S_Nut
SETUP=ESTKF_n50_T_S
SETUP=ENS_n50_floatsal_p20
SETUP=ESTKF_n50_T_S_Nplugin

INDIR=/g100_scratch/userexternal/ateruzzi/EAT_DA/WP4_tests/$DIRNAME/$SETUP/

OUTBASE=WP4_tests/
OUTDIR=$OUTBASE/$DIRNAME/$SETUP/
mkdir -p $OUTDIR

echo python ppn.py -i $INDIR -o $OUTDIR

echo ..............

echo python R6c.py -i $INDIR -o $OUTDIR

echo ..............

echo python P_c.py -i $INDIR -o $OUTDIR
