# eat_da_pseudo_lagrangian


# To Launch Spin up with slurm JOB ARRAY
# Example with two floats
sbatch -o slurm-%A_%a.out -e slurm-%A_%a.err --array=0-1 job_step_F1_spinup.slurm
sbatch -o slurm-%A_%a.out -e slurm-%A_%a.err --array=0-1 job_step_F2_ensemble.slurm
sbatch -o slurm-%A_%a.out -e slurm-%A_%a.err --array=0-1 job_step_F3_assimilation.slurm
