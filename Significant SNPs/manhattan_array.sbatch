#!/bin/bash
#SBATCH --partition=main
#SBATCH --time=5-00:00:00
#SBATCH --job-name=manhattan_array
#SBATCH --output=manhattan_job_%A_%a.out
#SBATCH --array=1-12          # Adjust according to your number of phenotype folders
#SBATCH --mem=120G
#SBATCH --cpus-per-task=4     # Enough for plotting
#SBATCH --mail-user=ivshins@post.bgu.ac.il
#SBATCH --mail-type=END,FAIL

module load anaconda
source /etc/profile.d/conda.sh
conda activate /sise/nadav-group/nadavrap-group/ECGs/env  # Replace with your actual conda env

# Run the Manhattan plot script with SLURM array task ID
python Manhattan_job.py ${SLURM_ARRAY_TASK_ID}