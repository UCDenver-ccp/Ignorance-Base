#!/usr/bin/env bash

##path to the main craft documents for training
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
scratch_fiji_path='/scratch/Users/mabo1182/'

ignorance_base='Ignorance-Base/'
all_data_corpus='All_Data_Corpus/'

articles='Articles/' #want files.txt
articles_metadata='Articles_metadata/'
pmcid_sentence_files_path='PMCID_files_sentences/' #the sentence files for the PMC articles'
section_info_path='section_info_BioC/'
section_format='BioC-sections'
article_summary_path='all_article_summary.txt'

word_results='Word_Analysis_Output_Results/'
knowtator_projects='z_KNOWTATOR_PROJECTS/'
all_data_results='ALL_DATA_RESULTS/'
ignorance_bionlp_files='z_BIONLP_BEST_MODELS/'

ignorance_network='Ignorance_Network/'
sentence_output='ALL_DATA_COMBINED_ignorance_sentences/'
ignorance_dictionary_output='ALL_DATA_COMBINED_ignorance_dictionary_files/'
pmcid_date_info='PMCID_date_info.txt'
all_data_visualization='ALL_DATA_VISUALIZATION/'
all_data_graphs='ALL_DATA_GRAPHS/'

all_lcs_path='Ontologies/Ontology_Of_Ignorance_all_cues_2021-07-30.txt'

##list of ontologies that have annotations to preproess
ignorance_ontologies='full_unknown,explicit_question,incomplete_evidence,probable_understanding,superficial_relationship,future_work,future_prediction,important_consideration,anomaly_curious_finding,alternative_options_controversy,difficult_task,problem_complication,question_answered_by_this_work'
broad_categories="['LEVELS_OF_EVIDENCE','BARRIERS','FUTURE_OPPORTUNITIES']"
broad_categories_dict="{'LEVELS_OF_EVIDENCE':['FULL_UNKNOWN','EXPLICIT_QUESTION','INCOMPLETE_EVIDENCE','PROBABLE_UNDERSTANDING','SUPERFICIAL_RELATIONSHIP'],'BARRIERS':['ALTERNATIVE_OPTIONS_CONTROVERSY','DIFFICULT_TASK','PROBLEM_COMPLICATION'],'FUTURE_OPPORTUNITIES':['FUTURE_PREDICTION','FUTURE_WORK','IMPORTANT_CONSIDERATION']}"
old_ignorance_types_dict="{'ALTERNATIVE_OPTIONS':'ALTERNATIVE_OPTIONS_CONTROVERSY','FUTURE_OPPORTUNITIES':'FUTURE_WORK'}"

all_combined_data='0_all_combined/'
it_occurence_count=1

included_articles='all'

##copy all the meta files to our all data corpus
old_metadata_folder='1_First_Full_Annotation_Task_9_13_19/document_collection_pre_natal/'
meta='.meta'

##combine all obos per pmcid
OBO_ontologies='CHEBI,CL,GO_BP,GO_CC,GO_MF,MOP,NCBITaxon,PR,SO,UBERON'
OBO_EXT_ontologies='CHEBI_EXT,CL_EXT,GO_BP_EXT,GO_CC_EXT,GO_MF_EXT,MOP_EXT,NCBITaxon_EXT,PR_EXT,SO_EXT,UBERON_EXT'
obos='OBOs/'
concept_system_output='concept_system_output/'
obos_bionlp_files='z_BIONLP_BEST_MODELS_OBOs/'
obos_ext_bionlp_files='z_BIONLP_BEST_MODELS_OBOs_EXT/'
obos_sentence_output='ALL_DATA_COMBINED_OBOs_sentences/'
obos_dictionary_output='ALL_DATA_COMBINED_OBOs_dictionary_files/'
obos_ext_dictionary_output='ALL_DATA_COMBINED_OBOs_EXT_dictionary_files/'
obos_all_combined_data='0_all_combined_OBOs/'
obos_ext_all_combined_data='0_all_combined_OBOs_EXT/'
#/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/Negacy_seq_2_seq_NER_model/Concept-Recognition-as-Translation/Output_Folders/Concept_Norm_Files/GO_BP/full_files
negacy_full_files='Negacy_seq_2_seq_NER_model/Concept-Recognition-as-Translation/Output_Folders/Concept_Norm_Files/'

