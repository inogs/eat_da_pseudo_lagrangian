#! /bin/bash


DIRNAME=float_east
SETUP=ENS_n50_fabmsall
SETUP=ENS_n50
SETUP=ENS_n50_fabms
SETUP=ENS_n50_nometeo_fabmsall

SETUP=ESTKF_n50_chl_float_fabmsall
SETUP=ESTKF_n50_chl_float_fabmsall_nometeo
SETUP=ESTKF_n50_chl_float_fabms

SETUP=ESTKF_n24_chlall_satw_fabms_nom1

WPDIR=WP5_tests

INDIR=/g100_scratch/userexternal/ateruzzi/EAT_DA/$WPDIR/$DIRNAME/$SETUP/

OUTBASE=$WPDIR/
OUTDIR=$OUTBASE/$DIRNAME/$SETUP/
mkdir -p $OUTDIR


VAR=N3_n # Naming should be as in result.nc
VAR=total_chlorophyll_calculator_result # Naming should be as in result.nc



echo python valid_float.py -i $INDIR -o $OUTDIR -v $VAR

echo ----------------------
echo python metrics_float.py -i $INDIR -o $OUTDIR
