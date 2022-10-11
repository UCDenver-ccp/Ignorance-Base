import os
import pandas as pd
import datetime
import argparse
import ast



def get_ont_totals(obo_unique_id_file_path):
	with open(obo_unique_id_file_path, 'r+') as obo_unique_id_file:
		for line in obo_unique_id_file:
			if line.startswith('TOTAL UNIQUE IDS FOR'):
				total_unique_ids = line.strip('\n').split('\t')[-1]
				break


	return total_unique_ids


if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('-ontologies', type=str, help='a list of ontologies to use delimited with ,')
	parser.add_argument('-obo_unique_ids_file_path', type=str, help='a list of the files to be evaluated delimited with ,')
	parser.add_argument('-output_path', type=str, help='the file path for the output of the summaries')


	args = parser.parse_args()

	ontologies = args.ontologies.split(',')

	with open('%s/%s.txt' %(args.output_path, '0_OBOS_UNIQUE_ID_SUMMARY_INFO'), 'w+') as obo_unique_ids_summary_file:
		obo_unique_ids_summary_file.write('%s\t%s\n' %('OBO', 'TOTAL UNIQUE IDS'))

		for obo in ontologies:
			obo_total = get_ont_totals('%s/%s_%s.txt' %(args.obo_unique_ids_file_path, obo,'unique_ids'))

			obo_unique_ids_summary_file.write('%s\t%s\n' %(obo, obo_total))


