#!/usr/bin/env bash


##list of all ontologies of interest
ontologies="CHEBI,CL,GO_BP,GO_CC,GO_MF,MOP,NCBITaxon,PR,SO,UBERON,CHEBI_EXT,CL_EXT,GO_BP_EXT,GO_CC_EXT,GO_MF_EXT,MOP_EXT,NCBITaxon_EXT,PR_EXT,SO_EXT,UBERON_EXT"

##code path
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'

##evaluation path
eval_path='Ignorance-Question-Work-Full-Corpus/OBOs/'
ignorance_corpus='Ignorance-Question-Corpus/'
ignorance_base_path='3_Ignorance_Base/'
ignorance_base_corpus='Ignorance-Base/Automated_Data_Corpus/'
ignorance_base_all_data_corpus='Ignorance-Base/All_Data_Corpus/'
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


python3 OBO_unique_ids_summary.py -ontologies=$ontologies -obo_unique_ids_file_path=$all_file_path$ignorance_base_path$ignorance_base_all_data_corpus$obos -output_path=$all_file_path$ignorance_base_path$ignorance_base_all_data_corpus$obos