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
import ast
from rdflib import URIRef
from datetime import datetime



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


def find_obo_ids_from_string_concept_list(OBO_to_node_info_dict, string_obo_concept_input_list):
	##OBO_to_node_info_dict[obo_id] = [entity_type, integer_id, entity_uri, label, description_definition, synonym]
	obo_ids_from_string_list_exact_match = set()
	obo_ids_from_string_list_label = set() ##obo_ids
	obo_ids_from_string_list_synonyms = set()

	for obo_id in OBO_to_node_info_dict.keys():
		[entity_type, integer_id, entity_uri, label, description_definition, synonym] = OBO_to_node_info_dict[obo_id]
		# print(label, synonym)
		# print(type(label), type(synonym))

		for string_obo_concept in string_obo_concept_input_list:
			# print(type(string_obo_concept))
			if '%s' %(string_obo_concept.lower()) == label.lower():
				obo_ids_from_string_list_exact_match.add(obo_id)
				continue
			elif string_obo_concept.lower() in label.lower():
				obo_ids_from_string_list_label.add(obo_id)
				continue
			elif '%s|' %(string_obo_concept.lower()) in synonym.lower() or '|%s' %(string_obo_concept.lower()) in synonym.lower():
				obo_ids_from_string_list_exact_match.add(obo_id)
			elif string_obo_concept.lower() in synonym.lower():
				obo_ids_from_string_list_synonyms.add(obo_id)
				continue
			else:
				pass

	return obo_ids_from_string_list_exact_match, obo_ids_from_string_list_label, obo_ids_from_string_list_synonyms


