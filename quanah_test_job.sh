#!/bin/bash
#SBATCH --job-name=testing_jets_csv
#SBATCH --output=quanah_outputs/%x.o%j
#SBATCH --error=quanah_errors/%x.e%j
#SBATCH --partition quanah
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=3994MB
#SBATCH --mail-user=<madison.howard@ttu.edu>
#SBATCH --mail-type=ALL

# actual code to execute
python testing_trained_NN.py $1 $2 $3 
