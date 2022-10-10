import pandas as pd
import networkx as nx
import datetime



def read_in_graph_pkl_file(graph_file_path):
    #read in a graph gpickle file
    graph = nx.read_gpickle(graph_file_path)
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


def find_node_by_node_type(graph, node_type_list):
    #return a list of all the nodes of a specific node_type
    node_type_of_interest_list = []
    for node in list(graph.nodes):
        if graph.nodes[node]['NODE_TYPE'].upper() in [node_type.upper() for node_type in node_type_list]:
            node_type_of_interest_list += [node]

        else:
            pass

    return node_type_of_interest_list


def find_node_with_specific_string(graph, node_type_list, attribute, string_of_interest):
    #returns a list of tuples with (node, attribute) with the string of interest in the attribute
    nodes_with_string_list = []

    node_type_of_interest_list = find_node_by_node_type(graph, node_type_list)
    for node in node_type_of_interest_list:
        ##TODO: make this a regex
        # print(graph[node]) #dict of neighbors
        if string_of_interest.lower() in graph.nodes[node][attribute.upper()].lower():
            nodes_with_string_list += [(node, graph.nodes[node][attribute.upper()])]
        else:
            pass

    return nodes_with_string_list


def find_neighbors_with_attribute(graph, node_list, node_type_list, attribute, ):
    ##retuns tuples of (neighbor, attribute) list matching the node_list - same order
    attributes_of_interest_list = []
    for node, node_attribute in node_list:
        # print('NEIGHBORS', graph[node])
        node_attribute_list = []
        for neighbor in graph[node].keys():
            # print(neighbor)
            # print(graph.nodes[neighbor])
            #need to make sure the neighbor has the correct node_type that I want
            if graph.nodes[neighbor]['NODE_TYPE'].upper() in [node_type.upper() for node_type in node_type_list]:
                node_attribute_list += [(neighbor, graph.nodes[neighbor][attribute.upper()])]
            else:
                pass

        attributes_of_interest_list += [node_attribute_list]


    return attributes_of_interest_list



def create_pandas_dataframe(all_lists, all_names):
    panda_dict = {} #name to list
    for i, l in enumerate(all_lists):
        panda_dict[all_names[i]] = l

    df = pd.DataFrame(panda_dict)
    return df

