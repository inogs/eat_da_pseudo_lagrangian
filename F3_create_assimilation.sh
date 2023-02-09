#! /bin/bash
#conda activate eat
BASE_DIR=$PWD

SPINUP_FOLDER=$CINECA_SCRATCH/WP6_TEST
mkdir -p ${SPINUP_FOLDER}

declare -a float_list 
float_list=('6902903' '6901772')
N_float=${#float_list[@]}
N_ENSEMBLE=100

START=20190101
END__=20200101


START_NUDG=20180101
END___NUDG=20210101

rm -f assimilation_F3_folder_list.txt
for ((i=0;i<N_float; i++)); do
    cd $BASE_DIR
    echo ${float_list[${i}]}
    float=${float_list[${i}]}

    SPNDIR=${SPINUP_FOLDER}/${float}_spinup_F1
    ENSDIR=${SPINUP_FOLDER}/${float}_ensemble_F2
    WRKDIR=${SPINUP_FOLDER}/${float}_assimilation_F3
    echo $WRKDIR >> assimilation_F3_folder_list.txt

# create spiunp folder for each float
    rm -rf $WRKDIR
    cp -r $ENSDIR  $WRKDIR

#create perturbations on forcings
    cd $WRKDIR
    cp gotm.yaml_ensemble_F2 gotm.yaml
    eat-gotm-gen yaml gotm.yaml ${N_ENSEMBLE} -f fabm/yaml_file
    cp ${BASE_DIR}/runESTKF.py .


done

#conda deactivate
