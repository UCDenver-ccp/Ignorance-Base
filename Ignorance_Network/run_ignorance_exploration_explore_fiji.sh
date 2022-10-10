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
ignorance_ontologies_ordered='question_answered_by_this_work,full_unknown,explicit_question,incomplete_evidence,superficial_relationship,probable_understanding,anomaly_curious_finding,alternative_options_controversy,difficult_task,problem_complication,future_work,future_prediction,important_consideration'
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
#current_ignorance_multigraph='0_IGNORANCE_MULTIGRAPH_03_06_22.gpickle'


#full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_07_22.gpickle'
#full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_10_22.gpickle'
#full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_11_22.gpickle'
#full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_21_22.gpickle'
full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_23_22.gpickle'
preprocess_sentences_dict='0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_PREPROCESSED_SENTENCE_DICT.pkl'
all_sentences_dict='0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_ALL_SENTENCES_DICT.pkl'

#string_obo_concept_input_list="vitamin D"
#obo_id_list_full='PR_000014420,MONDO_0010619,PR_000010289,PR_000016990,PR_P29377,GO_0036378,PR_000004967,PR_Q15819,MONDO_0008660,PR_000029672,PR_P78562,PR_000006110,CHEBI_73558,MONDO_0004574,PR_000010284,PR_O60244,PR_O75448,PR_P05937,GO_0004879,PR_000010304,PR_Q02318,PR_000010296,PR_000010286,MONDO_0024300,PR_Q9Y2X0,PR_Q9NPJ6,GO_0009111,PR_Q9NVC6,PR_Q9UHV7,PR_Q9ULK4,PR_Q15648,PR_000010279,MONDO_0005520,CHEBI_28940,PR_Q9H3M7,PR_000010295,GO_0048018'
#obo_id_list='CHEBI_89324,CHEBI_73558,PR_Q02318,CHEBI_28940,PR_000006110,CHEBI_28934,CHEBI_27300'

exploration='EXPLORATION/'
vitamin_d_folder='Vitamin_D/'
clustering='clustering/'
enrichment='enrichment/'

##gather the correct obo_ids we want from string list
string_obo_concept_input_list="vitamin D"
obo_id_list_vitamin_D_Teri='CHEBI_27300,CHEBI_73558,CHEBI_28940,CHEBI_28934'
output_order='ARTICLE_DATE,NUM_IGNORANCE_CUES'

vitamin_D_ignorance_file_list='vitamin-D_CHEBI_27300_ignorance_statements_.txt,vitamin-D2_CHEBI_28934_ignorance_statements_.txt'

vitamin_D_not_ignorance_file_list='vitamin-D_CHEBI_27300_not_ignorance_statements.txt,vitamin-D2_CHEBI_28934_not_ignorance_statements.txt'

##echo $vitamin_D_ignorance_file_list
###PREPROCESS THE SPECIFIC FILES
python3 ignorance_exploration_explore_preprocess.py -ignorance_full_graph=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -specific_ignorance_statements_sentence_folder=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder -specific_ignorance_statements_file_list=$vitamin_D_ignorance_file_list -specific_not_ignorance_statements_sentence_folder=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder -specific_not_ignorance_statements_file_list=$vitamin_D_not_ignorance_file_list -preprocess_sentence_dict_path=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$preprocess_sentences_dict -all_sentences_dict_path=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$all_sentences_dict  -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder --obo_id_list=$obo_id_list_vitamin_D_Teri



##BIOSENT2VEC EXPLORATION
biosent2vec_model_file='BioSentVec_PubMed_MIMICIII-bigram_d700.bin'
ignorance_preprocessed_sentence_file='IGNORANCE_PREPROCESSED_SENTENCES.pkl'
ignorance_sentence_dict_file='IGNORANCE_SENTENCE_DICT.pkl'
not_ignorance_preprocessed_sentence_file='NOT_IGNORANCE_PREPROCESSED_SENTENCES.pkl'
not_ignorance_sentence_dict_file='NOT_IGNORANCE_SENTENCE_DICT.pkl'
all_article_summary='all_article_summary.txt'
kmeans_num_clusters='1,10,15,20'


