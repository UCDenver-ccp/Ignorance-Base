import os
import nltk
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import pickle
import ast

def change_concept_numbers(bionlp_file_path, file_prefix):



	for root, directories, filenames in os.walk(bionlp_file_path):
		for filename in sorted(filenames):
			if filename.startswith(file_prefix):
				new_file_info = []
				with open(bionlp_file_path+filename, 'r+') as bionlp_file:

					for line in bionlp_file:
						line_info = line.strip('\n').split('\t')[1:]
						new_line = ''
						for l in line_info:
							new_line += '\t%s' %(l)
						new_file_info += [new_line]

				with open(bionlp_file_path+filename, 'w+') as bionlp_file_overwrite:
					for i, n in enumerate(new_file_info):
						bionlp_file_overwrite.write('T%s%s\n' %(i, n))






if __name__=='__main__':
	parser = argparse.ArgumentParser()


	parser.add_argument('-file_prefex', type=str, help='the file path to the pmcid sentence files')
	parser.add_argument('-ignorance_bionlp_file_path', type=str, help='file path to the ignorance bionlp files')

	args = parser.parse_args()

	change_concept_numbers(args.ignorance_bionlp_file_path, args.file_prefex)
