#! /bin/bash

SCRATCH_PL=/g100_scratch/userexternal/plazzari/
EXPERIMENT_FOLDER=$SCRATCH_PL/WP6_TEST_4/

START=20190101
END__=20200101

DEPTH=300

OUTBASE=/g100_scratch/userexternal/ateruzzi/EAT_DA/ELAB/FLOAT_HOVM/
mkdir -p $OUTBASE


for float in $(ls -d $EXPERIMENT_FOLDER/*spinup* | xargs -n1 basename | cut -c1-7); do
       echo $float
       OUTDIR=$OUTBASE/${float}_hovmoeller/
       mkdir -p $OUTDIR
       python plot_hovmoeller_float.py -o $OUTDIR -f $float -v CHLA -s $START -e $END__ -mn 0 -mx 0.75 -d $DEPTH
       python plot_hovmoeller_float.py -o $OUTDIR -f $float -v NITRATE -s $START -e $END__ -mn 0 -mx 4 -d $DEPTH

done

