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
#current_ignorance_multigraph='0_IGNORANCE_MULTIGRAPH_03_06_22.gpickle'
#full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_07_22.gpickle'
#full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_10_22.gpickle'
#full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_11_22.gpickle'
#full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_21_22.gpickle'
full_ignorance_graph='0_FULL_IGNORANCE_MULTIGRAPH_03_23_22.gpickle'

string_obo_concept_input_list="vitamin D"
#obo_id_list_full='PR_000014420,MONDO_0010619,PR_000010289,PR_000016990,PR_P29377,GO_0036378,PR_000004967,PR_Q15819,MONDO_0008660,PR_000029672,PR_P78562,PR_000006110,CHEBI_73558,MONDO_0004574,PR_000010284,PR_O60244,PR_O75448,PR_P05937,GO_0004879,PR_000010304,PR_Q02318,PR_000010296,PR_000010286,MONDO_0024300,PR_Q9Y2X0,PR_Q9NPJ6,GO_0009111,PR_Q9NVC6,PR_Q9UHV7,PR_Q9ULK4,PR_Q15648,PR_000010279,MONDO_0005520,CHEBI_28940,PR_Q9H3M7,PR_000010295,GO_0048018'
#obo_id_list='CHEBI_89324,CHEBI_73558,PR_Q02318,CHEBI_28940,PR_000006110,CHEBI_28934,CHEBI_27300'

exploration='EXPLORATION/'
vitamin_d_folder='Vitamin_D/'


##gather the correct obo_ids we want from string list
string_obo_concept_input_list="vitamin D"
##exact match
python3 ignorance_exploration_gather_data.py -ignorance_full_graph=$all_file_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -pheknowlator_node_info=$all_file_path$ignorance_base$ignorance_network$pheknowlator_node_info --string_obo_concept_input_list="$string_obo_concept_input_list" -output_path=$all_file_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder
##not exact match

false='False'
python3 ignorance_exploration_gather_data.py -ignorance_full_graph=$all_file_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -pheknowlator_node_info=$all_file_path$ignorance_base$ignorance_network$pheknowlator_node_info --string_obo_concept_input_list="$string_obo_concept_input_list" -output_path=$all_file_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder --string_exact_match=$false



##gather the sentences from the obo_ids
obo_id_list_vitamin_D_Teri='CHEBI_27300,CHEBI_73558,CHEBI_28940,CHEBI_28934'
#python3 ignorance_exploration_gather_data.py -ignorance_full_graph=$all_file_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -pheknowlator_node_info=$all_file_path$ignorance_base$ignorance_network$pheknowlator_node_info --obo_concept_input_list=$obo_id_list_vitamin_D_Teri -output_path=$all_file_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder



##specific ignorance categories and obo_ids
#specific_ignorance_categories='full_unknown,
#python3 ignorance_exploration_gather_data.py -ignorance_full_graph=$all_file_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -pheknowlator_node_info=$all_file_path$ignorance_base$ignorance_network$pheknowlator_node_info --obo_concept_input_list=$obo_id_list_vitamin_D_Teri -output_path=$all_file_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder --specific_ignorance_categories=$ignorance_ontologies



##output order
output_order='ARTICLE_DATE,NUM_IGNORANCE_CUES'
#python3 ignorance_exploration_gather_data.py -ignorance_full_graph=$all_file_path$ignorance_base$ignorance_network$all_data_graphs$full_ignorance_graph -pheknowlator_node_info=$all_file_path$ignorance_base$ignorance_network$pheknowlator_node_info --obo_concept_input_list=$obo_id_list_vitamin_D_Teri -output_path=$all_file_path$ignorance_base$ignorance_network$exploration$vitamin_d_folder --specific_ignorance_categories=$ignorance_ontologies --output_order=$output_order