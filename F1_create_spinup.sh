#! /bin/bash
BASE_DIR=$PWD

SPINUP_FOLDER=$CINECA_SCRATCH/WP6_TEST
mkdir -p ${SPINUP_FOLDER}

declare -a float_list 
float_list=('6902903' '6901772')
N_float=${#float_list[@]}

START=20190101
END__=20200101


START_NUDG=20180101
END___NUDG=20210101


for ((i=0;i<N_float; i++)); do
    cd $BASE_DIR
    echo ${float_list[${i}]}
    float=${float_list[${i}]}

    WRKDIR=${SPINUP_FOLDER}/${float}_spinup
    echo $WRKDIR >> spinup_folder_list.txt

# create spiunp folder for each float
    cp -r template_setup_spinup  $WRKDIR

#extract profile from float as observation files
    cd $BASE_DIR/SETTING_ARGO/EXTRACT_PROFILES/
    bash launcher.sh ${float} ${START} ${END__} $WRKDIR

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

done
