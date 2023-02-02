#! /bin/bash
BASE_DIR=$PWD

SPINUP_FOLDER=$CINECA_SCRATCH/WP6_TEST
mkdir -p ${SPINUP_FOLDER}

declare -a float_list 
float_list=('6902903' '6901772')
N_float=${#float_list[@]}
N_ENSEMBLE=50

START=20190101
END__=20200101


START_NUDG=20180101
END___NUDG=20210101

rm ensemble_F2_folder_list.txt
for ((i=0;i<N_float; i++)); do
    cd $BASE_DIR
    echo ${float_list[${i}]}
    float=${float_list[${i}]}

    SPNDIR=${SPINUP_FOLDER}/${float}_spinup_F1
    WRKDIR=${SPINUP_FOLDER}/${float}_ensemble_F2
    echo $WRKDIR >> ensemble_F2_folder_list.txt

# create spiunp folder for each float
    rm -rf $WRKDIR
    cp -r $SPNDIR  $WRKDIR

#create fabm files with different parameters
    cd $BASE_DIR/FABM_YAML_ENSEMBLE_GENARATION
    source $HOME/sequence3.sh
    bash crea_param_1D.sh ${N_ENSEMBLE}
    deactivate
    module purge
    mv fabm_????.yaml $WRKDIR
#create perturbations on forcings
    cd $WRKDIR
    cp gotm.yaml_ensemble_F2 gotm.yaml
    conda activate eat
    eat-gotm-gen yaml gotm.yaml ${N_ENSEMBLE} -p surface/u10/scale_factor 0.20 -p surface/v10/scale_factor 0.20 -f fabm/yaml_file
    conda deactivate


done
