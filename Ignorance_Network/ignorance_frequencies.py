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


def read_in_pickle_dict(pickle_dict_filepath):
	with open(pickle_dict_filepath, 'rb') as pickle_dict_file:
		pickle_dict = pickle.load(pickle_dict_file)
		return pickle_dict


def ignorance_category_count(ignorance_sentence_dict, ignorance_category_count_dict):
	ignorance_categories_not_collected = set([])
	for sent_num, info in ignorance_sentence_dict.items():
		# print(info)
		sent_ignorance_category_list = [i[0] for i in info[4]]
		sent_ignorance_category_list_set = set(sent_ignorance_category_list)
		# print(sent_ignorance_category_list)
		for ig_cat in sent_ignorance_category_list_set:
			if ignorance_category_count_dict.get(ig_cat.upper()):
				ignorance_category_count_dict[ig_cat.upper()][0] += 1
			else:
				ignorance_categories_not_collected.add(ig_cat.upper())

		# raise Exception('hold')

	##find percentages over the total sentences
	for ig_cat in ignorance_category_count_dict.keys():
		ignorance_category_count_dict[ig_cat][1] = (float(ignorance_category_count_dict[ig_cat][0]) / float(len(ignorance_sentence_dict.keys()))) * float(100)

	return ignorance_category_count_dict, ignorance_categories_not_collected


if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-ignorance_sentence_dict_file', type=str, help='the file path to the ignorance sentence dict')
	parser.add_argument('-ignorance_category_list', type=str, help='a list of ignorance categories of interest delimited by a , with no spaces')
	parser.add_argument('--all_sentences', type=str, help='true or false based on if we have all the sentences and need to get rid of not ignorance statements, default=false', default=False)
	parser.add_argument('-output_path', type=str, help='the output file path for the results')
	args = parser.parse_args()

	start_time = time.time()

	if args.all_sentences and args.all_sentences.lower() == 'true':
		all_sentence_dict = read_in_pickle_dict(args.ignorance_sentence_dict_file)
		total_sentences = len(all_sentence_dict)
		ignorance_sentence_dict = {k: v for k, v in all_sentence_dict.items() if v[4] != 'N/A'}
	else:
		ignorance_sentence_dict = read_in_pickle_dict(args.ignorance_sentence_dict_file)
		total_sentences = None

	ignorance_category_list_upper = args.ignorance_category_list.upper().split(',')

	ignorance_category_count_dict = {}  # ignorance category to [raw number, % out of all sentences)
	for i in ignorance_category_list_upper:
		ignorance_category_count_dict[i] = [0, None]

	ignorance_category_count_dict, ignorance_categories_not_collected = ignorance_category_count(ignorance_sentence_dict, ignorance_category_count_dict)
	print('IGNORANCE CATEGORIES NOT COLLECTED:')
	print(ignorance_categories_not_collected)
	# ignorance_category_list_upper.reverse()
	with open('%s_%s.txt' %(args.ignorance_sentence_dict_file.split('.pkl')[0], 'IGNORANCE_FREQUENCIES'), 'w+') as ignorance_freq_output:
		ignorance_freq_output.write('%s\t%s\t%s\n' %('IGNORANCE_CATEGORY', 'TOTAL IGNORANCE', 'PERCENT IGNORANCE (TOTAL SENTENCES DENOM)'))
		for ig_cat in ignorance_category_list_upper:
			ignorance_freq_output.write('%s\t%s\t%.2f%%\n' %(ig_cat.lower(), ignorance_category_count_dict[ig_cat][0], ignorance_category_count_dict[ig_cat][1]))

		ignorance_freq_output.write('\n%s\t%s\n' %('TOTAL IGNORANCE SENTENCES', len(ignorance_sentence_dict)))

		if total_sentences:
			ignorance_freq_output.write('\n%s\t%s\n' % ('TOTAL SENTENCES', total_sentences))


	print("--- %s seconds ---" % (time.time() - start_time))