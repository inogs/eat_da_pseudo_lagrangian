
DIRNAME=float_west
SETUP=ESTKF_n50_T_S
SETUP=ESTKF_n50_T_S_Nut
SETUP=ESTKF_n50_T_S_Nplugin
INDIR=/g100_scratch/userexternal/ateruzzi/EAT_DA/WP4_tests/$DIRNAME/$SETUP/
#INFILE=$INDIR/result.nc

OUTBASE=WP4_tests/
OUTDIR=$OUTBASE/$DIRNAME/$SETUP/
mkdir -p $OUTDIR

VAR=temp # Naming should be as in result.nc
VAR=salt # Naming should be as in result.nc
VAR=N3_n # Naming should be as in result.nc

DEPTH=1000 # Optionally, a depth limit can be added
          # default is 300 m

echo python plot_profiles_DA.py -i $INDIR -o $OUTDIR -v $VAR -d $DEPTH



