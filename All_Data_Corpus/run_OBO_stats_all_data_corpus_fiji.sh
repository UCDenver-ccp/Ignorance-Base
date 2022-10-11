#!/usr/bin/env bash

##path to the main craft documents for training
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'

##path to the evaluation files where all output will be stored during the evaluation
eval_path='Ignorance-Question-Work-Full-Corpus/OBOs/'
ignorance_corpus='Ignorance-Question-Corpus/'
ignorance_preprocess='Ignorance-Question-Work-Full-Corpus/Preprocess_Corpus/Output_Folders/'
ignorance_base_all_data_corpus='Ignorance-Base/All_Data_Corpus/'
output_results='Word_Analysis_Output_Results/'
obos='OBOs/'



##Folders for inputs and outputs
concept_system_output='concept_system_output/' #the folder for the final output of the full concept recognition run
article_folder='Articles/' #the folder with the PMC Articles text files
tokenized_files='Tokenized_Files/' #preprocessed article files to be word tokenized for BIO- format
obo_ignorance_overlap='OBO_ignorance_overlap/'
section_info_bioc='Word_Analysis_Output_Results/z_KNOWTATOR_PROJECTS/ALL_DATA_RESULTS/section_info_BioC/'
bioc_extension='.nxml.gz.txt.BioC-full_text.xml'

ignorance_ontology_file_path='Ontologies/Ontology_Of_Ignorance.owl'
ignorance_all_lcs_path='Ontologies/Ontology_Of_Ignorance_all_cues_2021-07-30.txt'

##list of ontologies that have annotations to preproess
ignorance_ontologies='full_unknown,explicit_question,incomplete_evidence,probable_understanding,superficial_relationship,future_work,future_prediction,important_consideration,anomaly_curious_finding,alternative_options_controversy,difficult_task,problem_complication,question_answered_by_this_work' #0_all_combined

ignorance_broad_categories='epistemics,barriers,levels_of_evidence,future_opportunities'

ignorance_extra_ontology_concepts="{'urgent_call_to_action':'important_consideration','than':'alternative_options_controversy','alternative_options':'alternative_options_controversy','is':'explicit_question','epistemics':'epistemics'}"



save_models_path='Models/SPAN_DETECTION/' #all the saved models for span detection
results_span_detection='Results_span_detection/' #results from the span detection runs
concept_norm_files='Concept_Norm_Files/' #the processed spans detected for concept normalization on the character level
pmcid_sentence_files_path='PMCID_files_sentences/' #the sentence files for the PMC articles
concept_annotation='concept-annotation/' #the concept annotations for CRAFT

##list of the ontologies of interest
OBO_ontologies="CHEBI,CL,GO_BP,GO_CC,GO_MF,MOP,NCBITaxon,PR,SO,UBERON"
#OBO_ontologies='CHEBI'

##list of the files to run through the concept recognition pipeline
all_files='all'

#all_files='PMC6000839'

OBO_model_dict="{'CHEBI':'BIOBERT','CL':'BIOBERT','GO_BP':'CRF','GO_CC':'BIOBERT','GO_MF':'BIOBERT','MOP':'BIOBERT','NCBITaxon':'CRF','PR':'BIOBERT','SO':'BIOBERT','UBERON':'BIOBERT'}"



python3 $fiji_path$eval_path/OBO_stats.py -OBO_bionlp_file_path=$fiji_path$ignorance_base_all_data_corpus$obos$concept_system_output -ignorance_ontologies=$ignorance_ontologies -ignorance_broad_categories=$ignorance_broad_categories -ignorance_all_lcs_path=$fiji_path$ignorance_corpus$ignorance_all_lcs_path -ignorance_extra_ontology_concepts=$ignorance_extra_ontology_concepts -ignorance_ontology_file_path=$fiji_path$ignorance_corpus$ignorance_ontology_file_path -ignorance_article_path=$fiji_path$ignorance_base_all_data_corpus$article_folder -ignorance_tokenized_files_path=$fiji_path$ignorance_base_all_data_corpus$tokenized_files -ignorance_sentence_folder_path=$fiji_path$ignorance_base_all_data_corpus$pmcid_sentence_files_path -OBO_ontologies=$OBO_ontologies -evaluation_files=$all_files -OBO_model_dict=$OBO_model_dict -OBO_output_path=$fiji_path$ignorance_base_all_data_corpus$obos -OBO_ignorance_overlap_path=$fiji_path$ignorance_base_all_data_corpus$obos$obo_ignorance_overlap -ignorance_date_info_path=$fiji_path$ignorance_base_all_data_corpus$section_info_bioc -ignorance_date_info_extension=$bioc_extension