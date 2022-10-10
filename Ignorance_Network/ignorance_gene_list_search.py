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
import re
import nltk
from nltk.corpus import stopwords
import time
import numpy as np



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


def find_genes_and_proteins_from_gene_list(gene_list, OBO_to_node_info_dict):
	##output the gene nodes and protein nodes that relate to our gene list

	gene_to_OBO_dict = {} ##gene -> OBO id list

	for obo_id in OBO_to_node_info_dict.keys():
		entity_type, integer_id, entity_uri, label, description_definition, synonym = OBO_to_node_info_dict[obo_id]

		##genes:
		if 'gene' in entity_uri:
			for gene_symbol in gene_list:
				if label == gene_symbol or label == '%s (human)' %(gene_symbol):
					if gene_to_OBO_dict.get(gene_symbol):
						gene_to_OBO_dict[gene_symbol] += [obo_id]
					else:
						gene_to_OBO_dict[gene_symbol] = [obo_id]
					break
				else:
					pass
		##proteins
		elif 'PR' in entity_uri:
			# print(synonym)
			for gene_symbol in gene_list:
				if label == gene_symbol or gene_symbol in synonym.split('|'):
					if gene_to_OBO_dict.get(gene_symbol):
						gene_to_OBO_dict[gene_symbol] += [obo_id]
					else:
						gene_to_OBO_dict[gene_symbol] = [obo_id]
					break
				else:
					pass

		##all the other obos
		else:
			pass



	return gene_to_OBO_dict


def find_other_obos(gene_symbol, obo_gene_list, graph, OBO_to_node_info_dict):
	gene_other_obos_dict= {} #dict from other_obo to count of its appearence
	for obo_id in obo_gene_list:
		[entity_type, integer_id, entity_uri, label, description_definition, synonym] = OBO_to_node_info_dict[obo_id]
		uriref_node = URIRef(entity_uri.replace('<', '').replace('>', ''))

		obo_id_neighbors = graph[uriref_node]
		for n in obo_id_neighbors.keys():
			obo_id_edge_info = graph.get_edge_data(n, uriref_node)

			for key in obo_id_edge_info.keys():
				##the edges connecting OBOs and sentences
				if type(key) is int:
					break
				else:
					# print(str(key))

					##relations ontology
					if 'RO' in str(key):
						# print('relations ontology')

						##interacts with - RO_0002434; molecularly interacts with = RO_0002436 (TODO: chebi to go with RO_0002436 not used - secondary relationship)
						if 'RO_0002434' in str(key) or 'RO_0002436' in str(key):
							##gene to chebi and pr to chebi
							if 'CHEBI_' in str(n) and ('PR_' in obo_id or 'gene/' in str(entity_uri)):
								chebi_obo_id = n.split('/')[-1]
								if gene_other_obos_dict.get(chebi_obo_id):
									gene_other_obos_dict[chebi_obo_id] += 1
								else:
									gene_other_obos_dict[chebi_obo_id] = 1

							## PR to PR (TODO: decide if we want this because two steps removed)
							elif 'PR_' in str(key) and 'PR_' in obo_id:
								pr_obo_id = n.split('/')[-1]
								if gene_other_obos_dict.get(pr_obo_id):
									gene_other_obos_dict[pr_obo_id] += 1
								else:
									gene_other_obos_dict[pr_obo_id] = 1

							else:
								pass

						##genetically interacts with = RO_0002435 (TODO: gathering extra gene info even though not useful right now for ignorance)
						elif 'RO_0002435' in str(key):
							if 'gene/' in str(n) and 'gene/' in str(entity_uri):
								gene_obo_id = n.split('/')[-1]
								if gene_other_obos_dict.get(gene_obo_id):
									gene_other_obos_dict[gene_obo_id] += 1
								else:
									gene_other_obos_dict[gene_obo_id] = 1
							else:
								pass


						##has gene product = RO_0002205
						elif 'RO_0002205' in str(key):
							if 'PR_' in str(n) and 'gene/' in str(entity_uri):
								pr_obo_id1 = n.split('/')[-1]
								if gene_other_obos_dict.get(pr_obo_id1):
									gene_other_obos_dict[pr_obo_id1] += 1
								else:
									gene_other_obos_dict[pr_obo_id1] = 1
							else:
								pass

						##located in = RO_0001025
						elif 'RO_0001025' in str(key):
							if ('UBERON_' in str(n) or 'GO_' in str(n) or 'CL_' in str(n)) and 'PR_' in obo_id:
								uberon_go_cc_obo_id = n.split('/')[-1]
								if gene_other_obos_dict.get(uberon_go_cc_obo_id):
									gene_other_obos_dict[uberon_go_cc_obo_id] += 1
								else:
									gene_other_obos_dict[uberon_go_cc_obo_id] = 1

							else:
								pass

						##participates in = RO_0000056
						elif 'RO_0000056' in str(key):
							if 'GO_' in str(n) and 'PR_' in obo_id:
								go_bp_obo_id = n.split('/')[-1]
								if gene_other_obos_dict.get(go_bp_obo_id):
									gene_other_obos_dict[go_bp_obo_id] += 1
								else:
									gene_other_obos_dict[go_bp_obo_id] = 1

							else:
								pass

						##has function = RO_0000085
						elif 'RO_0000085' in str(key):
							if 'GO_' in str(n) and 'PR_' in obo_id:
								go_mf_obo_id = n.split('/')[-1]
								if gene_other_obos_dict.get(go_mf_obo_id):
									gene_other_obos_dict[go_mf_obo_id] += 1
								else:
									gene_other_obos_dict[go_mf_obo_id] = 1

							else:
								pass


						##none of the ROs we want
						else:
							pass



						# print(n)
						# print(obo_id_edge_info)
						# raise Exception('hold')

					elif 'subClassOf' in str(key):
						# print('subclassof')
						# print(n)
						# print(obo_id_edge_info)
						# raise Exception('hold')

						##rdfs:subClassOf = subclass of
						if 'SO_' in str(n) and 'gene/' in str(entity_uri):
							so_obo_id = n.split('/')[-1]
							if gene_other_obos_dict.get(so_obo_id):
								gene_other_obos_dict[so_obo_id] += 1
							else:
								gene_other_obos_dict[so_obo_id] = 1

						else:
							pass

					else:
						pass


	# print(gene_other_obos_dict)
	# raise Exception('hold')



	return gene_other_obos_dict




