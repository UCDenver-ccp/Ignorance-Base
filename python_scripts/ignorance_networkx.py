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
import copy



def read_in_pkl_file(article, file_path, pkl_file_list):
    for pkl_file in pkl_file_list:
        with open('%s%s' %(file_path, pkl_file), 'rb') as pf:
            data = pickle.load(pf)
            # print('FILE OF INTEREST:', pkl_file)
            #
            # print('TYPE AND LENGTH OF DATA:', type(data), len(data))
            if 'subject_scope_to_concept_mention_info' in pkl_file:
                subject_scope_to_concept_mention_info_dict = data
            elif 'concept_mention_info' in pkl_file:
                concept_mention_info_dict = data
            elif 'subject_scope_info' in pkl_file:
                subject_scope_info_dict = data

            else:
                raise Exception('ERROR: Weird other file that should not exist!')


    return concept_mention_info_dict, subject_scope_info_dict, subject_scope_to_concept_mention_info_dict


def read_pmcid_date_info(file_path, filename):
    article_date_info_dict = {} #pmcid -> date
    with open('%s%s' %(file_path, filename), 'r') as pmcid_info_file:
        next(pmcid_info_file)
        for line in pmcid_info_file:
            pmcid, date = line.strip('\n').split('\t')
            article_date_info_dict[pmcid] = date

    return article_date_info_dict

def read_pmcid_count_summary_stats_info(file_path, articles):
    article_count_summary_stats_dict = {}  # dict: article -> [total_sentence_count, total_word_count]

    with open(file_path, 'r') as article_count_summary_stats_file:
        # Headers: ARTICLE	TOTAL_SENTENCE_COUNT	TOTAL_WORD_COUNT
        for line in article_count_summary_stats_file:
            if line.startswith('PMC'):
                [a, total_sentence_count, total_word_count] = line.strip('\n').split('\t')
                # print(a, type(a))
                a = a.split('.')[0]
                if a not in articles:
                    print(a)
                    raise Exception(
                        'ERROR: There is an article in the summary count stats that does not exist in our input list (check the article lists)')

                elif article_count_summary_stats_dict.get(a):
                    raise Exception(
                        'ERROR: Duplicate article counts that should not exist. Check the summary stats file)')
                else:
                    article_count_summary_stats_dict[a] = [int(total_sentence_count), int(
                        total_word_count)]  # change these to integers for issues down the line


            else:
                pass  # header

    return article_count_summary_stats_dict


