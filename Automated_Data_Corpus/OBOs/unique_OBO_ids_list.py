import os
import re
import gzip
import argparse
import numpy as np


def unique_OBO_ids_list(OBO, OBO_file_path, evaluation_files, output_path):
	unique_OBO_set = set()

	##collect all the obos from each article in evaluation files
	for root, directories, filenames in os.walk('%s%s/' %(OBO_file_path, OBO)):
		for filename in sorted(filenames):
			if filename.endswith('.bionlp') and (filename.split('local_')[-1].replace('.nxml.gz.bionlp','') in evaluation_files or evaluation_files[0].lower() == 'all'):
				with open(root+filename, 'r+') as OBO_bionlp_file:
					#no header
					##lines: T0	CHEBI:33290 1616 1620	food
					for line in OBO_bionlp_file:
						line_list = line.split('\t')
						obo_id = line_list[1].split(' ')[0]
						unique_OBO_set.add(obo_id)

			else:
				pass


	##output the OBO id unique set
	with open('%s%s_%s.txt' %(output_path, OBO, 'unique_ids'), 'w+') as OBO_unique_output_file:
		OBO_unique_output_file.write('%s %s:\t%s\n\n' %('TOTAL UNIQUE IDS FOR', OBO, len(unique_OBO_set)))
		OBO_unique_output_file.write('%s\n' %('UNIQUE OBO IDS'))

		for u in unique_OBO_set:
			OBO_unique_output_file.write('%s\n' %(u))


	return unique_OBO_set





if __name__=='__main__':


	parser = argparse.ArgumentParser()

	parser.add_argument('-ontologies', type=str, help='a list of ontologies to use delimited with , no spaces')
	parser.add_argument('-OBO_file_path', type=str, help='file path to the OBO output file')
	parser.add_argument('-evaluation_files', type=str, help='a list of the files to be evaluated delimited with ,')
	parser.add_argument('-output_path', type=str,
						help='output path for the results')

	args = parser.parse_args()


	ontologies = args.ontologies.split(',')
	evaluation_files = args.evaluation_files.split(',')


	for OBO in ontologies:
		unique_OBO_set = unique_OBO_ids_list(OBO, args.OBO_file_path, evaluation_files, args.output_path)