#!/bin/bash
#SBATCH --job-name=run4_two_inputs
#SBATCH --output=quanah_outputs/%x.o%j
#SBATCH --error=quanah_errors/%x.e%j
#SBATCH --partition quanah
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=3994MB
#SBATCH --mail-user=<madison.howard@ttu.edu>
#SBATCH --mail-type=ALL

# actual code to execute
./run.sh $1 $2 
