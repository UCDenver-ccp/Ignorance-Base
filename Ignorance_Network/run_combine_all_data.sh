#!/usr/bin/env bash

##path to the main craft documents for training
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'

ignorance_base='3_Ignorance_Base/Ignorance-Base/'
all_data_corpus='All_Data_Corpus/'

articles='Articles/' #want files.txt
articles_metadata='Articles_metadata/'
pmcid_sentence_files_path='PMCID_files_sentences/' #the sentence files for the PMC articles'
section_info_path='section_info_BioC/'
section_format='BioC-sections'

word_results='Word_Analysis_Output_Results/'
knowtator_projects='z_KNOWTATOR_PROJECTS/'
all_data_results='ALL_DATA_RESULTS/'
ignorance_bionlp_files='z_BIONLP_BEST_MODELS/'

ignorance_network='Ignorance_Network/'
sentence_output='ALL_DATA_COMBINED_ignorance_sentences/'
dictionary_output='ALL_DATA_COMBINED_ignorance_dictionary_files/'

all_lcs_path='Ontologies/Ontology_Of_Ignorance_all_cues_2021-07-30.txt'

##list of ontologies that have annotations to preproess
ignorance_ontologies='full_unknown,explicit_question,incomplete_evidence,probable_understanding,superficial_relationship,future_work,future_prediction,important_consideration,anomaly_curious_finding,alternative_options_controversy,difficult_task,problem_complication,question_answered_by_this_work'

all_combined_data='0_all_combined/'
it_occurence_count=1

included_articles='all'

##copy all the meta files to our all data corpus
old_metadata_folder='1_First_Full_Annotation_Task_9_13_19/document_collection_pre_natal/'
meta='.meta'
#cp $all_file_path$old_metadata_folder/*.meta $all_file_path$ignorance_base$all_data_corpus$articles_metadata/

python3 combine_all_data.py -all_lcs_path=$all_file_path$ignorance_base$all_data_corpus$word_results$knowtator_projects$all_data_results$all_lcs_path -included_articles=$included_articles -ignorance_ontologies=$ignorance_ontologies -sentence_file_path=$all_file_path$ignorance_base$all_data_corpus$pmcid_sentence_files_path -bionlp_file_path=$all_file_path$ignorance_base$all_data_corpus$word_results$ignorance_bionlp_files -sentence_output_folder=$all_file_path$ignorance_base$ignorance_network$sentence_output -dictionary_output_folder=$all_file_path$ignorance_base$ignorance_network$dictionary_output -all_combined_data=$all_combined_data -it_occurence_count=$it_occurence_count -output_folder=$all_file_path$ignorance_base$ignorance_network -meta_data_article_file_path=$all_file_path$ignorance_base$all_data_corpus$articles_metadata
