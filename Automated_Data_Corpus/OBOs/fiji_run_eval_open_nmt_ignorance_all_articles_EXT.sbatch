#!/bin/bash
# Job name
#SBATCH --job-name=full_OBO_opennmt_ignorance_EXT

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
#SBATCH --error=/Users/mabo1182/Ignorance-Base/Automated_Data_Corpus/OBOs/eo/full_OBO_opennmt_ignorance_EXT_%j.err
#SBATCH --output=/Users/mabo1182/Ignorance-Base/Automated_Data_Corpus/OBOs/eo/full_OBO_opennmt_ignorance_EXT_%j.out



cd /Users/mabo1182/Ignorance-Base/Automated_Data_Corpus/OBOs/
date
./fiji_run_eval_open_nmt_ignorance_all_articles_EXT.sh
date

