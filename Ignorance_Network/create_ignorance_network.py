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



def read_pmcid_date_info(file_path, filename):
	article_info_dict = {} #pmcid -> [date, sentence count, word count]
	with open('%s%s' %(file_path, filename), 'r') as pmcid_info_file:
		next(pmcid_info_file)
		for line in pmcid_info_file:
			pmcid, date = line.strip('\n').split('\t')
			article_info_dict[pmcid] = [date, None, None]

	return article_info_dict

def read_pmcid_count_summary_stats_info(article_info_dict, file_path):
	##article_info_dict = {} #pmcid -> [date, sentence count, word count]

	with open(file_path, 'r') as article_count_summary_stats_file:
		# Headers: ARTICLE	TOTAL_SENTENCE_COUNT	TOTAL_WORD_COUNT
		next(article_count_summary_stats_file)
		for line in article_count_summary_stats_file:
			[a, total_sentence_count, total_word_count] = line.strip('\n').split('\t')
			# print(a, type(a))
			a = a.split('.nxml')[0]
			if article_info_dict.get(a):
				## change these to integers for issues down the line
				article_info_dict[a][1] = int(total_sentence_count)
				article_info_dict[a][2] = int(total_word_count)
			else:
				print('article', a)
				raise Exception('ERROR: Issue we have stats on the pmcid but not the date?!')




	return article_info_dict



def read_in_pkl_file(file_path):

	with open(file_path, 'rb') as pf:
		data_dict = pickle.load(pf)
		return data_dict



def add_ignorance_taxonomy_to_graph(graph, ontology_of_ignorance_file_path, current_ignorance_types, broad_categories_dict, old_ignorance_types_dict, ignorance_taxonomy_attributes, broad_ignorance_taxonomy_attributes, taxonomy_lexical_cue_attributes):
	##return graph

	##ADD IGNORANCE TYPES: node and edge to one large node - ignorance_taxonomy_attributes = ['NODE_TYPE']

	for bc in broad_categories_dict:
		# print(bc)
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
			if it.upper() in broad_categories_dict.keys():
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






