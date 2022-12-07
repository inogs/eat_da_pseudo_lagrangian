#!/bin/bash


VAR=TEMP
VAR=PSAL

FLOAT=6901772 #east
FLOAT=6902903 #west

START=20181220
END=20200120

OUTDIR=$PWD/NUDG_PROFILES/${VAR}_${FLOAT}/
mkdir -p $OUTDIR


echo python extract_float_forgotm.py -v $VAR -o $OUTDIR -f $FLOAT -s $START -e $END