pheknowlator_graph_file='PheKnowLator_v3.0.2_full_subclass_relationsOnly_OWLNETS_SUBCLASS_purified_NetworkxMultiDiGraph.gpickle'
pheknowlator_node_info='PheKnowLator_v3.0.2_full_subclass_relationsOnly_OWLNETS_SUBCLASS_purified_NodeLabels.txt'
#current_ignorance_graph='0_IGNORANCE_GRAPH_03_04_22.gpickle'
##CREATE IGNORANCE GRAPH FROM SCRATCH!
#python3 create_ignorance_network.py -ignorance_ontologies=$ignorance_ontologies -ignorance_broad_categories=$broad_categories -ignorance_broad_categories_dict=$broad_categories_dict -old_ignorance_types_dict=$old_ignorance_types_dict -included_articles=$included_articles -article_path=$all_file_path$ignorance_base$all_data_corpus$articles -all_lcs_path=$all_file_path$ignorance_base$all_data_corpus$word_results$knowtator_projects$all_data_results$all_lcs_path -working_directory=$all_file_path$ignorance_base$ignorance_network -pmcid_date_info_path=$pmcid_date_info -corpus_path=$all_file_path$ignorance_base$all_data_corpus -all_article_summary_path=$article_summary_path -ignorance_dictionary_folder=$all_file_path$ignorance_base$ignorance_network$ignorance_dictionary_output -pheknowlator_graph_path=$all_file_path$ignorance_base$ignorance_network$pheknowlator_graph_file -pheknowlator_node_info=$all_file_path$ignorance_base$ignorance_network$pheknowlator_node_info -OBO_ontologies=$OBO_ontologies -OBO_EXT_ontologies=$OBO_EXT_ontologies -OBO_dictionary_folder=$all_file_path$ignorance_base$ignorance_network$obos_dictionary_output -OBO_EXT_dictionary_folder=$all_file_path$ignorance_base$ignorance_network$obos_ext_dictionary_output -OBO_EXT_dictionary_folder=$all_file_path$negacy_full_files -OBO_original_file_path=$all_file_path$negacy_full_files  -visualization_output_path=$all_file_path$ignorance_base$ignorance_network$all_data_visualization -graph_output_path=$all_file_path$ignorance_base$ignorance_network$all_data_graphs

#current_ignorance_multigraph='0_IGNORANCE_MULTIGRAPH_03_06_22.gpickle'
#current_ignorance_multigraph='0_IGNORANCE_MULTIGRAPH_03_11_22.gpickle'
#current_ignorance_multigraph='0_IGNORANCE_MULTIGRAPH_03_21_22.gpickle'
current_ignorance_multigraph='0_IGNORANCE_MULTIGRAPH_03_23_22.gpickle'


##CREATE FULL IGNORANCE GRAPH FROM EXISTING IGNORANCE GRAPH
#python3 create_ignorance_network.py -ignorance_ontologies=$ignorance_ontologies -ignorance_broad_categories=$broad_categories -ignorance_broad_categories_dict=$broad_categories_dict -old_ignorance_types_dict=$old_ignorance_types_dict -included_articles=$included_articles -article_path=$all_file_path$ignorance_base$all_data_corpus$articles -all_lcs_path=$all_file_path$ignorance_base$all_data_corpus$word_results$knowtator_projects$all_data_results$all_lcs_path -working_directory=$all_file_path$ignorance_base$ignorance_network -pmcid_date_info_path=$pmcid_date_info -corpus_path=$all_file_path$ignorance_base$all_data_corpus -all_article_summary_path=$article_summary_path -ignorance_dictionary_folder=$all_file_path$ignorance_base$ignorance_network$ignorance_dictionary_output -pheknowlator_graph_path=$all_file_path$ignorance_base$ignorance_network$pheknowlator_graph_file -pheknowlator_node_info=$all_file_path$ignorance_base$ignorance_network$pheknowlator_node_info -OBO_ontologies=$OBO_ontologies -OBO_EXT_ontologies=$OBO_EXT_ontologies -OBO_dictionary_folder=$all_file_path$ignorance_base$ignorance_network$obos_dictionary_output -OBO_EXT_dictionary_folder=$all_file_path$ignorance_base$ignorance_network$obos_ext_dictionary_output -OBO_original_file_path=$all_file_path$negacy_full_files -visualization_output_path=$all_file_path$ignorance_base$ignorance_network$all_data_visualization -graph_output_path=$all_file_path$ignorance_base$ignorance_network$all_data_graphs --saved_ignorance_graph=$all_file_path$ignorance_base$ignorance_network$all_data_graphs$current_ignorance_multigraph


##PREPROCESS ALL THE SENTENCES IN OUR IGNORANCE-BASE GETTING RID OF LEXICAL CUES AND STOPWORDS
full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_23_22.gpickle'
python3 preprocess_ignorance_network.py -ignorance_full_graph=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -pheknowlator_node_info=$scratch_fiji_path$ignorance_base$ignorance_network$pheknowlator_node_info -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs