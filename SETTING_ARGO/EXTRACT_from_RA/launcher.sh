#! /bin/bash


WORKING_DIR=$1
DATE=$2
INREA=/g100_work/OGS_devC/V9C/RUNS_SETUP/PREPROC/IC/RST_2019_R3c/
MASKFILE=/g100_work/OGS_devC/V10C/RUNS_SETUP/run3.1/wrkdir/MODEL/meshmask.nc
FILEZ=${WORKING_DIR}/grid.dat

LON=12.36 # eliminare
LAT=39.36 # eliminare
DEPTH=3485.2 #<-- Check Guido

OUTDIR=${WORKING_DIR}/ICfromREA/
mkdir -p $OUTDIR

python extract_ICfromREA_for_gotm.py -i $INREA -n $LON -t $LAT -o $OUTDIR -d $DATE -m $MASKFILE -z $FILEZ -p $DEPTH
