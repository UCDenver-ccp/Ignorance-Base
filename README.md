# Ignorance-Base
The ignorance-base combines biomedical concept classifiers and ignorance classifiers in order to understand the state of our scientific ignorance through two new exploration methods: (1) exploration of the ignorance-base by topic (exploration by topic) and (2) exploration of the ignorance-base by experimental results (exploration by experimental results).

Exploration by topic is called just EXPLORATION in our file system. Exploration by experimental results is called GENE_LIST_ENRICHMENT.

Clone this repository to create the ignorance-base from scratch or add more articles. 

If you do not want to do it from scratch, a full ignorance-base can be found in Ignorance_Network/ALL_DATA_GRAPHS/0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_ALL_SENTENCES_DICT.pkl.zip (you will need to unzip it). There is other supporting information in the file as well.


Our ignorance-base contains 1,643 articles with 91 having gold standard ignorance annotations (prefix GS) and 1,552 run automatically for ignorance identification. All 1,643 articles have automatic classification for the biomedical concepts to ten OBOs from CRAFT. The 91 have the OBOs run over them separately from the 1,552. Look at the powerpoint for more details on it and the data representation. 

A lot of our work was run on a supercomputer, FIJI, out of boulder to save time, space, and computing resources. There are two different environments we used and these can be found in Automated_Data_Corpus/Anaconda_Environments_for_FIJI/. Use the general_environment unless you are runnning BioBERT or OpenNMT, then use the other one. Many files have matching .sbatch files which are files to run the scripts on FIJI.

The ignorance-classifiers are based on our prior work that created the classifiers: https://github.com/UCDenver-ccp/Ignorance-Question-Work-Full-Corpus as well as the ignorance-corpus we created: https://github.com/UCDenver-ccp/Ignorance-Question-Corpus.
Please clone both of these repositories because we utilize python scripts from them for this work. 

The biomedical concept classifiers relies on our previous work found here: https://github.com/UCDenver-ccp/Concept-Recognition-as-Translation. Please close this repository. We connect our ignorance-graph with PheKnowLator: https://github.com/callahantiff/PheKnowLator.

Please put all these repositories in the same place. That will become the fiji_path or all_files_path variables below.



## Automated Data Corpus: The first step to creating the ignorance-base is to automatically run the classifiers over all of your articles in a text format.

0. We are working in the Automated_Data_Corpus/ folder. In general, everything is created automatically aside from the Aritcle/ folder, assuming that all of the github repositories mentioned above are dowloaded.  

1. Place all articles of interest in the Articles/ folder. There are already the 1,552 not gold standard ones there. All articles must be in txt format and have the suffix .nxml.gz.txt

