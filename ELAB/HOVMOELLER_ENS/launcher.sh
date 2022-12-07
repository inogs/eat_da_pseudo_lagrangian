
DIRNAME=float_east
SETUP=ENS_n10
INDIR=/g100_scratch/userexternal/ateruzzi/EAT_DA/WP4_tests/$DIRNAME/$SETUP/
#INFILE=$INDIR/result.nc

OUTBASE=WP4_tests/
OUTDIR=$OUTBASE/$DIRNAME/$SETUP/
mkdir -p $OUTDIR

VAR=N1_p # Naming should be as in result.nc

DEPTH=400 # Optionally, a depth limit can be added
          # default is 300 m

#AGGVAR=P_Chl # Naming should be composed by the name of the group
AGGVAR=P_run # Naming should be composed by the name of the group
     # to be aggregated
     # (P for phyto, Z for zoo, B for bacteria, etc.)
     # and by the name of componenent 
     # (Chl for chlorophyl, c for carbon, etc.)

VARLINE=N3_n  # Can be a group of variables or a variable
      # If a single variable the naming should be as in results.nc
      # If a group of variable naming should be composed by
      # the name of the group
      # (P for phyto, Z for zoo, B for bacteria, etc.)
      # and by the name of componenent
      # A line will be plotted for each element of the group
      # (P_EIR will produce a line for the EIR of each phyto,
      # Z_c will plot a line for c of eah zoo, etc.)
LINEVALUE=1.0

# examples
# -> To plot N1_p
#echo python plot_hovmoeller_ens.py -i $INDIR -o $OUTDIR -v $VAR 
# -> To do the same plot untill deplim
echo python plot_hovmoeller_ens.py -i $INDIR -o $OUTDIR -v $VAR -d $DEPTH

# -> To plot the total phyto chl
echo python plot_hovmoeller_ens.py -i $INDIR -o $OUTDIR -g $AGGVAR -d $DEPTH

# -> To plot the total phyto chl and lines of phyto EIRs at EIR=$LINEVALUE
echo python plot_hovmoeller_ens.py -i $INDIR -o $OUTDIR -g $AGGVAR -l $VARLINE -k $LINEVALUE -vl 0.1 -vm 0.7
