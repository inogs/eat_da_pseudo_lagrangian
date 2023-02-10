#! /bin/bash

#SBATCH --job-name=EAT_ENSEMBLE
#SBATCH -N4
#SBATCH --ntasks-per-node=26
#SBATCH --time=2:00:00
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

IFS=$'\r\n' GLOBIGNORE='*' command eval  'ensemble_folder_list=($(cat ensemble_F2_folder_list.txt))'

cd ${ensemble_folder_list[${SLURM_ARRAY_TASK_ID}]}

mpiexec -n 100 eat_model_gotm --separate_gotm_yaml #--separate_restart_file

date
