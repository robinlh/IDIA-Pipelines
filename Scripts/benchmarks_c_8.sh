#!/bin/bash

#SBATCH --job-name='multi'
#SBATCH --cpus-per-task=4
#SBATCH --mem=16GB
#SBATCH --output=logs/multi-%j-stdout.log
#SBATCH --error=logs/multi-%j-stderr.log

echo "Submitting SLURM job: benchmarks using 4 cores"
singularity exec /users/robh/containers/ubuntu_python_lite.sif python /users/robh/scripts/benchmarks.py 4 /users/robh/logs/num_comp.logs