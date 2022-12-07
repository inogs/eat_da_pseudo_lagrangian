INBASE=WP5_tests/
DIRNAME=float_east
SETUP=ENS_n50_fabmsall
SETUP=ENS_n50_fabms
SETUP=ENS_n50
SETUP=ENS_n50_nometeo_fabmsall

SETUP=ESTKF_n50_chl_float_fabmsall
SETUP=ESTKF_n50_chl_float_fabms
SETUP=ESTKF_n50_chl_float_fabmsall_nometeo
SETUP=ESTKF_n50_chl_float_fabmsall_nom07
SETUP=ESTKF_n50_chl_float_fabmsall_nom1
SETUP=ESTKF_n50_chl_floatsatd_fabmsall_nometeo
SETUP=ESTKF_n50_chl_floatsatw_fabmsall_nom08
SETUP=ESTKF_n50_chl_floatsatw_fabmsall_nom099
SETUP=ESTKF_n50_chl_floatsatw_fabmsall_nometeo
SETUP=ESTKF_n50_chl_floatsatw_fabmsall_nom099HC
SETUP=ESTKF_n50_chlnut_floatsatw_fabmsall_nometeo
SETUP=ESTKF_n50_chlall_satw_fabmsall_nometeo

SETUP=ENS_n24_norst
SETUP=ENS_n50_norst
SETUP=ESTKF_n24_chlall_satw_fabmsall_nom08
SETUP=ESTKF_n24_chlall_satw_fabms_nom08
SETUP=ESTKF_n50_chlall_satw_fabmsall_nom08
SETUP=ENS_n24_fabms_nometeo
SETUP=ESTKF_n24_chlall_satw_fabms_nom09
SETUP=ESTKF_n24_chlall_satw_fabms_nom1
SETUP=ESTKF_n24_chlall_satd_fabms_nom1
SETUP=ESTKF_n24_chlall_satw_fabms_nom1_errH
SETUP=ESTKF_n24_chlall_satw_fabms_nom08_errH
SETUP=ESTKF_n24_chlall_satw_fabms_nom08_errVH
SETUP=ESTKF_n24_chlall_satw_fabms_nom1_errV
SETUP=ESTKF_n24_chlall_satw_fabms_nom08_errV
SETUP=ESTKF_n24_chlall_satw_fabms_nom1_errVmin01
SETUP=ESTKF_n24_chlall_satw_fabmsall_nom1_errVmin01
SETUP=ESTKF_n50_chlall_satw_fabmsall_nom1_errVmin01
INDIR=/g100_scratch/userexternal/ateruzzi/EAT_DA/$INBASE/$DIRNAME/$SETUP/
#INFILE=$INDIR/result.nc

OUTBASE=$INBASE
OUTDIR=$OUTBASE/$DIRNAME/$SETUP/
mkdir -p $OUTDIR

VAR=N3_n # Naming should be as in result.nc

DEPTH=300 # Optionally, a depth limit can be added
          # default is 300 m

#AGGVAR=P_Chl # Naming should be composed by the name of the group
AGGVAR=P_Chl # Naming should be composed by the name of the group
     # to be aggregated
     # (P for phyto, Z for zoo, B for bacteria, etc.)
     # and by the name of componenent 
     # (Chl for chlorophyl, c for carbon, etc.)

# examples
# -> To plot N1_p
#echo python plot_hovmoeller_ens.py -i $INDIR -o $OUTDIR -v $VAR 
# -> To do the same plot untill deplim
echo python plot_hovmoeller_mean_std.py -i $INDIR -o $OUTDIR -v $VAR -d $DEPTH -vl 0 -vm 4
VAR=N1_p # Naming should be as in result.nc
echo python plot_hovmoeller_mean_std.py -i $INDIR -o $OUTDIR -v $VAR -d $DEPTH -vl 0 -vm .1

# -> To plot the total phyto chl
echo python plot_hovmoeller_mean_std.py -i $INDIR -o $OUTDIR -g $AGGVAR -d $DEPTH -vl 0 -vm .75


#N1_p lim 0 - 0.1
#N3_n lim 0 - 6
#P_chl lim 0 - 0.5
#P_c lim 0 - 25
#P_run lim 1 - 15
