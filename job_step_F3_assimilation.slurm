#! /bin/bash

#SBATCH --job-name=EAT_ASSIMILATION
#SBATCH -N4 
#SBATCH --ntasks-per-node=26
#SBATCH --time=0:10:00
#SBATCH --mem=300gb
#SBATCH --account=icei_Rosati
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

IFS=$'\r\n' GLOBIGNORE='*' command eval  'assimilation_folder_list=($(cat assimilation_F3_folder_list.txt))'
IFS=$'\r\n' GLOBIGNORE='*' command eval  'ensemble_folder_list=($(cat ensemble_F2_folder_list.txt))'

cd ${assimilation_folder_list[${SLURM_ARRAY_TASK_ID}]}

cp ${ensemble_folder_list[${SLURM_ARRAY_TASK_ID}]}/restart_????.nc ${assimilation_folder_list[${SLURM_ARRAY_TASK_ID}]}/

mpiexec -n 1 python runESTKF.py : -n 100 eat-gotm --separate_gotm_yaml --separate_restart_file

date
