import argparse
import pickle
import networkx as nx
import re
from nltk.corpus import stopwords
import time
from rdflib import URIRef


def read_in_pkl_graph(graph_path):
	graph = nx.read_gpickle(graph_path)
	return graph


def pheknowlator_node_info(pheknowlator_node_info_path):
	##goal: dictionary from OBO to the rest of the information

	OBO_to_node_info_dict = {} #OBO_id -> all info
	with open(pheknowlator_node_info_path, 'r+') as pheknowlator_node_info_file:
		#header: all tab delimited: entity_type	integer_id	entity_uri	label	description/definition	synonym
		next(pheknowlator_node_info_file)
		for line in pheknowlator_node_info_file:
			entity_type, integer_id, entity_uri, label, description_definition, synonym = line.strip('\n').split('\t')
			#<http://purl.obolibrary.org/obo/CHEBI_97734>
			#<https://uswest.ensembl.org/Homo_sapiens/Transcript/Summary?t=ENST00000398460>
			obo_id = entity_uri.split('/')[-1].strip('>') #the last part of the uri

			if OBO_to_node_info_dict.get(obo_id):
				print(obo_id)
				print(OBO_to_node_info_dict[obo_id])
				raise Exception('ERROR: Issue with duplicate OBO ids in pheknowlator node file')
			else:
				OBO_to_node_info_dict[obo_id] = [entity_type, integer_id, entity_uri, label, description_definition, synonym]



	return OBO_to_node_info_dict