def gather_all_sentences_with_obo_id(obo_id, OBO_to_node_info_dict, graph, output_path):
	##integer_id is the node label
	[entity_type, integer_id, entity_uri, label, description_definition, synonym] = OBO_to_node_info_dict[obo_id]
	# print(obo_id)
	# print(graph[int(integer_id
	obo_id_degrees = graph.degree(integer_id)
	# print(obo_id_degrees)

	uriref_node = URIRef(entity_uri.replace('<', '').replace('>',''))

	obo_id_neighbors = graph[uriref_node]

	ig = 0
	nig = 0
	ignorance_sent_info_dict = {} #number to information
	not_ignorance_sent_info_dict = {} #number to infomration


	# print(obo_id_neighbors)
	# raise Exception('hold')
	for n in obo_id_neighbors.keys():
		# print(n)

		##we want sentences:
		if n.startswith('S'):
			# print(graph[n])
			##TODO!
			##get all obo_edges: obo_edge_attributes=['OBO_MENTION_ID','OBO_MENTION_TEXT','OBO_MENTION_SPAN']
			obo_id_edge_info = graph.get_edge_data(n, uriref_node)
			# print(obo_id_edge_info, type(obo_id_edge_info))

			##get all sentence information: #sentence_attributes=['NODE_TYPE','SENTENCE_SPAN','SENTENCE_TEXT','SENTENCE_ANNOTATION_ID']

			sentence_info_dict = graph.nodes[n] ##dictionary of sentence information: {'NODE_TYPE': 'SENTENCE', 'SENTENCE_SPAN': (3297, 3404), 'SENTENCE_TEXT': ['Vitamin D status is determined by measuring circulating serum levels of 25-hydroxy vitamin D2\u2009+\u20093(25(OH)D).'], 'SENTENCE_ANNOTATION_ID': 'PMC6011374_16'}

			sentence_span = sentence_info_dict['SENTENCE_SPAN'] ##tuple and integer
			sentence_start = sentence_span[0]

			sentence_text_lower = sentence_info_dict['SENTENCE_TEXT'][0].lower() #list of a string
			# print(sentence_text_lower)
			# print(sentence_span)
			sentence_annotation_id = sentence_info_dict['SENTENCE_ANNOTATION_ID']
			ignorance_sentence = False
			# sentence_output_text = ''


			##get all OBO information
			all_obo_mention_edge_dict = graph[n][uriref_node]  # {0: {'OBO_MENTION_ID': 'PMC6056931_T88', 'OBO_MENTION_TEXT': 'vitamin A', 'OBO_MENTION_SPAN': [(37542, 37551)]}, 1: {'OBO_MENTION_ID': 'PMC6056931_T89', 'OBO_MENTION_TEXT': 'vitamin C', 'OBO_MENTION_SPAN': [(37556, 37565)]}}

			##TODO: error with obos capturing too much!
			# print(len(all_obo_mention_edge_dict.keys()))
			# print(all_obo_mention_edge_dict)
			sentence_obo_ids = []
			sentence_obo_starts = []
			sentence_obo_mention_text = []
			sentence_output_text = sentence_text_lower
			for i, obo_mention_edge_dict in all_obo_mention_edge_dict.items():
				# print(i, obo_mention_edge_dict)
				obo_mention_text = obo_mention_edge_dict['OBO_MENTION_TEXT']
				sentence_obo_ids += [obo_id]
				obo_mention_span_list = obo_mention_edge_dict['OBO_MENTION_SPAN'] #list of tuples of spans
				# print(obo_mention_span_list)
				for j, (start, end) in enumerate(obo_mention_span_list):
					if sentence_output_text.islower():
						obo_sentence_text = sentence_text_lower[start - sentence_start: end - sentence_start].title()
						sentence_output_text = sentence_text_lower[:start - sentence_start] + obo_sentence_text + sentence_text_lower[ end - sentence_start:]
					else:
						obo_sentence_text = sentence_output_text[start - sentence_start: end - sentence_start].title()
						sentence_output_text = sentence_output_text[:start - sentence_start] + obo_sentence_text + sentence_output_text[end - sentence_start:]
					if j == 0:
						sentence_obo_starts += [start-sentence_start]
						sentence_obo_mention_text += [obo_mention_text]
					else:
						pass
					# print(sentence_output_text)

			# print('sentence obo ids', sentence_obo_ids)



			##get article date from sentence - use PMCID from sentence id #article_attributes=['NODE_TYPE','ARTICLE_DATE','TOTAL_SENTENCE_COUNT','TOTAL_WORD_COUNT', 'IGNORANCE_SENTENCE_COUNT']
			article_node = n.split('-')[1].replace('S', '') #article pmcid
			article_info_dict = graph.nodes[article_node]
			article_date = article_info_dict['ARTICLE_DATE']
			# print(article_info_dict)



			##get annotated lexical cues with ignorance taxonomy information
			sentence_neighbors = graph[n]
			sentence_lc_categories = []
			sentence_lc_starts = []
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
						lc_sentence_text = sentence_output_text[lc_start-sentence_start: lc_end-sentence_start].upper()
						sentence_output_text = sentence_output_text[:lc_start-sentence_start] + lc_sentence_text + sentence_output_text[lc_end-sentence_start:]
						if j == 0:
							sentence_lc_starts += [lc_start-sentence_start]
						else:
							pass

					##find ignorance category of lcs
					lc_neighbors = graph[s]
					# print(lc_mention_text)
					# print(lc_neighbors)
					canonical = True
					for l in lc_neighbors:
						# print('lc neighbor', l, graph.nodes[l])
						#taxonomy_lexical_cue_attributes=['NODE_TYPE','ANNOTATION_TEXT'] - TAXONOMY_LEXICAL_CUE
						if graph.nodes[l]['NODE_TYPE'] == 'TAXONOMY_LEXICAL_CUE':
							tax_lc_node = l

						#ignorance_taxonomy_attributes=['NODE_TYPE'] - IGNORANCE_TAXONOMY_CATEGORY
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
					if other_obo_id == obo_id:
						pass
					else:
						for i, other_obo_mention_edge_info_dict in all_other_obo_mention_edge_info_dict.items():

							sentence_obo_ids += [other_obo_id]
							other_obo_mention_text = other_obo_mention_edge_info_dict['OBO_MENTION_TEXT']
							other_obo_mention_span_list = other_obo_mention_edge_info_dict['OBO_MENTION_SPAN']  # list of tuples of spans
							# print(other_obo_mention_text)

							for j, (o_start, o_end) in enumerate(other_obo_mention_span_list):
								other_obo_sentence_text = sentence_output_text[o_start - sentence_start: o_end - sentence_start].title()
								sentence_output_text = sentence_output_text[:o_start - sentence_start] + other_obo_sentence_text + sentence_output_text[o_end - sentence_start:]
								if j == 0:
									sentence_obo_starts += [o_start-sentence_start]
									sentence_obo_mention_text += [other_obo_mention_text]
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
			sorted_sentence_obo_info = [(id, OBO_to_node_info_dict[id][3], r, m) for id, r, m in sorted_sentence_obo_ids]
			# raise Exception('hold')

			##sort the lexical cues by starts
			zipped_lists_lc = zip(sentence_lc_starts, sentence_lc_categories)
			# print(sentence_obo_ids)
			sorted_zipped_lists_lc = sorted(zipped_lists_lc)
			sorted_sentence_lc = [(element, r) for r, element in sorted_zipped_lists_lc]
			# sorted_sentence_lc_info = [it for  in sorted_sentence_lc]



			##output both ignorance statements and not - we can check it maybe?
			if ignorance_sentence:
				# obo_ignorance_output_file.write('%s\t%s\t%s\t%s\t%s\n' %(article_node, article_date, [sentence_output_text], sorted_sentence_lc, sorted_sentence_obo_info))
				if ignorance_sent_info_dict.get(ig):
					print(ig)
					print(ignorance_sent_info_dict[ig])
					raise Exception('ERROR: Issue with ignorance dict')
				else:
					pass

				ignorance_sent_info_dict[ig] = [article_node, article_date, n, [sentence_output_text], sorted_sentence_lc, len(sorted_sentence_lc), sorted_sentence_obo_info]
				ig += 1

				# raise Exception('hold')

			else:
				##also output not ignorance statements
				# obo_no_ignorance_output_file.write('%s\t%s\t%s\t%s\t%s\n' % (article_node, article_date, [sentence_output_text], 'N/A', sorted_sentence_obo_info))
				if not_ignorance_sent_info_dict.get(nig):
					raise Exception('ERROR: Issue with not ignorance dict')
				else:
					pass

				not_ignorance_sent_info_dict[nig] = [article_node, article_date, n, [sentence_output_text], 'N/A', 'N/A', sorted_sentence_obo_info]
				nig += 1

			# raise Exception('hold')
		else:
			pass

	return ignorance_sent_info_dict, not_ignorance_sent_info_dict, label




