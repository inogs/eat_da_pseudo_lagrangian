#! /bin/bash

SCRATCH_PL=/g100_scratch/userexternal/plazzari/
TESTN=WP6_TEST_3
EXPERIMENT_FOLDER=$SCRATCH_PL/$TESTN/
SETUP=Z5_parameters_p_sum_assimilation
DIRTXT=_instances_${SETUP}_F3

START=20190101
END__=20200101

DEPTH=300

OUTBASE=/g100_scratch/userexternal/ateruzzi/EAT_DA/ELAB/HOVMOELLER_ENS/$TESTN/
mkdir -p $OUTBASE


for float in $(ls -d $EXPERIMENT_FOLDER/*spinup* | xargs -n1 basename | cut -c1-7); do
       echo $float
       INDIR=$EXPERIMENT_FOLDER/${float}${SETUP}/
       OUTDIR=$OUTBASE/$SETUP/${float}_enshovmoeller/
       mkdir -p $OUTDIR
       var=N3_n
       echo $var
       python plot_hovmoeller_mean_std.py -i $INDIR -o $OUTDIR -v $var -d $DEPTH -vl 0 -vm 4
       var=N1_p
       echo $var
       python plot_hovmoeller_mean_std.py -i $INDIR -o $OUTDIR -v $var -d $DEPTH -vl 0 -vm .1
       aggvar=P_Chl
       echo $aggvar
       python plot_hovmoeller_mean_std.py -i $INDIR -o $OUTDIR -g $aggvar -d $DEPTH -vl 0 -vm .75

done