##TODO: update this with more stuff and rerun!!!
#todo local
#python3 ignorance_exploration_explore_visualizations.py -processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$ignorance_preprocessed_sentence_file -not_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$not_ignorance_preprocessed_sentence_file -biosent2vec_model_file=$scratch_fiji_path$ignorance_base$ignorance_network$biosent2vec_model_file -kmeans_num_clusters=$kmeans_num_clusters -ignorance_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$ignorance_sentence_dict_file -not_ignorance_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$not_ignorance_sentence_dict_file -all_article_summary_file_path=$scratch_fiji_path$ignorance_base$all_data_corpus$all_article_summary --obo_id_list=$obo_id_list_vitamin_D_Teri -ignorance_categories=$ignorance_ontologies_ordered -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$clustering


##TODO: preprocess all of the vitamin D equivalent ones without the lexical cues to see the difference and do wordclouds of these
###PREPROCESS THE SPECIFIC FILES - NO IGNORANCE
no_ignorance='True'
python3 ignorance_exploration_explore_preprocess.py -ignorance_full_graph=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -specific_ignorance_statements_sentence_folder=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder -specific_ignorance_statements_file_list=$vitamin_D_ignorance_file_list -specific_not_ignorance_statements_sentence_folder=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder -specific_not_ignorance_statements_file_list=$vitamin_D_not_ignorance_file_list -preprocess_sentence_dict_path=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$preprocess_sentences_dict -all_sentences_dict_path=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$all_sentences_dict  -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder --obo_id_list=$obo_id_list_vitamin_D_Teri --no_ignorance=$no_ignorance

kmeans_num_clusters='1'
all_article_summary='all_article_summary.txt'
no_ignorance='no_ignorance'
underscore='_'
#todo local
#python3 ignorance_exploration_explore_visualizations.py -processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$no_ignorance$underscore$ignorance_preprocessed_sentence_file  -not_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$no_ignorance$underscore$not_ignorance_preprocessed_sentence_file  -biosent2vec_model_file=$scratch_fiji_path$ignorance_base$ignorance_network$biosent2vec_model_file -kmeans_num_clusters=$kmeans_num_clusters -ignorance_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$no_ignorance$underscore$ignorance_sentence_dict_file -not_ignorance_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$no_ignorance$underscore$not_ignorance_sentence_dict_file -all_article_summary_file_path=$scratch_fiji_path$ignorance_base$all_data_corpus$all_article_summary --obo_id_list=$obo_id_list_vitamin_D_Teri -ignorance_categories=$no_ignorance -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder


##IGNORANCE ENRICHMENT ANALYSIS VS NOT - VITAMIN D VS NOT - TO SHOW THE DIFFERENCE THAT IGNORANCE CAN MAKE
exposure_name='vitamin_d'
true='true'
python3 ignorance_exploration_explore_word_enrichment.py --obo_id_list=$obo_id_list_vitamin_D_Teri -exposure_name=$exposure_name -exposure_sentence_dict_file="$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$ignorance_sentence_dict_file,$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$not_ignorance_sentence_dict_file" -not_exposure_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$all_sentences_dict --all_sentence_comparison=$true -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/

##preprocessed exposure stuff
#-exposure_processed_sentences="$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$ignorance_preprocessed_sentence_file,$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$not_ignorance_preprocessed_sentence_file" -not_exposure_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$preprocess_sentences_dict


##preprocess the obo_ids enriched to also see with no ignorance
all='all'
none='none'
specific_obo_ids='specific_obo_ids/'
obo_enrichment_file='0_VITAMIN_D_SENTENCE_OBO_ID_ENRICHMENT_P_VALUES.txt'
no_ignorance='True'
python3 ignorance_exploration_explore_preprocess.py -ignorance_full_graph=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -specific_ignorance_statements_sentence_folder=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/ -specific_ignorance_statements_file_list=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$obo_enrichment_file -specific_not_ignorance_statements_sentence_folder=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/ -specific_not_ignorance_statements_file_list=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$obo_enrichment_file -preprocess_sentence_dict_path=$none -all_sentences_dict_path=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$all_sentences_dict  -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --obo_id_list=$obo_id_list_vitamin_D_Teri --exposure_name=$exposure_name --no_ignorance=$no_ignorance


