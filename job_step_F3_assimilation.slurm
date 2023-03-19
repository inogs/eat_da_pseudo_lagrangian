#! /bin/bash

#SBATCH --job-name=EAT_ASSIMILATION
#SBATCH -N4 
#SBATCH --ntasks-per-node=26
#SBATCH --time=0:05:00
#SBATCH --mem=300gb
#SBATCH --account=OGS21_PRACE_P
#SBATCH --partition=g100_usr_prod
#SBATCH --mail-type=ALL
##SBATCH --mail-user=

echo $SLURM_JOB_ID
echo $SLURM_ARRAY_JOB_ID
echo $SLURM_ARRAY_TASK_ID
echo $SLURM_ARRAY_TASK_COUNT
echo $SLURM_ARRAY_TASK_MAX
echo $SLURM_ARRAY_TASK_MIN

cd $SLURM_SUBMIT_DIR

ulimit -s unlimited

date

conda activate eat
EXPERIMENT_FOLDER=$CINECA_SCRATCH/WP6_TEST

#IFS=$'\r\n' GLOBIGNORE='*' command eval  'assimilation_folder_list=($(cat assimilation_F3_folder_list.txt))'
#IFS=$'\r\n' GLOBIGNORE='*' command eval  'ensemble_folder_list=($(cat ensemble_F2_folder_list.txt))'

#float_list=('/g100_scratch/userexternal/plazzari/WP6_TEST/6902903_ensemble_F2'
#6901772_instances_light_parameters_EPS0r_assimilation_F3

float_list=('6902903'
            '6901772')

model_list=('light' 
             'Z5' 
             'light' 
             'P1' 
             'Z5' 
             'P1' 
             'P1' 
             'Z5' 
             'P1' 
             'P1' 
             'P1')
param_list=('EPS0r'
             'p_pu'
             'pEIR_eow'
             'p_sum'
             'p_sum'
             'p_qlcPPY'
             'p_qup'
             'p_pu_ea'
             'p_alpha_chl'
             'p_qplc'
             'p_srs')

i_float=$((SLURM_ARRAY_TASK_ID/11))
i_param=$((SLURM_ARRAY_TASK_ID%11)) # 11 = number of params

WRKDIR=${EXPERIMENT_FOLDER}/${float_list[${i_float}]}_instances_${model_list[${i_param}]}_parameters_${param_list[${i_param}]}_assimilation_F3

cd $WRKDIR

cp ${EXPERIMENT_FOLDER}/${float_list[${i_float}]}_ensemble_F2/restart_????.nc ${WRKDIR}/

rm result_????.nc

#mpiexec -n 1 python runESTKF.py : -n 100 eat-gotm --separate_gotm_yaml --separate_restart_file
mpiexec -n 1 python runESTKF_template.py -pm ${model_list[${i_param}]} -pp ${param_list[${i_param}]} : -n 100 eat-gotm --separate_gotm_yaml --separate_restart_file

date