def add_ignorance_taxonomy_to_graph(graph, ontology_of_ignorance_file_path, current_ignorance_types, broad_categories_dict, old_ignorance_types_dict, ignorance_taxonomy_attributes, broad_ignorance_taxonomy_attributes, taxonomy_lexical_cue_attributes):
    ##return graph

    ##ADD IGNORANCE TYPES: node and edge to one large node - ignorance_taxonomy_attributes = ['NODE_TYPE']

    for bc in broad_categories_dict:
        graph.add_node(bc.upper(), NODE_TYPE='BROAD_IGNORANCE_TAXONOMY_CATEGORY')
        graph.add_edge(bc.upper(), 'IGNORANCE_TAXONOMY')



        #narrower categories:
        for it in broad_categories_dict[bc]:
            graph.add_node(it.upper(), NODE_TYPE='IGNORANCE_TAXONOMY_CATEGORY')
            graph.add_edge(it.upper(), bc.upper())

            ##check to make sure we have attributes in each node - at least node_type
            if len(graph.nodes[it.upper()]) == 0:
                print('finished with nodes', it.upper(), graph.nodes[it.upper()])
                for a in ignorance_taxonomy_attributes:
                    print(a, graph.nodes[it.upper()][a])

                raise Exception('ERROR: issue with adding attributes to the node - narrow ignorance category')
            else:
                pass


        ##check to make sure we have attributes in each node - at least node_type
        if len(graph.nodes[bc.upper()]) == 0:
            print('finished with nodes', bc.upper(), graph.nodes[bc.upper()])
            for a in broad_ignorance_taxonomy_attributes:
                print(a, graph.nodes[bc.upper()][a])

            raise Exception('ERROR: issue with adding attributes to the node - broad ignorance category')
        else:
            pass


    ##add in the rest of the missing categories that are not under a broad one (both a narrow and a broad category): broad_ignorance_taxonomy_attributes = ['NODE_TYPE']

    for it in current_ignorance_types:
        try:
            if graph.nodes[it.upper()]:
                pass
            else:
                pass
        except KeyError:
            graph.add_node(it.upper(), NODE_TYPE='IGNORANCE_TAXONOMY_CATEGORY')
            graph.add_edge(it.upper(), 'IGNORANCE_TAXONOMY') #one large node for all its

        ##check to make sure we have attributes in each node - at least node_type
        if len(graph.nodes[it.upper()]) == 0:
            print('finished with nodes', it.upper(), graph.nodes[it.upper()])
            for a in ignorance_taxonomy_attributes:
                print(a, graph.nodes[it.upper()][a])

            raise Exception('ERROR: issue with adding attributes to the node - both narrow and broad ignorance category')
        else:
            pass

    ##ADD LEXICAL CUES WITH EDGES TO EACH IGNORANCE TYPE: taxonomy_lexical_cue_attributes = ['NODE_TYPE', 'ANNOTATION_TEXT']

    all_lcs_dict = {} #dict from lc -> [synonym, ignorance_category]
    errors_dict = {'future_work': ('future_work', 'future_work', 'FUTURE_WORK'), 'future_prediction':('future_prediction', 'future_prediction', 'FUTURE_PREDICTION')}

    all_ignorance_types = set([])
    with open(ontology_of_ignorance_file_path, 'r') as ontology_of_ignorance_file:
        next(ontology_of_ignorance_file) #header: LEXICAL CUE	SYNONYMS	IGNORANCE TYPE
        for line in ontology_of_ignorance_file:
            lc, synonym, it = line.strip('\n').split('\t')
            ##create all_lcs_dict
            if all_lcs_dict.get(lc):
                raise Exception('ERROR: Issue with duplicate lexical cues and ignorance type pairs in all_lcs_file_path!')
            else:
                if lc.lower() in errors_dict:
                    lc, synonym, it = errors_dict[lc]
                else:
                    pass
                ##assign everything
                all_lcs_dict[lc] = [synonym, it]
                all_ignorance_types.add(it)

            ##add to graph

            # if it.upper() in old_ignorance_types_dict.keys() and lc.upper() not in current_ignorance_types:
            #     #if the wrong it is in there with an old one!
            #     graph.add_edge(lc.lower(), old_ignorance_types_dict[it.upper()].upper())
            if it.upper() in broad_categories:
                graph.add_edge(lc.lower(), it.upper())
            elif it.upper() not in current_ignorance_types:
                print(lc, synonym, it)
                raise Exception('ERROR: Issue with missing ignorance types - need to check it out')
            else:
                # print(lc, type(lc))
                graph.add_node(lc.lower(), NODE_TYPE='TAXONOMY_LEXICAL_CUE', ANNOTATION_TEXT=synonym)
                graph.add_edge(lc.lower(), it.upper())

            ##check to make sure we have attributes in each node - at least node_type
            if len(graph.nodes[lc.lower()]) == 0:
                print('finished with nodes', lc.lower(), graph.nodes[lc.lower()])
                for a in taxonomy_lexical_cue_attributes:
                    print(a, graph.nodes[lc.lower()][a])
                raise Exception('ERROR: issue with adding attributes to the node - lexical cue')
            else:
                pass

    ##TODO: Missing (lexical_cue, ignorance_type) pairs:
    missing_pairs = [('urgent_call_to_action', 'urgent_call_to_action', 'IMPORTANT_CONSIDERATION'), ('than', 'than', 'ALTERNATIVE_OPTIONS_CONTROVERSY'), ('is', 'is', 'EXPLICIT_QUESTION')] #lexial cue, synonym, and it
    for mp in missing_pairs:
        if mp[2] not in current_ignorance_types:
            raise Exception('ERROR: Issue with missing pairs ignorance type not in the current list')
        else:
            graph.add_node(mp[0].lower(), NODE_TYPE='TAXONOMY_LEXICAL_CUE', ANNOTATION_TEXT=mp[1])
            graph.add_edge(mp[0].lower(), mp[2].upper())
            if all_lcs_dict.get(mp[0]):
                raise Exception('ERROR: Lexical cue is already in the dictionary!')
            else:
                all_lcs_dict[mp[0]] = [mp[1], mp[2]]

    return graph, all_lcs_dict, all_ignorance_types






