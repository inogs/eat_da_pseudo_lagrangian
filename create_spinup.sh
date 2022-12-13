#! /bin/bash
BASE_DIR=$PWD
declare -a float_list 
float_list=('6902903' '6901772')
N_float=${#float_list[@]}

START=20190101
END__=20200101
OUTDIR=

for ((i=0;i<N_float; i++)); do
    echo ${float_list[${i}]}
    float=${float_list[${i}]}
    cd $BASE_DIR
#extract profile 
    cd SETTING_ARGO/EXTRACT_PROFILES/
    bash launcher.sh ${float} ${START} ${END__}


#launcher -- > 

done
