#!/usr/bin/env bash


##list of all ontologies of interest
ontologies="CHEBI,CL,GO_BP,GO_CC,GO_MF,MOP,NCBITaxon,PR,SO,UBERON"

##code path
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'


##evaluation path
ignorance_question_work_full_corpus='Ignorance-Question-Work-Full-Corpus/'
ignorance_corpus='Ignorance-Question-Corpus/'
ignorance_base_path='3_Ignorance_Base/'
ignorance_base_corpus='Ignorance-Base/Automated_Data_Corpus/'
ignorance_base_all_data_corpus='Ignorance-Base/All_Data_Corpus/'
output_results='Word_Analysis_Output_Results/'
obos='OBOs/'

results_span_detection='Results_span_detection/'
##results from concept normalization path
results_concept_norm_files='Results_concept_norm_files/'
results_concept_norm_files_ext='-model-char_step_100000_pred.txt'
gs='GS_'
##concept normalization path with files to link the results with the word tokenized PMC articles
concept_norm_files='Concept_Norm_Files/'
##the full concept recognition output folder
concept_system_output='concept_system_output/'
biobert='BIOBERT'


declare -a ont=('CHEBI' 'CL' 'GO_BP' 'GO_CC' 'GO_MF' 'MOP' 'NCBITaxon' 'PR' 'SO' 'UBERON' 'CHEBI_EXT' 'CL_EXT' 'GO_BP_EXT' 'GO_CC_EXT' 'GO_MF_EXT' 'MOP_EXT' 'NCBITaxon_EXT' 'PR_EXT' 'SO_EXT' 'UBERON_EXT')

##loop over each ontology and move everything we need and delete extra stuff
for i in "${ont[@]}"
do
    echo "$i"

#    ##RESULTS_SPAN_DETECTION
#    ##remove BIOBERT folder from all data corpus for each ontology
#    rm -r $fiji_path$ignorance_base_all_data_corpus$obos$results_span_detection$i/$biobert/*
#
#    rm $fiji_path$ignorance_base_all_data_corpus$obos$results_span_detection$i/*crf*
#
#    ##add in the gold standard stuff
#    cp $fiji_path$ignorance_question_work_full_corpus$obos$results_span_detection$i/*biobert* $fiji_path$ignorance_base_all_data_corpus$obos$results_span_detection$i/
#

#
#    ##CONCEPT NORM FILES
#    #remove the *combo* and *DISC* files
#    rm $fiji_path$ignorance_base_all_data_corpus$obos$concept_norm_files$i/*combo*
#    rm $fiji_path$ignorance_base_all_data_corpus$obos$concept_norm_files$i/*DISC*
#
#    #add the gold standard
#    cp  $fiji_path$ignorance_question_work_full_corpus$obos$concept_norm_files$i/*biobert* $fiji_path$ignorance_base_all_data_corpus$obos$concept_norm_files$i/


#    ##RESULTS CONCEPT NORM FILES
#    #add the gold standard and change the name for the gold standard
#    cp $fiji_path$ignorance_question_work_full_corpus$obos$results_concept_norm_files$i/*pred.txt $fiji_path$ignorance_question_work_full_corpus$obos$results_concept_norm_files$i/$gs$i$results_concept_norm_files_ext
#
#    mv $fiji_path$ignorance_question_work_full_corpus$obos$results_concept_norm_files$i/$gs$i$results_concept_norm_files_ext $fiji_path$ignorance_base_all_data_corpus$obos$results_concept_norm_files$i/


    ##CONCEPT SYSTEM OUTPUT gold standard
    cp $fiji_path$ignorance_question_work_full_corpus$obos$concept_system_output$i/*biobert* $fiji_path$ignorance_base_all_data_corpus$obos$concept_system_output$i/

    ##CONCEPT SYSTEM OUTPUT automated data corpus
    cp $fiji_path$ignorance_base_corpus$obos$concept_system_output$i/*biobert* $fiji_path$ignorance_base_all_data_corpus$obos$concept_system_output$i/




done