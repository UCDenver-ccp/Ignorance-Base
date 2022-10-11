#!/usr/bin/env bash

##path to the main craft documents for training
all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'

##path to the held out 30 documents for gold standard evaluation
craft_st_path='../Concept-Recognition-as-Translation/craft-st-2019/'

##path to the concept recognition project
negacy_folder='negacy_project/'
concept_recognition_path='Concept-Recognition-as-Translation/'
code='Code/'

code_path=$fiji_path$negacy_folder$concept_recognition_path$code

##path to the evaluation files where all output will be stored during the evaluation
eval_path='Ignorance-Question-Work-Full-Corpus/OBOs/'
ignorance_corpus='Ignorance-Question-Corpus/'
ignorance_base_path='3_Ignorance_Base/'
ignorance_base_corpus='Ignorance-Base/Automated_Data_Corpus/'
output_results='Word_Analysis_Output_Results/'
obos='OBOs/'

##Folders for inputs and outputs
concept_system_output='concept_system_output/' #the folder for the final output of the full concept recognition run
article_folder='Articles/' #the folder with the PMC Articles text files
tokenized_files='Tokenized_Files/' #preprocessed article files to be word tokenized for BIO- format

#/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/Negacy_seq_2_seq_NER_model/Concept-Recognition-as-Translation/Models/SPAN_DETECTION/CHEBI
save_models_path='Models/SPAN_DETECTION/' #all the saved models for span detection
results_span_detection='Results_span_detection/' #results from the span detection runs
concept_norm_files='Concept_Norm_Files/' #the processed spans detected for concept normalization on the character level
pmcid_sentence_files_path='PMCID_files_sentences_EXT/' #the sentence files for the PMC articles
concept_annotation='concept-annotation/' #the concept annotations for CRAFT

##list of the ontologies of interest
ontologies="CHEBI_EXT,CL_EXT,GO_BP_EXT,GO_CC_EXT,GO_MF_EXT,MOP_EXT,NCBITaxon_EXT,PR_EXT,SO_EXT,UBERON_EXT"

##list of the files to run through the concept recognition pipeline
all_files='all'

##if a gold standard exists (true or false)
gold_standard='False'

##the span detection algorithm to use
algos='CRF' ##CRF, LSTM, LSTM_CRF, CHAR_EMBEDDINGS, LSTM_ELMO, BIOBERT

###copy all the articles to OBOs/Articles/ folder
#cp $all_file_path$ignorance_corpus$article_folder/* $all_file_path$eval_path$article_folder

##preprocess the articles (word tokenize) to prepare for span detection no matter the algorithm
#craft_path - not used (only eval_path)
#concept_recognition_path - not used unless gold standard
#concept_annotation - not used
python3 $code_path/eval_preprocess_docs.py -craft_path=$craft_st_path -concept_recognition_path=$fiji_path$negacy_folder$concept_recognition_path -eval_path=$scratch_path$ignorance_base_corpus$obos -concept_system_output=$concept_system_output -article_folder=$scratch_path$ignorance_base_corpus$article_folder -tokenized_files=$tokenized_files -pmcid_sentence_files=$pmcid_sentence_files_path -concept_annotation=$concept_annotation -ontologies=$ontologies -evaluation_files=$all_files --gold_standard=$gold_standard


declare -a algos=('CRF' 'BIOBERT')
for algo in "${algos[@]}"
do


    biobert='BIOBERT'
    lstm_elmo='LSTM_ELMO'

    if [ $algo == $biobert ]; then

        ##creates the biobert test.tsv file
        python3 $code_path/eval_span_detection.py -ontologies=$ontologies -excluded_files=$all_files -tokenized_file_path=$scratch_path$ignorance_base_corpus$obos$tokenized_files -save_models_path=$fiji_path$negacy_folder$concept_recognition_path$save_models_path -algos=$algo -output_path=$scratch_path$ignorance_base_corpus$obos$results_span_detection --pmcid_sentence_files_path=$pmcid_sentence_files_path --gold_standard=$gold_standard

        ##copy train.tsv and train_dev.tsv
        ignorance_biobert_path='Ignorance-Question-Work-Full-Corpus/Word_Analysis/BioBERT_Classification/SPAN_DETECTION_MODELS/1_binary_combined/BIOBERT/'
        train='train.tsv'
        train_dev='train_dev.tsv'
        cp $fiji_path$ignorance_biobert_path$train  $scratch_path$ignorance_base_corpus$obos$tokenized_files$algo/
        cp $fiji_path$ignorance_biobert_path$train_dev  $scratch_path$ignorance_base_corpus$obos$tokenized_files$algo/


        ## 1. Move ONTOLOGY_test.tsv (where ONTOLOGY are all the ontologies) file to supercomputer for predictions (Fiji)
        ## 2. On the supercomputer run 0_craft_fiji_run_eval_biobert.sh
        ## 3. Move the biobert models local to save for each ontology
        ## 4. Move label_test.txt and token_test.txt locally for each ontology
        ## 5. Run 0_craft_run_eval_biobert_pipepine_1.5.sh to process the results from BioBERT



    ##Run lstm-elmo on supercomputer because issues locally (ideally with GPUs)
    elif [ $algos == $lstm_elmo ]; then
        tokenized_files_updated='Tokenized_Files'
        pmcid_sentence_files_path_updated='PMCID_files_sentences'

        ## 1. Move tokenized files to supercomputer (fiji)
        ## 2. Move sentence files (PMCID_files_sentences/) to supercomputer (fiji)
        ## 3. Run 0_craft_fiji_run_eval_pipeline_1.sh (ONTOLOGY is the ontologies of choice) on supercomputer
        ## 4. Move the /Output_Folders/Evaluation_Files/Results_span_detection/ files for LSTM_ELMO local: ONTOLOGY_LSTM_ELMO_model_weights_local_PMCARTICLE.txt where ONTOLOGY is the ontology of interest and PMCARTICLE is the PMC article ID
        ## 5. Run 0_craft_run_eval_LSTM_ELMO_pipeline_1.5.sh to process the results from LSTM_ELMO


    ## the rest of the span detection algorithms can be run locally
    else

        ##runs the span detection models locally
        python3 $code_path/eval_span_detection.py -ontologies=$ontologies -excluded_files=$all_files -tokenized_file_path=$scratch_path$ignorance_base_corpus$obos$tokenized_files -save_models_path=$fiji_path$negacy_folder$concept_recognition_path$save_models_path -algos=$algo -output_path=$scratch_path$ignorance_base_corpus$obos$results_span_detection --pmcid_sentence_files_path=$pmcid_sentence_files_path --gold_standard=$gold_standard

        ##process the spans to run through concept normalization
        python3 $code_path/eval_preprocess_concept_norm_files.py -ontologies=$ontologies -results_span_detection_path=$scratch_path$ignorance_base_corpus$obos$results_span_detection -concept_norm_files_path=$scratch_path$ignorance_base_corpus$obos$concept_norm_files -evaluation_files=$all_files



    ##run the open_nmt to predict
    #run_eval_open_nmt.sh

    fi


done