def add_ignorance_article_info_to_graph(graph, article_info_dicts_list, article, article_info_dict, all_lcs_dict, current_ignorance_types, broad_categories, old_ignorance_types_dict, article_attributes, sentence_attributes, annotated_lexical_cues_attributes):

	#return the new updated graph each time adding in the new node and edges

	[concept_mention_info_dict, subject_scope_info_dict, subject_scope_to_concept_mention_info_dict] = article_info_dicts_list

	##ADD ARTICLE NODE: article_attributes = ['NODE_TYPE', 'ARTICLE_DATE', 'TOTAL_SENTENCE_COUNT', 'TOTAL_WORD_COUNT', 'IGNORANCE_SENTENCE_COUNT']
	graph.add_node(article, NODE_TYPE='ARTICLE', ARTICLE_DATE=article_info_dict[article][0], TOTAL_SENTENCE_COUNT=article_info_dict[article][1], TOTAL_WORD_COUNT=article_info_dict[article][2], IGNORANCE_SENTENCE_COUNT=len(subject_scope_to_concept_mention_info_dict.keys()))

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
			new_sentence_id = 'S%s-%s' %(sentence_id.split('_')[-1], article)
			sentence_start_list, sentence_end_list, sentence_text, sentence_id_1, annotation_type_lower, sentence_num = subject_scope_info_dict[sentence_id]
			# print(sentence_start_list, sentence_end_list, sentence_text, sentence_id, annotation_type_lower, sentence_num)

			if not annotation_type_lower or annotation_type_lower.lower() == 'subject_scope':
				##none means that it is not a statement of ignorance
				pass
			else:
				raise Exception('ERROR: Issue with sentence annotation type')

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
			# if 'risk' in mention_text.lower():
			# 	print(mention_start_list, mention_end_list, mention_text, annotated_lexical_cue,
			# 		  mention_ignorance_category, mention_sentence_id)
				# raise Exception('hold')
			# print(mention_start_list, mention_end_list, mention_text, annotated_lexical_cue, mention_ignorance_category, mention_sentence_id)
			# print('current mention id', mention_id)
			if mention_text.startswith('...'):
				print(mention_start_list, mention_end_list, mention_text, annotated_lexical_cue,
					  mention_ignorance_category, mention_sentence_id)
				raise Exception('ERROR: mention text startswith ...')
			if mention_text.endswith('...'):
				print(mention_start_list, mention_end_list, mention_text, annotated_lexical_cue,
					  mention_ignorance_category, mention_sentence_id)
				raise Exception('ERROR: mention text endswith ...')

			new_mention_id = 'LC%s-%s' %(mention_id.split('_')[-1], article)

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

			#TODO!!!!
			#add edges based on annotated lexical cue:
			#1. annotated lexical cue is an ignorance category
			if annotated_lexical_cue.upper() in current_ignorance_types:
				#new cue not in ignorance taxonomy - add to ignorance taxonomy also as a NEW_CUE as the ANNOTATION_TEXT
				if annotated_lexical_cue.lower() == mention_ignorance_category.lower():
					new_cue = mention_text.replace(' ... ', '...').replace(' ', '_').lower()
					# if 'risk' in new_cue:
					# 	print(new_cue, mention_text)
					# 	print(mention_start_list, mention_end_list, mention_text, annotated_lexical_cue,
					# 		  mention_ignorance_category, mention_sentence_id)

					if new_cue.startswith('...'):
						raise Exception('ERROR: mention text startswith ...')
					if new_cue.endswith('...'):
						raise Exception('ERROR: mention text endswith ...')
					graph.add_node(new_cue, NODE_TYPE='TAXONOMY_LEXICAL_CUE', ANNOTATION_TEXT='NEW_CUE')
					graph.add_edge(new_cue, mention_ignorance_category.upper())
					graph.add_edge(new_mention_id, new_cue)

				#cue exists but we take a different one - exception case - so we map to both the lexical cue and ignorance category
				else:
					#map to lexical cue and different ignorance category so it's counted in both - adding 2 edges - annotated_lexical_cue is the canonical ignorance category and mention_ignorance_category is the correct one!
					# print('got here')
					# print(mention_id)
					# print(concept_mention_info_dict[mention_id])
					graph.add_edge(new_mention_id, mention_text.replace(' ... ', '...').replace(' ', '_').lower()) #the canonical lexical cue (lowercase)!
					# print('mention_ignorance_category')
					if mention_ignorance_category.upper() in current_ignorance_types:
						graph.add_edge(new_mention_id, mention_ignorance_category.upper())
					else:
						raise Exception('ERROR: Issue with missing ignorance category in annotations!')
					# print(graph.nodes[mention_text.replace(' ... ', '...').replace(' ', '_').lower()])
					# print(graph.nodes[new_mention_id])
					# raise Exception('hold')

			##broad category issue with the name sbeing there also - added future_work node for taxonomy lexical cues
			elif annotated_lexical_cue.upper() in broad_categories:
				##FUTURE_OPPORTUNITIES NODE!
				# print(graph.nodes['future_work'])
				graph.add_edge(new_mention_id, mention_ignorance_category.upper())
				# raise Exception('hold')

			##2. annotated lexical cue is good with canonical ignorance category! - adding 1 edge
			else:
				graph.add_edge(new_mention_id, annotated_lexical_cue)


			##check to make sure we have attributes in each node - at least node_type
			if len(graph.nodes[new_mention_id]) == 0:
				print('finished with nodes', new_mention_id, graph.nodes[new_mention_id])
				for a in annotated_lexical_cues_attributes:
					print(a, graph.nodes[new_mention_id][a])

				raise Exception('ERROR: issue with adding attributes to the node - annotated lexical cue')
			else:
				pass


			# try:
			# 	print(graph.nodes['future_opportunities'])
			# 	print(article, sentence_id, mention_id)
			# 	print(concept_mention_info_dict[mention_id])
			# 	raise Exception('hold')
			# except KeyError:
			# 	pass


		# if mention_id == 'PMC3427250.nxml.gz-21':
			#     print(article)
			#     print(mention_text)
			#     raise Exception('hold')


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


def full_OBO_prediction_info(OBO_original_file_path, obo_ontologies, ):

	obo_prediction_info_dict = {} #dict from obo_id to obo

	for obo in obo_ontologies:
		with open('%s%s/%s/%s_%s.txt' %(OBO_original_file_path, obo, 'full_files', obo, 'combo_tgt_concept_ids'), 'r+') as obo_file, open('%s%s/%s/%s_%s.txt' %(OBO_original_file_path, obo, 'full_files', obo, 'combo_tgt_concept_ids_val'), 'r+') as obo_file_val:
			for line in obo_file:
				obo_id = line.strip('\n')
				if obo_prediction_info_dict.get(obo_id):
					if obo_prediction_info_dict[obo_id] == obo:
						pass
					else:
						print(obo_id)
						print(obo)
						print(obo_prediction_info_dict[obo_id])
						raise Exception('ERROR: Issue with duplicate obo id in different obos')
				else:
					obo_prediction_info_dict[obo_id] = obo


			for line in obo_file_val:
				obo_id = line.strip('\n')
				if obo_prediction_info_dict.get(obo_id):
					if obo_prediction_info_dict[obo_id] == obo:
						pass
					else:
						print(obo_id)
						print(obo)
						print(obo_prediction_info_dict[obo_id])
						raise Exception('ERROR: Issue with duplicate obo id in different obos')
				else:
					obo_prediction_info_dict[obo_id] = obo

	return obo_prediction_info_dict


