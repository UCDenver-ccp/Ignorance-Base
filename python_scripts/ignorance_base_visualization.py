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




def read_in_graph_pkl_file(graph_file_path):
    graph = nx.read_gpickle(graph_file_path)
    return graph


##https://stackoverflow.com/questions/17381006/large-graph-visualization-with-python-and-networkx
def save_graph(graph, file_name, pos_name_list, pos_list):
    # initialze Figure
    # plt.figure(num=None, figsize=(20, 20), dpi=80)



    # pos = nx.spring_layout(graph) #todo: there are different layouts to use
    for p, pos in enumerate(pos_list):
        plt.axis('off')
        fig = plt.figure(1)
        pos_name = pos_name_list[p]
        #https://stackoverflow.com/questions/3567018/how-can-i-specify-an-exact-output-size-for-my-networkx-graph
        nx.draw_networkx_nodes(graph, pos, node_size=10)
        nx.draw_networkx_edges(graph, pos, node_size=10)
        nx.draw_networkx_labels(graph, pos, font_size=5)

        # cut = 1.00
        # xmax = cut * max(xx for xx, yy in pos.values())
        # ymax = cut * max(yy for xx, yy in pos.values())
        # plt.xlim(0, xmax)
        # plt.ylim(0, ymax)

        plt.savefig(file_name.replace('.png', '_%s.png' %(pos_name)), bbox_inches="tight")
        pylab.close()
        del fig








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

    visualizations_folder ='Visualizations/Ignorance_Network_Vis/'

    dictionary_output_folder = output_folder + dictionary_folder

    pmcid_date_info = 'PMCID_date_info.txt'

    article_count_summary_stats_file_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Concept-Recognition-as-Translation-master/Output_Folders/eval_preprocess_article_summary.txt'

    current_ignorance_graph_file = 'IGNORANCE_GRAPH_60_ARTICLES_09_02_21.gpickle'

    ##save graph by date so we know when it is from
    today = datetime.datetime.now()
    d = today.strftime('%x').replace('/', '_') ##TODO: make sure the date is correct for the file we want
    # print(type(d))
    current_d = '09_06_21'


    ##read in all gpickle files ignorance file
    # Ignorance_Graph = read_in_graph_pkl_file('%s%s%s' %(output_folder, visualizations_folder, current_ignorance_graph_file))

    for root, directories, filenames in os.walk('%s%s' %(output_folder, visualizations_folder)):
        for filename in sorted(filenames):
            if filename.endswith('.gpickle') and d in filename: ##TODO: affects this!
                print('CURRENT GRAPH:', filename)
                start_time = time.time()
                current_graph = read_in_graph_pkl_file('%s%s' % (root, filename))
                print("--- %.2f min to load graph ---" % (float(time.time() - start_time) / float(60)))


                # print(list(Ignorance_Graph.nodes))
                print('NUMBER OF NODES:', len(list(current_graph.nodes)))
                print('NUMBER OF EDGES:', len(list(current_graph.edges)))
                # print(Ignorance_Graph.nodes.data())  # list of tuples

                start_time = time.time()
                # Assuming that the graph g has nodes and edges entered
                today = datetime.datetime.now()
                d = today.strftime('%x').replace('/', '_')
                vis_output_file = '%s%s.png' %(root, filename.replace('.gpickle','_VIZ'))


                ##trying different positions for the nodes in the graph - spring seems to be the best!
                # pos_name_list = ['spring', 'random', 'circular', 'shell']  # trying out a few different ones
                # pos_list = [nx.spring_layout(current_graph), nx.random_layout(current_graph), nx.circular_layout(current_graph), nx.shell_layout(current_graph)]

                #spring is final pos!
                pos_name_list = ['spring']
                pos_list = [nx.spring_layout(current_graph)]

                save_graph(current_graph, '%s%s.png' %(root, filename.replace('.gpickle','_VIZ')), pos_name_list, pos_list) # it can also be saved in .svg, .png. or .ps formats
                # plotly_visualization(Ignorance_Graph, '%s%s' %(output_folder, visualizations_folder))
                print("--- %.2f min to save graph ---" % (float(time.time() - start_time) / float(60)))


    ##DASH APP
    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    # app.title = "Ignorance-base Network"
    # app.run_server(debug=True)