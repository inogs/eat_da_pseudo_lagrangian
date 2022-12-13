#!/bin/bash

declare -a VAR_list
VAR_list=('PSAL' 'TEMP' 'NITRATE' 'CHLA')
N_VAR=${#VAR_list[@]}

#VAR=PSAL
#VAR=TEMP
#VAR=NITRATE
#VAR=CHLA
DEPTH=300

#FLOAT=6902903 #west
#FLOAT=6901772 #east
FLOAT=$1
START=$2
END__=$3

for ((i=0;i<N_VAR; i++)); do

	VAR=${VAR_list[${i}]}

        OUTDIR=$PWD/PROFILES_ERRadd_mul/P1.2_A0.02/${VAR}_${FLOAT}/
        mkdir -p $OUTDIR


#       python extract_float_profiles_addmul.py -v $VAR -o $OUTDIR -f $FLOAT -s $START -e $END__ -d 200
        python extract_float_profiles.py -v $VAR -o $OUTDIR -f $FLOAT -s $START -e $END__ -d 200


        OUTDIR=$PWD/HOVMOELLER/${VAR}_${FLOAT}/
        mkdir -p $OUTDIR

        python plot_hovmoeller.py -v $VAR -o $OUTDIR -f $FLOAT -s $START -e $END__

done

