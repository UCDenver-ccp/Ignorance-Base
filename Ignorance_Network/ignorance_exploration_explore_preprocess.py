import argparse
import pickle
import networkx as nx
import ast
import re
from nltk.corpus import stopwords
import time
import os
import pandas as pd




def read_in_pkl_graph(graph_path):
	graph = nx.read_gpickle(graph_path)
	return graph

def read_in_pickle_dict(pickle_dict_filepath):
	with open(pickle_dict_filepath, 'rb') as pickle_dict_file:
		pickle_dict = pickle.load(pickle_dict_file)
		return pickle_dict

def all_graph_lexical_cue_words(graph):
	all_taxonomy_lcs = []
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


	return list(set(all_taxonomy_lcs))


def read_in_specific_sentence_files(sentence_filepath, sentence_dict, negative):
	if sentence_dict:
		pass
	else:
		sentence_dict = {} # sent_num -> info

	sentence_start = False
	file_type = False
	with open(sentence_filepath, 'r+') as sentence_file:
		for line in sentence_file:
			##the header before the sentences start
			if line.startswith('ARTICLE'):
				sentence_start = True
			elif line.startswith('\tARTICLE'):
				sentence_start = True
				file_type = True
			##sentences now
			elif sentence_start:
				if file_type:
					##'SENTENCE NUM', 'ARTICLE', 'ARTICLE DATE', 'SENTENCE NUM', 'SENTENCE', 'IGNORANCE CATEGORIES', 'NUM IGNORANCE CATEGORIES', 'OBO ID (LABEL)'
					sent_num, article, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info = line.strip('\n').split('\t')
				else:
					#'ARTICLE', 'ARTICLE DATE', 'SENTENCE NUM', 'SENTENCE', 'IGNORANCE CATEGORIES', 'NUM IGNORANCE CATEGORIES', 'OBO ID (LABEL)'
					article, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info = line.strip('\n').split('\t')


				if sentence_dict.get(sent_num):
					print('Sentence captured multiple times')
					print(sentence_filepath)
					# raise Exception('ERROR: Issue with specific sentence numbering and capturing')
				else:
					if negative:
						##fix the prime issue for the chemicals stuff
						if type(ast.literal_eval(sorted_sentence_obo_info)) == str:
							print('sorted info with errors')
							print(sorted_sentence_obo_info)
							sorted_sentence_obo_info = sorted_sentence_obo_info.replace('""', "\'").strip('"')
							new_sorted_sentence_obo_info = ''
							sorted_sentence_obo_info_split = sorted_sentence_obo_info.split("), (")

							# if len(sorted_sentence_obo_info_split) != 3:
							# 	new_sorted_sentence_obo_info_split = []



							for e in sorted_sentence_obo_info_split:
								# print('start')
								# print(e)

								e1 = e.split("', ")
								# print('E1', e1)
								# print(len(e1))
								for i, e2 in enumerate(e1):
									# print('E2', e2)
									if i == 0:
										if new_sorted_sentence_obo_info:
											new_sorted_sentence_obo_info += "), (%s', " % (e2)
										else:
											new_sorted_sentence_obo_info += "%s', " % (e2)
									elif i == 1:
										if len(e2.split("'")) > 2:
											# print(e2)
											updated_chem_name = e2[1:].replace("'", "*")
											print('UPDATED CHEM NAME', updated_chem_name)

											new_sorted_sentence_obo_info += "'%s', " % (updated_chem_name)

										else:
											new_sorted_sentence_obo_info += "%s', " % (e2)
									elif i == 2:
										if len(e2.split("'")) > 3:
											print(e2.split(", '"))
											if e2.split(", '")[-1].endswith("]"):
												updated_text = e2.split(", '")[-1][:-3].replace('""', "").strip('"').replace("'", "*")
												# print(type(updated_text))
												print('updated text other ending', updated_text)
												new_sorted_sentence_obo_info += "%s, '%s')]" %(e2.split(", '")[0], updated_text)
											else:
												updated_text = e2.split(", '")[-1][:-1].replace('""', "").strip('"').replace("'", "*")
												print('UPDATED TEXT', updated_text)
												new_sorted_sentence_obo_info += "%s, '%s'" %(e2.split(", '")[0], updated_text)
										else:
											new_sorted_sentence_obo_info += "%s" %(e2)
								# if "John's Wort" in e:
								# 	print([new_sorted_sentence_obo_info], type(new_sorted_sentence_obo_info))
								# 	raise Exception('hold')

							print(new_sorted_sentence_obo_info)
							# if "Peyer's patches" in sorted_sentence_obo_info:
							# 	raise Exception('hold')



							# print('ideally fixed errors')
							# print([new_sorted_sentence_obo_info])

							if type(ast.literal_eval(new_sorted_sentence_obo_info)) == str:
								raise Exception('ERROR: Issue with sorted sentence obo info converting to a list')
							elif '[' not in new_sorted_sentence_obo_info or ']' not in new_sorted_sentence_obo_info:
								print(sorted_sentence_obo_info)
								print(new_sorted_sentence_obo_info)
								raise Exception('ERROR: need to finish the string')
							else:
								sorted_sentence_obo_info = new_sorted_sentence_obo_info

						else:
							pass


						if type(ast.literal_eval(sentence_output_text)) == str:
							sentence_output_text_list = [sentence_output_text[1:-1]]
						elif type(ast.literal_eval(sentence_output_text)) == list:
							sentence_output_text_list = ast.literal_eval(sentence_output_text)
						else:
							raise Exception('ERROR: Issue with sentence_output_text ignorance')


						sentence_dict[sent_num] = [article, article_date, sent_num, sentence_output_text_list, sorted_sentence_lc, num_lc, ast.literal_eval(sorted_sentence_obo_info)] ##na for sorted sentence lc and num lc


					else:

						##TODO: weird error with quotes for making things a list so we have to fix it - CHEBI_66212, CHEBI_27844, CHEBI_73285

						##changed the prime ' to a start * because i dont think it is used - all for chemicals


						if type(ast.literal_eval(sorted_sentence_obo_info)) == str:
							# print('sorted info with errors')
							# print(sorted_sentence_obo_info)
							print('sorted info with errors')
							print(sorted_sentence_obo_info)
							sorted_sentence_obo_info = sorted_sentence_obo_info.replace('""', "\'").strip('"')
							new_sorted_sentence_obo_info = ''
							sorted_sentence_obo_info_split = sorted_sentence_obo_info.split("), (")

							# if len(sorted_sentence_obo_info_split) != 3:
							# 	new_sorted_sentence_obo_info_split = []

							for e in sorted_sentence_obo_info_split:
								# print('start')
								# print(e)

								e1 = e.split("', ")
								# print('E1', e1)
								# print(len(e1))
								for i, e2 in enumerate(e1):
									# print('E2', e2)
									if i == 0:
										if new_sorted_sentence_obo_info:
											new_sorted_sentence_obo_info += "), (%s', " % (e2)
										else:
											new_sorted_sentence_obo_info += "%s', " % (e2)
									elif i == 1:
										if len(e2.split("'")) > 2:
											# print(e2)
											updated_chem_name = e2[1:].replace("'", "*")
											print('UPDATED CHEM NAME', updated_chem_name)

											new_sorted_sentence_obo_info += "'%s', " % (updated_chem_name)

										else:
											new_sorted_sentence_obo_info += "%s', " % (e2)
									elif i == 2:
										if len(e2.split("'")) > 3:
											print(e2.split(", '"))
											if e2.split(", '")[-1].endswith("]"):
												updated_text = e2.split(", '")[-1][:-3].replace('""', "").strip(
													'"').replace("'", "*")
												# print(type(updated_text))
												print('updated text other ending', updated_text)
												new_sorted_sentence_obo_info += "%s, '%s')]" % (
												e2.split(", '")[0], updated_text)
											else:
												updated_text = e2.split(", '")[-1][:-1].replace('""', "").strip(
													'"').replace("'", "*")
												print('UPDATED TEXT', updated_text)
												new_sorted_sentence_obo_info += "%s, '%s'" % (
												e2.split(", '")[0], updated_text)
										else:
											new_sorted_sentence_obo_info += "%s" % (e2)
							# if "John's Wort" in e:
							# 	print([new_sorted_sentence_obo_info], type(new_sorted_sentence_obo_info))
							# 	raise Exception('hold')

							print(new_sorted_sentence_obo_info)

							if type(ast.literal_eval(new_sorted_sentence_obo_info)) == str:
								raise Exception('ERROR: Issue with sorted sentence obo info converting to a list')
							elif '[' not in new_sorted_sentence_obo_info or ']' not in new_sorted_sentence_obo_info:
								print(sorted_sentence_obo_info)
								print(new_sorted_sentence_obo_info)
								raise Exception('ERROR: need to finish the string')
							else:
								sorted_sentence_obo_info = new_sorted_sentence_obo_info

						else:
							pass


						if type(ast.literal_eval(sentence_output_text)) == str:
							sentence_output_text_list = [sentence_output_text[1:-1]]
						elif type(ast.literal_eval(sentence_output_text)) == list:
							sentence_output_text_list = ast.literal_eval(sentence_output_text)
						else:
							raise Exception('ERROR: Issue with sentence_output_text not ignorance')

						# print(type(sentence_output_text_list))
						sentence_dict[sent_num] = [article, article_date, sent_num, sentence_output_text_list, ast.literal_eval(sorted_sentence_lc), int(num_lc), ast.literal_eval(sorted_sentence_obo_info)]


			##the header of the file
			else:
				pass


	return sentence_dict


