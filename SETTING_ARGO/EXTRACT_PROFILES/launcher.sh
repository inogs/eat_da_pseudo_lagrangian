#!/bin/bash


VAR=PSAL
VAR=TEMP
VAR=NITRATE
VAR=CHLA
DEPTH=300

FLOAT=6902903 #west
FLOAT=6901772 #east

START=20190101
END=20200101

OUTDIR=$PWD/PROFILES_ERRadd_mul/P1.2_A0.02/${VAR}_${FLOAT}/
mkdir -p $OUTDIR


echo python extract_float_profiles_addmul.py -v $VAR -o $OUTDIR -f $FLOAT -s $START -e $END -d 200


OUTDIR=$PWD/HOVMOELLER/${VAR}_${FLOAT}/
mkdir -p $OUTDIR

echo python plot_hovmoeller.py -v $VAR -o $OUTDIR -f $FLOAT -s $START -e $END