def add_article_info_to_graph(graph, article_to_all_dicts, article, article_date_info_dict, article_count_summary_stats_dict, all_lcs_dict, current_ignorance_types, old_ignorance_types_dict, article_attributes, sentence_attributes, annotated_lexical_cues_attributes):
    #return the new updated graph each time adding in the new node and edges
    [concept_mention_info_dict, subject_scope_info_dict, subject_scope_to_concept_mention_info_dict] = article_to_all_dicts[article]

    ##ADD ARTICLE NODE: article_attributes = ['NODE_TYPE', 'ARTICLE_DATE', 'TOTAL_SENTENCE_COUNT', 'TOTAL_WORD_COUNT', 'IGNORANCE_SENTENCE_COUNT']
    graph.add_node(article, NODE_TYPE='ARTICLE', ARTICLE_DATE=article_date_info_dict[article], TOTAL_SENTENCE_COUNT=article_count_summary_stats_dict[article][0], TOTAL_WORD_COUNT=article_count_summary_stats_dict[article][1], IGNORANCE_SENTENCE_COUNT=len(subject_scope_to_concept_mention_info_dict.keys()))

    #add edge to ALL_ARTICLES large node
    graph.add_edge(article, 'ALL_ARTICLES')

    ##check to make sure we have attributes in each node - at least node_type
    if len(graph.nodes[article]) == 0:
        print('finished with nodes', article, graph.nodes[article])
        for a in article_attributes:
            print(a, graph.nodes[article][a])

        raise Exception('ERROR: issue with adding attributes to the node - article')
    else:
        pass



    ##ADD SENTENCE NODES: sentence_attributes = ['SENTENCE_SPAN', 'SENTENCE_TEXT', 'SENTENCE_ANNOTATION_ID']
    for sentence_id, concept_mention_list in subject_scope_to_concept_mention_info_dict.items():
        if article in sentence_id:
            new_sentence_id = 'S%s-%s' %(sentence_id.split('-')[-1], article)
            sentence_start_list, sentence_end_list, sentence_text, annotation_type_lower, annotation_type_upper, empty = subject_scope_info_dict[sentence_id]
            if annotation_type_lower.lower() != 'subject_scope':
                raise Exception('ERROR: Issue with annotation type')
            else:
                pass
            if len(sentence_start_list) > 1 or len(sentence_end_list) > 1:
                print('sentence start list:', len(sentence_start_list))
                print('sentence end list:', len(sentence_end_list))
                raise Exception('ERROR: Issue with sentence start or end list length')
            else:
                sentence_span = (sentence_start_list[0], sentence_end_list[0])

        else:
            raise Exception('ERROR: Issue with the sentences not matching the correct article in the subject_scope_to_concept_mention_info_dict')

        ##add sentence node
        graph.add_node(new_sentence_id, NODE_TYPE='SENTENCE', SENTENCE_SPAN=sentence_span, SENTENCE_TEXT=sentence_text, SENTENCE_ANNOTATION_ID=sentence_id)

        ##add sentence edges to the article itself
        graph.add_edge(new_sentence_id, article)

        ##check to make sure we have attributes in each node - at least node_type
        if len(graph.nodes[new_sentence_id]) == 0:
            print('finished with nodes', new_sentence_id, graph.nodes[new_sentence_id])
            for a in sentence_attributes:
                print(a, graph.nodes[new_sentence_id][a])

            raise Exception('ERROR: issue with adding attributes to the node - sentence')
        else:
            pass



        ##ANNOTATED LEXICAL CUE INFORMATION FOR EACH SENTENCE: annotated_lexical_cues_attributes = ['NODE_TYPE', 'MENTION_ANNOTATION_ID', 'MENTION_SPAN', 'MENTION_TEXT']
        for mention_id in concept_mention_list:
            mention_start_list, mention_end_list, mention_text, annotated_lexical_cue, mention_ignorance_category, mention_sentence_id = concept_mention_info_dict[mention_id]
            # print('current mention id', mention_id)

            new_mention_id = 'LC%s-%s' %(mention_id.split('-')[-1], article)

            if len(mention_start_list) != len(mention_end_list):
                raise Exception('ERROR: Issue with mention start and end list lengths not matching - issue with annotations!')
            else:
                mention_span_list = [] #tuples of starts and ends
                for i, s in enumerate(mention_start_list):
                    mention_span_list += [(s, mention_end_list[i])]


            graph.add_node(new_mention_id, NODE_TYPE='ANNOTATED_LEXICAL_CUE', MENTION_ANNOTATION_ID=mention_id, MENTION_SPAN= mention_span_list, MENTION_TEXT=mention_text)

            ##add edges in to both new_sentence_id and taxonomy_lexical_cue/taxonomy_ignorance_category
            ##sentence_id edge add:
            if mention_sentence_id != sentence_id:
                raise Exception('ERROR: Issue with mention_sentence_id matching the correct sentence in general - issue with subject_scope_to_concept_mention_info_dict')
            else:
                graph.add_edge(new_mention_id, new_sentence_id)

            ##taxonomy_lexical_cue edge add: need to check both annotated_lexical_cue matches taxonomy_lexical_cue and mention_ignorance_category matches taxonomy_ignorance_category (Ignorance_Graph.edges(annotated_lexical_cue)
            ###if the annotated_lexical_cue or the text mention matches a lexical cue with '_' instead of spaces is in the taxonomy then we check the ignorance category matches and add it
                ##old ignorance types mapping to new ones:


            # if annotated_lexical_cue.upper().strip('0_') in old_ignorance_types_dict:
            #     graph.add_edge(new_mention_id,
            #                    old_ignorance_types_dict[annotated_lexical_cue.upper().strip('0_')].lower())
            #     print(article)
            #     print(mention_id)
            #     print(annotated_lexical_cue)
            #     print(mention_text)
            #     print(mention_ignorance_category)
            #     raise Exception('hold')
            #     # print('find it here!')


            if all_lcs_dict.get(annotated_lexical_cue.lower().strip('0_')):
                print('got here!')
                print(mention_ignorance_category)
                print(annotated_lexical_cue)
                print(all_lcs_dict[annotated_lexical_cue.lower().strip('0_')][-1])
                # if annotated_lexical_cue.lower().strip('0_') in old_ignorance_types_dict.keys():
                #     annotated_lexical_cue =



                #ignorance category matches - add edge to lexical cue
                if mention_ignorance_category == all_lcs_dict[annotated_lexical_cue.lower().strip('0_')][-1]:
                    # print('and here!')

                    graph.add_edge(new_mention_id, annotated_lexical_cue.lower().strip('0_'))


                #lexical cue exist but different category - map to taxonomy ignorance category
                else:
                    # print('mention_text', mention_text)
                    # print('mention ignorance category', mention_ignorance_category)
                    # print('annotated_lexical_cue', annotated_lexical_cue)

                    #map to lexical cue and different ignorance category so it's counted in both



                    graph.add_edge(new_mention_id, annotated_lexical_cue.lower().strip('0_'))
                    if mention_ignorance_category.upper() in current_ignorance_types:
                        graph.add_edge(new_mention_id, mention_ignorance_category.upper())
                    else:
                        raise Exception('ERROR: Issue with missing ignorance category in annotations!')

            #the text mention matches a lexical cue with '_' instead of spaces is in the taxonomy then we check the ignorance category matches and add it
            elif all_lcs_dict.get(mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_')):
                # print('got here')
                # print(annotated_lexical_cue)
                # print(all_lcs_dict[mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_')])
                if annotated_lexical_cue.upper().strip('0_') in current_ignorance_types and annotated_lexical_cue.upper().strip('0_') == all_lcs_dict[mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_')][-1]:
                    graph.add_edge(new_mention_id, mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_').lower()) ##map it to the correct lexical cue

                ##maps to a different category but still exist in lexical cues
                elif annotated_lexical_cue.upper().strip('0_') in current_ignorance_types:
                    graph.add_edge(new_mention_id, mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_').lower()) ##map it to the correct lexical cue and map it to the igonrance category that is different
                    graph.add_edge(new_mention_id, annotated_lexical_cue.upper().strip('0_'))

                elif annotated_lexical_cue.upper().strip('0_') in old_ignorance_types_dict.keys():
                    if old_ignorance_types_dict[annotated_lexical_cue.upper().strip('0_')] == mention_ignorance_category.upper():
                        ##if all ignorance categories align with the ontology
                        if all_lcs_dict[mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_')][-1].upper() == mention_ignorance_category.upper():
                            # print(all_lcs_dict[mention_text.replace(' ','_').lower()])
                            print(mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_').lower())
                            graph.add_edge(new_mention_id, mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_'))
                        #if the ignorance categories don't align with the ontology
                        else:
                            graph.add_edge(new_mention_id, mention_text.lower().replace(' ... ','...').replace(' ', '_').rstrip('_'))
                            graph.add_edge(new_mention_id, mention_ignorance_category.upper())
                    else:
                        raise Exception('ERROR: Issue with old ignorance types dict and mention ignorance category not aligning!')



                ##total error - TODO!!! #added in manually some lexical cues!
                else:
                    print('mention_text', mention_text)
                    print('mention ignorance category', mention_ignorance_category)
                    print('annotated_lexical_cue', annotated_lexical_cue)
                    raise Exception('ERROR: Issue with lexical cue still missing and mapped to ignorance category in the first place')




            #lexical cue does not exist
            else:
                print('mention_text', mention_text)
                print('mention ignorance category', mention_ignorance_category)
                print('annotated_lexical_cue', annotated_lexical_cue)
                raise Exception('ERROR: Issue with missing lexical cues in all_lcs_dict/file!')




            ##check to make sure we have attributes in each node - at least node_type
            if len(graph.nodes[new_mention_id]) == 0:
                print('finished with nodes', new_mention_id, graph.nodes[new_mention_id])
                for a in annotated_lexical_cues_attributes:
                    print(a, graph.nodes[new_mention_id][a])

                raise Exception('ERROR: issue with adding attributes to the node - annotated lexical cue')
            else:
                pass


            # if mention_id == 'PMC3427250.nxml.gz-21':
            #     print(article)
            #     print(mention_text)
            #     raise Exception('hold')

    ##TODO: NEED TO ADD OBOS FOR EACH ARTICLE FROM BILL IDEALLY BUT AT LEAST FROM NEGACY PIPELINE ESPECIALLY IF SAME FORMAT!





    return graph


def remove_specific_nodes_by_degree(graph, node_type, degree_criteria_list):
    #delete if in degree_criteria_list
    for n in list(graph.nodes):
        if graph.nodes[n]['NODE_TYPE'].upper() == node_type.upper() and graph.degree[n] in degree_criteria_list:
            graph.remove_node(n)
        else:
            #keep the node
            pass


    return graph


def save_networkx_graph(graph, output_file):
    nx.write_gpickle(graph, output_file)



if __name__=='__main__':
    ##gold standard annotions v1 path
    gold_standard_annotation_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Annotations/'

    current_ignorance_types = ['ALTERNATIVE_OPTIONS_CONTROVERSY', 'ANOMALY_CURIOUS_FINDING', 'DIFFICULT_TASK',
                               'EXPLICIT_QUESTION', 'FULL_UNKNOWN', 'FUTURE_PREDICTION', 'FUTURE_WORK',
                               'IMPORTANT_CONSIDERATION', 'INCOMPLETE_EVIDENCE', 'PROBABLE_UNDERSTANDING',
                               'PROBLEM_COMPLICATION', 'QUESTION_ANSWERED_BY_THIS_WORK', 'SUPERFICIAL_RELATIONSHIP']

    old_ignorance_types_dict = {'ALTERNATIVE_OPTIONS':'ALTERNATIVE_OPTIONS_CONTROVERSY', 'FUTURE_OPPORTUNITIES': 'FUTURE_WORK'}

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

    # articles = ['PMC3427250']

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

    ##GET THE ARTICLE DATE INFO AS METADATA - TODO: ADD MORE LATER
    article_date_info_dict = read_pmcid_date_info(output_folder, pmcid_date_info)
    ##get article sentence count data
    article_count_summary_stats_dict = read_pmcid_count_summary_stats_info(article_count_summary_stats_file_path, articles)






    ##GET ALL THE DICTIONARIES FOR EACH ARTICLE
    article_dictionary_files_dict = {} #dict: article -> [list of dictionary file names]
    for root, directories, filenames in os.walk(dictionary_output_folder):
        for filename in sorted(filenames):
            if filename.split('_')[0] in articles:
                article = filename.split('_')[0]
                if article_dictionary_files_dict.get(article):
                    article_dictionary_files_dict[article] += [filename]
                else:
                    article_dictionary_files_dict[article] = [filename]

    article_to_all_dicts = {} #article -> [list of dictionaries]
    for i, article in enumerate(articles):
        concept_mention_info_dict, subject_scope_info_dict, subject_scope_to_concept_mention_info_dict = read_in_pkl_file(article, dictionary_output_folder, article_dictionary_files_dict[article])

        article_to_all_dicts[article] = [concept_mention_info_dict, subject_scope_info_dict, subject_scope_to_concept_mention_info_dict]



    #concept mention info dict: concept_mention_id -> [[concept span], lexical cue, text, ignorance_type, sentence_id]
    # print(article_to_all_dicts[articles[0]][0])
    #subject_scope_info_dict: subject_scope_id -> [[subject_span], sentence, subject_scope, SUBJECT_SCOPE]
    # print(article_to_all_dicts[articles[0]][1])
    #subject_scope_to_concept_mention_info_dict: subject_scope_id -> [concept_ids]
    # print(article_to_all_dicts[articles[0]][2])


    ###IGNORANCE GRAPH INITIALIZATION AND INFORMATION NEEDED FOR GRAPH
    Ignorance_Graph = nx.Graph()
    Ignorance_Graph.add_node('ALL_ARTICLES', NODE_TYPE='ALL_ARTICLES') #ONE LARGE NODE
    Ignorance_Graph.add_node('IGNORANCE_TAXONOMY', NODE_TYPE='IGNORANCE_TAXONOMY') #ONE LARGE NODE
    # print(Ignorance_Graph.nodes.data())
    # raise Exception('hold')
    large_nodes = ['ALL_ARTICLES','IGNORANCE_TAXONOMY']

    all_articles_attributes = ['NODE_TYPE']
    ignorance_taxonomy_attributes = ['NODE_TYPE']
    broad_ignorance_taxonomy_attributes = ['NODE_TYPE']
    narrow_ignorance_taxonomy_attributes = ['NODE_TYPE']
    taxonomy_lexical_cue_attributes = ['NODE_TYPE', 'ANNOTATION_TEXT']
    article_attributes = ['NODE_TYPE', 'ARTICLE_DATE', 'TOTAL_SENTENCE_COUNT', 'TOTAL_WORD_COUNT', 'IGNORANCE_SENTENCE_COUNT']
    sentence_attributes = ['NODE_TYPE', 'SENTENCE_SPAN', 'SENTENCE_TEXT', 'SENTENCE_ANNOTATION_ID']
    annotated_lexical_cues_attributes = ['NODE_TYPE', 'MENTION_ANNOTATION_ID', 'MENTION_SPAN', 'MENTION_TEXT']

    ##save graph by date so we know when it is from
    today = datetime.datetime.now()
    d = today.strftime('%x').replace('/', '_')


    attribute_dict = {'ALL_ARTICLES': all_articles_attributes, 'IGNORANCE_TAXONOMY': ignorance_taxonomy_attributes ,'ARTICLE':article_attributes, 'SENTENCE':sentence_attributes, 'BROAD_IGNORANCE_TAXONOMY_CATEGORY': broad_ignorance_taxonomy_attributes, 'IGNORANCE_TAXONOMY_CATEGORY':narrow_ignorance_taxonomy_attributes, 'TAXONOMY_LEXICAL_CUE':taxonomy_lexical_cue_attributes, 'ANNOTATED_LEXICAL_CUE': annotated_lexical_cues_attributes}



    ##ADD IGNORANCE TAXONOMY TO THE GRAPH in general (lexical cues and ignorance categories)
    Ignorance_Graph, all_lcs_dict, all_ignorance_types = add_ignorance_taxonomy_to_graph(Ignorance_Graph, all_lcs_path, current_ignorance_types, broad_categories_dict, old_ignorance_types_dict, narrow_ignorance_taxonomy_attributes, broad_ignorance_taxonomy_attributes, taxonomy_lexical_cue_attributes)
    print(all_ignorance_types) ##{'ALTERNATIVE_OPTIONS_CONTROVERSY', 'QUESTION_ANSWERED_BY_THIS_WORK', 'FUTURE_WORK', 'INCOMPLETE_EVIDENCE', 'ANOMALY_CURIOUS_FINDING', 'FUTURE_PREDICTION', 'EXPLICIT_QUESTION', 'IMPORTANT_CONSIDERATION', 'PROBLEM_COMPLICATION', 'DIFFICULT_TASK', 'FUTURE_OPPORTUNITIES', 'SUPERFICIAL_RELATIONSHIP', 'PROBABLE_UNDERSTANDING', 'FULL_UNKNOWN'}

    # raise Exception('hold')

    ##ignorance taxonomy graph only
    Ignorance_Taxonomy_Graph = copy.deepcopy(Ignorance_Graph)
    specific_article_graph = nx.Graph()
    Ignorance_Taxonomy_Graph.remove_node('ALL_ARTICLES')

    ##per article graphs
    Ignorance_Graph_copy = copy.deepcopy(Ignorance_Graph)
    article_graph_dict = {} #dict from article -> article graph
    small_article_graph_dict = {} #dict from article -> article graph with just the nodes of interest (no extra lexical cues)
    # print('initial article graph inf')
    # print(len(list(Ignorance_Graph_copy.nodes)), len(list(Ignorance_Graph_copy.edges)))


    ###IGNORANCE GRAPH ADD NODES PER ARTICLE
    for i, article in enumerate(articles):


        # if i == 0:
        Ignorance_Graph = add_article_info_to_graph(Ignorance_Graph, article_to_all_dicts, article, article_date_info_dict, article_count_summary_stats_dict, all_lcs_dict, current_ignorance_types, old_ignorance_types_dict, article_attributes, sentence_attributes, annotated_lexical_cues_attributes)

        # print('before each article')

        ##initialize graph for each article: need to make sure it is one article at a time: initial_article_graph is not getting updated!
        initial_article_graph = copy.deepcopy(Ignorance_Graph_copy)
        # print(len(list(initial_article_graph.nodes)), len(list(initial_article_graph.edges)))
        if len(list(Ignorance_Graph_copy.nodes)) != len(list(initial_article_graph.nodes)) or len(list(Ignorance_Graph_copy.edges)) != len(list(initial_article_graph.edges)):
            raise Exception('ERROR : Issue with initializing each articles graph!')
        else:
            # specific_article_graph.clear()
            specific_article_graph = add_article_info_to_graph(initial_article_graph, article_to_all_dicts, article, article_date_info_dict, article_count_summary_stats_dict, all_lcs_dict, current_ignorance_types, old_ignorance_types_dict, article_attributes, sentence_attributes, annotated_lexical_cues_attributes)
            # print('after each article')
            # print(len(list(initial_article_graph.nodes)), len(list(initial_article_graph.edges)))
            # print(len(list(specific_article_graph.nodes)), len(list(specific_article_graph.edges)))

            article_graph_dict[article] = specific_article_graph

            ##small article graph without any extra lexical cues
            small_initial_article_graph = copy.deepcopy(specific_article_graph)
            #remove all TAXONOMY_LEXICAL_CUE nodes with degree 1 (meaning that they are only attached to the ignorance taxonomy and not the ANNOTATED_LEXICAL CUES (which would have degrees of 2)
            degree_criteria_list = [1]
            small_article_graph = remove_specific_nodes_by_degree(small_initial_article_graph, 'TAXONOMY_LEXICAL_CUE', degree_criteria_list)

            small_article_graph_dict[article] = small_article_graph

            # print('small article graph')
            # print(len(list(small_article_graph.nodes)), len(list(small_article_graph.edges)))


    # raise Exception('hold')





            # print('SAVING ARTICLE GRAPH FOR %s WITH %s nodes and %s edges' % (
            # article, len(list(specific_article_graph.nodes)), len(list(specific_article_graph.edges))))
            # save_networkx_graph(specific_article_graph, "%s%s%s_%s_%s.gpickle" % (
            # output_folder, visualizations_folder, article, 'IGNORANCE_GRAPH', d))

            # initial_article_graph.clear()
            # specific_article_graph.clear()


    # raise Exception('hold')


    ###EXPLORE/VISUALIZE GRAPH
    ##Nodes
    print('finished graph!')
    # print(list(Ignorance_Graph.nodes))
    # print(len(list(Ignorance_Graph.nodes)))
    # print(Ignorance_Graph.nodes.data()) #list of tuples
    for n in Ignorance_Graph.nodes.data():
        # print('NODE:', n[0], n)
        # if n[0] in large_nodes:
        #     print('NODE:', n[0])
        if len(n[1]) == 0:
            print(n)
            raise Exception('ERROR: Issue with there being no attributes for the node!')

        elif n[1]['NODE_TYPE'] not in attribute_dict.keys():
            print(n[1])
            raise Exception('ERROR: Missing node type in dictionary with attributes.')

        else:
            specific_attribute_dict = attribute_dict[n[1]['NODE_TYPE']]
            for attribute in specific_attribute_dict[1:]: #SKIP NODE_TYPE
                print('%s: %s' % (attribute, n[1][attribute]))


        # #article information
        # if n[1]['NODE_TYPE'] == 'ARTICLE':
        #     for a_a in article_attributes:
        #         print('%s: %s' %(a_a, n[1][a_a]))
        #
        # #sentence information
        # if n[1]['NODE_TYPE'] =='SENTENCE':
        #     for a_a in article

    ##Edges
    # print(list(Ignorance_Graph.edges))






    ##SAVE THE FULL IGNORANCE BASE
    print('SAVING IGNORANCE GRAPH WITH %s nodes and %s edges' %(len(list(Ignorance_Graph.nodes)), len(list(Ignorance_Graph.edges))))
    save_networkx_graph(Ignorance_Graph, "%s%s%s_%s.gpickle" %(output_folder, visualizations_folder, 'IGNORANCE_GRAPH_60_ARTICLES', d))
    # nx.write_gpickle(Ignorance_Graph, "%s%s%s_%s.gpickle" %(output_folder, visualizations_folder, 'IGNORANCE_GRAPH_60_ARTICLES', d))

    ##SAVE THE IGNORANCE TAXONOMY SEPRATELY
    print('SAVING IGNORANCE TAXONOMY GRAPH WITH %s nodes and %s edges' % (len(list(Ignorance_Taxonomy_Graph.nodes)), len(list(Ignorance_Taxonomy_Graph.edges))))
    save_networkx_graph(Ignorance_Taxonomy_Graph, "%s%s%s_%s.gpickle" % (output_folder, visualizations_folder, 'IGNORANCE_TAXONOMY_GRAPH', d))
    # nx.write_gpickle(Ignorance_Taxonomy_Graph,"%s%s%s_%s.gpickle" % (output_folder, visualizations_folder, 'IGNORANCE_TAXONO_GRAPH', d))

    ##save each article graph
    for article in article_graph_dict:
        print('SAVING ARTICLE GRAPH FOR %s WITH %s nodes and %s edges' %(article, len(list(article_graph_dict[article].nodes)), len(list(article_graph_dict[article].edges))))
        save_networkx_graph(article_graph_dict[article], "%s%s%s_%s_%s.gpickle" % (output_folder, visualizations_folder, article, 'IGNORANCE_GRAPH', d))

        print('SAVING SMALL ARTICLE GRAPH FOR %s WITH %s nodes and %s edges' %(article, len(list(small_article_graph_dict[article].nodes)), len(list(small_article_graph_dict[article].edges))))
        save_networkx_graph(small_article_graph_dict[article], "%s%s%s_%s_%s.gpickle" % (output_folder, visualizations_folder, article, 'SMALL_IGNORANCE_GRAPH', d))

