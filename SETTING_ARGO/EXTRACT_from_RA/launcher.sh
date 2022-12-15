#! /bin/bash


WORKING_DIR=$1
DATE_START=$2
DATE__END=$3
INREA=/g100_work/OGS_devC/V9C/RUNS_SETUP/PREPROC/IC/RST_2019_R3c/
MASKFILE=/g100_work/OGS_devC/V10C/RUNS_SETUP/run3.1/wrkdir/MODEL/meshmask.nc
FILEZ=${WORKING_DIR}/grid.dat
float=$4
python read_lat_lon.py -fln ${float} -d_s $DATE_START -d_e $DATE__END
source lon.txt #get initial lon
source lat.txt #get initial lat
echo $LON
echo $LAT
#DEPTH=3485.2 #<-- Check Guido
DEPTH=10000.

OUTDIR=${WORKING_DIR}/ICfromREA/
mkdir -p $OUTDIR

python extract_ICfromREA_for_gotm.py -i $INREA -n $LON -t $LAT -o $OUTDIR -d $DATE_START -m $MASKFILE -z $FILEZ -p $DEPTH
