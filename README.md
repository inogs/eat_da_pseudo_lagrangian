#!/bin/bash

source ~/sequence3.sh

# example of sequence3.sh
#module purge
#module load autoload
#module load intel/oneapi-2021--binary
#module load intelmpi/oneapi-2021--binary
#module load mkl/oneapi-2021--binary
#module load cmake/3.21.4
#source /g100_work/OGS21_PRACE_P/COPERNICUS/py_env_3.6.8/bin/activate
#export PYTHONPATH=$PYTHONPATH:/g100_work/OGS21_PRACE_P/COPERNICUS/bit.sea

bash ./F1_create_spinup.sh

sbatch -o slurm-%A_%a.out -e slurm-%A_%a.err --array=0-1 job_step_F1_spinup.slurm

deactivate

module purge

conda activate eat

bash ./F2_create_ensemble.sh

sbatch -o slurm-%A_%a.out -e slurm-%A_%a.err --array=0-1 job_step_F2_ensemble.slurm

rm  assimilation_F3_folder_list.txt

sbatch -o STD_OUTERR/slurm-%A_%a.out -e STD_OUTERR/slurm-%A_%a.err --array=0-21 job_step_F3_assimilation_preproc.slurm

sbatch -o STD_OUTERR/slurm-%A_%a.out -e STD_OUTERR/slurm-%A_%a.err --array=0-21 job_step_F3_assimilation.slurm

conda deactivate
