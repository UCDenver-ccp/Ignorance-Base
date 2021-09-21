import os
import nltk
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import pickle


def read_in_pkl_file(file_path, pkl_file_list):
    for pkl_file in pkl_file_list:
        with open('%s%s' %(file_path, pkl_file), 'rb') as pf:
            data = pickle.load(pf)
            print('FILE OF INTEREST:', pkl_file)

            print('TYPE AND LENGTH OF DATA:', type(data), len(data))

            if len(data) <= 10:
                print('SMALL ENOUGH DATA TO PRINT ALL:')
                print(data)
            else:
                j = 0
                print('TOO LARGE OF DATA SO 10 POINTS:')
                for key, value in data.items():
                    if j <= 10:
                        print(key, value)
                        j += 1





if __name__=='__main__':
    ##gold standard annotions v1 path
    gold_standard_annotation_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Annotations/'

    current_ignorance_types = ['ALTERNATIVE_OPTIONS_CONTROVERSY', 'ANOMALY_CURIOUS_FINDING', 'DIFFICULT_TASK',
                               'EXPLICIT_QUESTION', 'FULL_UNKNOWN', 'FUTURE_PREDICTION', 'FUTURE_WORK',
                               'IMPORTANT_CONSIDERATION', 'INCOMPLETE_EVIDENCE', 'PROBABLE_UNDERSTANDING',
                               'PROBLEM_COMPLICATION', 'QUESTION_ANSWERED_BY_THIS_WORK', 'SUPERFICIAL_RELATIONSHIP']

    ##gold standard v1 with training updated
    articles = ['PMC1247630', 'PMC1474522', 'PMC1533075', 'PMC1626394', 'PMC2009866', 'PMC2265032', 'PMC2396486',
                'PMC2516588', 'PMC2672462', 'PMC2874300', 'PMC2885310', 'PMC2889879', 'PMC2898025', 'PMC2999828',
                'PMC3205727', 'PMC3272870', 'PMC3279448', 'PMC3313761', 'PMC3342123', 'PMC3348565', 'PMC3373750',
                'PMC3400371', 'PMC3427250', 'PMC3513049', 'PMC3679768', 'PMC3800883', 'PMC3914197', 'PMC3915248',
                'PMC3933411', 'PMC4122855', 'PMC4304064', 'PMC4311629', 'PMC4352710', 'PMC4377896', 'PMC4428817',
                'PMC4500436', 'PMC4564405', 'PMC4653409', 'PMC4653418', 'PMC4683322', 'PMC4859539', 'PMC4897523',
                'PMC4954778', 'PMC4992225', 'PMC5030620', 'PMC5143410', 'PMC5187359', 'PMC5273824', 'PMC5501061',
                'PMC5540678', 'PMC5685050', 'PMC5812027', 'PMC6000839', 'PMC6011374', 'PMC6022422', 'PMC6029118',
                'PMC6033232', 'PMC6039335', 'PMC6054603', 'PMC6056931']

    all_lcs_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Ontologies/Ontology_Of_Ignorance_all_cues_2020-08-25.txt'

    output_folder = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/3_Ignorance_Base/Ignorance-Base/Output_Folders/'
    sentence_folder = 'PMCID_Sentence_Files/'

    sentence_output_folder = output_folder + sentence_folder

    all_combined_data = '0_all_combined'

    dictionary_folder = 'dictionary_files/'

    dictionary_output_folder = output_folder + dictionary_folder


    article_dictionary_files_dict = {} #dict: article -> [list of dictionary file names]
    for root, directories, filenames in os.walk(dictionary_output_folder):
        for filename in sorted(filenames):
            if filename.split('_')[0] in articles:
                article = filename.split('_')[0]
                if article_dictionary_files_dict.get(article):
                    article_dictionary_files_dict[article] += [filename]
                else:
                    article_dictionary_files_dict[article] = [filename]


    for i, article in enumerate(articles):
        if i < 2:
            read_in_pkl_file(dictionary_output_folder, article_dictionary_files_dict[article])