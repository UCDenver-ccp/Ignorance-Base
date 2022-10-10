import os
import nltk
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import pickle
import ast


def combine_all_OBOs_per_pmcid(article, ontologies, bionlp_folder, output_folder):

		with open('%s%s_%s.bionlp' %(output_folder, 'BEST', article), 'w+') as bionlp_combined_file:
			i = 0
			for ont in ontologies:
				try:
					with open('%s%s/%s_%s_%s%s' %(bionlp_folder, ont, ont, 'biobert_model_local', article, '.nxml.gz.bionlp'), 'r+') as bionlp_file:

						for line in bionlp_file:
							line_info = line.strip('\n').split('\t')[1:]
							new_line = 'T%s' %(i)
							for l in line_info:
								new_line += '\t%s' %(l)

							bionlp_combined_file.write('%s\n' %(new_line))
							i += 1

				##not every pmcid has an ontology file
				except FileNotFoundError:
					pass




if __name__=='__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-included_articles', type=str, help='either a list of all ')
	parser.add_argument('-OBO_ontologies', type=str, help='list of OBO ontologies to combine delimited with , no spaces')
	parser.add_argument('-bionlp_folder', type=str, help='the file path to the original bionlp files to combine')
	parser.add_argument('-output_folder', type=str, help='the file path to the output of the combined bionlp files')
	parser.add_argument('--article_path', type=str, help='optional folder to the articles if included articles is all', default='Articles/')
	args = parser.parse_args()

	if args.included_articles.lower() == 'all':
		included_articles_list = []
		for root, directories, filenames in os.walk(args.article_path):
			for filename in sorted(filenames):
				if filename.endswith('.nxml.gz.txt'):
					included_articles_list += [filename.split('.nxml')[0]]
				else:
					print(filename)
					# raise Exception('ERROR: Issue with extra file types in the articles!')
	else:
		included_articles_list = args.included_articles.split(',')

	obo_ontologies = args.OBO_ontologies.split(',')


	for article in included_articles_list:
		combine_all_OBOs_per_pmcid(article, obo_ontologies, args.bionlp_folder, args.output_folder)

