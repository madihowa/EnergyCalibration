#!/bin/bash
#SBATCH --job-name=initial_inputs207
#SBATCH --output=quanah_output/%x.o%j
#SBATCH --error=quanah_error/%x.e%j
#SBATCH --partition nocona
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=128
#SBATCH --mem-per-cpu=3994MB
#SBATCH --mail-user=<madison.howard@ttu.edu>
#SBATCH --mail-type=ALL

# actual code to execute
./run.sh trial_1_epoch_1 list_inputs.csv