if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--gene_list', type=str, help='a list of genes (gene symbols) to use to pull out ignorance statements, delimited with comma , no spaces', default=None)
	parser.add_argument('--gene_list_path', type=str, help='the path to a file with the gene list (gene symbols) - a title on the first line and then one gene symbol per line', default=None)
	parser.add_argument('-ignorance_full_graph', type=str, help='the file path to the ignorance full graph that we want to explore as a .gpickle file')
	parser.add_argument('-pheknowlator_node_info', type=str, help='file path to the node information for pheknowlator')
	parser.add_argument('-OBO_ontologies', type=str, help='a list of the OBO ontologies of interest delimited with , no spaces')
	parser.add_argument('-output_path', type=str, help='the output file path for the results')
	args = parser.parse_args()

	start_time = time.time()

	##read in OBO_ontologies
	OBO_ontologies = args.OBO_ontologies.split(',')


	##read in gene list
	if args.gene_list:
		gene_list = args.gene_list.split(',')
	elif args.gene_list_path:
		with open(args.gene_list_path, 'r+') as gene_list_file:
			next(gene_list_file) ##title
			gene_list = []
			for line in gene_list_file:
				gene_list += [line.strip('\n')]
	else:
		raise Exception('ERROR: Issue with no gene list as either a list or a path to a file')

	if len(gene_list) != len(set(gene_list)):
		print(gene_list)
		raise Exception('ERROR: Issue with duplicates in the gene list. Please fix.')
	else:
		pass

	print('Gene List:', gene_list)

	##read in gpickle ignorance graph file
	Full_Ignorance_Graph = read_in_pkl_graph(args.ignorance_full_graph)
	print('PROGRESS: read in full ignorance graph')

	##read in all phewknowlator node info
	OBO_to_node_info_dict = pheknowlator_node_info(
		args.pheknowlator_node_info)  # OBO_to_node_info_dict[obo_id] = [entity_type, integer_id, entity_uri, label, description_definition, synonym]
	print('PROGRESS: read in node Pheknowlator node info')


	##find genes and proteins from pheknowlator node list
	gene_to_OBO_dict = find_genes_and_proteins_from_gene_list(gene_list, OBO_to_node_info_dict)
	print(len(gene_list))
	print(len(gene_to_OBO_dict.keys()))

	##TODO: these are the genes that are not mapped to our pheknowlator!!!
	print('genes not mapped', set(gene_list) - set(gene_to_OBO_dict.keys()))


	##output the results of finding the gene list
	with open('%s%s.txt' %(args.output_path, 'vitamin_D_gene_list_OBO_ids'), 'w+') as gene_list_OBO_file:
		gene_list_OBO_file.write('%s\t%s\n' %('GENE SYMBOL', 'OBO_ID_LIST (GENE OR PROTEIN)'))
		for gene_symbol in gene_list:
			if gene_to_OBO_dict.get(gene_symbol):
				obo_id_list = gene_to_OBO_dict[gene_symbol]
			else:
				obo_id_list = []

			gene_list_OBO_file.write('%s\t%s\n' %(gene_symbol, obo_id_list))


	## find the other OBOs with the gene list and protein list using RO
	gene_to_all_OBO_dict = {}
	for gene_symbol in gene_list:
		if gene_to_OBO_dict.get(gene_symbol):
			obo_id_list = gene_to_OBO_dict[gene_symbol]

			##find the other obos
			gene_other_obos_dict = find_other_obos(gene_symbol, obo_id_list, Full_Ignorance_Graph, OBO_to_node_info_dict)
			if len(set([item[1] for item in gene_other_obos_dict.items()])) > 1:
				print(gene_symbol)
				print(set([item[1] for item in gene_other_obos_dict.items()]))
				print(gene_other_obos_dict)
			else:
				pass

			##TODO: combine all of it - make sure no duplicates!
			gene_to_all_OBO_dict[gene_symbol] = list(set(obo_id_list + list(gene_other_obos_dict.keys())))
		else:
			gene_to_all_OBO_dict[gene_symbol] = []


	##output all gene to obo info and use it to search for ignorance statements
	with open('%s%s.txt' %(args.output_path, 'vitamin_D_gene_list_all_OBO_ids'), 'w+') as gene_list_all_OBO_file:
		gene_list_all_OBO_file.write('%s\t%s\t%s\n' %('GENE SYMBOL', 'OBO_ID_LIST (ALL)', 'TOTAL OBOS'))
		for gene_symbol in gene_list:
			gene_list_all_OBO_file.write('%s\t%s\t%s\n' %(gene_symbol, gene_to_all_OBO_dict[gene_symbol], len(gene_to_all_OBO_dict[gene_symbol])))


	##grab the accounting of all the genes combined by obo_id
	obo_id_to_gene_list_dict = {} ##obo_id -> gene symbols it includes (the number of mentions it gets from the original gene list
	for gene_symbol in gene_list:
		gene_obo_id_list = gene_to_all_OBO_dict[gene_symbol]

		if gene_obo_id_list:
			for obo_id in gene_obo_id_list:
				##TODO: sort for just the ontologies we care about
				if obo_id.split('_')[0] in OBO_ontologies:
					if obo_id_to_gene_list_dict.get(obo_id):
						obo_id_to_gene_list_dict[obo_id] += [gene_symbol]
					else:
						obo_id_to_gene_list_dict[obo_id] = [gene_symbol]

				##get rid of the gene ids mainly
				else:
					pass


		##some genes have no OBO_ids - not found
		else:
			pass


	##output all obo to gene info
	with open('%s%s.txt' %(args.output_path, 'vitamin_D_gene_list_OBO_ids_to_genes'), 'w+') as gene_list_OBO_ids_to_genes_file:
		gene_list_OBO_ids_to_genes_file.write('%s\t%s\t%s\n' %('OBO_ID', 'GENE LIST', 'TOTAL GENES'))
		for obo_id in obo_id_to_gene_list_dict.keys():

			gene_list_OBO_ids_to_genes_file.write('%s\t%s\t%s\n' %(obo_id, obo_id_to_gene_list_dict[obo_id], len(obo_id_to_gene_list_dict[obo_id])))

	print('PROGRESS: We have %s OBO ids to look at for %s genes' %(len(obo_id_to_gene_list_dict.keys()), len(gene_list)))

	##output just obos to use
	with open('%s%s.txt' %(args.output_path, 'vitamin_D_gene_list_OBO_ids'), 'w+') as gene_list_OBO_ids_file:
		gene_list_OBO_ids_file.write('%s\n' %('OBO_ID'))
		for obo_id in obo_id_to_gene_list_dict.keys():

			gene_list_OBO_ids_file.write('%s\n' %(obo_id))


	print("--- %s seconds ---" % (time.time() - start_time))