def output_by_df_column_count(string_of_interest, dataframe, column_name, entities_list, output_folder, date):
    # column_of_interest = dataframe[column_name]
    # print(column_of_interest)

    count_dict = {} #dict from entity -> count

    ##PER ENTITY WE GET SMALLER DATAFRAMES
    for entity in entities_list:
        print(entity)
        #https://stackoverflow.com/questions/53342715/pandas-dataframe-select-rows-where-a-list-column-contains-any-of-a-list-of-strin
        # df[pd.DataFrame(df.species.tolist()).isin(selection).any(1).values]
        df_subset = dataframe[pd.DataFrame(dataframe[column_name].tolist()).isin([entity]).any(1).values]
        print(df_subset.shape)
        df_subset.to_csv(r'%s%s_%s_%s_%s.csv' % (output_folder, string_of_interest.replace(' ','_'), entity, df_subset.shape[0], date), index=False)

        if count_dict.get(entity):
            raise Exception('ERROR: Issue with duplicate entities in entity list!')
        else:
            count_dict[entity] = df_subset.shape[0]

    sorted_entities_list = [x for _, x in sorted(zip(list(count_dict.values()), entities_list), reverse = True)]
    print(sorted_entities_list)
    with open('%s%s_%s_%s.txt' %(output_folder, string_of_interest.replace(' ', '_'), 'summary_counts', date), 'w+') as summary_count_output:
        summary_count_output.write('%s\t%s\n' %(column_name, 'COUNT'))
        for e in sorted_entities_list:
            summary_count_output.write('%s\t%s\n' %(e,count_dict[e]))








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



    dictionary_output_folder = output_folder + dictionary_folder

    pmcid_date_info = 'PMCID_date_info.txt'

    article_count_summary_stats_file_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Concept-Recognition-as-Translation-master/Output_Folders/eval_preprocess_article_summary.txt'

    current_ignorance_graph_file = 'IGNORANCE_GRAPH_60_ARTICLES_09_11_21.gpickle' ##TODO: make sure this is the most up-to-date file!!!

    ##save graph by date so we know when it is from
    today = datetime.datetime.now()
    d = today.strftime('%x').replace('/', '_')

    Ignorance_Graph = read_in_graph_pkl_file('%s%s%s' %(output_folder, visualizations_folder,current_ignorance_graph_file))

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

    ##find sentences with a specific string in it
    string_of_interest = 'vitamin D'
    sentence_node_type_list = ['SENTENCE']
    senetence_attribute = 'SENTENCE_TEXT'

    nodes_with_string_list = find_node_with_specific_string(Ignorance_Graph, sentence_node_type_list, senetence_attribute, string_of_interest)
    print(len(nodes_with_string_list))

    ##find the article dates for each sentence node
    article_node_type_list = ['ARTICLE']
    date_attribute = 'ARTICLE_DATE'
    date_attributes_of_interest_list = find_neighbors_with_attribute(Ignorance_Graph, nodes_with_string_list, article_node_type_list, date_attribute)
    print(len(date_attributes_of_interest_list)) #tuple of (node, attribute)

    if len(nodes_with_string_list) != len(date_attributes_of_interest_list):
        raise Exception('ERROR: Issue with length of attribute list compared to node list!')
    else:
        pass


    # print(nodes_with_string_list[:10])
    # print(date_attributes_of_interest_list[:10])

    ##grab the annotated lexical cues for these sentences
    annotated_lexical_cue_node_type_list = ['ANNOTATED_LEXICAL_CUE']
    annotated_lexical_cue_attribUte = 'MENTION_TEXT'
    annotated_lexical_cue_attributes_of_interest = find_neighbors_with_attribute(Ignorance_Graph, nodes_with_string_list, annotated_lexical_cue_node_type_list, annotated_lexical_cue_attribUte, )

    # print(len(annotated_lexical_cue_attributes_of_interest))
    # print(annotated_lexical_cue_attributes_of_interest[:10])

    if len(annotated_lexical_cue_attributes_of_interest) != len(nodes_with_string_list):
        raise Exception('ERROR: Issue with annotated lexical cue attributes of interest list')
    else:
        pass


    ##TODO: grab the ignorance types for these annotated lexical cues
    ##ignorance_lexical_cues
    full_ignorance_taxonomy_info = []
    full_ignorance_taxonomy_lexical_cue_info = []
    for l in annotated_lexical_cue_attributes_of_interest:
        final_ignorance_taxonomy_category_list = [] ##flattened
        final_taxonomy_lexical_cue_list = []  # flattened
        # print('lexical cue graph')
        # print(l)


        ##if the annotated lexical cue is also attached to an ignorance category then it is a non-standard mapping
        non_standard_ignorance_taxonomy = find_neighbors_with_attribute(Ignorance_Graph, l,['IGNORANCE_TAXONOMY_CATEGORY'], 'NODE_TYPE')
        # print(non_standard_ignorance_taxonomy)

        if len(l) != len(non_standard_ignorance_taxonomy):
            raise Exception('ERROR: Issue with non_standard_ignorance_taxonomy')
        else:
            pass



        ##take all the annotated lexical cues and graph their taxonomy lexical cues
        taxonomy_lexical_cue_list = find_neighbors_with_attribute(Ignorance_Graph, l, ['TAXONOMY_LEXICAL_CUE'], 'ANNOTATION_TEXT')
        # print('taxonomy lexical cues')
        # print(taxonomy_lexical_cue_list)

        if len(non_standard_ignorance_taxonomy) != len(taxonomy_lexical_cue_list):
            raise Exception('ERROR: Issue with taxonomy lexical cue list')
        else:
            pass

        ##grab all the possible ignorance taxonomy categories based on the lexical cues
        possible_taxonomy_category_list = []
        for tlc in taxonomy_lexical_cue_list:
            # print(tlc)
            taxonomy_category = find_neighbors_with_attribute(Ignorance_Graph, tlc, ['IGNORANCE_TAXONOMY_CATEGORY'], 'NODE_TYPE')
            # print(taxonomy_category)
            possible_taxonomy_category_list += taxonomy_category

        if len(taxonomy_lexical_cue_list) != len(possible_taxonomy_category_list):
            raise Exception('ERROR: Issue with possible taxonomy category list')
        else:
            pass

        ##final taxonomy category list based on determining if it is non-standard or not and taking that over the ignorance taxonomy ones

        for i, t in enumerate(non_standard_ignorance_taxonomy):
            ##update the taxonomy words to flatten

            ##sometimes it was annotated to the ignorance category if it was new at the time
            # print(taxonomy_lexical_cue_list[i])
            if len(set(taxonomy_lexical_cue_list[i][0])) == 1 and list(set(taxonomy_lexical_cue_list[i][0]))[0].upper() in current_ignorance_types:
                # print(l[i][1])
                final_taxonomy_lexical_cue_list += [(l[i][1], taxonomy_lexical_cue_list[i][0][1])]
                # print([(l[i][1], taxonomy_lexical_cue_list[i][0][1])])
                # print(final_taxonomy_lexical_cue_list[i-2:])
                # raise Exception('hello')

            else:
                final_taxonomy_lexical_cue_list += taxonomy_lexical_cue_list[i]


            ##update all the taxonomy categories to be either the nonstandard or the taxonomy one
            if t:
                ##TODO: can add a marking that says it is non-standard
                final_ignorance_taxonomy_category_list += t
            else:
                final_ignorance_taxonomy_category_list += possible_taxonomy_category_list[i]

        # print(final_ignorance_taxonomy_category_list)
        # print(final_taxonomy_lexical_cue_list)

        if len(possible_taxonomy_category_list) != len(final_ignorance_taxonomy_category_list):
            raise Exception('ERROR: Issue with final ignorance taxonomy category list')
        else:
            pass

        if len(final_ignorance_taxonomy_category_list) != len(final_taxonomy_lexical_cue_list):
            raise Exception('ERROR: Issue with final taxonomy lexical cue list')
        else:
            pass

        ##update all things
        full_ignorance_taxonomy_info += [final_ignorance_taxonomy_category_list]
        full_ignorance_taxonomy_lexical_cue_info += [final_taxonomy_lexical_cue_list]

    # raise Exception('hold')

    if len(annotated_lexical_cue_attributes_of_interest) != len(full_ignorance_taxonomy_lexical_cue_info):
        print(len(full_ignorance_taxonomy_lexical_cue_info))
        raise Exception('ERROR: Issue with full ignorance taxonomy lexical cue info')
    else:
        pass
    if len(annotated_lexical_cue_attributes_of_interest) != len(full_ignorance_taxonomy_info):
        print(len(full_ignorance_taxonomy_info))
        raise Exception('ERROR: Issue with full ignorance taxonomy info')
    else:
        pass




    print('finished gathering all data!')

    print(nodes_with_string_list[2])
    print(date_attributes_of_interest_list[2])
    print(annotated_lexical_cue_attributes_of_interest[2])
    print(full_ignorance_taxonomy_info[2])
    print(full_ignorance_taxonomy_lexical_cue_info[2])

    ##create a pandas dataframe of all the info
    all_dates = [d[0][1] for d in date_attributes_of_interest_list]
    all_articles = [a[0][0] for a in date_attributes_of_interest_list]
    all_sentences = [s[1] for s in nodes_with_string_list]
    all_ignorance_categories = [] #sets of all the ignorance categories
    all_lexical_cues = [] #(lexical cue, ignorance category)
    for i, lc in enumerate(annotated_lexical_cue_attributes_of_interest):
        current_ignorance_categories = set([])
        current_lexical_cues = []
        # print(lc)
        # print(full_ignorance_taxonomy_info[i])
        for j, l in enumerate(lc):
            # print(j)
            # print(l)
            # print(full_ignorance_taxonomy_info[i][j])
            # print(full_ignorance_taxonomy_lexical_cue_info[i][j])

            current_ignorance_categories.add(full_ignorance_taxonomy_info[i][j][0])
            current_lexical_cues += [(full_ignorance_taxonomy_lexical_cue_info[i][j][0], full_ignorance_taxonomy_info[i][j][0])]


        all_lexical_cues += [current_lexical_cues]
        all_ignorance_categories += [current_ignorance_categories]




    all_lists = [all_dates, all_articles, all_sentences, all_ignorance_categories, all_lexical_cues]
    all_names = ['DATE', 'ARTICLE', 'SENTENCE', 'IGNORANCE_CATEGORIES', 'ANNOTATED LEXICAL CUES']
    string_df = create_pandas_dataframe(all_lists, all_names)
    print(string_df.head())

    string_df.to_csv(r'%s%sINFO_TABLE_%s_%s.csv' %(output_folder, evolution_folder, string_of_interest, d), index=False)

    output_by_df_column_count(string_of_interest, string_df, 'IGNORANCE_CATEGORIES', current_ignorance_types, output_folder+evolution_folder, d)






