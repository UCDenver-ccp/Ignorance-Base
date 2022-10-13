# Ignorance-Base
The ignorance-base combines biomedical concept classifiers and ignorance classifiers in order to understand the state of our scientific ignorance through two new exploration methods: (1) exploration of the ignorance-base by topic (exploration by topic) and (2) exploration of the ignorance-base by experimental results (exploration by experimental results).

Exploration by topic is called just EXPLORATION in our file system. Exploration by experimental results is called GENE_LIST_ENRICHMENT.

Clone this repository to create the ignorance-base from scratch or add more articles. 

If you do not want to do it from scratch, a full ignorance-base can be found in Ignorance_Network/ALL_DATA_GRAPHS/0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_ALL_SENTENCES_DICT.pkl.zip (you will need to unzip it). There is other supporting information in the file as well.


Our ignorance-base contains 1,643 articles with 91 having gold standard ignorance annotations (prefix GS) and 1,552 run automatically for ignorance identification. All 1,643 articles have automatic classification for the biomedical concepts to ten OBOs from CRAFT. The 91 have the OBOs run over them separately from the 1,552. 

A lot of our work was run on a supercomputer, FIJI, out of boulder to save time, space, and computing resources. There are two different environments we used and these can be found in Automated_Data_Corpus/Anaconda_Environments_for_FIJI/. Use the general_environment unless you are runnning BioBERT or OpenNMT, then use the other one. Many files have matching .sbatch files which are files to run the scripts on FIJI.

The ignorance-classifiers are based on our prior work that created the classifiers: https://github.com/UCDenver-ccp/Ignorance-Question-Work-Full-Corpus as well as the ignorance-corpus we created: https://github.com/UCDenver-ccp/Ignorance-Question-Corpus.
Please clone both of these repositories because we utilize python scripts from them for this work. 

The biomedical concept classifiers relies on our previous work found here:https://github.com/UCDenver-ccp/Concept-Recognition-as-Translation. Please close this repository. 

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

1. run_combine_all_data.sh - need to also do it for the OBOs
 
2. run_combine_all_data_OBO.sh - moved to the all data corpus stuff (see comment above)




















