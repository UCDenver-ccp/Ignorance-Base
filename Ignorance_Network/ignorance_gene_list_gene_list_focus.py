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


def read_in_list_with_header(filepath, column):
	final_list = []
	with open(filepath, 'r+') as file:
		next(file) ##header to skip
		for line in file:
			list_item = line.strip('\n').split('\t')
			try:
				final_list += [list_item[column]]
			except IndexError:
				raise Exception('ERROR: Issue with column number is out of range of file information. Indexing starts at 0')

	return final_list

def read_in_david_output_file(david_file):
	david_go_enriched_obo_ids_dict = {} #obo_id -> [Bonferroni, BH]
	with open(david_file, 'r+') as file:
		next(file) ##header to skip
		for line in file:
			list_item = line.strip('\n').split('\t')
			# get rid of ~ stuff and replace : with _ for obo id
			go_id = list_item[1].split('~')[0].replace(':', '_')
			go_id_label = list_item[1].split('~')[1]
			bonferroni_pval = float(list_item[-3])
			bh_pval = float(list_item[-2])
			if bh_pval < 0.05:
				if david_go_enriched_obo_ids_dict.get(go_id):
					raise Exception('ERROR: Issue with repeat GO IDs in DAVID output')
				else:
					pass

				david_go_enriched_obo_ids_dict[go_id] = [bonferroni_pval, bh_pval, go_id_label]
			else:
				pass

	return david_go_enriched_obo_ids_dict


def read_in_coverage_file(coverage_filepath):
	coverage_dict = {} #obo_id -> [gene list, total genes]
	with open(coverage_filepath, 'r+') as coverage_file:
		next(coverage_file)
		for line in coverage_file:
			obo_id, gene_list, total_genes = line.strip('\n').split('\t')
			gene_list = ast.literal_eval(gene_list)
			if coverage_dict.get(obo_id):
				raise Exception('ERROR: Issue with duplicates in obo_ids to gene list')
			else:
				pass

			coverage_dict[obo_id] = [gene_list, int(total_genes)]

	return coverage_dict



