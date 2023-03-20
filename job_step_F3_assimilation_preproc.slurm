#! /bin/bash

#SBATCH --job-name=PRE_EAT_ASSIMILATION
#SBATCH --time=0:05:00
#SBATCH --mem=6gb
#SBATCH --account=OGS21_PRACE_P
#SBATCH --partition=g100_all_serial
##SBATCH --qos=g100_qos_dbg
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

#IFS=$'\r\n' GLOBIGNORE='*' command eval  'assimilation_folder_list=($(cat assimilation_F3_folder_list.txt))'
#IFS=$'\r\n' GLOBIGNORE='*' command eval  'ensemble_folder_list=($(cat ensemble_F2_folder_list.txt))'

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

i_float=$((SLURM_ARRAY_TASK_ID/11))
i_param=$((SLURM_ARRAY_TASK_ID%11)) # 10 = number of params

bash ./F3_create_assimilation.sh ${i_float} ${i_param}

date
