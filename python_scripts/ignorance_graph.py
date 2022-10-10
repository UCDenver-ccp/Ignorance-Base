import os
import pickle


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


def read_pmcid_info(file_path, filename):
    article_date_info_dict = {} #pmcid -> date
    with open('%s%s' %(file_path, filename), 'r') as pmcid_info_file:
        next(pmcid_info_file)
        for line in pmcid_info_file:
            pmcid, date = line.strip('\n').split('\t')
            article_date_info_dict[pmcid] = date

    return article_date_info_dict



def find_node_BFS(graph, items_to_find):
    # print('items to find', items_to_find)
    # for i in items_to_find:
        # print(i.get_value())

    explored = []
    # keep track of nodes to be checked
    queue = []
    for hn in graph:
        # print('head node', hn, hn.get_value())
        queue += [hn]
        # keep looping until there are nodes still to be checked
        while queue:
            # pop shallowest node (first node) from queue
            # print('queue', queue)
            # print('explored', explored)
            node = queue.pop(0)

            # print('node:', node, type(node))#, node.get_value())


            ##make sure it is not already explored
            if node not in explored:
                # print('node', node, node.get_value())
                # print('node value', node.get_value())
                # print('node tuple:', node_tuple)
                if node not in items_to_find:
                    # add node to list of checked nodes
                    explored.append(node)
                    neighbours = node.get_edges()  # list of edges with the matching type
                    # print('all neighbors', neighbours)
                    # raise Exception('PAUSE!')

                    # add neighbours of node to queue
                    if neighbours:
                        for neighbour in neighbours:
                            # print('neighbor', neighbour) #,neighbour.get_value(), neighbour.get_edges())
                            if isinstance(neighbour, tuple):
                                neighbour_updated = neighbour[0]
                            else: #node!
                                print(neighbour)
                                # neighbour_updated = neighbour
                                raise Exception('ERROR: SHOULD ALWAYS BE TUPLES THAT INCLUDE THE MATCH TYPE!')

                            queue.append(neighbour_updated) #we don't want the matching type to keep looping through
                    else:
                        pass

                ##we found the node in the graph head nodes
                else:
                    # print('HERE!')
                    # raise Exception('hold please!')
                    return node
            else:
                pass


    return 'NEW_HEAD_NODE'




class Node:
    def __init__(self, ntype, value, edges):
        self.ntype = ntype.upper()
        self.value = value
        self.edges = edges



    def get_ntype(self):
        return self.ntype

    def get_value(self):
        return self.value

    def get_edges(self):
        return self.edges



    def add_edges(self, new_node_edges):
        #a list of the tuples to add
        # for new_edge in new_edges:
        #     self.edges += [new_edge]
        if self.edges:
            self.edges += new_node_edges
        else:
            self.edges = new_node_edges

    def delete_edges(self, del_edges):
        #del edges = a list of the tuples to get rid of
        # print(self.edges)
        # print(del_edges)
        for d_edge in del_edges:
            if self.edges:
                # print(self.edges)
                d_edge_index = self.edges.index(d_edge)
                self.edges.pop(d_edge_index)
            else:
                pass


    def __eq__(self, other):
        #match on value not edges
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.get_value()[0] == other.get_value()[0] #and self.get_edges() == other.get_edges()


