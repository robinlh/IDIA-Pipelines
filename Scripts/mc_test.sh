#!/bin/bash

#SBATCH --job-name='mc_bench'
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=4GB
#SBATCH --time=00:10:00
#SBATCH --output=logs/mc_bench-%j-stdout.log
#SBATCH --error=logs/mc_bench-%j-stderr.log

echo "Submitting SLURM job: benchmarks using 32 cores"
mpirun singularity exec /idia/software/containers/python3-2019-09-25.simg python /users/robh/repos/IDIA-Pipelines/Python/Benchmarking/MonteCarlo/parallel_pi.py

