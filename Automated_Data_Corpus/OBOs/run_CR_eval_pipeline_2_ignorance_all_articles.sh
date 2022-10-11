#!/usr/bin/env bash

##list of all ontologies of interest
ontologies="CHEBI,CL,GO_BP,GO_CC,GO_MF,MOP,NCBITaxon,PR,SO,UBERON"

##code path
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'
negacy_folder='negacy_project/'
concept_recognition_path='Concept-Recognition-as-Translation/'
code='Code/'
all_code_path=$fiji_path$negacy_folder$concept_recognition_path$code
#/Users/mabo1182/negacy_project/Concept-Recognition-as-Translation/Code/

##evaluation path
eval_path='Ignorance-Question-Work-Full-Corpus/OBOs/'
ignorance_corpus='Ignorance-Question-Corpus/'
ignorance_base_path='3_Ignorance_Base/'
ignorance_base_corpus='Ignorance-Base/Automated_Data_Corpus/'
output_results='Word_Analysis_Output_Results/'
obos='OBOs/'

##results from concept normalization path
results_concept_norm_files='Results_concept_norm_files/'
##concept normalization path with files to link the results with the word tokenized PMC articles
concept_norm_files='Concept_Norm_Files/'
##the full concept recognition output folder
concept_system_output='concept_system_output/'
##if there is a gold standard, the gold standard folder for evaluation
gold_standard='None'

##evaluation files we are working with
all_files='all'

##perform the evaluation analysis
evaluate='False'



##run the open_nmt to predict
#run_eval_open_nmt.sh


#if evaluate is false -> dont need a gold standard option because it is not used
##full concept system output for the full run of concept recognition
python3 $all_code_path/eval_concept_system_output.py -ontologies=$ontologies -concept_norm_results_path=$scratch_path$ignorance_base_corpus$obos$results_concept_norm_files -concept_norm_link_path=$scratch_path$ignorance_base_corpus$obos$concept_norm_files -output_file_path=$scratch_path$ignorance_base_corpus$obos$concept_system_output -gold_standard_path=$gold_standard -eval_path=$scratch_path$ignorance_base_corpus$obos -evaluation_files=$all_files -evaluate=$evaluate


