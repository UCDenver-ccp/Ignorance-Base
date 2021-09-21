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




#https://plotly.com/python/network-graphs/#network-graphs-in-dash
#https://stackoverflow.com/questions/17381006/large-graph-visualization-with-python-and-networkx
#https://towardsdatascience.com/python-interactive-network-visualization-using-networkx-plotly-and-dash-e44749161ed7


def create_graph_for_dash(graph, filename):
    ##add position tags
    pos = nx.shell_layout(graph) ##dict from node to array in 2D space created by shell_layout
    # print(pos)
    for node in graph.nodes:
        graph.nodes[node]['pos'] = list(pos[node])


    ##create edges: Add edges as disconnected lines in a single trace and nodes as a scatter trace
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = graph.nodes[edge[0]]['pos']
        x1, y1 = graph.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in graph.nodes():
        x, y = graph.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))


    ##color node points: Color node points by the number of connections. Another option would be to size points by the number of connections i.e. node_trace.marker.size = node_adjacencies

    ##good copy
    # node_adjacencies = []
    # node_text = []
    # for i, adjacencies in enumerate(graph.adjacency()):
    #     print(adjacencies)
    #     node_adjacencies.append(len(adjacencies[1]))
    #     node_text.append('# of connections: %s\n' %(str(len(adjacencies[1]))))
    # # raise Exception('hold')
    #
    # node_trace.marker.color = node_adjacencies
    # node_trace.text = node_text


    node_adjacencies = []
    node_text = []
    for i, adjacencies in enumerate(graph.adjacency()):
        print(adjacencies)
        node = adjacencies[0]
        print(graph.nodes[node])
        attribute_info_sting = '%s, ' %(node)
        attribute_dict = graph.nodes[node]
        acceptable_attributes = []

        for attribute, value in attribute_dict.items():
            '''
            large_nodes = ['ALL_ARTICLES','IGNORANCE_TAXONOMY']

            all_articles_attributes = ['NODE_TYPE']
            ignorance_taxonomy_attributes = ['NODE_TYPE']
            broad_ignorance_taxonomy_attributes = ['NODE_TYPE']
            narrow_ignorance_taxonomy_attributes = ['NODE_TYPE']
            taxonomy_lexical_cue_attributes = ['NODE_TYPE', 'ANNOTATION_TEXT']
            article_attributes = ['NODE_TYPE', 'ARTICLE_DATE', 'TOTAL_SENTENCE_COUNT', 'TOTAL_WORD_COUNT', 'IGNORANCE_SENTENCE_COUNT']
            sentence_attributes = ['NODE_TYPE', 'SENTENCE_SPAN', 'SENTENCE_TEXT', 'SENTENCE_ANNOTATION_ID']
            annotated_lexical_cues_attributes = ['NODE_TYPE', 'MENTION_ANNOTATION_ID', 'MENTION_SPAN', 'MENTION_TEXT']
            '''
            if attribute.upper() == 'NODE_TYPE':

                if value.upper() == 'ALL_ARTICLES':
                    attribute_info_sting += '%s' % (value.lower().replace('_',' '))
                elif value.upper() == 'ARTICLE':
                    attribute_info_sting += '%s, ' %(value.lower().replace('_',' '))
                    acceptable_attributes += ['ARTICLE_DATE', 'TOTAL_SENTENCE_COUNT', 'TOTAL_WORD_COUNT', 'IGNORANCE_SENTENCE_COUNT']
                elif value.upper() == 'SENTENCE':
                    attribute_info_sting += '%s, ' % (value.lower().replace('_',' '))
                    acceptable_attributes += ['SENTENCE_SPAN', 'SENTENCE_TEXT']
                elif value.upper() == 'ANNOTATED_LEXICAL_CUE':
                    attribute_info_sting += '%s, ' % (value.lower().replace('_',' '))
                    acceptable_attributes += ['MENTION_SPAN', 'MENTION_TEXT']
                elif value.upper() == 'IGNORANCE_TAXONOMY':
                    attribute_info_sting += '%s, ' % (value.lower().replace('_',' '))
                elif value.upper() == 'BROAD_IGNORANCE_TAXONOMY_CATEGORY':
                    attribute_info_sting += '%s, ' % (value.lower().replace('_',' '))
                elif value.upper() == 'IGNORANCE_TAXONOMY_CATEGORY':
                    attribute_info_sting += '%s, ' % (value.lower().replace('_',' '))
                elif value.upper() == 'TAXONOMY_LEXICAL_CUE':
                    attribute_info_sting += '%s, ' % (value.lower().replace('_',' '))
                else:
                    print(attribute, value)
                    raise Exception('ERROR: Issue with missing a nodetype value!')

            elif attribute.upper() == 'POS':
                pass
            elif attribute in acceptable_attributes:
                attribute_info_sting += '%s:\t%s, ' % (attribute.lower(), value)
            else:
                pass

        node_adjacencies.append(len(adjacencies[1])) #dictionary of adjacency list
        attribute_info_sting += '%s:\t%s' %('# of connections', str(len(adjacencies[1])))



        node_text.append(attribute_info_sting)


    # raise Exception('hold')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text


    ##create network graph
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Ignornance graph from file: %s' %(filename),
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Ignorance Graph",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    # fig.show()
    return fig


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
    d = today.strftime('%x').replace('/', '_')
    # print(type(d))
    current_d = '09_11_21' ##TODO: current date!!


    ##read in all gpickle files ignorance file
    # Ignorance_Graph = read_in_graph_pkl_file('%s%s%s' %(output_folder, visualizations_folder, current_ignorance_graph_file))
    # all_figs = []
    app = dash.Dash()

    file_count = 0
    for root, directories, filenames in os.walk('%s%s' %(output_folder, visualizations_folder)):
        for filename in sorted(filenames):
            if filename.endswith('.gpickle') and (d in filename or current_d in filename) and 'SMALL' in filename:
                file_count += 1
                print('CURRENT GRAPH:', filename)
                start_time = time.time()
                current_graph = read_in_graph_pkl_file('%s%s' % (root, filename))
                print("--- %.2f min to load graph ---" % (float(time.time() - start_time) / float(60)))


                # print(list(Ignorance_Graph.nodes))
                print('NUMBER OF NODES:', len(list(current_graph.nodes)))
                print('NUMBER OF EDGES:', len(list(current_graph.edges)))
                # print(Ignorance_Graph.nodes.data())  # list of tuples
                # if file_count == 7:
                print('current filename', filename)
                fig = create_graph_for_dash(current_graph, filename)

                app.layout = html.Div([
                    dcc.Graph(figure=fig)
                ])

                app.run_server(debug=True, use_reloader=False)

                # else:
                #     pass
                    # raise Exception('hold!')

    ##show figures on DASH
    # Run this app with `python ignorance_base_dash_app.py` and
    # visit http://127.0.0.1:8050/ in your web browser.
    # print(len(all_figs))



