#!/bin/bash

#SBATCH --job-name='bench'
#SBATCH --cpus-per-task=32
#SBATCH --mem=16GB
#SBATCH --output=logs/bench-%j-stdout.log
#SBATCH --error=logs/bench-%j-stderr.log

echo "Submitting SLURM job: benchmarks using 32 cores"
singularity exec /users/robh/containers/ubuntu_python_lite.sif python /users/robh/scripts/benchmarks.py 32 /users/robh/logs/num_comp.logs