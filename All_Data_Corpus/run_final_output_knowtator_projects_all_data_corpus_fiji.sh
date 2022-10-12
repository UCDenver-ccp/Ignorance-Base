#!/usr/bin/env bash

##path to the main craft documents for training
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'


corpus_path='/Ignorance-Question-Corpus/'
corpus_name='Ignorance-Question-Corpus'


##folder to the articles within the craft path
articles='Articles/' #want files.txt

##folder to the concept annotations within the craft path
concept_annotation='Annotations/'
all_lcs_path='Ontologies/Ontology_Of_Ignorance_all_cues_2021-07-30.txt'
ontology_file_path='Ontologies/Ontology_Of_Ignorance.owl'
ontology_folder='Ontologies/'
profiles_folder='Profiles/'


##list of ontologies that have annotations to preproess
ontologies='full_unknown,explicit_question,incomplete_evidence,probable_understanding,superficial_relationship,future_work,future_prediction,important_consideration,anomaly_curious_finding,alternative_options_controversy,difficult_task,problem_complication,question_answered_by_this_work,1_binary_combined,0_all_combined'
#ontologies='0_all_combined'
#ontologies='1_binary_combined'

broad_categories='epistemics,barriers,levels_of_evidence,future_opportunities'


best_model_dict="{'CRF':['full_unknown','difficult_task'],'BIOBERT':['explicit_question','incomplete_evidence','probable_understanding','superficial_relationship','future_work','future_prediction','important_consideration','anomaly_curious_finding','alternative_options_controversy','problem_complication','question_answered_by_this_work']}"

##output path for the BIO- format files that are tokenized
eval_path='Ignorance-Question-Work-Full-Corpus/Word_Analysis/Held_Out_Evaluation/'
new_articles='Ignorance-Question-Work-Full-Corpus/New_Articles/'
ignorance_base_all_data_corpus_path='Ignorance-Base/All_Data_Corpus/'
ignorance_base_path='3_Ignorance_Base/'
ignorance_base_corpus='Ignorance-Base/Automated_Data_Corpus/'
output_results='Word_Analysis_Output_Results/'


##folder name for sentence files
pmcid_sentence_files_path='PMCID_files_sentences/' #the sentence files for the PMC articles'
tokenized_files='Tokenized_Files/' #preprocessed article files to be word tokenized for BIO- format

preprocess_corpus='Ignorance-Question-Work-Full-Corpus/Preprocess_Corpus/Output_Folders/'

corpus_construction='Ignorance-Question-Work-Full-Corpus/Corpus_Construction/'

##corpus name - craft here
corpus='ignorance'



##list of excluded files from training: held out eval files for larger corpus
all_files='all'



###the algo and the corresponding results file
algos='CRF,BIOBERT'
#algos='BIOBERT'
#results_folders='BioBERT_Classification_Results'
results_folders='CRF_Classification_Results,BioBERT_Classification_Results'
bionlp_folder='z_BIONLP_OUTPUT_FORMAT/'
knowtator_folder='z_KNOWTATOR_OUTPUT_FORMAT/'
separate_all_combined_output='13_separate_combined'
bionlp_best_models_folder='z_BIONLP_BEST_MODELS/'
knowtator_best_models_folder='z_KNOWTATOR_BEST_MODELS/'
file_types=''
best_algo='BEST'


#python3 $fiji_path$new_articles/final_output_combine_best_models.py -ontologies=$ontologies -algos=$algos -result_folders=$results_folders -results_path=$scratch_path$ignorance_base_corpus$output_results -output_path=$scratch_path$ignorance_base_corpus$output_results$bionlp_best_models_folder -evaluation_files=$all_files -best_model_type=$bionlp_folder$separate_all_combined_output -best_model_dict=$best_model_dict --article_path=$scratch_path$ignorance_base_corpus$articles
#
#
#

##create a knowtator file
#python3 $fiji_path$eval_path/final_output_knowtator_format.py -ontologies=$ontologies -all_lcs_path=$fiji_path$corpus_path$all_lcs_path -ontology_file_path=$fiji_path$corpus_path$ontology_file_path -broad_categories=$broad_categories -article_path=$scratch_path$ignorance_base_corpus$articles -xml_folder=$knowtator_best_models_folder -bionlp_folder=$bionlp_best_models_folder -algos=$best_algo -result_folders=$results_folders -results_path=$scratch_path$ignorance_base_corpus$output_results -file_types=$file_types -evaluation_files=$all_files




##final knowtator project
knowtator_projects='z_KNOWTATOR_PROJECTS/'
model='ALL_DATA_RESULTS'
underscore='_'
article_ext='.nxml.gz.txt'
annotation_ext='.nxml.gz.xml.'
annotation_ext2='.xml'
profiles_file='Default.xml'
knowtator_ext='.knowtator'



mkdir $fiji_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$model
cd $fiji_path$ignorance_base_all_data_corpus_path$output_results$knowtator_projects$model/
##create all the files and folders for the knowtator project
mkdir $articles
mkdir $concept_annotation
mkdir $ontology_folder
mkdir $profiles_folder
cp $fiji_path$corpus_path/$corpus_name$knowtator_ext .
mv $corpus_name$knowtator_ext $model$knowtator_ext



#for e in "${eval[@]}"
#    do
        cp $fiji_path$ignorance_base_all_data_corpus_path$articles/*$article_ext $articles
        ##copy the annotation files from gold standard and from automated data corpus
        cp $fiji_path$ignorance_base_corpus$output_results$knowtator_best_models_folder/*$annotation_ext*$annotation_ext2  $concept_annotation
        cp $fiji_path$corpus_path$concept_annotation/*$annotation_ext*$annotation_ext2  $concept_annotation
        cp $fiji_path$corpus_path$ontology_file_path $ontology_folder
        cp $fiji_path$corpus_path$profiles_folder$profiles_file $profiles_folder


#    done