def ignorance_category_find(ignorance_category_list, ignorance_example_tracking, ignorance_sent_info_dict, ignorance_specific_info_dict):
	for d in ignorance_sent_info_dict.keys(): #numbers
		# print('got here!')
		# print(d)
		article_node, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lcs, sorted_sentence_obo_info = ignorance_sent_info_dict[d]
		sent_ignorance_categories_set = set([l[0].lower() for l in sorted_sentence_lc])
		# print(sent_ignorance_categories_set)
		for sig in sent_ignorance_categories_set:
			if sig in ignorance_category_list:
				sig_index = ignorance_category_list.index(sig.lower())
				num_track = ignorance_example_tracking[sig_index]
				if ignorance_specific_info_dict[sig.lower()].get(num_track):
					print(ignorance_specific_info_dict[sig.lower()][num_track])
					raise Exception('ERROR: Issue with ignorance specific tracking')
				else:
					pass
				# if num_track == 0:
				ignorance_specific_info_dict[sig.lower()][num_track] = [article_node, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lcs, sorted_sentence_obo_info]
				ignorance_example_tracking[sig_index] += 1
				# print('found one!')
				# elif num_track > 0:
				# 	if ignorance_specific_info_dict[sig.lower()].get(num_track):
				# 		raise Exception('ERROR: Issue with ignorance specific tracking')
				# 	else:
				# 		pass
				# 	ignorance_specific_info_dict[sig.lower()][num_track] = [article_node, article_date, sentence_output_text, sorted_sentence_lc, sorted_sentence_obo_info]
				# 	ignorance_example_tracking[sig_index] += 1
				# 	print('found more!')
				# else:
				# 	pass
			else:
				pass

	return ignorance_specific_info_dict


def output_order_info(order_type, ignorance_sent_info_dict):
	#article_node, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info = ignorance_sent_info_dict[ig]

	if order_type.upper() == 'ARTICLE_DATE':
		article_date_list = [(i, info[1]) for i, info in ignorance_sent_info_dict.items()]
		##datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
		article_date_list.sort(key = lambda x : datetime.strptime(x[1], '%m/%Y'))
		# print(article_date_list)
		# if article_date_list:
			# print(type(article_date_list[0][1]))

			# raise Exception('hold')
		key_order = [a[0] for a in article_date_list]
		return key_order
	elif order_type.upper() == 'NUM_IGNORANCE_CUES':
		num_lc_list = [(i, info[5]) for i, info in ignorance_sent_info_dict.items()]
		num_lc_list.sort(key = lambda x : x[1], reverse=True)

		# print(num_lc_list[15])
		key_order = [n[0] for n in num_lc_list]
		return key_order
	else:
		print('invalid order type:', order_type)
		raise Exception('ERROR: Issue with the input order type not supported')