if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-david_enrichment_filepath', type=str, help='the file path to the DAVID GO Enrichment analysis results file - the functional annotation chart')
	parser.add_argument('--obo_ids_no_information_ignorance', type=str, help='the file path to the file with the obo ids that do not match ignorance stuff', default=None)
	parser.add_argument('--obo_ids_no_information_not_ignorance', type=str, help='the file path to the file with the obo ids that do not match any not ignorance stuff', default=None)
	parser.add_argument('-all_obo_ids_with_info', type=str, help='file path to the obo id enrichment no ignorance to get all the obo ids that matched something')
	parser.add_argument('-obo_coverage_file', type=str, help='the file path to the obo coverage information from the gene list')
	parser.add_argument('-no_ignorance_enrichment_df_file', type=str, help='the file path to the no ignorance enrichment file that is a pandas dataframe to compare')
	parser.add_argument('-ignorance_enrichment_df_file', type=str, help='the file path to the ignorance enrichment file that is a pandas dataframe to compare')
	parser.add_argument('-output_path', type=str, help='the output file path for the results')
	args = parser.parse_args()

	start_time = time.time()

	##get david info stuff
	david_go_enriched_obo_ids_dict = read_in_david_output_file(args.david_enrichment_filepath)



	##get no information stuff
	if args.obo_ids_no_information_ignorance:
		obo_ids_no_information_ignorance = read_in_list_with_header(args.obo_ids_no_information_ignorance, 0)
	else:
		obo_ids_no_information_ignorance = []

	if args.obo_ids_no_information_not_ignorance:
		obo_ids_no_information_not_ignorance = read_in_list_with_header(args.obo_ids_no_information_not_ignorance, 0)
	else:
		obo_ids_no_information_not_ignorance = []

	##goal is the overlap between the two to say there really is no information on either side:
	truly_no_information_obos = set(obo_ids_no_information_ignorance).intersection(obo_ids_no_information_not_ignorance)
	with open('%s%s.txt' %(args.output_path, 'OBO_ID_no_ignorance_base_info'), 'w+') as no_info_obo_ids:
		no_info_obo_ids.write('%s\n' %('OBO_ID NO INFO'))
		for obo_id in truly_no_information_obos:
			no_info_obo_ids.write('%s\n' %(obo_id))


	print('truly no information obos:', len(truly_no_information_obos))

	##get all the obo ids we do have info about
	obo_ids_with_info = read_in_list_with_header(args.all_obo_ids_with_info, 1)


	##get the enrichment information
	general_enrichment_info_df = pd.read_csv(args.no_ignorance_enrichment_df_file, sep='\t')
	general_enrichment_info_df = general_enrichment_info_df.reset_index()

	ignorance_enrichment_info_df = pd.read_csv(args.ignorance_enrichment_df_file, sep='\t')
	ignorance_enrichment_info_df = ignorance_enrichment_info_df.reset_index()


	##DAVID GO ENRICHMENT STUFF
	##see if we have info on david go enriched obo ids
	with open('%s%s.txt' %(args.output_path, 'david_go_enrichment_ignorance_info'), 'w+') as david_output_file:
		david_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %('GO_OBO_ID', 'GO_OBO_LABEL', 'BONFERRONI P-VALUE', 'BENJAMINI-HOCHBERG', 'IGNORANCE-BASE (Y, N)', 'IGNORANCE (Y, N)', 'NOT IGNORANCE(Y, N)', 'GENERAL INDEX', 'GENERAL BONFERRONI P-VALUE', 'GENERAL BENGAMINI-HOCHBERG P-VALUE', 'IGNORANCE INDEX', 'IGNORANCE BONFERRONI P-VALUE', 'IGNORANCE BENGAMINI-HOCHBERG P-VALUE'))
		for go_id, pvals in david_go_enriched_obo_ids_dict.items():
			if go_id in obo_ids_with_info:

				#check if it is in ignorance or not
				if go_id in obo_ids_no_information_ignorance:
					ignorance_info = 'N'
				else:
					ignorance_info = 'Y'
				if go_id in obo_ids_no_information_not_ignorance:
					not_ignorance_info = 'N'
				else:
					not_ignorance_info = 'Y'

				if ignorance_info == 'N' and not_ignorance_info == 'N':
					raise Exception('ERROR: Issue with go_id in ignorance and not knowing its in ignorance-base')
				else:
					pass

				##find the general info
				general_index = general_enrichment_info_df.index[general_enrichment_info_df['OBO_ID'] == go_id].tolist()
				if len(general_index) > 1:
					raise Exception('ERROR: Issue with general enrichment results having duplicate OBO IDs')
				else:
					general_index = general_index[0]


				##find the ignorance info
				ignorance_index_list = ignorance_enrichment_info_df.index[ignorance_enrichment_info_df['OBO_ID'] == go_id].tolist()
				# print(ignorance_index)
				if len(ignorance_index_list) > 1:
					raise Exception('ERROR: Issue with ignorance enrichment results having duplicate OBO IDs')
				elif len(ignorance_index_list) == 1:
					ignorance_index = ignorance_index_list[0]
				else:
					ignorance_index = None


				if ignorance_index:
					david_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (go_id, pvals[2], pvals[0], pvals[1], 'Y', ignorance_info, not_ignorance_info, general_index, general_enrichment_info_df.iloc[general_index]['BONFERRONI_CRRECTION_P_VALUE'], general_enrichment_info_df.iloc[general_index]['BH_CRRECTION_P_VALUE'], ignorance_index, ignorance_enrichment_info_df.iloc[ignorance_index]['BONFERRONI_CRRECTION_P_VALUE'], ignorance_enrichment_info_df.iloc[ignorance_index]['BH_CRRECTION_P_VALUE']))
				else:
					david_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
					go_id, pvals[2], pvals[0], pvals[1], 'Y', ignorance_info, not_ignorance_info, general_index,
					general_enrichment_info_df.iloc[general_index]['BONFERRONI_CRRECTION_P_VALUE'],
					general_enrichment_info_df.iloc[general_index]['BH_CRRECTION_P_VALUE'], 'N/A',
					'N/A','N/A'))


			##no ignorance base info
			else:
				if go_id not in truly_no_information_obos:
					# print(go_id)
					##no information on it at all
					david_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (go_id, pvals[2], pvals[0], pvals[1], 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'))
					# raise Exception('ERROR: Issue with truly no obo ids matching the obo ids with info')
				else:
					david_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (go_id, pvals[2], pvals[0], pvals[1], 'N', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'))





	##OBO COVERAGE - do it for all and then sort by coverage!
	coverage_dict = read_in_coverage_file(args.obo_coverage_file)
	with open('%s%s.txt' %(args.output_path, 'coverage_obo_enrichment_ignorance_info'), 'w+') as coverage_output_file:
		coverage_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %('OBO_ID', 'OBO_LABEL', 'COVERAGE', 'IGNORANCE-BASE (Y, N)', 'IGNORANCE (Y, N)', 'NOT IGNORANCE(Y, N)', 'GENERAL INDEX', 'GENERAL BONFERRONI P-VALUE', 'GENERAL BENGAMINI-HOCHBERG P-VALUE', 'IGNORANCE INDEX', 'IGNORANCE BONFERRONI P-VALUE', 'IGNORANCE BENGAMINI-HOCHBERG P-VALUE'))


		for obo_id, coverage_info in coverage_dict.items():
			if obo_id in obo_ids_with_info:

				#check if it is in ignorance or not
				if obo_id in obo_ids_no_information_ignorance:
					ignorance_info = 'N'
				else:
					ignorance_info = 'Y'
				if obo_id in obo_ids_no_information_not_ignorance:
					not_ignorance_info = 'N'
				else:
					not_ignorance_info = 'Y'

				if ignorance_info == 'N' and not_ignorance_info == 'N':
					raise Exception('ERROR: Issue with obo_id in ignorance and not knowing its in ignorance-base')
				else:
					pass

				##find the general info
				general_index = general_enrichment_info_df.index[general_enrichment_info_df['OBO_ID'] == obo_id].tolist()
				if len(general_index) > 1:
					raise Exception('ERROR: Issue with general enrichment results having duplicate OBO IDs')
				else:
					general_index = general_index[0]


				##find the ignorance info
				# print(obo_id)
				ignorance_index_list = ignorance_enrichment_info_df.index[ignorance_enrichment_info_df['OBO_ID'] == obo_id].tolist()
				# print(ignorance_index_list)
				# print(len(ignorance_index_list))

				if len(ignorance_index_list) > 1:
					raise Exception('ERROR: Issue with ignorance enrichment results having duplicate OBO IDs')
				elif len(ignorance_index_list) == 1:
					ignorance_index = ignorance_index_list[0]
				else:
					ignorance_index = None

				# print('ignorance index', ignorance_index)
				if ignorance_index_list:
					coverage_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (obo_id, general_enrichment_info_df.iloc[general_index]['OBO_LABEL'], coverage_dict[obo_id][1], 'Y', ignorance_info, not_ignorance_info, general_index, general_enrichment_info_df.iloc[general_index]['BONFERRONI_CRRECTION_P_VALUE'], general_enrichment_info_df.iloc[general_index]['BH_CRRECTION_P_VALUE'], ignorance_index, ignorance_enrichment_info_df.iloc[ignorance_index]['BONFERRONI_CRRECTION_P_VALUE'], ignorance_enrichment_info_df.iloc[ignorance_index]['BH_CRRECTION_P_VALUE']))
					# print('ignorance')
				else:
					coverage_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
						obo_id, general_enrichment_info_df.iloc[general_index]['OBO_LABEL'], coverage_dict[obo_id][1] ,
						'Y', ignorance_info, not_ignorance_info, general_index,
						general_enrichment_info_df.iloc[general_index]['BONFERRONI_CRRECTION_P_VALUE'],
						general_enrichment_info_df.iloc[general_index]['BH_CRRECTION_P_VALUE'], 'N/A',
						'N/A','N/A'))
					# print('no ignorance')

				# if obo_id == 'SO_0000704':
				# 	raise Exception('hold')

			##no ignorance base info
			else:
				if obo_id not in truly_no_information_obos:
					# print(go_id)
					##no information on it at all
					coverage_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (obo_id, general_enrichment_info_df.iloc[general_index]['OBO_LABEL'], coverage_dict[obo_id][1], 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'))
				# raise Exception('ERROR: Issue with truly no obo ids matching the obo ids with info')
				else:
					coverage_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (obo_id, general_enrichment_info_df.iloc[general_index]['OBO_LABEL'], coverage_dict[obo_id][1], 'N', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'))








	print("--- %s seconds ---" % (time.time() - start_time))