def add_OBO_article_info_to_graph(graph, article, article_info_dicts_list, obo_ontologies, obo_attributes, OBO_to_node_info_dict, obo_prediction_info_dict, obo_predict_issues, obo_non_existent_issues, obo_total_mapped, obo_total_not_mapped):
	##GOAL: add edges between sentences with OBOs to the OBO in PheKnowlator
	# print(article_info_dicts_list)
	[concept_mention_info_dict, subject_scope_info_dict, subject_scope_to_concept_mention_info_dict] = article_info_dicts_list

	for sentence_id, concept_mention_list in subject_scope_to_concept_mention_info_dict.items():
		if article in sentence_id:
			node_sentence_id = 'S%s-%s' %(sentence_id.split('_')[-1], article)
			if Full_Ignorance_Graph.has_node(node_sentence_id):
				pass
			else:
				raise Exception('ERROR: Issue with sentence node not existing in full ignorance graph for phenowlator')
		else:
			raise Exception('ERROR: Issue with sentence id mixup for OBOs stuff')
		##OBO concept mention INFORMATION FOR EACH SENTENCE: obo_edge_attributes = ['OBO_SPANNED_TEXT']
		for obo_mention_id in concept_mention_list:
			#PMC6056931_T331 -> [[41259], [41262], 'eat', 'GO:0016265', 'GO_BP', 'PMC6056931_262']
			mention_start_list, mention_end_list, obo_mention_text, obo_id, obo, mention_sentence_id = concept_mention_info_dict[obo_mention_id]
			# print(mention_id)
			# print(concept_mention_info_dict[mention_id])
			# obo_edge_attributes = [''OBO_MENTION_ID'', 'OBO_MENTION_TEXT', 'OBO_MENTION_SPAN'] #tuples of a span list

			##OBO_MENTION_SPAN
			if len(mention_start_list) != len(mention_end_list):
				raise Exception('ERROR: Issue with mention start and end list lengths not matching - issue with OBO information!')
			else:
				obo_mention_span_list = [] #tuples of starts and ends
				for i, s in enumerate(mention_start_list):
					obo_mention_span_list += [(s, mention_end_list[i])]

			if sentence_id == mention_sentence_id:
				pass
			else:
				raise Exception('ERROR: Issue with sentence id information for OBOs')

			##see if we can find the node in pheknowlator
			##if we find the node add it to the graph: node_sentence_id -> obo_integer_id in pheknowlator
			if OBO_to_node_info_dict.get(obo_id.replace(':', '_')):
				print('found OBO!', obo_id)
				#entity_type, integer_id, entity_uri, label, description_definition, synonym
				#obo_node_id = OBO_to_node_info_dict[obo_id.replace(':', '_')][1] #integer_id
				obo_node_id = URIRef(OBO_to_node_info_dict[obo_id.replace(':', '_')][2].replace('<', '').replace('>',''))
				graph.add_edge(node_sentence_id, obo_node_id, OBO_MENTION_ID=obo_mention_id, OBO_MENTION_TEXT=obo_mention_text, OBO_MENTION_SPAN=obo_mention_span_list)
				obo_total_mapped += 1

			##node not found in pheknowlator
			else:
				obo_total_not_mapped += 1
				##the obo id can be in out predictions information
				if obo_prediction_info_dict.get(obo_id):
					print('OBO_ID in information prediction but not Pheknowlator:', obo_id, obo_mention_text, obo_mention_id)
					obo_predict_issues.add(obo_id)
				else:
					print('OBO_ID non-existent!', obo_id)
					print(obo_mention_id, concept_mention_info_dict[obo_mention_id])
					obo_non_existent_issues.add(obo_id)
					# raise Exception('ERROR: Issue with missing obo node in pheknowlator')



	return graph, obo_predict_issues, obo_non_existent_issues, obo_total_mapped, obo_total_not_mapped




