#!/bin/bash
# Job name
#SBATCH --job-name=full_run_best_models

# Email job progress
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mayla.boguslav@cuanschutz.edu 


# Resource allocation
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --mem=500gb
#SBATCH -p long
#SBATCH --time=100:00:00

# Log errors here:
#SBATCH --error=/Users/mabo1182/Ignorance-Base/Automated_Data_Corpus/eo/full_run_best_models_%j.err
#SBATCH --output=/Users/mabo1182/Ignorance-Base/Automated_Data_Corpus/eo/full_run_best_models_%j.out


cd /Users/mabo1182/Ignorance-Base/Automated_Data_Corpus/
date
./run_final_output_combine_best_models_all_articles.sh
date

