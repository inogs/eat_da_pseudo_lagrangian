#! /bin/bash
source $HOME/sequence3.sh
BASE_DIR=$PWD

. setup.sh
#EXPERIMENT_FOLDER=$CINECA_SCRATCH/WP6_TEST
mkdir -p ${EXPERIMENT_FOLDER}

declare -a float_list 
float_list=('6902903' '6901772')
N_float=${#float_list[@]}

START=20190101
END__=20200101


START_NUDG=20180101
END___NUDG=20210101

rm spinup_folder_list.txt # clean list of folders

for ((i=0;i<N_float; i++)); do
    cd $BASE_DIR
    echo ${float_list[${i}]}
    float=${float_list[${i}]}

    WRKDIR=${EXPERIMENT_FOLDER}/${float}_spinup_F1
    echo $WRKDIR >> spinup_folder_list.txt

# clean and create spiunp folder for each float
    rm -rf $WRKDIR
    cp -r template_setup_spinup $WRKDIR

#extract profile from float as observation files --> moved to F3
#   cd $BASE_DIR/SETTING_ARGO/EXTRACT_PROFILES/
#   bash launcher.sh ${float} ${START} ${END__} $WRKDIR/ToAssimilate

#extract sat data along float track as observation files --> moved to F3
#   cd $BASE_DIR/SETTING_SAT/EXTRACT_DATA/
#   bash launcher.sh ${float} $WRKDIR/ToAssimilate

#extract profile from float as nudging files
    cd $BASE_DIR/SETTING_ARGO/EXTRACT_gotm_nudg/
    bash launcher.sh ${float} ${START_NUDG} ${END___NUDG} $WRKDIR

#extract initial conditions from reanalysis
    cd $BASE_DIR/SETTING_ARGO/EXTRACT_from_RA/
    bash launcher.sh ${WRKDIR} ${START} ${END__} ${float}

#copy meteo file from ERA5
    cp /g100_work/IscrB_3DSBM/gocchipinti/FLOAT/meteo.${float}.dat ${WRKDIR}/meteo.dat
    cp /g100_work/IscrB_3DSBM/gocchipinti/FLOAT/precip.${float}.dat ${WRKDIR}/precip.dat

#create fabm file with initial parameters
    cd $BASE_DIR/FABM_YAML_SPINUP_GENARATION
    bash crea_param_1D.sh 1
    mv fabm_0001.yaml $WRKDIR/fabm.yaml

# copy the correct gotm.yaml
    cd $WRKDIR
    cp gotm.yaml_spinup_F1 gotm.yaml
done
deactivate
module purge
