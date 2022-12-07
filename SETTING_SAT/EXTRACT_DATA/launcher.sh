INSAT_DAILY=/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/ONLINE_V8C/SAT/CHL/MULTISENSOR/1Km/NRT/DAILY/CHECKED_24/
INSAT_WEEKLY=/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/ONLINE_V8C/SAT/CHL/MULTISENSOR/1Km/NRT/WEEKLY_1_24/
MASKFILE=/g100_scratch/userexternal/ateruzzi/MASKS_V8/meshmask.nc
DIRVARSAT=VAR_SAT

ln -s $INSAT_DAILY INSAT_DAILY
ln -s $INSAT_WEEKLY INSAT_WEEKLY

LON=20.75233
LAT=35.62733


ERRM=1.25

TYPE=DAILY
TYPE=WEEKLY
INSAT=INSAT_$TYPE/
OUTDIR=ERR_ADDMUL/P${ERRM}_AVARSATmin01/SATCHL_${LON}_${LAT}_$TYPE/
mkdir -p $OUTDIR

#echo python extract_obs_chlsat_err.py -i $INSAT -o $OUTDIR -ln $LON -lt $LAT -m $MASKFILE -v $DIRVARSAT -em $ERRM
echo python extract_obs_chlsat_err_01min.py -i $INSAT -o $OUTDIR -ln $LON -lt $LAT -m $MASKFILE -v $DIRVARSAT -em $ERRM


#OUTDIR=ERR_ADDMUL/P5_A0.03/SATCHL_${LON}_${LAT}_$TYPE/
#mkdir -p $OUTDIR

#echo python extract_obs_chlsat.py -i $INSAT -o $OUTDIR -ln $LON -lt $LAT -m $MASKFILE

