#!/bin/bash
# Job name
#SBATCH --job-name=GPU_biobert_all_articles

# Email job progress
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mayla.boguslav@cuanschutz.edu 


# Resource allocation
#SBATCH -p titan
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=3
#SBATCH --mem=24gb
#SBATCH --gres=gpu
#SBATCH --time 100:00:00


# Log errors here:
#SBATCH --error=/Users/mabo1182/Ignorance-Base/Automated_Data_Corpus/eo/GPU_biobert_all_articles_%j.err
#SBATCH --output=/Users/mabo1182/Ignorance-Base/Automated_Data_Corpus/eo/GPU_biobert_all_articles_%j.out


cd /Users/mabo1182/Ignorance-Base/Automated_Data_Corpus
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH 
export PATH=/usr/local/cuda/bin:$PATH
date
./fiji_run_biobert_all_articles_fiji.sh
date
