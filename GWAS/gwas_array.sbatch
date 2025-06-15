#!/bin/bash
#SBATCH --partition=main
#SBATCH --time=6-00:00:00
#SBATCH --job-name=GWAS_without_norm_job
#SBATCH --output=GWAS_without_norm_job_%A_%a.out
#SBATCH --array=1-12          # Replace <N> with number of phenotype files
#SBATCH --mem=250G
#SBATCH --cpus-per-task=120
#SBATCH --mail-user=ivshins@post.bgu.ac.il
#SBATCH --mail-type=END,FAIL

module load anaconda
source /etc/profile.d/conda.sh
conda activate /sise/nadav-group/nadavrap-group/ECGs/env # Replace with your actual conda environment

# Run Python script with array task ID
python gwas_without_norm_job.py ${SLURM_ARRAY_TASK_ID}
