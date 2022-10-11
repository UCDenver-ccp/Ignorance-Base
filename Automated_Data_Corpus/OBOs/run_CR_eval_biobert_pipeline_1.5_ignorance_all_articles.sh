#!/usr/bin/env bash


all_file_path='/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/'
fiji_path='/Users/mabo1182/'
scratch_path='/scratch/Users/mabo1182/'

CR_models_base_path='/Users/mabo1182/negacy_project/'

negacy_folder='negacy_project/'
concept_recognition_path='Concept-Recognition-as-Translation/'
code='Code/'
code_path=$CR_models_base_path$concept_recognition_path$code


biobert_scripts_path='Ignorance-Question-Work-Full-Corpus/Word_Analysis/BioBERT_Classification/biobert/'



eval_path='Ignorance-Question-Work-Full-Corpus/OBOs/'
ignorance_corpus='Ignorance-Question-Corpus/'
ignorance_base_path='3_Ignorance_Base/'
ignorance_base_corpus='Ignorance-Base/Automated_Data_Corpus/'
output_results='Word_Analysis_Output_Results/'
obos='OBOs/'

tokenized_files='Tokenized_Files/' #preprocessed article files to be word tokenized for BIO- format
results_span_detection='Results_span_detection/' #results from the span detection runs
concept_norm_files='Concept_Norm_Files/'
pmcid_sentence_files_path='PMCID_files_sentences/'


biobert_path='BIOBERT/'
output='output/'

save_models_path='Models/SPAN_DETECTION/'

model='model.ckpt-' ##TODO: need highest number found - need to gather this from eval_results

biobert_original='biobert_v1.0_pubmed_pmc/'

##list of the ontologies of interest
ontologies="CHEBI,CL,GO_BP,GO_CC,GO_MF,MOP,NCBITaxon,PR,SO,UBERON"

##list of the files to run through the concept recognition pipeline
all_files='all'

##if a gold standard exists (true or false)
gold_standard='False'

##the algorithm we are focusing on - specifically BioBERT due to running
algos='BIOBERT'  ##CRF, LSTM, LSTM_CRF, CHAR_EMBEDDINGS, LSTM_ELMO, BIOBERT



##FOR BIOBERT
biobert='BIOBERT'
if [ $algos == $biobert ]; then
    ##0. you have just run the BioBERT models on fiji for span detection
    ##1. Bring the results files local for each ontology - all files with "*_test.txt*"
    declare -a arr=('CHEBI' 'CL' 'GO_BP' 'GO_CC' 'GO_MF' 'MOP' 'NCBITaxon' 'PR' 'SO' 'UBERON')

    ##loop over each ontology and run the corresponding model


#    ##Grab all files with "*_test.txt*" local with fiji
#    for i in "${arr[@]}"
#    do
#       echo $i
#       results_path=$fiji_path$eval_path$results_span_detection$i/$biobert_path
#       local_path=$all_file_path$eval_path$results_span_detection$i/$biobert_path
#       scp mabo1182@fiji.colorado.edu:$results_path/*_test.txt* $local_path
#       rm $local_path/logits_test.txt
#
#    done


    ##2. Detokenize all BioBERT results files (updated the detokenize script)

    biotags='B,I,O-,O' #ordered for importance
    gold_standard='false'
    true='true'

    declare -a ont=('CHEBI' 'CL' 'GO_BP' 'GO_CC' 'GO_MF' 'MOP' 'NCBITaxon' 'PR' 'SO' 'UBERON')

    ##loop over each ontology and reformat the BioBERT output files to match the input
    for i in "${ont[@]}"
    do
        echo "$i"

        NER_DIR=$scratch_path$ignorance_base_corpus$obos$tokenized_files$biobert_path
        OUTPUT_DIR=$scratch_path$ignorance_base_corpus$obos$results_span_detection$i/$biobert_path

        ##detokenize the bioBERT results files
        python3 $fiji_path$biobert_scripts_path/biobert_ner_detokenize_updated.py --token_test_path=$OUTPUT_DIR/token_test.txt --label_test_path=$OUTPUT_DIR/label_test.txt --answer_path=$NER_DIR/test.tsv --output_dir=$OUTPUT_DIR --biotags=$biotags --gold_standard=$gold_standard

        echo 'DONE WITH TEST.TSV'


        ##if gold standard then we also want the gold standard information using the ontology_test.tsv files
        if [ $gold_standard == $true ]; then
            ont_test='_test.tsv'
            python3 $fiji_path$biobert_scripts_path/biobert_ner_detokenize_updated.py --token_test_path=$OUTPUT_DIR/token_test.txt --label_test_path=$OUTPUT_DIR/label_test.txt --answer_path=$NER_DIR/$i$ont_test --output_dir=$OUTPUT_DIR --biotags=$biotags --gold_standard=$gold_standard


            ##classification report if gold standard
            python3 $code_path/biobert_classification_report.py --ner_conll_results_path=$OUTPUT_DIR/ --biotags=$biotags --ontology=$i --output_path=$OUTPUT_DIR/ --gold_standard=$gold_standard

            #copy the classification report to the main results with ontology name
            biobert_class_report='_biobert_local_eval_files_classification_report.txt'
            cp $OUTPUT_DIR/biobert_classification_report.txt $eval_path$results_span_detection$i/$i$biobert_class_report


        fi

    done



    biobert_prediction_results=$scratch_path$ignorance_base_corpus$obos$results_span_detection

    ##create the evaluation dataframe!
    python3 $code_path/biobert_eval_dataframe_output.py -ontologies=$ontologies -excluded_files=$all_files -tokenized_file_path=$scratch_path$ignorance_base_corpus$obos$tokenized_files -biobert_prediction_results=$biobert_prediction_results -output_path=$biobert_prediction_results -algos=$algos --pmcid_sentence_files_path=$pmcid_sentence_files_path

fi





##preprocess to get all the concepts for the next steps
python3 $code_path/eval_preprocess_concept_norm_files.py -ontologies=$ontologies -results_span_detection_path=$scratch_path$ignorance_base_corpus$obos$results_span_detection -concept_norm_files_path=$scratch_path$ignorance_base_corpus$obos$concept_norm_files -evaluation_files=$all_files


##run the open_nmt to predict
#run_eval_open_nmt.sh