def all_graph_lexical_cue_words(graph, OBO_to_node_info_dict):
	all_taxonomy_lcs = []
	sentences_dict = {} #sentence_num -> sentence text lower

	for n in list(graph.nodes):
		##grab the taxonomy lexical cues nodes
		try:
			if graph.nodes[n]['NODE_TYPE'] == 'TAXONOMY_LEXICAL_CUE':
				if '...' in n:
					annotation_text = graph.nodes[n]['ANNOTATION_TEXT']

					##TODO: ERROR WITH STARTING WITH ... BUT UNCLEAR WHY!
					# if n.startswith('...'):
					# 	print(n)
					# 	print(graph.nodes[n])
					# 	raise Exception('ERROR: ... at the beginning of the lexical cue')
					# if n.endswith('...'):
					# 	print(n)
					# 	print(graph.nodes[n])
					# 	raise Exception('ERROR: ... at the end of the lexical cue')

					# print(annotation_text)
					if annotation_text == 'NEW_CUE':
						# print('got here')
						regex = n.rstrip('...').lstrip('...').replace('...', '.{%s,%s}' %(0, 20))
					# print(regex)
					else:
						regex = annotation_text

					if regex in all_taxonomy_lcs:
						# print(regex)
						# print(n)
						pass
					# 	raise Exception('regex issue')
					all_taxonomy_lcs += [regex]
				else:
					if n in all_taxonomy_lcs:
						# print(n)
						pass
					# 	raise Exception('lc issue')
					all_taxonomy_lcs += [n]



			##collect the sentences too:
			elif graph.nodes[n]['NODE_TYPE'] == 'SENTENCE':
				sentence_text = graph.nodes[n]['SENTENCE_TEXT'][0].lower()  # a list so we graph the info
				sentence_span = graph.nodes[n]['SENTENCE_SPAN']
				sentence_start = int(sentence_span[0])
				sentence_end = int(sentence_span[1])


				sentence_obo_ids = []
				sentence_obo_starts = []
				sentence_obo_mention_text = []

				article = n.split('-')[-1]
				article_date = graph.nodes[article]['ARTICLE_DATE']

				##get annotated lexical cues with ignorance taxonomy information
				sentence_neighbors = graph[n]
				sentence_lc_categories = []
				sentence_lc_starts = []
				ignorance_sentence = False

				for s in sentence_neighbors:

					##lexical cues
					if s.startswith('LC'):
						ignorance_sentence = True

						##get lexical cue info: annotated_lexical_cues_attributes=['NODE_TYPE','MENTION_ANNOTATION_ID','MENTION_SPAN','MENTION_TEXT']
						# {'NODE_TYPE': 'ANNOTATED_LEXICAL_CUE', 'MENTION_ANNOTATION_ID': 'PMC3257641_T348', 'MENTION_SPAN': [(1237, 1240)], 'MENTION_TEXT': 'but'}
						lexical_cue_info = graph.nodes[s]
						lc_mention_span_list = lexical_cue_info['MENTION_SPAN']
						lc_mention_text = lexical_cue_info['MENTION_TEXT']
						for j, (lc_start, lc_end) in enumerate(lc_mention_span_list):
							if j == 0:
								sentence_lc_starts += [lc_start - sentence_start]
								break
							else:
								pass


						##find ignorance category of lcs
						lc_neighbors = graph[s]
						# print(lc_mention_text)
						# print(lc_neighbors)
						canonical = True
						for l in lc_neighbors:
							# print('lc neighbor', l, graph.nodes[l])
							# taxonomy_lexical_cue_attributes=['NODE_TYPE','ANNOTATION_TEXT'] - TAXONOMY_LEXICAL_CUE
							if graph.nodes[l]['NODE_TYPE'] == 'TAXONOMY_LEXICAL_CUE':
								tax_lc_node = l

							# ignorance_taxonomy_attributes=['NODE_TYPE'] - IGNORANCE_TAXONOMY_CATEGORY
							elif graph.nodes[l]['NODE_TYPE'] == 'IGNORANCE_TAXONOMY_CATEGORY':
								canonical = False
								lc_ignorance_category = l
							# print('ignorance taxonomy', l)
							# print(tax_lc_node)
							# print(lc_mention_text)
							# print(l)
							# raise Exception('hold')

							##other sentences
							else:
								# print('here', l)
								continue

						if canonical:
							##get ignorance info: ignorance_taxonomy_attributes=['NODE_TYPE'] - 'IGNORANCE_TAXONOMY_CATEGORY'
							# print('got here')
							lc_tax_neighbors = graph[tax_lc_node]
							for t in lc_tax_neighbors:
								if graph.nodes[t]['NODE_TYPE'] == 'IGNORANCE_TAXONOMY_CATEGORY':
									lc_ignorance_category = t
						# print(lc_ignorance_category)
						# print(lc_mention_text, )

						else:
							##lc_ignorance_category already defined ideally by connection
							pass

						# print(lc_ignorance_category)

						sentence_lc_categories += [lc_ignorance_category]

					# raise Exception('hold')

					##TODO: more obos! - FIX
					elif s.startswith('http'):
						# print(s.split('/')[-1])
						##get other obo ids:
						all_other_obo_mention_edge_info_dict = graph.get_edge_data(n, s)
						# print(all_other_obo_mention_edge_info_dict)
						other_obo_id = s.split('/')[-1]

						for i, other_obo_mention_edge_info_dict in all_other_obo_mention_edge_info_dict.items():

							sentence_obo_ids += [other_obo_id]
							other_obo_mention_text = other_obo_mention_edge_info_dict['OBO_MENTION_TEXT']
							other_obo_mention_span_list = other_obo_mention_edge_info_dict['OBO_MENTION_SPAN']  # list of tuples of spans
							# print(other_obo_mention_text)

							for j, (o_start, o_end) in enumerate(other_obo_mention_span_list):
								if j == 0:
									sentence_obo_starts += [o_start - sentence_start]
									sentence_obo_mention_text += [other_obo_mention_text]
									break
								else:
									pass
					# print(sentence_obo_ids)
					# print(sentence_output_text)
					# raise Exception('hold')
					else:
						pass

				##sort the obo_ids by starts and then need labels for output
				zipped_lists = zip(sentence_obo_starts, sentence_obo_ids, sentence_obo_mention_text)
				# print(sentence_obo_ids)
				sorted_zipped_lists = sorted(zipped_lists)
				# print(sorted_zipped_lists)
				sorted_sentence_obo_ids = [(element, r, m) for r, element, m in sorted_zipped_lists]
				sorted_sentence_obo_info = [(id, OBO_to_node_info_dict[id][3], r, m) for id, r, m in
											sorted_sentence_obo_ids]
				# if sorted_sentence_obo_info:
				# 	print('got here')
				# 	print(sorted_sentence_obo_info)
				# raise Exception('hold')

				##sort the lexical cues by starts
				zipped_lists_lc = zip(sentence_lc_starts, sentence_lc_categories)
				# print(sentence_obo_ids)
				sorted_zipped_lists_lc = sorted(zipped_lists_lc)
				sorted_sentence_lc = [(element, r) for r, element in sorted_zipped_lists_lc]
				# sorted_sentence_lc_info = [it for  in sorted_sentence_lc]
				# if sorted_sentence_lc:
				# 	print('got here')
				# 	print(sorted_sentence_lc)



				##'ARTICLE', 'ARTICLE DATE', 'SENTENCE NUM', 'SENTENCE', 'IGNORANCE CATEGORIES', 'NUM IGNORANCE CATEGORIES', 'OBO ID (LABEL)'
				if ignorance_sentence:

					sentences_dict[n] = [article, article_date, n, [sentence_text], sorted_sentence_lc, len(sorted_sentence_lc), sorted_sentence_obo_info]
					if len(sorted_sentence_lc) == 0:
						print(n)
						print(sentences_dict[n])
						raise Exception('ERROR: Issue with gathering the lexical cue information')
				else:
					sentences_dict[n] = [article, article_date, n, [sentence_text], 'N/A', 'N/A', sorted_sentence_obo_info]


				# print(n, processed_sentence_text)
			else:
				pass

		##other nodes - pheknowlator!
		except KeyError:
			continue

	# raise Exception('hold')

	# if len(set(all_taxonomy_lcs)) != len(all_taxonomy_lcs):
	# 	print(len(set(all_taxonomy_lcs)), len(all_taxonomy_lcs))
	# 	raise Exception('ERROR: Issue with capturing duplicates of taxonomy cues')
	# else:
	# 	pass
	print(len(all_taxonomy_lcs), len(set(all_taxonomy_lcs)))


	return list(set(all_taxonomy_lcs)), sentences_dict


