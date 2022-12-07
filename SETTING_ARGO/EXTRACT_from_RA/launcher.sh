#! /bin/bash


DATE=20190101
INREA=/g100_scratch/userexternal/ateruzzi/EAT_DA/SETTING_ARGO/EXTRACT_from_RA/RA_24/RESTARTS/$DATE/
MASKFILE=RA_24/meshmask.nc
FILEZ=/g100/home/userexternal/ateruzzi/seamless-notebooks/setups/float_east/grid.dat

LON=12.36
LAT=39.36
DEPTH=3485.2

OUTDIR=OUTPROF/P${LON}_${LAT}_${DATE}/
mkdir -p $OUTDIR

echo python extract_ICfromREA_for_gotm.py -i $INREA -n $LON -t $LAT -o $OUTDIR -d $DATE -m $MASKFILE -z $FILEZ -p $DEPTH
