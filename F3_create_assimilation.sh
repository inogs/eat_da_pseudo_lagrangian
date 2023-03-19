#! /bin/bash
#conda activate eat
#export PYTHONPATH=$PYTHONPATH:/g100_work/OGS21_PRACE_P/COPERNICUS/bit.sea
#export PYTHONPATH=$PYTHONPATH:/g100_work/OGS_devC/V10C/RUNS_SETUP/SEAMLESS/bit.sea
BASE_DIR=$PWD

. setup.sh
#EXPERIMENT_FOLDER=$CINECA_SCRATCH/WP6_TEST
mkdir -p ${EXPERIMENT_FOLDER}

declare -a float_list 
float_list=('6902903' '6901772')
N_float=${#float_list[@]}
N_ENSEMBLE=100

declare -a param_list

param_list=('instances_light_parameters_EPS0r'
             'instances_Z5_parameters_p_pu'
             'instances_light_parameters_pEIR_eow'
	     'instances_P1_parameters_p_sum'
             'instances_Z5_parameters_p_sum'
             'instances_P1_parameters_p_qlcPPY'
             'instances_P1_parameters_p_qup'
             'instances_Z5_parameters_p_pu_ea'
             'instances_P1_parameters_p_alpha_chl'
             'instances_P1_parameters_p_qplc'
             'instances_P1_parameters_p_srs') 

N_param=${#param_list[@]}

START=20190101
END__=20200101


START_NUDG=20180101
END___NUDG=20210101

#rm -f assimilation_F3_folder_list.txt

i=$1 # float index
p=$2 # parameter index

#for ((i=0;i<N_float; i++)); do
#    for ((p=0;p<N_param; p++)); do
       cd $BASE_DIR
       echo ${float_list[${i}]}
       float=${float_list[${i}]}
       param=${param_list[${p}]}
   
       SPNDIR=${EXPERIMENT_FOLDER}/${float}_spinup_F1
       ENSDIR=${EXPERIMENT_FOLDER}/${float}_ensemble_F2
       WRKDIR=${EXPERIMENT_FOLDER}/${float}_${param}_assimilation_F3
       echo $WRKDIR >> assimilation_F3_folder_list.txt
   
# create data assimilation folder for each float
       rm -rf $WRKDIR
       cp -r $ENSDIR  $WRKDIR

#extract profile from float as observation files
       cd $BASE_DIR/SETTING_ARGO/EXTRACT_PROFILES/
       bash launcher.sh ${float} ${START} ${END__} $WRKDIR/ToAssimilate

#extract sat data along float track as observation files
       cd $BASE_DIR/SETTING_SAT/EXTRACT_DATA/
       bash launcher.sh ${float} $WRKDIR/ToAssimilate
   
#create fabm files with different parameters
       cd $BASE_DIR/FABM_YAML_ASSIMILATION_GENARATION
       bash crea_param_1D.sh ${N_ENSEMBLE} ${param} ${WRKDIR}
       mv fabm_????.yaml $WRKDIR
   
#create perturbations on forcings
       cd $WRKDIR
       cp gotm.yaml_ensemble_F2 gotm.yaml
       eat-gotm-gen yaml gotm.yaml ${N_ENSEMBLE} -p surface/u10/scale_factor 0.20 -p surface/v10/scale_factor 0.20 -f fabm/yaml_file
       cp ${BASE_DIR}/runESTKF_template.py .
   
#   done
#done

#conda deactivate
