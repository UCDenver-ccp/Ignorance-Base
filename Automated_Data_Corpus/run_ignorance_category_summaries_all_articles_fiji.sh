#!/usr/bin/env bash

##path to the main craft documents for training
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'

corpus_path='/Ignorance-Question-Corpus/'
corpus_name='Ignorance-Question-Corpus'


##folder to the articles within the craft path
articles='Articles/' #want files.txt


##list of ontologies that have annotations to preproess
ontologies='full_unknown,explicit_question,incomplete_evidence,probable_understanding,superficial_relationship,future_work,future_prediction,important_consideration,anomaly_curious_finding,alternative_options_controversy,difficult_task,problem_complication,question_answered_by_this_work'
#ontologies='0_all_combined'
#ontologies='1_binary_combined'

broad_categories='epistemics,barriers,levels_of_evidence,future_opportunities'


ignorance_base_path='3_Ignorance_Base/'
ignorance_base_corpus='Ignorance-Base/Automated_Data_Corpus/'
new_articles_path='Ignorance-Question-Work-Full-Corpus/New_Articles/'
output_results='Word_Analysis_Output_Results/'


##folder name for sentence files
pmcid_sentence_files_path='PMCID_files_sentences/' #the sentence files for the PMC articles'
tokenized_files='Tokenized_Files/' #preprocessed article files to be word tokenized for BIO- format



##list of excluded files from training: held out eval files for larger corpus
all_files='all'

ignorance_category_summary_output='Ignorance_Categories_Summaries/'
bionlp_best_models_folder='z_BIONLP_BEST_MODELS/'
knowtator_best_models_folder='z_KNOWTATOR_BEST_MODELS/'
best_algo='BEST'

python3 $fiji_path$new_articles_path/ignorance_category_summaries.py -ontologies=$ontologies -algos=$best_algo -bionlp_path=$scratch_path$ignorance_base_corpus$output_results$bionlp_best_models_folder -sentence_path=$scratch_path$ignorance_base_corpus$pmcid_sentence_files_path -output_path=$scratch_path$ignorance_base_corpus$output_results$ignorance_category_summary_output -evaluation_files=$all_files --article_path=$scratch_path$ignorance_base_corpus$articles