def remove_specific_nodes_by_degree(graph, node_type, degree_criteria_list):
	#delete if in degree_criteria_list
	for n in list(graph.nodes):
		# print(n)
		# print(graph.nodes[n])
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
	# gold_standard_annotation_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Annotations/'

	# current_ignorance_types = ['ALTERNATIVE_OPTIONS_CONTROVERSY', 'ANOMALY_CURIOUS_FINDING', 'DIFFICULT_TASK',
	# 						   'EXPLICIT_QUESTION', 'FULL_UNKNOWN', 'FUTURE_PREDICTION', 'FUTURE_WORK',
	# 						   'IMPORTANT_CONSIDERATION', 'INCOMPLETE_EVIDENCE', 'PROBABLE_UNDERSTANDING',
	# 						   'PROBLEM_COMPLICATION', 'QUESTION_ANSWERED_BY_THIS_WORK', 'SUPERFICIAL_RELATIONSHIP']

	# old_ignorance_types_dict = {'ALTERNATIVE_OPTIONS':'ALTERNATIVE_OPTIONS_CONTROVERSY', 'FUTURE_OPPORTUNITIES': 'FUTURE_WORK'}
	#
	# broad_categories = ['LEVELS_OF_EVIDENCE', 'BARRIERS', 'FUTURE_OPPORTUNITIES']
	# broad_categories_dict = {'LEVELS_OF_EVIDENCE' : ['FULL_UNKNOWN', 'EXPLICIT_QUESTION', 'INCOMPLETE_EVIDENCE', 'PROBABLE_UNDERSTANDING', 'SUPERFICIAL_RELATIONSHIP'], 'BARRIERS': ['ALTERNATIVE_OPTIONS_CONTROVERSY', 'DIFFICULT_TASK', 'PROBLEM_COMPLICATION'], 'FUTURE_OPPORTUNITIES': ['FUTURE_PREDICTION', 'FUTURE_WORK', 'IMPORTANT_CONSIDERATION']}

	##gold standard v1 with training updated
	# articles = ['PMC1247630', 'PMC1474522', 'PMC1533075', 'PMC1626394', 'PMC2009866', 'PMC2265032', 'PMC2396486',
	# 			'PMC2516588', 'PMC2672462', 'PMC2874300', 'PMC2885310', 'PMC2889879', 'PMC2898025', 'PMC2999828',
	# 			'PMC3205727', 'PMC3272870', 'PMC3279448', 'PMC3313761', 'PMC3342123', 'PMC3348565', 'PMC3373750',
	# 			'PMC3400371', 'PMC3427250', 'PMC3513049', 'PMC3679768', 'PMC3800883', 'PMC3914197', 'PMC3915248',
	# 			'PMC3933411', 'PMC4122855', 'PMC4304064', 'PMC4311629', 'PMC4352710', 'PMC4377896', 'PMC4428817',
	# 			'PMC4500436', 'PMC4564405', 'PMC4653409', 'PMC4653418', 'PMC4683322', 'PMC4859539', 'PMC4897523',
	# 			'PMC4954778', 'PMC4992225', 'PMC5030620', 'PMC5143410', 'PMC5187359', 'PMC5273824', 'PMC5501061',
	# 			'PMC5540678', 'PMC5685050', 'PMC5812027', 'PMC6000839', 'PMC6011374', 'PMC6022422', 'PMC6029118',
	# 			'PMC6033232', 'PMC6039335', 'PMC6054603', 'PMC6056931']

	# articles = ['PMC3427250']

	# print('NUM ARTICLES:', len(articles))

	# all_lcs_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Ontologies/Ontology_Of_Ignorance_all_cues_2020-08-25.txt'

	# output_folder = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/3_Ignorance_Base/Ignorance-Base/Output_Folders/'
	# sentence_folder = 'PMCID_Sentence_Files/'
	#
	# sentence_output_folder = output_folder + sentence_folder
	#
	# all_combined_data = '0_all_combined'
	#
	# dictionary_folder = 'dictionary_files/'
	#
	# visualizations_folder ='Visualizations/Ignorance_Network_Vis/'
	#
	# dictionary_output_folder = output_folder + dictionary_folder
	#
	# # pmcid_date_info = 'PMCID_date_info.txt'
	#
	# article_count_summary_stats_file_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Concept-Recognition-as-Translation-master/Output_Folders/eval_preprocess_article_summary.txt'



	parser = argparse.ArgumentParser()
	parser.add_argument('-ignorance_ontologies', type=str, help='a list of the ignorance ontologies delimited with , no spaces')
	parser.add_argument('-ignorance_broad_categories', type=str, help='a list of the broad categories as a string to be converted to a list, no spaces please')
	parser.add_argument('-ignorance_broad_categories_dict', type=str, help='a dictionary of the broad categories to the narrow ones as a string to be converted to a dictionary, no spaces please')
	parser.add_argument('-old_ignorance_types_dict', type=str, help='a dictionary of the old ignorance types to the new ones as a string to be converted to a dictionary, no spaces please')
	parser.add_argument('-included_articles', type=str, help='a list of the articles delimited with , no spaces', default='all')
	parser.add_argument('-article_path', type=str, help='the file path to all the articles')
	parser.add_argument('-all_lcs_path', type=str, help='the file path to the current lexical cue list')
	parser.add_argument('-working_directory', type=str, help='the file path to the current working directory')
	parser.add_argument('-pmcid_date_info_path', type=str, help='the file path to the pmcid date info starting from the working directory')
	parser.add_argument('-corpus_path', type=str, help='the file path to the corpus we are using')
	parser.add_argument('-all_article_summary_path', type=str, help='the file path to the article summary stats starting from the corpus path')
	parser.add_argument('-ignorance_dictionary_folder', type=str, help='path to dictionary  output folder')
	parser.add_argument('-pheknowlator_graph_path', type=str, help='file path to the phewknowlator gpickle file as a string')
	parser.add_argument('-pheknowlator_node_info', type=str, help='file path to the node information for pheknowlator')
	parser.add_argument('-OBO_ontologies', type=str, help='a list of the OBO ontologies as a string delimited with a , with no spaces')
	parser.add_argument('-OBO_EXT_ontologies', type=str, help='a list of the OBO_EXT ontologies as a string delimited with a , with no spaces')
	parser.add_argument('-OBO_dictionary_folder', type=str, help='path to dictionary output folder')
	parser.add_argument('-OBO_EXT_dictionary_folder', type=str, help='path to dictionary output folder')
	parser.add_argument('-OBO_original_file_path', type=str, help='the file path to the original list of OBO/OBO_EXT concepts')
	parser.add_argument('-visualization_output_path', type=str, help='the file path to for the output visualizations folder')
	parser.add_argument('-graph_output_path', type=str, help='the file path to for the output graph folder')
	parser.add_argument('--saved_ignorance_graph', type=str, help='optional: the file path to the gpickle ignorance graph it exists, default is None', default=None)
	args = parser.parse_args()


	if args.included_articles.lower() == 'all':
		included_articles = []
		for root, directories, filenames in os.walk(args.article_path):
			for filename in sorted(filenames):
				if filename.endswith('.nxml.gz.txt'):
					included_articles += [filename.split('.nxml.gz.txt')[0]]
	else:
		included_articles = args.included_articles.split(',')

	print('NUM ARTICLES:', len(included_articles))

	ignorance_ontologies = [i.upper() for i in args.ignorance_ontologies.split(',')]
	ignorance_broad_categories = ast.literal_eval(args.ignorance_broad_categories)
	ignorance_broad_categories_dict = ast.literal_eval(args.ignorance_broad_categories_dict)
	old_ignorance_types_dict = ast.literal_eval(args.old_ignorance_types_dict)

	OBO_ontologies = args.OBO_ontologies.split(',')
	OBO_EXT_ontologies = args.OBO_EXT_ontologies.split(',')

	##GET THE ARTICLE DATE INFO AS METADATA - TODO: ADD MORE LATER
	article_info_dict = read_pmcid_date_info(args.working_directory, args.pmcid_date_info_path)
	##get article sentence count data
	article_info_dict = read_pmcid_count_summary_stats_info(article_info_dict, args.corpus_path + args.all_article_summary_path )

	print(len(article_info_dict))
	# raise Exception('hold')



	##GET ALL THE DICTIONARIES FOR EACH ARTICLE
	article_dictionary_files_dict = {} #dict: article -> [list of dictionary file names] -> [[],[],[]]
	article_to_all_dicts = {}  # article -> [list of dictionaries]
	for i, dict_path in enumerate([args.ignorance_dictionary_folder, args.OBO_dictionary_folder, args.OBO_EXT_dictionary_folder]):
		print(dict_path)
		for root, directories, filenames in os.walk(dict_path):
			for filename in sorted(filenames):
				#order because of sort: concept, subject_scope, subject_scope_to_concept_mention

				if filename.split('_concept')[0] in included_articles:
					article = filename.split('_concept')[0]

				elif filename.split('_subject')[0] in included_articles:
					article = filename.split('_subject')[0]
				else:
					continue

				##get the dictionary
				data_dict = read_in_pkl_file(root + filename)

				##save all the relevant stuff per article in order: ignorance, OBO, OBO_EXT and concept, subject_scope, subject_scope_to_concept_mention within all of them
				##ignorance dicts, OBO dicts, OBO_EXT dicts
				if article_dictionary_files_dict.get(article):
					# if 'subject_scope' in filename and 'OBOs_dictionary' in root:
					# 	print(filename)
					# 	print(data_dict)
					# 	raise Exception('hold')
					article_dictionary_files_dict[article][i] += [filename]
					article_to_all_dicts[article][i] += [data_dict]
					# print('and here!')
					# print(len(data_dict))
					# print('got here', article)
					# print(article_to_all_dicts[article])
				#initialize it for the first one and that's it
				else:
					article_dictionary_files_dict[article] = [[filename], [], []]
					article_to_all_dicts[article] = [[data_dict], [], []]



	##check that all the data is there
	if len(article_dictionary_files_dict.keys()) != len(article_to_all_dicts.keys()):
		raise Exception('ERROR: Issue with gathering all dictionaries and keeping records of files')
	else:
		print('finished all dictionary gathering!', len(article_to_all_dicts))

	# for key in article_to_all_dicts.keys():


	# raise Exception('hold!')


	##Ignorance graph information!
	large_nodes = ['ALL_ARTICLES', 'IGNORANCE_TAXONOMY']

	all_articles_attributes = ['NODE_TYPE']
	ignorance_taxonomy_attributes = ['NODE_TYPE']
	broad_ignorance_taxonomy_attributes = ['NODE_TYPE']
	narrow_ignorance_taxonomy_attributes = ['NODE_TYPE']
	taxonomy_lexical_cue_attributes = ['NODE_TYPE', 'ANNOTATION_TEXT']
	article_attributes = ['NODE_TYPE', 'ARTICLE_DATE', 'TOTAL_SENTENCE_COUNT', 'TOTAL_WORD_COUNT',
						  'IGNORANCE_SENTENCE_COUNT']
	sentence_attributes = ['NODE_TYPE', 'SENTENCE_SPAN', 'SENTENCE_TEXT', 'SENTENCE_ANNOTATION_ID']
	annotated_lexical_cues_attributes = ['NODE_TYPE', 'MENTION_ANNOTATION_ID', 'MENTION_SPAN', 'MENTION_TEXT']
	obo_edge_attributes = ['OBO_MENTION_ID', 'OBO_MENTION_TEXT', 'OBO_MENTION_SPAN']

	##save graph by date so we know when it is from
	today = datetime.datetime.now()
	d = today.strftime('%x').replace('/', '_')

	attribute_dict = {'ALL_ARTICLES': all_articles_attributes, 'IGNORANCE_TAXONOMY': ignorance_taxonomy_attributes,
					  'ARTICLE': article_attributes, 'SENTENCE': sentence_attributes,
					  'BROAD_IGNORANCE_TAXONOMY_CATEGORY': broad_ignorance_taxonomy_attributes,
					  'IGNORANCE_TAXONOMY_CATEGORY': narrow_ignorance_taxonomy_attributes,
					  'TAXONOMY_LEXICAL_CUE': taxonomy_lexical_cue_attributes,
					  'ANNOTATED_LEXICAL_CUE': annotated_lexical_cues_attributes}  # , 'OBO_SPANNED_TEXT':obo_edge_attributes}

	if args.saved_ignorance_graph:
		Ignorance_Graph = nx.read_gpickle(args.saved_ignorance_graph)
	else:
		###IGNORANCE GRAPH INITIALIZATION AND INFORMATION NEEDED FOR GRAPH
		Ignorance_Graph = nx.MultiGraph()
		Ignorance_Graph.add_node('ALL_ARTICLES', NODE_TYPE='ALL_ARTICLES') #ONE LARGE NODE
		Ignorance_Graph.add_node('IGNORANCE_TAXONOMY', NODE_TYPE='IGNORANCE_TAXONOMY') #ONE LARGE NODE
		# print(Ignorance_Graph.nodes.data())
		# raise Exception('hold')


		##ADD IGNORANCE TAXONOMY TO THE GRAPH in general (lexical cues and ignorance categories)
		Ignorance_Graph, all_lcs_dict, all_ignorance_types = add_ignorance_taxonomy_to_graph(Ignorance_Graph, args.all_lcs_path, ignorance_ontologies , ignorance_broad_categories_dict, old_ignorance_types_dict, narrow_ignorance_taxonomy_attributes, broad_ignorance_taxonomy_attributes, taxonomy_lexical_cue_attributes)
		##check that the ignorance graph has no empty nodes:
		for n in list(Ignorance_Graph.nodes):
			if len(Ignorance_Graph.nodes[n]):
				pass
			else:
				print(n, Ignorance_Graph.nodes[n])
				raise Exception('ERROR: Issue that there is a node with no attributes after adding taxonomy!')

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
		for i, article in enumerate(included_articles):


			# if i == 0:
			##ignorance dictionary add first per article - article_to_all_dicts[article][0]
			Ignorance_Graph = add_ignorance_article_info_to_graph(Ignorance_Graph, article_to_all_dicts[article][0], article, article_info_dict, all_lcs_dict, ignorance_ontologies, ignorance_broad_categories, old_ignorance_types_dict, article_attributes, sentence_attributes, annotated_lexical_cues_attributes)

			##check that the ignorance graph has no empty nodes:
			for n in list(Ignorance_Graph.nodes):
				if len(Ignorance_Graph.nodes[n]):
					# pass
					if Ignorance_Graph.nodes[n]['NODE_TYPE'] == 'TAXONOMY_LEXICAL_CUE':
						if n.startswith('...'):
							print(n)
							print(Ignorance_Graph.nodes[n])
							raise Exception('ERROR: Issue with ... starting taxonomy lexical cue')
						elif n.endswith('...'):
							print(n)
							print(Ignorance_Graph.nodes[n])
							raise Exception('ERROR: Issue with ... ending taxonomy lexical cue')
						else:
							pass
					else:
						pass
				else:
					print(article)
					print(n,Ignorance_Graph.nodes[n])
					raise Exception('ERROR: Issue that there is a node with no attributes for ignorance graph after adding articles!')
			# print('before each article')




			##initialize graph for each article: need to make sure it is one article at a time: initial_article_graph is not getting updated!
			initial_article_graph = copy.deepcopy(Ignorance_Graph_copy)
			# print(len(list(initial_article_graph.nodes)), len(list(initial_article_graph.edges)))
			if len(list(Ignorance_Graph_copy.nodes)) != len(list(initial_article_graph.nodes)) or len(list(Ignorance_Graph_copy.edges)) != len(list(initial_article_graph.edges)):
				raise Exception('ERROR : Issue with initializing each articles graph!')


			else:
				# specific_article_graph.clear()
				specific_article_graph = add_ignorance_article_info_to_graph(initial_article_graph, article_to_all_dicts[article][0], article, article_info_dict, all_lcs_dict, ignorance_ontologies, ignorance_broad_categories, old_ignorance_types_dict, article_attributes, sentence_attributes, annotated_lexical_cues_attributes)
				# print('after each article')
				# print(len(list(initial_article_graph.nodes)), len(list(initial_article_graph.edges)))
				# print(len(list(specific_article_graph.nodes)), len(list(specific_article_graph.edges)))
				##check that the ignorance graph has no empty nodes:
				for n in list(specific_article_graph.nodes):
					if len(specific_article_graph.nodes[n]):
						pass
					else:
						print(n, specific_article_graph.nodes[n])
						raise Exception('ERROR: Issue that there is a node with no attributes for specific article graph!')

				article_graph_dict[article] = specific_article_graph

				##small article graph without any extra lexical cues
				small_initial_article_graph = copy.deepcopy(specific_article_graph)
				#remove all TAXONOMY_LEXICAL_CUE nodes with degree 1 (meaning that they are only attached to the ignorance taxonomy and not the ANNOTATED_LEXICAL CUES (which would have degrees of 2)
				degree_criteria_list = [1]
				small_article_graph = remove_specific_nodes_by_degree(small_initial_article_graph, 'TAXONOMY_LEXICAL_CUE', degree_criteria_list)

				##check that the ignorance graph has no empty nodes:
				for n in list(small_article_graph.nodes):
					if len(small_article_graph.nodes[n]):
						pass
					else:
						print(n, small_article_graph.nodes[n])
						raise Exception('ERROR: Issue that there is a node with no attributes for small article graph!')
				small_article_graph_dict[article] = small_article_graph

				# print('small article graph')
				# print(len(list(small_article_graph.nodes)), len(list(small_article_graph.edges)))


		# raise Exception('hold')

		###EXPLORE/VISUALIZE GRAPH - OUTPUT THE GRAPH!
		##Nodes
		# raise Exception('hold')
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
			elif n[1]['NODE_TYPE'] == 'TAXONOMY_LEXICAL_CUE':
				if n[0].startswith('...'):
					print(n)
					print(Ignorance_Graph.nodes[n])
					raise Exception('ERROR: Issue with ... starting taxonomy lexical cue')
				elif n[0].endswith('...'):
					print(n)
					print(Ignorance_Graph.nodes[n])
					raise Exception('ERROR: Issue with ... ending taxonomy lexical cue')
				else:
					pass

			else:
				specific_attribute_dict = attribute_dict[n[1]['NODE_TYPE']]
				for attribute in specific_attribute_dict[1:]:  # SKIP NODE_TYPE
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

		##SAVE THE IGNORANCE BASE
		print('SAVING IGNORANCE GRAPH WITH %s nodes and %s edges' % (
		len(list(Ignorance_Graph.nodes)), len(list(Ignorance_Graph.edges))))
		save_networkx_graph(Ignorance_Graph, "%s%s_%s.gpickle" % (args.graph_output_path, '0_IGNORANCE_MULTIGRAPH', d))
		# nx.write_gpickle(Ignorance_Graph, "%s%s%s_%s.gpickle" %(output_folder, visualizations_folder, 'IGNORANCE_GRAPH_60_ARTICLES', d))

		##SAVE THE IGNORANCE TAXONOMY SEPRATELY
		print('SAVING IGNORANCE TAXONOMY GRAPH WITH %s nodes and %s edges' % (
		len(list(Ignorance_Taxonomy_Graph.nodes)), len(list(Ignorance_Taxonomy_Graph.edges))))
		save_networkx_graph(Ignorance_Taxonomy_Graph,
							"%s%s_%s.gpickle" % (args.graph_output_path, '0_IGNORANCE_TAXONOMY_MULTIGRAPH', d))
		# nx.write_gpickle(Ignorance_Taxonomy_Graph,"%s%s%s_%s.gpickle" % (output_folder, visualizations_folder, 'IGNORANCE_TAXONO_GRAPH', d))

		##save each article graph
		for article in article_graph_dict:
			print('SAVING ARTICLE GRAPH FOR %s WITH %s nodes and %s edges' % (
			article, len(list(article_graph_dict[article].nodes)), len(list(article_graph_dict[article].edges))))
			save_networkx_graph(article_graph_dict[article],
								"%s%s_%s_%s.gpickle" % (args.graph_output_path, article, 'IGNORANCE_MULTIGRAPH', d))

			print('SAVING SMALL ARTICLE GRAPH FOR %s WITH %s nodes and %s edges' % (
			article, len(list(small_article_graph_dict[article].nodes)),
			len(list(small_article_graph_dict[article].edges))))
			save_networkx_graph(small_article_graph_dict[article], "%s%s_%s_%s.gpickle" % (
			args.graph_output_path, article, 'SMALL_IGNORANCE_MULTIGRAPH', d))



	###TODO:ADD OBO INFORMATION per article
	print('PROGRESS: Adding Pheknowlator for OBOs')
	PheKnowlator_Graph = nx.read_gpickle(args.pheknowlator_graph_path) #connect pheknowlator to ignorance graph
	##add node dictionary to help us find nodes in pheknowlator
	OBO_to_node_info_dict = pheknowlator_node_info(args.pheknowlator_node_info)

	##get all OBO information for where the OBOs came from so we know what is correct or incorrect based on OBO predictions
	obo_prediction_info_dict = full_OBO_prediction_info(args.OBO_original_file_path, OBO_ontologies)

	Full_Ignorance_Graph = nx.compose(Ignorance_Graph, PheKnowlator_Graph)
	print('PROGRESS: Combined ignorance graph with Pheknowlator')

	obo_total_mapped = 0
	obo_total_not_mapped = 0
	obo_predict_issues = set()
	obo_non_existent_issues = set()
	for i, article in enumerate(included_articles):
		print(article)
		Full_Ignorance_Graph, obo_predict_issues, obo_non_existent_issues, obo_total_mapped, obo_total_not_mapped = add_OBO_article_info_to_graph(Full_Ignorance_Graph, article, article_to_all_dicts[article][1], OBO_ontologies, obo_edge_attributes, OBO_to_node_info_dict, obo_prediction_info_dict, obo_predict_issues, obo_non_existent_issues, obo_total_mapped, obo_total_not_mapped)

	# print(obo_non_existent_issues)
	# print(obo_predict_issues)
	# print(len(obo_non_existent_issues))
	# print(len(obo_predict_issues))


	##output all
	print('SUCCESSFULLY CONNECTED %s TO PHEKNOWLATOR WITH %s NOT MAPPED!' %(obo_total_mapped, obo_total_not_mapped))
	print('PHEKNOWLATOR INFORMATION:', len(list(PheKnowlator_Graph.nodes)), len(list(PheKnowlator_Graph.edges)))

	##save full ignorance graph
	print('SAVING FULL IGNORANCE GRAPH WITH %s nodes and %s edges' % (len(list(Full_Ignorance_Graph.nodes)), len(list(Full_Ignorance_Graph.edges))))
	save_networkx_graph(Full_Ignorance_Graph, "%s%s_%s.gpickle" % (args.graph_output_path, '0_FULL_IGNORANCE_MULTIGRAPH', d))

	##save prediction issue obos
	print('SAVING UNIQUE OBO_IDS PREDICTION ISSUES:', len(obo_predict_issues))
	with open('%s%s.txt' %(args.working_directory, 'OBOs_unique_prediction_issues'), 'w+') as predict_issues_file:
		for obo_issue in obo_predict_issues:
			predict_issues_file.write('%s\n' %(obo_issue))

	##save non-existent obos issues
	print('SAVING UNIQUE OBO_IDS NON-EXISTENT ISSUES:', len(obo_non_existent_issues))
	with open('%s%s.txt' % (args.working_directory, 'OBOs_unique_non_existent_issues'), 'w+') as non_existent_issues_file:
		for obo_issue in obo_non_existent_issues:
			non_existent_issues_file.write('%s\n' % (obo_issue))




