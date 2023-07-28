DIR_INSAT_DAILY=/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/ONLINE_V9C/SAT/CHL/MULTISENSOR/1Km/NRT/DAILY/CHECKED_24/
DIR_INSAT_WEEKLY=/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/ONLINE_V9C/SAT/CHL/MULTISENSOR/1Km/NRT/WEEKLY_1_24/
MASKFILE=/g100_scratch/userexternal/ateruzzi/MASKS_V8/meshmask.nc
DIRVARSAT=VAR_SAT

ln -fs $DIR_INSAT_DAILY SAT_hT
ln -fs $DIR_INSAT_WEEKLY SAT_lT

#LON=20.75233
#LAT=35.62733
floatname=$1
#floatname="6902903"


INSAT=$2
OUTDIR=$3
ERRM=00
ERRA=00
mkdir -p $OUTDIR

#echo python extract_obs_chlsat_err.py -i $INSAT -o $OUTDIR -ln $LON -lt $LAT -m $MASKFILE -v $DIRVARSAT -em $ERRM
#echo python extract_obs_chlsat_err_01min.py -i $INSAT -o $OUTDIR -ln $LON -lt $LAT -m $MASKFILE -v $DIRVARSAT -em $ERRM
#python  float_extract_obs_chlsat.py -i $INSAT -o $OUTDIR -m $MASKFILE -v $DIRVARSAT -em $ERRM -fln $floatname
python  float_extract_obs_chlsat_err.py -i $INSAT -o $OUTDIR -m $MASKFILE -fln $floatname -em $ERRM -ea $ERRA

#OUTDIR=ERR_ADDMUL/P5_A0.03/SATCHL_${LON}_${LAT}_$TYPE/
#mkdir -p $OUTDIR

#echo python extract_obs_chlsat.py -i $INSAT -o $OUTDIR -ln $LON -lt $LAT -m $MASKFILE