def all_graph_sentences_preprocess(sentences_dict, all_taxonomy_lcs):
	preprocess_sentence_dict = {}  # sent_num -> preprocessed sentence

	english_stopwords = set(stopwords.words('english'))
	for sent_num in sentences_dict.keys():
		processed_sentence_text = sentences_dict[sent_num][3][0]

		##get rid of all lexical cues
		get_rid_lc_count = 0
		for lc in all_taxonomy_lcs:
			# print(lc)
			regex_lc = r' %s ' % (lc.lower().replace('_', ' ').replace('?', '\?').replace(')', '\)').replace('(', '\('))
			prev_sent_len = len(processed_sentence_text)
			processed_sentence_text = re.sub(regex_lc, ' ', processed_sentence_text)  # doesnt do anything if it is not there

			if prev_sent_len == len(processed_sentence_text):
				pass
			else:
				# print(regex_lc)
				get_rid_lc_count += 1
		# print(processed_sentence_text)
		# print(len(processed_sentence_text))

		# print(processed_sentence_text)
		# print(len(processed_sentence_text))
		# print(get_rid_lc_count)
		# print(obo_id_list_count)

		##get rid of stopwords!
		processed_sentence_text_list = [w for w in processed_sentence_text.split(' ') if not w.lower() in english_stopwords]
		processed_sentence_text = ' '.join(processed_sentence_text_list)
		# print(processed_sentence_text)

		preprocess_sentence_dict[sent_num] = processed_sentence_text



	return preprocess_sentence_dict







if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-ignorance_full_graph', type=str, help='the file path to the ignorance full graph that we want to explore as a .gpickle file')
	parser.add_argument('-pheknowlator_node_info', type=str, help='file path to the node information for pheknowlator')
	parser.add_argument('-output_path', type=str, help='the output file path for the results')
	args = parser.parse_args()


	start_time = time.time()

	##read in gpickle ignorance graph file
	Full_Ignorance_Graph = read_in_pkl_graph(args.ignorance_full_graph)

	##read in all phewknowlator node info
	OBO_to_node_info_dict = pheknowlator_node_info(args.pheknowlator_node_info)  # OBO_to_node_info_dict[obo_id] = [entity_type, integer_id, entity_uri, label, description_definition, synonym]

	all_taxonomy_lcs, sentences_dict = all_graph_lexical_cue_words(Full_Ignorance_Graph, OBO_to_node_info_dict)
	print('NUMBER OF TAXONOMY LEXICAL CUES:', len(all_taxonomy_lcs))

	##output the sentence dict
	output_sentence_dict = open('%s%s_%s.pkl' % (
	args.output_path, args.ignorance_full_graph.split('/')[-1].replace('.gpickle', ''), 'ALL_SENTENCES_DICT'), 'wb')
	pickle.dump(sentences_dict, output_sentence_dict)
	output_sentence_dict.close()

	##gather all the sentences from the ignorance graph
	preprocess_sentence_dict = all_graph_sentences_preprocess(sentences_dict, all_taxonomy_lcs)
	print('NUMBER OF SENTENCES PREPROCESSED:', len(preprocess_sentence_dict.keys()))



	##output the preprocesed sentence dict
	output_preprocess_sentence_dict = open('%s%s_%s.pkl' % (args.output_path, args.ignorance_full_graph.split('/')[-1].replace('.gpickle', ''), 'PREPROCESSED_SENTENCE_DICT'), 'wb')
	pickle.dump(preprocess_sentence_dict, output_preprocess_sentence_dict)
	output_preprocess_sentence_dict.close()


	print("--- %s seconds ---" % (time.time() - start_time))
