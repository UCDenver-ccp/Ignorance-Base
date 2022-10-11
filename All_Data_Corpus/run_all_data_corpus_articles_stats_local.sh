#!/usr/bin/env bash

##path to the main craft documents for training
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'

corpus_path='/Ignorance-Question-Corpus/'


new_articles_path='Ignorance-Question-Work-Full-Corpus/New_Articles/'
ignorance_base_all_data_corpus_path='Ignorance-Base/All_Data_Corpus/'
ignorance_local_path='3_Ignorance_Base/'
knowtator_projects='z_KNOWTATOR_PROJECTS/'
all_data_results='ALL_DATA_RESULTS/'
output_results='Word_Analysis_Output_Results/'

##folder to the articles within the craft path
articles='Articles/' #want files.txt

##folder to the concept annotations within the craft path
concept_annotation='Annotations/'

##section info path
section_info_path='section_info_BioC/'
section_format='BioC-sections'

##list of ontologies that have annotations to preproess
ontologies='full_unknown,explicit_question,incomplete_evidence,probable_understanding,superficial_relationship,future_work,future_prediction,important_consideration,anomaly_curious_finding,alternative_options_controversy,difficult_task,problem_complication,question_answered_by_this_work,0_all_combined,1_binary_combined'

##output path for the BIO- format files that are tokenized
eval_path='Ignorance-Question-Work-Full-Corpus/Word_Analysis/Held_Out_Evaluation/'

##folder name for sentence files
pmcid_sentence_files_path='PMCID_files_sentences/' #the sentence files for the PMC articles'
tokenized_files='Tokenized_Files/' #preprocessed article files to be word tokenized for BIO- format

preprocess_corpus='Ignorance-Question-Work-Full-Corpus/Preprocess_Corpus/'

corpus_construction='Ignorance-Question-Work-Full-Corpus/Corpus_Construction/'
iaa_calculations='IAA_calculations/'

##corpus name - craft here
corpus='ignorance'
all_lcs_path='Ontologies/Ontology_Of_Ignorance_all_cues_2021-07-30.txt'

all_files='all'

##existant summary stuff
eval_preprocess_summary_files='eval_preprocess_article_summary'



##copy the all_lcs_path!
#cp $fiji_path$corpus_path$all_lcs_path $fiji_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$all_data_results$all_lcs_path

##get BioC information from API
#python3 $fiji_path$corpus_construction$iaa_calculations/collect_BioC_section_info.py -article_path=$fiji_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$all_data_results$articles -save_xml_path=$fiji_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$all_data_results$section_info_path


##run gold standard summary
#python3 $all_file_path$corpus_construction$iaa_calculations/gold_standard_summary_stats.py -gs_path=$all_file_path$ignorance_local_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$all_data_results -article_path=$articles -annotation_path=$concept_annotation -all_lcs_path=$all_lcs_path -section_info_path=$section_info_path -section_format=$section_format

#
#
###preprocess the docs to get the pmcid sentence files so we have the ignorance statements vs not
#python3 $all_file_path$preprocess_corpus/preprocess_docs.py -craft_path=$fiji_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$all_data_results -articles=$articles -concept_annotation=$concept_annotation -ontologies=$ontologies -output_path=$fiji_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$all_data_results$tokenized_files -pmcid_sentence_path=$pmcid_sentence_files_path -corpus=$corpus --all_lcs_path=$fiji_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$all_data_results$all_lcs_path
#
#
#
python3 $all_file_path$new_articles_path/new_article_stats.py -corpus_path=$all_file_path$ignorance_local_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$all_data_results -article_path=$articles -annotation_path=$concept_annotation -all_lcs_path=$all_lcs_path -pmcid_sentence_file_path=$pmcid_sentence_files_path