2. Ignorance Classification Process: bash scripts to run
	
	a. preprocess_all_articles_fiji.sh: Splits the articles into sentences and words to create the input format for the classifiers. Outputs respectively to PMCID_files_sentences/ and Tokenized_Files/. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"

	b. span_detection_all_articles_fiji.sh: Runs span detection for the CRF and prepares the data for BioBERT. (BioBERT) needs a GPU to run. Output to Word_Analysis_Output_Results/CRF_Classification_Results/ for CRF and the BioBERT preprocessed data can be found at Tokenized_Files/BIOBERT/. This can take a whole day to run. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"

	c. fiji_run_biobert_all_articles_fiji.sh: Runs BioBERT classification on a GPU. Need to make sure that biobert_v1.0_pubmed_pmc is in Ignorance-Question-Work-Full-Corpus/Word_Analysis/BioBERT_Classification/. (Download and unzip it from here: https://drive.google.com/file/d/1jGUu2dWB1RaeXmezeJmdiPKQp3ZCmNb7/view). Outputs to Word_Analysis_Output_Results/CRF_Classification_Results/BioBERT_CLASSIFICATION/ignorance_category/BIOBERT/. This takes multiple days to run potentailly. Variables to change:

		i. all_file_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

	d. postprocess_BioBERT_all_data_all_articles_fiji.sh: Postprocess the BioBERT results (NER detokenize). Puts the output of BioBERT into the proper format for the rest of the steps. Outputs to Word_Analysis_Output_Results/CRF_Classification_Results/BioBERT_CLASSIFICATION/ignorance_category/BIOBERT/. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"


	e. final_output_formats_all_articles_fiji.sh: Takes all the output from the ignorance classifiers and converts it all to the formats .bionlp and the knowtator format. Outputs: /Word_Analysis_Output_Results/BioBERT_Classification_Results/z_BIONLP_OUTPUT_FORMAT/ and Word_Analysis_Output_Results/BioBERT_Classification_Results/z_KNOWTATOR_OUTPUT_FORMAT/ respectively. It also creates knowtator projects and this script will make folders as needed. Output is: Word_Analysis_Output_Results/z_KNOWTATOR_PROJECTS/. Variables to change:
		
		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"


	f. run_final_output_combine_best_models_all_articles.sh: This script picks out the best models for both formats and creates a knowtator project with them. Outputs: /Word_Analysis_Output_Results/z_BIONLP_BEST_MODELS/, /Word_Analysis_Output_Results/z_KNOWTATOR_BEST_MODELS/, and /Word_Analysis_Output_Results/z_KNOWTATOR_PROJECTS/. In creating the knowtator projects, this script will make folders as needed. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"

	g. run_ignorance_category_summaries_all_articles_fiji.sh: Creates summary files for the ignorance classificaiton information. Outputs to Word_Analysis_Output_Results/Ignorance_Categories_Summaries/. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"

3. Biomedical Concept Classication Process: bash scripts to run. We run only BioBERT it was the best model from our previous work for span detection for 10 ontologies from CRAFT. We are working in Automated_Data_Corpus/OBOs/ folder going forward. There are the regular OBOs and the exention OBOs (OBO_EXT). Many scripts run OBO and OBO_EXT separately with two different scripts. These scripts focus on the 1,552 articles. Overall, a lot of these steps take a while to run.

	a. Untar the OBOs folder system. In general the files are too big to upload so we provide the file system needed. Within Automated_Data_Corpus/ run (this will open all the correct folders within OBOs/): 

		tar -xzf OBOs.tar.gz

	b. run_CR_eval_pipeline_1_ignorance_all_articles.sh and run_CR_eval_pipeline_1_ignorance_all_articles_EXT.sh: The first step of the concept recognition pipeline that preprocesses all articles BioBERT. Outputs: Tokenized_Files/, PMCID_files_sentences/, PMCID_files_sentences_EXT, Results_span_detection/OBO/BIOBERT/. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"

		iv. code_path = the code path to the Concept-Recognition-as-Translation/Code/ Folder

	c. fiji_run_biobert_eval_ignorance_all_articles.sh (also partial ones for speed) and fiji_run_biobert_eval_ignorance_all_articles_EXT.sh: Runs BioBERT for all OBOs. Output: Results_span_detection/OBO/BIOBERT/. Variables to change:

		i. CR_models_base_path = the base path to Concept-Recognition-as-Translation/ folder

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. fiji_path = the path to all github repositories

	d. run_CR_eval_biobert_pipeline_1.5_ignorance_all_articles.sh and run_CR_eval_biobert_pipeline_1.5_ignorance_all_articles_EXT.sh: Postprocesses the BioBERT output to the correct format for concept normalization. Output: Results_span_detection/OBOs/. Also prepares data for concept normalization. Output: Concept_Norm_Files/OBOs/. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. CR_models_base_path = the base path to Concept-Recognition-as-Translation/ folder

	e. fiji_run_eval_open_nmt_ignorance_all_articles.sh and fiji_run_eval_open_nmt_ignorance_all_articles_EXT.sh: Runs the concept normalization pipeline with OpenNMT. Output: Results_concept_norm_files/OBOs/. Variables to change:

		i. CR_models_base_path = the base path to Concept-Recognition-as-Translation/ folder

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. fiji_path = the path to all github repositories

	f. run_CR_eval_pipeline_2_ignorance_all_articles.sh and run_CR_eval_pipeline_2_ignorance_all_articles_EXT.sh: Combines span detection and concept normalization results to the folder concept_system_output/OBO/. The output format is .bionlp.

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"

		iv. code_path = the code path to the Concept-Recognition-as-Translation/Code/ Folder




## All Data Corpus: Combining the gold standard data and the automated data corpus together. We also run summary statistics.

0. We are working in the All_Data_Corpus/ folder. 

1. Ignorance_move_all_data_to_combine.sh: Add the gold standard information and the automated information to the full data corpus (Articles, PMCID_sentence_files, and the bionlp files). Variables to change:
	
	a. fiji_path = the path to all github repositories.

2. OBOs_move_all_data_to_combine.sh: Add the gold standard and automated data corpus OBO and OBO_EXT information to the full data corpus (OBOs/concept_system_output/). Variables to change:

	a. fiji_path = the path to all github repositories.

3. run_combine_all_data_OBOs.sh: combine all the OBO data (OBOs/z_BIONLP_BEST_MODELS_OBOs/ and OBOs/z_BIONLP_BEST_MODELS_OBOs_EXT). Variables to change:
	
	a. all_file_path = the path to all github repositories.

4. run_fix_GS_bionlp_concept_numbers.sh: fixes the numbering for the concept annotations for the gold standard documents in Word_Analysis_Output_Results/z_BIONLP_BEST_MODELS/GS_

	a. all_file_path = the path to all github repositories.

5. run_final_output_knowtator_projects_all_data_corpus_fiji.sh: creates a knowtator project for full data corpus called ALL_DATA_RESULTS (Word_Analysis_Output_Results/z_KNOWTATOR_PROJECTS/ALL_DATA_RESULTS/). Variables to change:
	
	a. fiji_path = the path to all github repositories.

6. run_all_data_corpus_articles_stats.sh: creates summary files for the articles (all_article_summary.txt, eval_preprocess_article_summary.txt, Word_Analysis_Output_Results/z_KNOWTATOR_PROJECTS/ALL_DATA_RESULTS/gold_standard_summary[date].txt, lexical_cues_not_in_taxonomy.txt, sentence_type_counts.txt) including gathering the BioC metadata information (Word_Analysis_Output_Results/z_KNOWTATOR_PROJECTS/ALL_DATA_RESULTS/section_info_BioC/). Also creates PMCID sentence files and tokenized files for the knowtator project (Word_Analysis_Output_Results/z_KNOWTATOR_PROJECTS/ALL_DATA_RESULTS/). 
	
	a. fiji_path = the path to all github repositories.

7. run_OBO_stats_all_data_corpus_fiji.sh: creates summary files for the OBOs (OBOs/). Variables to change:
	
	a. fiji_path = the path to all github repositories.

8. run_unique_OBO_ids_list_all_corpus_fiji.sh: creates summary files per OBO for unique IDs in each (OBOs/concept_system_output/). Variables to change:

	a. fiji_path = the path to all github repositories.

9. run_OBO_unique_ids_summary.sh: Creates the summary file for all OBOs for unique IDs (OBOs/0_OBOS_UNIQUE_ID_SUMMARY_INFO.txt). Variables to change:
	
	a. all_file_path = the path to all github repositories.

10. run_ignorance_category_summaries_all_data_corpus_fiji.sh: creates ignorance category summaries (Word_Analysis_Output_Results/Ignorance_Categories_Summaries/). Variables to change:

	a. fiji_path = the path to all github repositories.





## Ignorance-Network

0. We are working in the Ignorance_Network/ folder. The ignorance-graph is too large to upload to GitHub, but we uploaded some supporting documents all in ALL_DATA_GRAPHS/: 0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_ALL_SENTENCES_DICT.pkl.zip, 0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_ALL_SENTENCES_DICT_IGNORANCE_FREQUENCIES.txt, 0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_PREPROCESSED_SENTENCE_DICT.pkl. 

1. run_combine_all_data.sh: Combines all the ignorance data and OBO/OBO_EXT data together into sentence and dictionary files ready to use in the creation of the ignorance-network. (ALL_DATA_COMBINED_ignorance_sentences/, ALL_DATA_COMBINED_ignorance_dictionary_files/, ALL_DATA_COMBINED_OBOs_sentences/, ALL_DATA_COMBINED_OBOs_dictionary_files/, ALL_DATA_COMBINED_OBOs_EXT_dictionary_files/). Variables to change:
	
	a. all_file_path = the path to all github repositories.

2. run_create_ignorance_network.sh: creates the ignorance-network and combines it with PheKnowLator to create the full ignorance-base with biomedical ontologies (ALL_DATA_GRAPHS/). Also preprocess all sentences in the ignorance-base in order to make downstream things easier (ALL_DATA_GRAPHS/0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_PREPROCESSED_SENTENCE_DICT.pkl). The preprocessing can take a very long time to run in general just FYI. You can either create the ignorance-base from scratch (current) or from an existing ignorance-graph (need to change variable current_ignorance_multigraph to the current one and unhighlight the python script below it). Variables to change:
	
	a. all_file_path = the path to all github repositories.

	b. current_ignorance_multigraph = if creating ignorance-base from an existing ignorance-graph, change this variable to the current ignorance-graph.

3. Exploration by Topic: Working in the EXPLORATION/ folder and our example is vitamin D in the Vitamin_D/ folder.
	
	a. ignorance_exploration_gather_data.sh: gather the data based on your search topic. Variables to change:

		i. all_file_path = the path to all github repositories.

		ii. vitamin_d_folder = our example topic folder name, feel free to change and create a different folder name.

		iii. full_ignorance_graph = the current full ignorance graph you are using

		iv. string_obo_concept_input_list = the list of topic strings to use to search for OBO terms. (choose exact match or not by --string_exact_match)

		v. obo_id_list_vitamin_D_Teri = the obo concepts we chose to use for our vitamin D example (feel free to change the name of the variable too)

		vi. specific_ignorance_categories = if interested in specific ignorance categories like 'full_unknown', use the variable and script below it to gather data just for that category.

		vii. output_order = if interested in outputting the data in a specific order, use this variable to choose that (e.g. ARTICLE_DATE, NUM_IGNORANCE_CUES).

	b. run_ignorance_exploration_explore.sh: run the exploration for our vitamin D example. Ignorance frequencies for the full network and just vitamin D sentences (ALL_DATA_GRAPHS/0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_ALL_SENTENCES_DICT_IGNORANCE_FREQUENCIES.txt and IGNORANCE_SENTENCE_DICT_IGNORANCE_FREQUENCIES.txt). Preprocess sentences for the full network and just vitamin D (all files ending in \_IGNORANCE_PREPROCESSED_SENTENCES.pkl, \_IGNORANCE_SENTENCE_DICT.pkl in ALL_DATA_GRAPHS/ as well). Visualizations including clustering (kmeans, hierarchical, tsne, pca), wordclouds, and bubble plots (clustering/ and enrichment/vitamin_D/specific_obo_ids/ and enrichment/word_ignorance/specific_obo_ids/). Enrichment for vitamin D vs not (enrichment/vitamin_D/), for the ignorance categories (enrichment/ignorance_category/), and for terms both words and OBO concepts (enrichment/word_ignorance/). Variables to change:

		i. all_file_path/scratch_fiji_path = the path to all github repositories.

		ii. vitamin_d_folder = our example topic folder name, feel free to change and create a different folder name.

		iii. full_ignorance_graph = the current full ignorance graph you are using

		iv. string_obo_concept_input_list = the list of topic strings to use to search for OBO terms. (choose exact match or not by --string_exact_match)

		v. obo_id_list_vitamin_D_Teri = the obo concepts we chose to use for our vitamin D example (feel free to change the name of the variable too)

		vi. vitamin_D_ignorance_file_list = a list of the ignorance files

		vii. vitamin_D_not_ignorance_file_list = a list of the not ignorance files

		viii. word_enrichment_list = a list of words to test for enrichment. These are related to our topic of vitamin D right now.

4. Exploration by experimental results (gene list ignorance enrichment): Working in the GENE_LIST_ENRICHMENT/ folder and our example is a vitamin D and spontaneous preterm birth gene list.

	a. run_ignorance_gene_list_enrichment.sh: Searches for the gene list OBOs (vitamin_D_gene_list_all_OBO_ids.txt abnd 3 files that begin with vitamin_D_gene_list_OBO_ids). The same analyses from exploration by topic (all in the EXPLORATION/Vitamin_D/ folders with clustering/ and enrichment/). We also add the gene list focused analyses (EXPLORATION/Vitamin_D/gene_list_focus/). Check all variables near the python scripts in the bash file. Some variables to change: 

		i. all_file_path/scratch_fiji_path = the path to all github repositories.

		ii. full_ignorance_graph = the current full ignorance graph you are using

		iii. preprocess_sentences_dict = the preprocessed sentence dict based on the ignorance graph name

		iv. all_sentences_dict = the sentence dict based on the ignorance graph name

		v. gene_list = the gene list of entrez gene IDs you want to explore (the 43 vitamin D ones we have now)

		vi. vitamin_D_gene_list_info = the file with all the gene list information

		vii. vitamin_D_gene_list = the gene list txt file with one gene per line of the file

		viii. pheknowlator_obo_ontologies = the ontologies to search for in PheKnowLator (the ones that overlap with CRAFT for now)

		ix. vitamin_d_folder = our example topic folder name, feel free to change and create a different folder name.

## Ignorance-base data representation: PheKnowLator and Ignorance-Graph

1. PheKnowLator information: https://github.com/callahantiff/PheKnowLator

	a. Entities from Ontologies of interest (showing Namespace, then URL):

		• Genes -- Entrez ( http://www.ncbi.nlm.nih.gov/gene/)

		• GO (GO_;  http://purl.obolibrary.org/obo/) 

		• ChEBI (CHEBI_;  http://purl.obolibrary.org/obo/) 

		• SO (SO_;  http://purl.obolibrary.org/obo/) 

		• UBERON (UBERON_;  http://purl.obolibrary.org/obo/) 

		• Human PR (PR_;  http://purl.obolibrary.org/obo/) 

		• CL (CL_;  http://purl.obolibrary.org/obo/) 

	 
	b. Relations (RO;  http://purl.obolibrary.org/obo/) 

		• RO_0002434 = interacts with

		• RO_0002436 = molecularly interacts with

		• RO_0002435 = genetically interacts with

		• RO_0002205 = has gene product

		• RO_0001025 = located in

		• RO_0000056 = participates in

		• RO_0000085 = has function

		• Rfs:SubClassOf = <http://www.w3.org/2000/01/rdf-schema#subClassOf>
		
		
	c. Triples using these ontologies with relation:

		• ChEBI, RO_0002434, Gene 

		• ChEBI, RO_0002436, GO (not used!!!)

		• ChEBI, RO_0002434, PR

		• Gene, RO_0002435, Gene

		• Gene, RO_0002205, PR

		• PR, RO_0001025, UBERON

		• PR, RO_0002436, ChEBI

		• PR, RO_0001025, CL

		• PR, RO_0000056, GO (BP)

		• PR, RO_0001025, GO (CC)

		• PR, RO_0000085, GO (MF)

		• PR, RO_0002436, PR

		• Gene, rdfs:subClassOf, SO

2. Ignorance-Graph information:

Node Name | Attributes | Edges
--- | --- | --- 
ALL_ARTICLES | NODE_TYPE | all articles
articles (PMCID####) | 'NODE_TYPE','ARTICLE_DATE','TOTAL_SENTENCE_COUNT','TOTAL_WORD_COUNT','IGNORANCE_SENTENCE_COUNT' | ALL_ARTICLES and sentence IDs
sentences (SENTENCE_ID) | 'NODE_TYPE','SENTENCE_SPAN','SENTENCE_TEXT','SENTENCE_ANNOTATION_ID' | articles, annotated lexical cues if they have, and OBO concepts if they have
annotated lexical cue (LC_ID) | 'NODE_TYPE','MENTION_ANNOTATION_ID','MENTION_SPAN','MENTION_TEXT' | sentence ids, taxonomy lexical cues, ignorance categories
taxonomy lexical cues (TLC_ID) | 'NODE_TYPE','ANNOTATION_TEXT' | lexical cues, ignorance categories
narrow ignorance category | 'NODE_TYPE' | taxonomy lexical cues and broad ignroance categories
broad ignorance category | 'NODE_TYPE' | narrow ignorance categories and IGNORANCE_TAXONOMY
IGNORANCE_TAXONOMY | 'NODE_TYPE' | broad ignorance categories
OBOs | Edge attributes: 'OBO_MENTION_ID','OBO_MENTION_TEXT','OBO_MENTION_SPAN' | connects OBO concepts in PheKnowLator to sentence ids
