##output everything!
def output_sentence_info(output_path, obo_id, label, ignorance_sent_info_dict, not_ignorance_sent_info_dict, ignorance_category, order_type, order):

	##output files:
	no_ignorance_statements = False
	no_not_ignorance_statements = False

	##ignorance statements
	if ignorance_sent_info_dict:
		file_ext = ''
		if order_type:
			file_ext += '%s' %(order_type)
		else:
			pass

		if ignorance_category:
			obo_ignorance_output_file = open('%s%s_%s_%s_%s_%s.txt' % (output_path, label.replace(' ', '-'), obo_id, ignorance_category.upper(), 'statements', file_ext), 'w+')
		else:
			obo_ignorance_output_file = open('%s%s_%s_%s_%s.txt' % (output_path, label.replace(' ', '-').replace('/','-'), obo_id, 'ignorance_statements', file_ext), 'w+')

		obo_ignorance_output_file.write('%s\t%s (%s)\n\n' % ('OBO_ID (LABEL):', obo_id, label))

		if ignorance_category:
			obo_ignorance_output_file.write('%s\t%s\n\n' %('IGNORANCE CATEGORY:', ignorance_category))
		else:
			pass


		obo_ignorance_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % ('ARTICLE', 'ARTICLE DATE', 'SENTENCE NUM', 'SENTENCE', 'IGNORANCE CATEGORIES', 'NUM IGNORANCE CATEGORIES', 'OBO ID (LABEL)'))



		if order_type:
			for ig in order:
				article_node, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info = ignorance_sent_info_dict[ig]
				obo_ignorance_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
				article_node, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info))
		else:
			for ig in ignorance_sent_info_dict.keys():
				article_node, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info = ignorance_sent_info_dict[ig]
				obo_ignorance_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (article_node, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info))
	else:
		no_ignorance_statements = True




	##non-ignorance statements
	if not_ignorance_sent_info_dict:
		obo_no_ignorance_output_file = open('%s%s_%s_%s.txt' % (output_path, label.replace(' ', '-'), obo_id, 'not_ignorance_statements'),
											'w+')
		obo_no_ignorance_output_file.write('%s\t%s (%s)\n\n' % ('OBO_ID (LABEL):', obo_id, label))
		obo_no_ignorance_output_file.write(
			'%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % ('ARTICLE', 'ARTICLE DATE', 'SENTENCE NUM', 'SENTENCE', 'IGNORANCE CATEGORIES','NUM IGNORANCE CATEGORIES', 'OBO ID (LABEL)'))
		for nig in not_ignorance_sent_info_dict.keys():
			article_node, article_date, sent_num, sentence_output_text, na, na, sorted_sentence_obo_info = not_ignorance_sent_info_dict[nig]
			obo_no_ignorance_output_file.write(
				'%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (article_node, article_date, sent_num, sentence_output_text, na, na, sorted_sentence_obo_info))
	else:
		no_not_ignorance_statements = True


	return no_ignorance_statements, no_not_ignorance_statements


if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-ignorance_full_graph', type=str, help='the file path to the ignorance full graph that we want to explore as a .gpickle file')
	parser.add_argument('-pheknowlator_node_info', type=str, help='file path to the node information for pheknowlator')
	parser.add_argument('-output_path', type=str, help='the output file path for the resuults')
	parser.add_argument('--obo_concept_input_list', type=str, help='a list of obo_ids with Ontology_id dlimited by , with no spaces, default None', default=None)
	parser.add_argument('--obo_concept_input_file', type=str, help='the file path to a list of the obo ids one per line with a header', default=None)
	parser.add_argument('--string_obo_concept_input_list', type=str, help='a list of strings of concepts to include delimited with , no spaces, default None', default=None)
	parser.add_argument('--string_exact_match', type=str, help='true or false if you only want exact matches for string obo concept input list, default is True', default=True)
	parser.add_argument('--specific_ignorance_categories', type=str, help='a list of strings of ignorance categories to gather separately as a string, default is None', default=None)
	parser.add_argument('--output_order', type=str, help='the order to output ignorance statements in a list format given these options: ARTICLE_DATE (earliest to latest), NUM_IGNORANCE_CUES (the number of ignorance cues - max to min); the default is None', default=None)





	args = parser.parse_args()

	##read in gpickle ignorance graph file
	Full_Ignorance_Graph = read_in_pkl_graph(args.ignorance_full_graph)
	# print(Full_Ignorance_Graph[('17988','1')])
	# raise Exception('hold')

	##read in all phewknowlator node info
	OBO_to_node_info_dict = pheknowlator_node_info(args.pheknowlator_node_info) #OBO_to_node_info_dict[obo_id] = [entity_type, integer_id, entity_uri, label, description_definition, synonym]

	##check OBO_ids and get OBO_ids for strings.
	good_obo_id_list = set() #the final list of the good obo_ids we can work with - no duplicates
	bad_obo_id_list = set() #the lsit of bad obo ids - no duplicates
	if args.obo_concept_input_list:
		obo_concept_input_list = args.obo_concept_input_list.split(',')
		for obo_id in obo_concept_input_list:
			if OBO_to_node_info_dict.get(obo_id.replace(':', '_')):
				good_obo_id_list.add(obo_id.replace(':', '_'))
			else:
				bad_obo_id_list.add(obo_id.replace(':', '_'))
	else:
		pass

	##check that the OBO_ids are good from a file if its there
	if args.obo_concept_input_file:
		with open(args.obo_concept_input_file, 'r+') as obo_concept_input_file:
			next(obo_concept_input_file) #header
			for line in obo_concept_input_file:
				obo_id = line.strip('\n')
				if OBO_to_node_info_dict.get(obo_id.replace(':', '_')):
					good_obo_id_list.add(obo_id.replace(':', '_'))
				else:
					bad_obo_id_list.add(obo_id.replace(':', '_'))
	else:
		pass



	##gather all the obo_ids for the string list
	if args.string_obo_concept_input_list:
		string_obo_concept_input_list = args.string_obo_concept_input_list.split(',')
		obo_ids_from_string_list_exact_match, obo_ids_from_string_list_label, obo_ids_from_string_list_synonyms = find_obo_ids_from_string_concept_list(OBO_to_node_info_dict, string_obo_concept_input_list)

		print('FINISHED GATHERING OBO LIST FROM STRINGS: %s exact match, %s label match, %s synonym match' %(len(obo_ids_from_string_list_exact_match), len(obo_ids_from_string_list_label), len(obo_ids_from_string_list_synonyms)))

		if args.string_exact_match is True or args.string_exact_match.lower() == 'true':
			good_obo_id_list = good_obo_id_list.union(obo_ids_from_string_list_exact_match)
		elif args.string_exact_match and args.string_exact_match.lower() == 'false':
			good_obo_id_list = good_obo_id_list.union(obo_ids_from_string_list_exact_match)
			good_obo_id_list = good_obo_id_list.union(obo_ids_from_string_list_label)
			good_obo_id_list = good_obo_id_list.union(obo_ids_from_string_list_synonyms)
		else:
			good_obo_id_list = good_obo_id_list.union(obo_ids_from_string_list_exact_match)

	else:
		pass

	good_obo_id_list_dict = {} #obo_id to label
	for obo_id in good_obo_id_list:
		good_obo_id_list_dict[obo_id] = OBO_to_node_info_dict[obo_id][3]
	print('GOOD OBO_IDS list:', good_obo_id_list)
	print('GOOD OBO IDS DICT:', good_obo_id_list_dict)
	print(len(good_obo_id_list))
	print('BAD OBO IDS TO FIX OR CHANGE BECAUSE NOT IN OUR GRAPH:', bad_obo_id_list)


	##make sure we can continue! meaning we have good_obo_id_list and no bad_obo_id_list
	if bad_obo_id_list:
		print(bad_obo_id_list)
		raise Exception('ERROR: Need to update the obo list to make sure that we only have good OBOs')
	elif good_obo_id_list:
		print('PROGRESS: We are good to continue with these OBO concepts')
		print(good_obo_id_list)
	else:
		raise Exception('ERROR: Need to input either obo_ids for obo_concept_input_list or strings for string_obo_concept_input_list')

	raise Exception('hold')

	##gather all sentences with the obo_ids
	obo_id_ignorance_info = {} #obo_id to the ignorance and not ignorance info
	for i, obo_id in enumerate(good_obo_id_list):
		ignorance_sent_info_dict, not_ignorance_sent_info_dict, label = gather_all_sentences_with_obo_id(obo_id, OBO_to_node_info_dict, Full_Ignorance_Graph, args.output_path)
		obo_id_ignorance_info[obo_id] = [label, ignorance_sent_info_dict, not_ignorance_sent_info_dict]


	##by ignorance category also
	if args.specific_ignorance_categories:
		ignorance_category_list = [sic.lower() for sic in args.specific_ignorance_categories.split(',')]  ##lowercase right now
		ignorance_example_tracking = [0 for icl in ignorance_category_list]
		print(ignorance_category_list)

	else:
		pass

	##output the information
	if args.output_order:
		output_order_list = args.output_order.upper().split(',')
	else:
		output_order_list = []


	#output all data by obo_id
	empty_ignorance_obo_ids = []
	empty_not_ignorance_obo_ids = []

	for obo_id in obo_id_ignorance_info:
		label, ignorance_sent_info_dict, not_ignorance_sent_info_dict = obo_id_ignorance_info[obo_id]


		##output order matters
		output_order_info_dict = {}
		if 'ARTICLE_DATE' in output_order_list:
			article_date_order = output_order_info('ARTICLE_DATE', ignorance_sent_info_dict)
			output_order_info_dict['ARTICLE_DATE'] = article_date_order
		if 'NUM_IGNORANCE_CUES' in output_order_list:
			num_ignorance_cues_order = output_order_info('NUM_IGNORANCE_CUES', ignorance_sent_info_dict)
			output_order_info_dict['NUM_IGNORANCE_CUES'] = num_ignorance_cues_order

		print(obo_id, label)
		##no order
		no_ignorance_statements, no_not_ignorance_statements = output_sentence_info(args.output_path, obo_id, label, ignorance_sent_info_dict, not_ignorance_sent_info_dict, None, None, None)
		if no_ignorance_statements:
			empty_ignorance_obo_ids += [obo_id]
		else:
			pass

		if no_not_ignorance_statements:
			empty_not_ignorance_obo_ids += [obo_id]
		else:
			pass

		#order
		if args.output_order:
			for o in output_order_list:
				no_ignorance_statements, no_not_ignorance_statements = output_sentence_info(args.output_path, obo_id, label, ignorance_sent_info_dict, not_ignorance_sent_info_dict, None, o, output_order_info_dict[o])
		else:
			pass


		##by ignorance category
		if args.specific_ignorance_categories:
			ignorance_specific_info_dict = {}  ##ignorance category to the ignorance_sent_info_dict and not_ignorance_sent_info_dict
			for icl in ignorance_category_list:
				ignorance_specific_info_dict[icl] = {}

			ignorance_specific_info_dict = ignorance_category_find(ignorance_category_list, ignorance_example_tracking, ignorance_sent_info_dict, ignorance_specific_info_dict)
			# print(ignorance_specific_info_dict)

			##output by ignorance category
			for igc in ignorance_category_list:
				igc_specific_dict = ignorance_specific_info_dict[igc]
				if igc_specific_dict:
					no_ignorance_statements, no_not_ignorance_statements = output_sentence_info(args.output_path, obo_id, label, igc_specific_dict, None, igc, None, None)
					ignorance_output_order_info_dict = {}
					if 'ARTICLE_DATE' in output_order_list:
						ignorance_article_date_order = output_order_info('ARTICLE_DATE', igc_specific_dict)
						ignorance_output_order_info_dict['ARTICLE_DATE'] = ignorance_article_date_order
					if 'NUM_IGNORANCE_CUES' in output_order_list:
						ignorance_num_ignorance_cues_order = output_order_info('NUM_IGNORANCE_CUES', igc_specific_dict)
						ignorance_output_order_info_dict['NUM_IGNORANCE_CUES'] = ignorance_num_ignorance_cues_order

					if args.output_order:
						for o in output_order_list:
							no_ignorance_statements, no_not_ignorance_statements = output_sentence_info(args.output_path, obo_id, label, igc_specific_dict, None, igc, o, ignorance_output_order_info_dict[o])


				else:
					pass





	##output all the empty stuff
	with open('%s%s.txt' %(args.output_path, 'OBO_ids_no_ignorance_statements'), 'w+') as OBO_ids_no_ignorance_statements:
		OBO_ids_no_ignorance_statements.write('%s\n' %('OBO_ID'))
		for obo_id in empty_ignorance_obo_ids:
			OBO_ids_no_ignorance_statements.write('%s\n' %(obo_id))


	with open('%s%s.txt' %(args.output_path, 'OBO_ids_no_not_ignorance_statements'), 'w+') as OBO_ids_no_not_ignorance_statements:
		OBO_ids_no_not_ignorance_statements.write('%s\n' %('OBO_ID'))
		for obo_id in empty_not_ignorance_obo_ids:
			OBO_ids_no_not_ignorance_statements.write('%s\n' %(obo_id))


