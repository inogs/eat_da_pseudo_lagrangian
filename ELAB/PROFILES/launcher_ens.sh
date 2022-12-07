
DIRNAME=float_west
SETUP=ENS_n50_floatsal_p20
INDIR=/g100_scratch/userexternal/ateruzzi/EAT_DA/WP4_tests/$DIRNAME/$SETUP/

OUTBASE=WP4_tests/
OUTDIR=$OUTBASE/$DIRNAME/$SETUP/
mkdir -p $OUTDIR

VAR=salt # Naming should be as in result.nc
VAR=temp # Naming should be as in result.nc

DEPTH=1000 

echo python plot_profiles_ens.py -i $INDIR -o $OUTDIR -v $VAR -d $DEPTH