kmeans_num_clusters='1'
all_article_summary='all_article_summary.txt'
no_ignorance='no_ignorance'
underscore='_'
#todo local
#python3 ignorance_exploration_explore_visualizations.py -processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --processed_sentences_ext=$ignorance_preprocessed_sentence_file -not_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --not_processed_sentences_ext=$not_ignorance_preprocessed_sentence_file -biosent2vec_model_file=$scratch_fiji_path$ignorance_base$ignorance_network$biosent2vec_model_file -kmeans_num_clusters=$kmeans_num_clusters -ignorance_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --ignorance_sentence_dict_file_ext=$ignorance_sentence_dict_file -not_ignorance_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --not_ignorance_sentence_dict_file_ext=$not_ignorance_sentence_dict_file -all_article_summary_file_path=$scratch_fiji_path$ignorance_base$all_data_corpus$all_article_summary --obo_id_list=$obo_id_list_vitamin_D_Teri -ignorance_categories=$no_ignorance -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids






##IGNORANCE CATEGORY ENRICHMENT OVER ALL IGNORANCE SENTENCES
exposure_name='ignorance_category'
true='true'
python3 ignorance_exploration_explore_word_enrichment.py --ignorance_categories_list=$ignorance_ontologies -exposure_name=$exposure_name -exposure_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$ignorance_sentence_dict_file -not_exposure_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$all_sentences_dict --all_sentence_comparison=$true -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/

##-exposure_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$ignorance_preprocessed_sentence_file -not_exposure_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$preprocess_sentences_dict


##OTHER WORD ENRICHMENT ANALYSIS IN IGNORANCE
word_enrichment_list="['obesity', 'iron', 'calcium', 'supplement', 'development', 'sclerosis', 'sun', 'ultraviolet', 'zinc', 'birthweight', 'rural', 'diet', 'schizophrenia', 'micronutrient', 'absorbed', 'absorption', 'multivitamin', 'allergies', 'atopy', 'environment', 'latitud', 'ambient', 'exposure', 'radiation', 'antioxidant', 'fetus', 'status', 'gestation']"
exposure_name='word_ignorance'

python3 ignorance_exploration_explore_word_enrichment.py --obo_id_list=$obo_id_list_vitamin_D_Teri --word_enrichment_list="$word_enrichment_list" -exposure_name=$exposure_name -exposure_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$ignorance_sentence_dict_file -not_exposure_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$not_ignorance_sentence_dict_file -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/

#-exposure_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$ignorance_preprocessed_sentence_file -not_exposure_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$not_ignorance_preprocessed_sentence_file


##TODO: explore the specific enriched OBOs
#preprocess the files
exposure_name='word_ignorance'
all='all'
none='none'
specific_obo_ids='specific_obo_ids/'
obo_enrichment_file='0_WORD_IGNORANCE_SENTENCE_OBO_ID_ENRICHMENT_P_VALUES.txt'

python3 ignorance_exploration_explore_preprocess.py -ignorance_full_graph=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -specific_ignorance_statements_sentence_folder=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/ -specific_ignorance_statements_file_list=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$obo_enrichment_file -specific_not_ignorance_statements_sentence_folder=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/ -specific_not_ignorance_statements_file_list=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$obo_enrichment_file -preprocess_sentence_dict_path=$none -all_sentences_dict_path=$scratch_fiji_path$ignorance_base$ignorance_network$all_data_graphs$all_sentences_dict  -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --obo_id_list=$obo_id_list_vitamin_D_Teri --exposure_name=$exposure_name

##TODO: create wordclouds for the preprocessed sentences
kmeans_num_clusters='1'
all_article_summary='all_article_summary.txt'
#todo local
#python3 ignorance_exploration_explore_visualizations.py -processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --processed_sentences_ext=$ignorance_preprocessed_sentence_file -not_processed_sentences=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --not_processed_sentences_ext=$not_ignorance_preprocessed_sentence_file -biosent2vec_model_file=$scratch_fiji_path$ignorance_base$ignorance_network$biosent2vec_model_file -kmeans_num_clusters=$kmeans_num_clusters -ignorance_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --ignorance_sentence_dict_file_ext=$ignorance_sentence_dict_file -not_ignorance_sentence_dict_file=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids --not_ignorance_sentence_dict_file_ext=$not_ignorance_sentence_dict_file -all_article_summary_file_path=$scratch_fiji_path$ignorance_base$all_data_corpus$all_article_summary --obo_id_list=$obo_id_list_vitamin_D_Teri -ignorance_categories=$ignorance_ontologies_ordered -output_path=$scratch_fiji_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder$enrichment$exposure_name/$specific_obo_ids