def preprocess_sentences(sentence_dict, all_taxonomy_lcs, obo_id_list, all_preprocess_sentence_dict, no_ignorance):


	preprocess_sentence_dict = {} # sent_num -> preprocessed sentence

	english_stopwords = set(stopwords.words('english'))

	for sent_num in sentence_dict.keys():
		article, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info = sentence_dict[sent_num]
		# print(sentence_dict[sent_num])
		##Get rid of the OBOs - TODO: figure out a way to take the preprocessed sentences with no lexical cues or stopwords to get rid of OBOs

		if obo_id_list:
			# for now we preprocess fully to make sure we know the obo_ids stuff exactly
			processed_sentence_text = sentence_output_text[0].lower().replace("'", "*") #not a list now!
			##TODO: issue with updating sentence in place!!! for processed_sentence_text
			print(processed_sentence_text)
			# print(sorted_sentence_obo_info)
			# print(type(sorted_sentence_obo_info))
			##get rid of obo_id_list via the spans
			if type(sorted_sentence_obo_info) == str:
				sorted_sentence_obo_info = ast.literal_eval(sorted_sentence_obo_info)
			else:
				pass
			# print(type(sorted_sentence_obo_info))
			sorted_sentence_obo_info.reverse()
			# print(len(sorted_sentence_obo_info))
			# print(len(processed_sentence_text))
			obo_id_list_count = 0
			for i, obo_info in enumerate(sorted_sentence_obo_info):
				overlap = False
				next_obo_id = None
				#id, label, start, mention_text

				print(obo_info)
				obo_id, obo_label, obo_start, obo_mention_text = obo_info
				##TODO:
				##deal with overlaps: skip the current one and move to the next one which will capture it
				if i != len(sorted_sentence_obo_info) - 1:
					next_obo_id, next_obo_label, next_obo_start, next_obo_mention_text = sorted_sentence_obo_info[i+1]

					if next_obo_start + len(next_obo_mention_text.replace(' ... ', '')) > obo_start:
						print('OVERLAPS IN CONCEPTS WE CARE ABOUT')
						print(obo_info)
						print(sorted_sentence_obo_info[i+1])
						overlap = True
					else:
						pass


				if obo_id in obo_id_list:
					obo_id_list_count += 1

					##if we have an overlap and they are both in things then we get rid of the next one
					if overlap and next_obo_id in obo_id_list:
						print('OVERLAP USED!')
						# raise Exception('hold')
						continue
					else:
						pass


					##split concept - discontinuous
					if '...' in obo_mention_text:
						obo_mention_text_split = obo_mention_text.split(' ... ')
						# obo_mention_text_split.reverse()
						print(processed_sentence_text)
						# print(obo_info)
						print(obo_mention_text_split)
						for s in obo_mention_text_split:
							if s.endswith(' ...'):
								s = s.replace(' ...', '')
							else:
								pass

							if s.startswith('... '):
								s = s.replace('... ', '')
							else:
								pass

							print([s])
							print(obo_start)
							# print(processed_sentence_text)
							s_index = processed_sentence_text.index(s.lower(), obo_start)
							processed_sentence_text = processed_sentence_text[:s_index] + processed_sentence_text[s_index + len(s):]
						# 	print(processed_sentence_text)
						# 	print(len(processed_sentence_text))
						# print(processed_sentence_text)
						# raise Exception('hold')

					##one concept - continuous
					else:
						obo_end = int(obo_start) + len(obo_mention_text)
						processed_sentence_text = processed_sentence_text[:obo_start] + processed_sentence_text[obo_end:]
						# print(processed_sentence_text)
						# print(len(processed_sentence_text))
				else:
					pass

			# print(processed_sentence_text)
			# print(len(processed_sentence_text))
			# print(obo_id_list_count)
			# raise Exception('hold')

			##get rid of all lexical cues
			if no_ignorance:
				pass
			else:
				get_rid_lc_count = 0
				for lc in all_taxonomy_lcs:
					# print(lc)
					regex_lc = r' %s ' %(lc.lower().replace('_', ' ').replace('?', '\?').replace(')', '\)').replace('(', '\('))
					prev_sent_len = len(processed_sentence_text)
					processed_sentence_text = re.sub(regex_lc, ' ', processed_sentence_text) #doesnt do anything if it is not there

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



			##TODO! get rid of stopwords!
			processed_sentence_text_list = [w for w in processed_sentence_text.split(' ') if not w.lower() in english_stopwords]
			processed_sentence_text = ' '.join(processed_sentence_text_list)
			# print(processed_sentence_text)



			preprocess_sentence_dict[sent_num] = processed_sentence_text

		else:
			processed_sentence_text = all_preprocess_sentence_dict[sent_num]
			preprocess_sentence_dict[sent_num] = processed_sentence_text


		# raise Exception('hold')

	return preprocess_sentence_dict





