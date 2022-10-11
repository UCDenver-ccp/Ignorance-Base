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

0. We are working in the Automated_Data_Corpus/ folder.

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

	a. run_CR_eval_pipeline_1_ignorance_all_articles.sh and run_CR_eval_pipeline_1_ignorance_all_articles_EXT.sh: The first step of the concept recognition pipeline that preprocesses all articles BioBERT. Outputs: Tokenized_Files/, PMCID_files_sentences/, PMCID_files_sentences_EXT, Results_span_detection/OBO/BIOBERT/. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"

		iv. code_path = the code path to the Concept-Recognition-as-Translation/Code/ Folder

	b. fiji_run_biobert_eval_ignorance_all_articles.sh (also partial ones for speed) and fiji_run_biobert_eval_ignorance_all_articles_EXT.sh: Runs BioBERT for all OBOs. Output: Results_span_detection/OBO/BIOBERT/. Variables to change:

		i. CR_models_base_path = the base path to Concept-Recognition-as-Translation/ folder

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. fiji_path = the path to all github repositories

	c. run_CR_eval_biobert_pipeline_1.5_ignorance_all_articles.sh and run_CR_eval_biobert_pipeline_1.5_ignorance_all_articles_EXT.sh: Postprocesses the BioBERT output to the correct format for concept normalization. Output: Results_span_detection/OBOs/. Also prepares data for concept normalization. Output: Concept_Norm_Files/OBOs/. Variables to change:

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. CR_models_base_path = the base path to Concept-Recognition-as-Translation/ folder

	d. fiji_run_eval_open_nmt_ignorance_all_articles.sh and fiji_run_eval_open_nmt_ignorance_all_articles_EXT.sh: Runs the concept normalization pipeline with OpenNMT. Output: Results_concept_norm_files/OBOs/. Variables to change:

		i. CR_models_base_path = the base path to Concept-Recognition-as-Translation/ folder

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. fiji_path = the path to all github repositories

	e. run_CR_eval_pipeline_2_ignorance_all_articles.sh and run_CR_eval_pipeline_2_ignorance_all_articles_EXT.sh: Combines span detection and concept normalization results to the folder concept_system_output/OBO/. The output format is .bionlp.

		i. fiji_path = the path to all github repositories

		ii. scratch_path = a temporary file system for FIJI. This can be the same as all_file_path. Make sure the Article/ folder is also here.

		iii. all_files = either a list of files or "all"

		iv. code_path = the code path to the Concept-Recognition-as-Translation/Code/ Folder




## All Data Corpus

## Ignorance-Network
