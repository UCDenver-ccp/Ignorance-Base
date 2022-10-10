import os
import nltk
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import pickle
import networkx as nx
import datetime
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pylab
import time


import dash
import dash_core_components as dcc
import dash_html_components as html
from colour import Color
from textwrap import dedent as d
import json

def get_all_strings(string_file_path):

    string_list = []

    with open(string_file_path, 'r+') as string_file:
        next(string_file) #header
        for gene in string_file:

            string_list += [gene.replace('\n','')]


    return string_list



def check_string_in_all_articles(all_articles_path, string, output_path):
    ##return a list of article files that contain the string
    articles_contain_string_list = []

    for root, directories, filenames in os.walk('%s' % (all_articles_path)):
        for filename in sorted(filenames):
            if filename.startswith('PMC') and filename.endswith('.nxml.gz.txt'):
                with open(all_articles_path+filename, 'r+') as article_file:
                    article_contents = article_file.read()
                    # print('got here')
                    if string.lower() in article_contents.lower():
                        articles_contain_string_list += [filename]
                        continue #continue to the next article
                    else:
                        pass
            else:
                pass

    ##output the article contain string list for each string
    if articles_contain_string_list:
        with open('%s%s_%s_%s_%s.txt' %(output_path, 'GENE', string, 'article_list', len(articles_contain_string_list)), 'w+') as output_file:
            output_file.write('%s\t%s\n' %('GENE:', string))
            for a in articles_contain_string_list:
                output_file.write('%s\n' %(a))
    else:
        #output_empty_file
        with open('%s%s_%s_%s_%s.txt' %(output_path, 'GENE', string, 'article_list', len(articles_contain_string_list)), 'w+') as output_file:
            output_file.write('%s\t%s\n' %('GENE:', string))


    return articles_contain_string_list



if __name__=='__main__':


    ##gold standard annotions v1 path
    gold_standard_annotation_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Annotations/'

    current_ignorance_types = ['ALTERNATIVE_OPTIONS_CONTROVERSY', 'ANOMALY_CURIOUS_FINDING', 'DIFFICULT_TASK',
                               'EXPLICIT_QUESTION', 'FULL_UNKNOWN', 'FUTURE_PREDICTION', 'FUTURE_WORK',
                               'IMPORTANT_CONSIDERATION', 'INCOMPLETE_EVIDENCE', 'PROBABLE_UNDERSTANDING',
                               'PROBLEM_COMPLICATION', 'QUESTION_ANSWERED_BY_THIS_WORK', 'SUPERFICIAL_RELATIONSHIP']

    old_ignorance_types_dict = {'ALTERNATIVE_OPTIONS':'ALTERNATIVE_OPTIONS_CONTROVERSY'}

    broad_categories = ['LEVELS_OF_EVIDENCE', 'BARRIERS', 'FUTURE_OPPORTUNITIES']
    broad_categories_dict = {'LEVELS_OF_EVIDENCE' : ['FULL_UNKNOWN', 'EXPLICIT_QUESTION', 'INCOMPLETE_EVIDENCE', 'PROBABLE_UNDERSTANDING', 'SUPERFICIAL_RELATIONSHIP'], 'BARRIERS': ['ALTERNATIVE_OPTIONS_CONTROVERSY', 'DIFFICULT_TASK', 'PROBLEM_COMPLICATION'], 'FUTURE_OPPORTUNITIES': ['FUTURE_PREDICTION', 'FUTURE_WORK', 'IMPORTANT_CONSIDERATION']}

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

    print('NUM ARTICLES:', len(articles))

    all_lcs_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Ontologies/Ontology_Of_Ignorance_all_cues_2020-08-25.txt'

    output_folder = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/3_Ignorance_Base/Ignorance-Base/Output_Folders/'

    sentence_folder = 'PMCID_Sentence_Files/'

    sentence_output_folder = output_folder + sentence_folder

    all_combined_data = '0_all_combined'

    dictionary_folder = 'dictionary_files/'

    evolution_folder ='Visualizations/Ignorance_Evolution/'
    visualizations_folder = 'Visualizations/Ignorance_Network_Vis/'
    enrichment_folder='Visualizations/Ignorance_Enrichment/'
    gene_list_file = '43_genes_list.txt'



    dictionary_output_folder = output_folder + dictionary_folder

    pmcid_date_info = 'PMCID_date_info.txt'

    article_count_summary_stats_file_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Concept-Recognition-as-Translation-master/Output_Folders/eval_preprocess_article_summary.txt'

    current_ignorance_graph_file = 'IGNORANCE_GRAPH_60_ARTICLES_09_11_21.gpickle' ##TODO: make sure this is the most up-to-date file!!!

    ##save graph by date so we know when it is from
    today = datetime.datetime.now()
    d = today.strftime('%x').replace('/', '_')

    all_article_path_v2 = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation_v2/Articles/'
    gold_standard_v2 = 'gold_standard_v2/'

    all_articles_development_large_set_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/1_First_Full_Annotation_Task_9_13_19/Articles/'
    all_articles_output = 'all_articles_development/'

    gene_list = get_all_strings(output_folder+enrichment_folder+gene_list_file)

    for gene in gene_list:
        check_string_in_all_articles(all_article_path_v2, gene,output_folder+enrichment_folder+gold_standard_v2)
        check_string_in_all_articles(all_articles_development_large_set_path, gene, output_folder + enrichment_folder+all_articles_output)