if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-ignorance_full_graph', type=str, help='the file path to the ignorance full graph that we want to explore as a .gpickle file')
	parser.add_argument('-specific_ignorance_statements_sentence_folder', type=str, help='the file path to the specific ignorance statement folder of interest')
	parser.add_argument('-specific_ignorance_statements_file_list', type=str, help='a list delimited with , (no spaces) of the files in the ignorance folder of interest, or all and need the extension')
	parser.add_argument('--specific_ignorance_statement_file_ext', type=str, help='if all files then the file extension to use, default is None', default=None)
	parser.add_argument('-specific_not_ignorance_statements_sentence_folder', type=str, help='the file path to the specific not ignorance statement folder of interest, or all and need the extension')
	parser.add_argument('-specific_not_ignorance_statements_file_list', type=str, help='a list delimited with , (no spaces) of the files in the not ignorance folder of interest')
	parser.add_argument('--specific_not_ignorance_statement_file_ext', type=str,
						help='if all files then the not file extension to use, default is None', default=None)
	parser.add_argument('-preprocess_sentence_dict_path', type=str, help='the file path to the full graph preprocessed sentence dict')
	parser.add_argument('-all_sentences_dict_path', type=str, help='the file path to the full graph sentence dict with all information')
	parser.add_argument('-output_path', type=str, help='the output file path for the results')
	parser.add_argument('--obo_id_list', type=str, help='optional: a list delimitted by , (no spaces) of the obo_ids of interest, if None, then we take the sentences from preprocessed sentence graph info', default=None)
	parser.add_argument('--exposure_name', type=str, help='the exposure name we are working in if using enriched obo ids or no ignorance, otherwise default None', default=None)
	parser.add_argument('--no_ignorance', type=str, help='true if there is no ignorance considerations but false otherwise and default false', default=False)

	args = parser.parse_args()

	##read in gpickle ignorance graph file
	# print(args.specific_ignorance_statements_file_list)
	Full_Ignorance_Graph = read_in_pkl_graph(args.ignorance_full_graph)

	##TODO: unhighlight when this is done on fiji
	if args.preprocess_sentence_dict_path.lower() == 'none':
		all_preprocess_sentence_dict = None
	else:
		all_preprocess_sentence_dict = read_in_pickle_dict(args.preprocess_sentence_dict_path)
	all_sentences_dict = read_in_pickle_dict(args.all_sentences_dict_path)

	##TODO: unhighlight once we are ready
	all_taxonomy_lcs = all_graph_lexical_cue_words(Full_Ignorance_Graph)
	print('NUMBER OF TAXONOMY LEXICAL CUES:', len(all_taxonomy_lcs))
	# print(args.specific_ignorance_statements_file_list)

	##ignorance statement files
	# print(str(args.specific_ignorance_statements_file_list))
	if str(args.specific_ignorance_statements_file_list).lower() == 'all':
		if args.specific_ignorance_statement_file_ext:
			specific_ignorance_statements_file_list = []
			for root, directories, filenames in os.walk(args.specific_ignorance_statements_sentence_folder):
				for filename in sorted(filenames):
					if filename.endswith(args.specific_ignorance_statement_file_ext):
						specific_ignorance_statements_file_list += [filename]
					else:
						pass
		else:
			raise Exception('ERROR: Issue with missing specific_ignorance_statement_file_ext, the file extension for all the files')

	elif str(args.specific_ignorance_statements_file_list).lower() == 'none':
		raise Exception('ERROR: must input atleast one specific ignorance statement file')

	elif 'ENRICHMENT_P_VALUES' in str(args.specific_ignorance_statements_file_list).upper():
		if args.exposure_name:
			pass
		else:
			raise Exception('ERROR: Issue with missing expsoure name for file stuff')


		enrichment_df = pd.read_table(args.specific_ignorance_statements_file_list, delimiter='\t')
		enriched_obo_id_list = list(enrichment_df.loc[enrichment_df['BH_CRRECTION_P_VALUE_REJECT'] == True, 'OBO_ID'])

		# print(enriched_obo_id_list) #['UBERON_0002405', 'GO_0007565', 'UBERON_0000104', 'SO_0000704', 'UBERON_0001442', 'UBERON_0007023', 'UBERON_0001004', 'GO_0007420', 'GO_0065007', 'PR_000045358', 'SO_0001023']

		enriched_obo_id_file_dict = {} #dict from obo_id to filepath
		for root, directories, filenames in os.walk(args.specific_ignorance_statements_sentence_folder):
			for filename in sorted(filenames):
				if filename.startswith(args.exposure_name.upper()) and 'SENTENCE' in filename:
					if filename.split('_')[-3] == 'ENRICHMENT':
						file_obo_id = filename.split('_')[-2]
					else:
						file_obo_id = filename.split('_')[-3] + '_' + filename.split('_')[-2]
					# print(file_obo_id)
					if file_obo_id in enriched_obo_id_list:
						if enriched_obo_id_file_dict.get(file_obo_id):
							raise Exception('ERROR: Issue with gathering multiple files')
						else:
							enriched_obo_id_file_dict[file_obo_id] = filename
					else:
						pass

		if len(enriched_obo_id_file_dict.keys()) != len(enriched_obo_id_list):

			# ##we have genes in here that are screwing us up
			# set_difference = [i.isdecimal() for i in list(set(enriched_obo_id_list) - set(enriched_obo_id_file_dict.keys()))]
			# if len(set(set_difference)) == 1 and set_difference[0] == True:
			# 	enriched_obo_id_list = enriched_obo_id_file_dict.keys()
			# else:
			print(len(enriched_obo_id_file_dict.keys()))
			print(len(enriched_obo_id_list))
			print(set(enriched_obo_id_list) - set(enriched_obo_id_file_dict.keys()))
			raise Exception('ERROR: Issue with missing files for some enriched obos')
		else:
			pass

		# print(enriched_obo_id_file_dict)
		specific_ignorance_statements_file_list = None

	else:
		specific_ignorance_statements_file_list = args.specific_ignorance_statements_file_list.split(',')


	if args.no_ignorance and args.no_ignorance.lower() == 'true':
		output_path = '%s%s_' %(args.output_path,'no_ignorance')
		no_ignorance = True
	else:
		output_path = args.output_path
		no_ignorance = False

	###not ignorance specific files
	if args.specific_not_ignorance_statements_file_list.lower() == 'all':
		if args.specific_not_ignorance_statement_file_ext:
			specific_not_ignorance_statements_file_list = []
			for root, directories, filenames in os.walk(args.specific_not_ignorance_statements_sentence_folder):
				for filename in sorted(filenames):
					if filename.endswith(args.specific_not_ignorance_statement_file_ext):
						specific_not_ignorance_statements_file_list += [filename]
					else:
						pass
		else:
			raise Exception('ERROR: Issue with missing specific_not_ignorance_statement_file_ext, the file extension for all the files')

	elif args.specific_not_ignorance_statements_file_list.lower() == 'none':
		specific_not_ignorance_statements_file_list = None

	elif 'ENRICHMENT_P_VALUES' in str(args.specific_not_ignorance_statements_file_list).upper():
		if args.exposure_name:
			pass
		else:
			raise Exception('ERROR: Issue with missing expsoure name for file stuff')

		enrichment_df = pd.read_table(args.specific_not_ignorance_statements_file_list, delimiter='\t')
		not_enriched_obo_id_list = list(enrichment_df.loc[enrichment_df['BH_CRRECTION_P_VALUE_REJECT'] == True, 'OBO_ID'])
		# print(not_enriched_obo_id_list) #['UBERON_0002405', 'GO_0007565', 'UBERON_0000104', 'SO_0000704', 'UBERON_0001442', 'UBERON_0007023', 'UBERON_0001004', 'GO_0007420', 'GO_0065007', 'PR_000045358', 'SO_0001023']

		not_enriched_obo_id_file_dict = {} #dict from obo_id to filepath
		for root, directories, filenames in os.walk(args.specific_not_ignorance_statements_sentence_folder):
			for filename in sorted(filenames):
				if filename.startswith('%s_%s' %('NOT', args.exposure_name.upper())) and 'SENTENCE' in filename:
					if filename.split('_')[-3] == 'ENRICHMENT':
						not_file_obo_id = filename.split('_')[-2]
					else:
						not_file_obo_id = filename.split('_')[-3] + '_' + filename.split('_')[-2]

					# print(file_obo_id)
					if not_file_obo_id in not_enriched_obo_id_list:
						if not_enriched_obo_id_file_dict.get(not_file_obo_id):
							raise Exception('ERROR: Issue with gathering multiple files for not ignorance')
						else:
							not_enriched_obo_id_file_dict[not_file_obo_id] = filename

		if len(not_enriched_obo_id_file_dict.keys()) != len(not_enriched_obo_id_list):
			raise Exception('ERROR: Issue with missing files for some enriched obos not ignorance')
		else:
			pass

		# print(not_enriched_obo_id_file_dict)
		specific_not_ignorance_statements_file_list = None
	else:
		specific_not_ignorance_statements_file_list = args.specific_not_ignorance_statements_file_list.split(',')



	if args.obo_id_list:
		obo_id_list = args.obo_id_list.split(',')
		if obo_id_list[0].lower() == 'none' or obo_id_list[0].lower() == 'false':
			obo_id_list = []
		else:
			pass
	else:
		obo_id_list = []

	not_obo_id_list = obo_id_list
	# print(obo_id_list)

	##TODO: it will mismatch because sometimes we have ignorance statements and sometimes not
	# if len(specific_ignorance_statements_file_list) != len(specific_not_ignorance_statements_file_list):
	# 	print(specific_ignorance_statements_file_list)
	# 	print(len(specific_ignorance_statements_file_list))
	# 	print(len(specific_not_ignorance_statements_file_list))
	# 	print(specific_not_ignorance_statements_file_list)
	# 	raise Exception('ERROR: Issue with needing the ignorance statement files and not ignorance statement files - mismatch')
	# else:
	# 	pass

	start_time = time.time()
	if specific_ignorance_statements_file_list:
		for f, ignorance_file in enumerate(specific_ignorance_statements_file_list):
			if f == 0:
				##first file so set it all up
				# print(ignorance_file)
				ignorance_sentence_dict = read_in_specific_sentence_files(args.specific_ignorance_statements_sentence_folder+ignorance_file, None, None)


			else:
				##add to the sentence file
				##TODO: should none be no_ignorance to be true or false with that?
				ignorance_sentence_dict = read_in_specific_sentence_files(args.specific_ignorance_statements_sentence_folder + ignorance_file, ignorance_sentence_dict, no_ignorance)


		##output the specific ignorance sentence dict
		output_sentence_dict = open('%s%s.pkl' % (output_path, 'IGNORANCE_SENTENCE_DICT'), 'wb')
		pickle.dump(ignorance_sentence_dict, output_sentence_dict)
		output_sentence_dict.close()

		##takes a while - maybe worth saving the processed sentences
		##create the dictionary of preprocessed sentences

		ignorance_preprocess_sentence_dict = preprocess_sentences(ignorance_sentence_dict, all_taxonomy_lcs, obo_id_list, all_preprocess_sentence_dict, no_ignorance)


		##save file
		print('PROGRESS: finished ignorance preprocessing sentences!')
		output = open('%s%s.pkl' % (output_path, 'IGNORANCE_PREPROCESSED_SENTENCES'), 'wb')
		pickle.dump(ignorance_preprocess_sentence_dict, output)
		output.close()

	else:
		for enriched_obo_id, enriched_obo_id_file in enriched_obo_id_file_dict.items():
			specific_obo_id_list = obo_id_list + [enriched_obo_id]

			print(args.specific_ignorance_statements_sentence_folder + enriched_obo_id_file)

			##TODO: should none be no_ignorance to be true or false with that?
			ignorance_sentence_dict = read_in_specific_sentence_files(args.specific_ignorance_statements_sentence_folder + enriched_obo_id_file, None, no_ignorance)
			# if 'VITAMIN_D_SENTENCE_OBO_ID_ENRICHMENT_PR_000001470_0.001.txt' in enriched_obo_id_file:
			# 	raise Exception('hold')

			##output the specific ignorance sentence dict
			output_sentence_dict = open('%s%s_%s.pkl' % (output_path, enriched_obo_id, 'IGNORANCE_SENTENCE_DICT'), 'wb')
			pickle.dump(ignorance_sentence_dict, output_sentence_dict)
			output_sentence_dict.close()

			##takes a while - maybe worth saving the processed sentences
			##create the dictionary of preprocessed sentences

			ignorance_preprocess_sentence_dict = preprocess_sentences(ignorance_sentence_dict, all_taxonomy_lcs, specific_obo_id_list, all_preprocess_sentence_dict, no_ignorance)

			##save file
			print('PROGRESS: finished ignorance preprocessing sentences!')
			output = open('%s%s_%s.pkl' % (output_path, enriched_obo_id, 'IGNORANCE_PREPROCESSED_SENTENCES'), 'wb')
			pickle.dump(ignorance_preprocess_sentence_dict, output)
			output.close()





	if specific_not_ignorance_statements_file_list:
		for nf, not_ignorance_file in enumerate(specific_not_ignorance_statements_file_list):
			if nf == 0:
				not_ignorance_sentence_dict = read_in_specific_sentence_files(args.specific_not_ignorance_statements_sentence_folder + not_ignorance_file, None, True)
			else:
				not_ignorance_sentence_dict = read_in_specific_sentence_files(args.specific_not_ignorance_statements_sentence_folder + not_ignorance_file, not_ignorance_sentence_dict, True)

		##output the specific ignorance sentence dict
		output_not_sentence_dict = open('%s%s.pkl' % (output_path, 'NOT_IGNORANCE_SENTENCE_DICT'), 'wb')
		pickle.dump(not_ignorance_sentence_dict, output_not_sentence_dict)
		output_not_sentence_dict.close()

		##create the dictionary of preprocessed sentences
		not_ignorance_preprocess_sentence_dict = preprocess_sentences(not_ignorance_sentence_dict, all_taxonomy_lcs, obo_id_list, all_preprocess_sentence_dict, no_ignorance)
		print('PROGRESS: finished not ignorance preprocessing sentences!')
		output1 = open('%s%s.pkl' % (output_path, 'NOT_IGNORANCE_PREPROCESSED_SENTENCES'), 'wb')
		pickle.dump(not_ignorance_preprocess_sentence_dict, output1)
		output1.close()

	else:
		for not_enriched_obo_id, not_enriched_obo_id_file in not_enriched_obo_id_file_dict.items():
			specific_not_obo_id_list = not_obo_id_list + [not_enriched_obo_id]
			not_ignorance_sentence_dict = read_in_specific_sentence_files(args.specific_not_ignorance_statements_sentence_folder + not_enriched_obo_id_file, None, True)

			##output the specific ignorance sentence dict
			not_output_sentence_dict = open('%s%s_%s.pkl' % (output_path, not_enriched_obo_id, 'NOT_IGNORANCE_SENTENCE_DICT'), 'wb')
			pickle.dump(not_ignorance_sentence_dict, not_output_sentence_dict)
			not_output_sentence_dict.close()

			##takes a while - maybe worth saving the processed sentences
			##create the dictionary of preprocessed sentences

			not_ignorance_preprocess_sentence_dict = preprocess_sentences(not_ignorance_sentence_dict, all_taxonomy_lcs, specific_not_obo_id_list, all_preprocess_sentence_dict, no_ignorance)

			##save file
			print('PROGRESS: finished not ignorance preprocessing sentences!')
			output = open('%s%s_%s.pkl' % (output_path, not_enriched_obo_id, 'NOT_IGNORANCE_PREPROCESSED_SENTENCES'), 'wb')
			pickle.dump(not_ignorance_preprocess_sentence_dict, output)
			output.close()


	print("--- %s seconds ---" % (time.time() - start_time))




