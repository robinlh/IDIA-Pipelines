#!/bin/bash

#SBATCH --job-name='bench'
#SBATCH --cpus-per-task=16
#SBATCH --mem=16GB
#SBATCH --output=logs/bench-%j-stdout.log
#SBATCH --error=logs/bench-%j-stderr.log

echo "Submitting SLURM job: benchmarks using 16 cores"
singularity exec /users/robh/containers/ubuntu_python_lite.sif python /users/robh/scripts/benchmarks.py 16 /users/robh/logs/num_comp.logs