class Graph:
    def __init__(self, graph_type):
        self.graph_type = graph_type
        self.head_nodes = [] #list of the headnodes of type node
        self.all_nodes_values = {} #dict: node value -> node type
        self.all_nodes_types = []


    def get_head_nodes(self):
        return self.head_nodes

    def insert_nodes(self, node_type, value, node_edges):
        ##ARTICLE NODES
        if node_type.upper() in ['ARTICLE', 'SENTENCE_SUBJECT', 'LEXICAL_CUE', 'OBO', 'IGNORANCE_CATEGORY']: #stand alone nodes - value = (PMCID, date), node_edges = None

            #initialize the node!
            node = Node(node_type, value, node_edges)


            if node_edges:
            ##all the values of nodes we have seen
                if self.all_nodes_values.get(value[0]):
                    pass
                else:
                    ##insert the node into the graph if new, otherwise add edges to the graph
                    self.all_nodes_values[value[0]] = node
                    # raise Exception('VALUE ALREADY IN ALL NODE VALUES')

                for ne in node.get_edges():
                    print(ne)
                    if ne not in self.all_nodes_values.keys():
                        self.all_nodes_values[value[0]] = node
                    else:
                        pass
                # print(self.all_nodes_values)

                ##insert the node into the graph if new, otherwise add edges to the graph

                if not self.head_nodes:
                    self.head_nodes += [node]
                else:
                    all_edges = node.get_edges() #all nodes!
                    print('all_edges', all_edges)
                    items_to_find = [node]
                    for e in all_edges:
                        items_to_find += [self.all_nodes_values[e]] ##the nodes to find without the match types

                    # items_to_find = [node] + all_edges
                    print('ITEMS TO FIND PLEASE!', items_to_find)
                    ##use BFS to see if we need to add things to the nodes!
                    node_connection = find_node_BFS(self.head_nodes, items_to_find)
                    print('NODE CONNECTION:', node_connection)
                    if node_connection == 'NEW_HEAD_NODE':
                        self.head_nodes += [node]
                    else:
                        #node_connection = a node that is in the path from items_to_find!
                        #the root node of the tree we want to insert
                        if node_connection == node:
                            # print('node edges', node_edges)
                            node_connection.add_edges(node_edges) #TODO - tuples

                        ## not the root node of the tree we are trying to insert - seems good!
                        else:
                            # print('node to add', value, node_edges)
                            # for edge in node_edges:
                            #     print('EDGE', edge[0].get_value())
                            # node_connection_index = items_to_find.index(node_connection)
                            # print('index of connecting node', node_connection_index)


                            for edge in node.get_edges():
                                print('edges:', edge)
                                if self.all_nodes_values[edge] == node_connection:
                                    edge_to_switch = edge #self.all_nodes_values[edge] #tuple with match_type
                                    # print('hellp', edge_to_switch)
                                else:
                                    pass
                            ##delete the original connection and add a new edge
                            node.delete_edges([edge_to_switch])
                            # edge_to_switch[0].add_edges([(node, edge_to_switch[1])]) #reversing the edges
                            node_connection.add_edges([(node, edge_to_switch)]) #add the reverse edge into the current tree using the node connection
                            # print('node connection info')
                            # print(node_connection.get_value())
                            # print(node_connection.get_edges())
                            # for edge in node_connection.get_edges():
                                # print('new_edge:', edge[0].get_value())
                                # print(edge[0].get_edges())
                                # for e in edge[0].get_edges():
                                #     print(e[0].get_value())
                            # raise Exception('MAKE SURE THE NODE CONNECTION WORKS!')
            else:
                node = Node(node_type, value, node_edges)
                self.head_nodes += [node]
                if value[0] not in self.all_nodes_values.keys():
                    self.all_nodes_values[value[0]] = node






        # #node_edges = [(edge_node, match_type)]
        # # print('node edges', node_edges)
        # if node_edges:
        #     ##all the values of nodes we have seen
        #     if value not in self.all_nodes_values:
        #         self.all_nodes_values.append(value)
        #     else:
        #         pass
        #         # raise Exception('VALUE ALREADY IN ALL NODE VALUES')
        #
        #     for ne in node_edges:
        #         if ne[0].get_value() not in self.all_nodes_values:
        #             self.all_nodes_values.append(ne[0].get_value())
        #
        #     ##insert the node into the graph if new, otherwise add edges to the graph
        #     node = Node(value, node_edges)
        #     if not self.head_nodes:
        #         self.head_nodes += [node]
        #     else:
        #         all_edges = node.get_edges() #all nodes!
        #         # print('all_edges', all_edges)
        #         items_to_find = [node]
        #         for e in all_edges:
        #             items_to_find += [e[0]] ##the nodes to find without the match types
        #
        #         # items_to_find = [node] + all_edges
        #         # print('ITEMS TO FIND PLEASE!', items_to_find)
        #         ##use BFS to see if we need to add things to the nodes!
        #         node_connection = find_node_BFS(self.head_nodes, items_to_find)
        #         if node_connection == 'NEW_HEAD_NODE':
        #             self.head_nodes += [node]
        #         else:
        #             #node_connection = a node that is in the path from items_to_find!
        #             #the root node of the tree we want to insert
        #             if node_connection == node:
        #                 # print('node edges', node_edges)
        #                 node_connection.add_edges(node_edges) #TODO - tuples
        #
        #             ## not the root node of the tree we are trying to insert - seems good!
        #             else:
        #                 # print('node to add', value, node_edges)
        #                 # for edge in node_edges:
        #                 #     print('EDGE', edge[0].get_value())
        #                 # node_connection_index = items_to_find.index(node_connection)
        #                 # print('index of connecting node', node_connection_index)
        #
        #
        #                 for edge in node.get_edges():
        #                     if edge[0] == node_connection:
        #                         edge_to_switch = edge #tuple with match_type
        #                     else:
        #                         pass
        #                 ##delete the original connection and add a new edge
        #                 node.delete_edges([edge_to_switch])
        #                 # edge_to_switch[0].add_edges([(node, edge_to_switch[1])]) #reversing the edges
        #                 node_connection.add_edges([(node, edge_to_switch[1])]) #add the reverse edge into the current tree using the node connection
        #                 # print('node connection info')
        #                 # print(node_connection.get_value())
        #                 # print(node_connection.get_edges())
        #                 # for edge in node_connection.get_edges():
        #                     # print('new_edge:', edge[0].get_value())
        #                     # print(edge[0].get_edges())
        #                     # for e in edge[0].get_edges():
        #                     #     print(e[0].get_value())
        #                 # raise Exception('MAKE SURE THE NODE CONNECTION WORKS!')
        # else:
        #     node = Node(value, node_edges)
        #     self.head_nodes += [node]
        #     if value not in self.all_nodes_values:
        #         self.all_nodes_values.append(value)





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

    print('NUM ARTICLES:', len(articles))

    all_lcs_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Ontologies/Ontology_Of_Ignorance_all_cues_2020-08-25.txt'

    output_folder = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/3_Ignorance_Base/Ignorance-Base/Output_Folders/'
    sentence_folder = 'PMCID_Sentence_Files/'

    sentence_output_folder = output_folder + sentence_folder

    all_combined_data = '0_all_combined'

    dictionary_folder = 'dictionary_files/'

    dictionary_output_folder = output_folder + dictionary_folder

    pmcid_date_info = 'PMCID_date_info.txt'

    ##GET THE ARTICLE DATE INFO AS METADATA - TODO: ADD MORE LATER
    article_date_info_dict = read_pmcid_info(output_folder, pmcid_date_info)


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


    ###ALL GRAPHS!!!

    ##CORPUS GRAPH
    corpus_graph = Graph('CORPUS')
    print(corpus_graph)
    print(corpus_graph.graph_type)

    ##ARTICLE NODES
    for i, article in enumerate(articles):
        if i < 5:
            pmcid_date = article_date_info_dict[article]
            corpus_graph.insert_nodes('article', (article, pmcid_date), None)


    ##SENTENCE NODES
    for i, article in enumerate(articles):
        if i < 5:
            article_subject_scope_info_dict = article_to_all_dicts[article][1]
            for sentence_id, subject_info in article_subject_scope_info_dict.items():
                corpus_graph.insert_nodes('sentence_subject', (sentence_id, subject_info[0], subject_info[1], subject_info[2]), [article])

    ##LEXICAL_CUE NODES
    for i, article in enumerate(articles):
        if i < 5:
            article_concept_mention_info_dict = article_to_all_dicts[article][0]
            for annotation_id, lexical_cue_info in article_concept_mention_info_dict.items():
                print('lexical cue info', lexical_cue_info) #[[33], [43], 'associated', 'associated', 'SUPERFICIAL_RELATIONSHIP', 'PMC1474522.nxml.gz-1']
                corpus_graph.insert_nodes('lexical_cue', (annotation_id, lexical_cue_info[0], lexical_cue_info[1], lexical_cue_info[2], lexical_cue_info[3], lexical_cue_info[4]), [lexical_cue_info[5]])


    ##IGNORANCE CATEGORY NODES - TODO!!!
    for i, article in enumerate(articles):
        if i < 5:
            article_concept_mention_info_dict = article_to_all_dicts[article][0]
            for annotation_id, lexical_cue_info in article_concept_mention_info_dict.items():
                ignorance_id = '%s-%s' % ('IGNORANCE_CATEGORY', current_ignorance_types.index(lexical_cue_info[4].upper()))
                print('ignorance id', ignorance_id, annotation_id)
                corpus_graph.insert_nodes('ignorance_category', (ignorance_id, lexical_cue_info[4]), [annotation_id])



    # for i, article in enumerate(articles):
    #     if i < 5:
    #         article_concept_mention_info_dict = article_to_all_dicts[article][0]
    #         for annotation_id, lexical_cue_info in article_concept_mention_info_dict.items():
    #             print('here')
    #             ignorance_id = '%s-%s' %('IGNORANCE_CATEGORY', current_ignorance_types.index(lexical_cue_info[4].upper()))
    #             print(ignorance_id, annotation_id)
    #             # corpus_graph.insert_nodes('ignorance_category', (ignorance_id, lexical_cue_info[4]), [annotation_id])


    # print(corpus_graph)
    # print(corpus_graph.all_nodes_values)
    print('HEAD NODES!')
    print(corpus_graph.head_nodes)
    print(len(corpus_graph.all_nodes_values), len(corpus_graph.head_nodes))

    for k, node in enumerate(corpus_graph.head_nodes):
        if k < 3:
            print(node.get_value())
            print(node.get_edges())
            print(node.get_ntype())
            for edge in node.get_edges():
                print(edge[0].get_value())
                print(edge[0].get_edges())
                print(edge[0].get_ntype())
                for edge2 in edge[0].get_edges():
                    print(edge2[0].get_value())
                    print(edge2[0].get_edges())
                    print(edge2[0].get_ntype())





    ##ARTICLE GRAPHS


    ##SENTENCE GRAPHS