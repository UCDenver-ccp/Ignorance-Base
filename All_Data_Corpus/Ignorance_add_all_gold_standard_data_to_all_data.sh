#!/usr/bin/env bash

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
gold_standard_annotation_results='GS_bionlp_articles_original/'
word_analysis_output_results='Word_Analysis_Output_Results/'
articles='Articles/'

results_span_detection='Results_span_detection/'
preprocess_corpus='Preprocess_Corpus/'
output_folders='Output_Folders/'
word_analysis='Word_Analysis/'
held_out_evaluation='Held_Out_Evaluation/'
tokenized_files='Tokenized_Files/'
training_tokenized_files='Training_Tokenized_Files/'
pmcid_sentence_files='PMCID_files_sentences/'
training_pmcid_sentence_files='Training_PMCID_files_sentences/'
##the full concept recognition output folder
concept_system_output='concept_system_output/'
biobert='BIOBERT'
z_bionlp_output_format='z_BIONLP_OUTPUT_FORMAT/'


##MOVE EVERYTHING FROM GOLD STANDARD TO ALL DATA CORPUS!

##copy all of the articles
cp $fiji_path$ignorance_corpus$articles/* $fiji_path$ignorance_base_all_data_corpus$articles


##copy all of the pmcid sentence files from held out evaluation
cp $fiji_path$ignorance_question_work_full_corpus$word_analysis$held_out_evaluation$pmcid_sentence_files/* $fiji_path$ignorance_base_all_data_corpus$pmcid_sentence_files

cp $fiji_path$ignorance_question_work_full_corpus$word_analysis$held_out_evaluation$training_pmcid_sentence_files /* $fiji_path$ignorance_base_all_data_corpus$pmcid_sentence_files


##copy all of the tokenized files
#remove the biobert stuff
#rm $fiji_path$ignorance_base_all_data_corpus$tokenized_files$biobert/*

#copy stuff over from held out evaluation
#cp $fiji_path$ignorance_question_work_full_corpus$word_analysis$held_out_evaluation$tokenized_files/* $fiji_path$ignorance_base_all_data_corpus$tokenized_files

#cp $fiji_path$ignorance_question_work_full_corpus$word_analysis$held_out_evaluation$training_tokenized_files/* $fiji_path$ignorance_base_all_data_corpus$tokenized_files


##copy all the gold standard annotation results
##from z_BIONLP_OUTPUT_FORMAT from preprocess corpus/output_folders
cp -r $fiji_path$ignorance_question_work_full_corpus$preprocess_corpus$output_folders$z_bionlp_output_format/* $fiji_path$ignorance_base_all_data_corpus$gold_standard_annotation_results



