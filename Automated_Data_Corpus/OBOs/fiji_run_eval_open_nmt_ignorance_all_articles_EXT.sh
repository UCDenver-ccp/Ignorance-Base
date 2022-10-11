#!/usr/bin/env bash

CR_models_base_path='/Users/mabo1182/negacy_project/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'
concept_recognition_path='Concept-Recognition-as-Translation/'
code='Code/'
all_code_path=$CR_models_base_path$concept_recognition_path$code
concept_norm_models='Models/CONCEPT_NORMALIZATION/'
full_models='full_files/seq_2_seq_output/'


##path to the evaluation files where all output will be stored during the evaluation
eval_path='Ignorance-Question-Work-Full-Corpus/OBOs/'
ignorance_corpus='Ignorance-Question-Corpus/'
ignorance_base_path='3_Ignorance_Base/'
ignorance_base_corpus='Ignorance-Base/Automated_Data_Corpus/'
output_results='Word_Analysis_Output_Results/'
obos='OBOs/'

##concept normalization folder
concept_norm_files='Concept_Norm_Files/'

##results from concept normalization folder
results_concept_norm_files='Results_concept_norm_files/'

##name of the model we are using for openNMT
declare -a mod=('model-char_step_100000')

##name of character source file that we want to predict the concept IDs for on the character level
char_file='_combo_src_file_char.txt'

##the output extension name for the predictions
char_file_output='_pred.txt'


##loop over each ontology openNMT model and run it for concept normalization
declare -a ont=('CHEBI_EXT' 'CL_EXT' 'GO_BP_EXT' 'GO_CC_EXT' 'GO_MF_EXT' 'MOP_EXT' 'NCBITaxon_EXT' 'PR_EXT' 'SO_EXT' 'UBERON_EXT')

for i in "${ont[@]}"
  do
    echo "$i"
      for j in "${mod[@]}"
      do
        ##runs the opennmt model for each ontology
        onmt_translate -model $CR_models_base_path$concept_recognition_path$concept_norm_models$i/$full_models$i-$j.pt -src $scratch_path$ignorance_base_corpus$obos$concept_norm_files$i/$i$char_file -output $scratch_path$ignorance_base_corpus$obos$results_concept_norm_files$i/$i-$j$char_file_output -replace_unk #-verbose #$i/
      done
  done
