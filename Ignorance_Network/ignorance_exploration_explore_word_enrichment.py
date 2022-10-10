import argparse
import pandas as pd
import pickle
import ast
import time
from scipy.stats import hypergeom
import statsmodels.api as sm
#from patsy import dmatrices



def read_in_pickle_dict(pickle_dict_filepath):
	with open(pickle_dict_filepath, 'rb') as pickle_dict_file:
		pickle_dict = pickle.load(pickle_dict_file)
		return pickle_dict


def gather_all_obo_ids(sentence_dict):
	obo_id_set = set()
	obo_id_sent_count = {} #obo_id -> [sentence count, obo_text, [sentence num list]]

	for sent_num, sent_info in sentence_dict.items():
		# print(sent_num)
		# print(sent_info)
		for i in sent_info[-1]:
			obo_id = i[0]
			obo_text = i[1]
			obo_id_set.add(obo_id)
			# print(obo_id)


			if obo_id_sent_count.get(obo_id):
				obo_id_sent_count[obo_id][0] += 1
				if sent_num in obo_id_sent_count[obo_id][2]:
					pass
				else:
					obo_id_sent_count[obo_id][2] += [sent_num]
			else:
				obo_id_sent_count[obo_id] = [1, obo_text, [sent_num]]


	if len(obo_id_sent_count.keys()) != len(obo_id_set):
		raise Exception('ERROR: Issue with obo id set!')
	else:
		pass

	return obo_id_set, obo_id_sent_count


def get_word_sentence_count(word, sentence_dict):
	##full sentence text for now

	word_sentence_count = 0
	sent_num_list = []
	for sent_num, sent_info in sentence_dict.items():
		sentence_text = sent_info[3][0]
		if word.lower() in sentence_text.lower():
			word_sentence_count += 1
			sent_num_list += [sent_num]
		else:
			pass

	return word_sentence_count, sent_num_list


def get_ignorance_category_sentence_count(ignorance_categories_list, sentence_dict):
	ignorance_category_sent_count = {} #ignorance_category -> [sentence_count, [sent_num_list]]

	for sent_num, sent_info in sentence_dict.items():
		# print(sent_info)
		# print(sent_info[4])
		for i in sent_info[4]:
			ig_cat = i[0].lower()
			if ig_cat in ignorance_categories_list:
				if ignorance_category_sent_count.get(ig_cat):
					ignorance_category_sent_count[ig_cat][0] += 1
					ignorance_category_sent_count[ig_cat][1] += [sent_num]
				else:
					ignorance_category_sent_count[ig_cat] = [1, [sent_num]]

	if len(ignorance_categories_list) != len(ignorance_category_sent_count.keys()):
		print(len(ignorance_categories_list))
		print(len(ignorance_category_sent_count.keys()))

		raise Exception('ERROR: Issue with ignorance category list gathering!')
	else:
		pass

	return ignorance_category_sent_count


def get_article_counts(dataframe):
	# article_counts_df = dataframe['ARTICLE','ARTICLE DATE'].value_counts()
	article_counts_df = dataframe.groupby(['ARTICLE', 'ARTICLE DATE']).size()
	article_counts_df = article_counts_df.to_frame(name='NUM SENTENCES').reset_index()
	article_counts_df = article_counts_df.sort_values(by=['NUM SENTENCES'], ascending=False)
	# print(article_counts_df)
	return article_counts_df


##https://alexlenail.medium.com/understanding-and-implementing-the-hypergeometric-test-in-python-a7db688a7458
def hypergeom_pval(x, M, n, N):
	pval = hypergeom.sf(x - 1, M, n, N) ##we want enrichment or over-representation. the sf is 1-cdf ( P(X >= x) )
	return pval


if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--obo_id_list', type=str, help='a list of the obo_ids used to gather the ignorance sentences, delimited with comma , no spaces', default=None)
	parser.add_argument('--word_enrichment_list', type=str, help='a list of words to see if they are enriched in ignorance in list form as a string', default=None)
	parser.add_argument('--ignorance_categories_list', type=str, help='a list of the ignorance categories to see if enriched, delimited with comma , no spaces', default=None)
	parser.add_argument('-exposure_name', type=str, help='the name of the type of exposure for the enrichment')
	# parser.add_argument('-exposure_processed_sentences', type=str, help='the file path to the ignorance preprocessed sentence .pkl file or a list of them delimited with a , no spaces')
	# parser.add_argument('-not_exposure_processed_sentences', type=str, help='the file path to the not ignorance preprocessed sentence .pkl file or a list of them delimited with a , no spaces')
	parser.add_argument('-exposure_sentence_dict_file', type=str, help='the file path to the ignorance sentence dict pkl file or a list of them delimited with a , no spaces')
	parser.add_argument('-not_exposure_sentence_dict_file', type=str, help='the file path to the not ignorance sentence dict pkl file or a list of them delimited with a , no spaces')
	parser.add_argument('-output_path', type=str, help='the output file path for the results')
	parser.add_argument('--all_sentence_comparison', type=str, help='true or false based on if we are comparing all sentences, default is false', default=False)
	args = parser.parse_args()



	start_time = time.time()
	exposure_name = args.exposure_name
	if str(args.all_sentence_comparison).lower() == 'false':
		all_sentence_comparison = False
	elif args.all_sentence_comparison:
		all_sentence_comparison = True
	else:
		all_sentence_comparison = False


	##TODO: PREPROCESSED FILES = NOT USED HERE!
	##read in the pickle dict file - may be a list
	# exposure_processed_sentences_file_list = args.exposure_processed_sentences.split(',')
	# not_exposure_processed_sentences_file_list = args.not_exposure_processed_sentences.split(',')


	# exposure_preprocessed_sentence_dict = {}
	# for file1 in exposure_processed_sentences_file_list:
	# 	exposure_preprocessed_sentence_dict1 = read_in_pickle_dict(file1) #sentence_num -> preprocessed sentence text
	# 	exposure_preprocessed_sentence_dict.update(exposure_preprocessed_sentence_dict1)

	# if all_sentence_comparison:
	# 	if ',' in args.not_exposure_processed_sentences:
	# 		raise Exception('ERROR: Issue with the not exposure file must be one file and not a list if all_sentence_comparison is true')
	# 	##ignorance categories: get rid of the exposure sentences and then after get rid of the not ignorance sentences below
	# 	else:
	# 		all_preprocessed_sentences_dict = read_in_pickle_dict(args.not_exposure_processed_sentences)
	# 		not_exposure_preprocessed_sentence_dict = dict(all_preprocessed_sentences_dict.items() - exposure_preprocessed_sentence_dict.items())
	# 		if len(not_exposure_preprocessed_sentence_dict.keys()) + len(exposure_preprocessed_sentence_dict.keys()) != len(all_preprocessed_sentences_dict.keys()):
	# 			raise Exception('ERROR: Issue with getting rid of exposure sentences from the all preprocessed sentence dict')
	# 		else:
	# 			pass
	#
	# else:
	# 	not_exposure_preprocessed_sentence_dict = {}
	# 	for file2 in not_exposure_processed_sentences_file_list:
	# 		not_exposure_preprocessed_sentence_dict1 = read_in_pickle_dict(file2)
	# 		not_exposure_preprocessed_sentence_dict.update(not_exposure_preprocessed_sentence_dict1)


	# print('%s statements:' %(exposure_name), len(exposure_preprocessed_sentence_dict.keys())) ###8688 sentences
	# print('not %s statements:' %(exposure_name), len(not_exposure_preprocessed_sentence_dict.keys())) ##2153 sentences

	##sentence_dict[sent_num] = [article, article_date, sent_num, ast.literal_eval(sentence_output_text), sorted_sentence_lc, num_lc, ast.literal_eval(sorted_sentence_obo_info)] ##na for sorted sentence lc and num lc
	exposure_sentence_dict_file_list = args.exposure_sentence_dict_file.split(',')
	not_exposure_sentence_dict_file_list = args.not_exposure_sentence_dict_file.split(',')

	exposure_sentence_dict = {}
	for file3 in exposure_sentence_dict_file_list:
		exposure_sentence_dict1 = read_in_pickle_dict(file3)
		exposure_sentence_dict.update(exposure_sentence_dict1)

	if all_sentence_comparison:
		if ',' in args.not_exposure_sentence_dict_file:
			raise Exception('ERROR: Issue with the not exposure file must be one file and not a list if all_sentence_comparison is true')
		else:
			all_sentences_dict = read_in_pickle_dict(args.not_exposure_sentence_dict_file)
			not_exposure_sentence_dict = {k: v for k, v in all_sentences_dict.items() if k not in exposure_sentence_dict}

			if len(not_exposure_sentence_dict.keys()) + len(exposure_sentence_dict.keys()) != len(all_sentences_dict.keys()):
				raise Exception('ERROR: Issue with getting rid of exposure sentences from the all preprocessed sentence dict')
			else:
				pass

			if args.ignorance_categories_list:
				#get rid of not ignorance sentences
				# for k,v in not_exposure_sentence_dict.items():
				# 	if v[4] != 'N/A':
				# 		print(v)
				not_exposure_sentence_dict = {k: v for k, v in not_exposure_sentence_dict.items() if v[4] != 'N/A'}
				##get rid of not ignorance preprocessed sentences - only keep the ones in the final not exposure ones
				# not_exposure_preprocessed_sentence_dict = {k: v for k, v in not_exposure_preprocessed_sentence_dict.items() if k in not_exposure_sentence_dict.keys()}

	else:
		not_exposure_sentence_dict = {}
		for file4 in not_exposure_sentence_dict_file_list:
			not_exposure_sentence_dict1 = read_in_pickle_dict(file4)
			not_exposure_sentence_dict.update(not_exposure_sentence_dict1)



	##dataframes
	exposure_sentence_df = pd.DataFrame.from_dict(exposure_sentence_dict, orient='index',
												   columns=['ARTICLE', 'ARTICLE DATE', 'SENTENCE NUM', 'SENTENCE',
															'IGNORANCE CATEGORIES', 'NUM IGNORANCE CATEGORIES',
															'OBO ID (LABEL)'])
	not_exposure_sentence_df = pd.DataFrame.from_dict(not_exposure_sentence_dict, orient='index',
													   columns=['ARTICLE', 'ARTICLE DATE', 'SENTENCE NUM', 'SENTENCE',
																'IGNORANCE CATEGORIES', 'NUM IGNORANCE CATEGORIES',
																'OBO ID (LABEL)'])

	print('total exposure sentences:', len(exposure_sentence_dict.keys()))
	print('total not exposure sentences:', len(not_exposure_sentence_dict.keys()))

	##output the per article stats for expoure vs not exposure
	exposure_article_counts_df = get_article_counts(exposure_sentence_df)
	not_exposure_article_counts_df = get_article_counts(not_exposure_sentence_df)
	exposure_article_counts_df.to_csv('%s%s.txt' % (args.output_path, '0_%s_ARTICLE_COUNTS' % (exposure_name.upper())), sep='\t')
	not_exposure_article_counts_df.to_csv('%s%s.txt' % (args.output_path, '0_NOT_%s_ARTICLE_COUNTS' % (exposure_name.upper())), sep='\t')

	combined_exposure_article_counts_df = pd.merge(exposure_article_counts_df, not_exposure_article_counts_df, how='outer', on=['ARTICLE', 'ARTICLE DATE']).fillna(0)
	combined_exposure_article_counts_df.to_csv('%s%s.txt' % (args.output_path, '0_ALL_%s_ARTICLE_COUNTS' % (exposure_name.upper())), sep='\t')


	# raise Exception('hold')


	##TODO: USING PREPROCESS FOR NUMBERS
	# M = len(exposure_preprocessed_sentence_dict.keys()) + len(not_exposure_preprocessed_sentence_dict.keys())  #the total population size (the number of sentences with the word we used to pull it out) - #10841
	# print('total sentences:', M)
	#
	# n = len(exposure_preprocessed_sentence_dict.keys()) #total number of ignorance sentences - 8688

	##USING SENTENCE DICT FOR NUMBERS WHICH SHOULD BE THE SAME
	M = len(exposure_sentence_dict.keys()) + len(not_exposure_sentence_dict.keys())  #the total population size (the number of sentences with the word we used to pull it out) - #10841
	print('total sentences:', M)


	n = len(exposure_sentence_dict.keys()) #total number of ignorance sentences - 8688

	##gather set of all OBOs in these sentences not and counts of sentences
	if args.obo_id_list and args.obo_id_list.lower() != 'none' and args.obo_id_list.lower() != 'false':
		obo_id_list_set = set(args.obo_id_list.split(','))
	else:
		##empty set if we don't have anything we want to get rid of for preprocessing
		obo_id_list_set = set([])

	exposure_obo_id_set, exposure_obo_id_sent_count = gather_all_obo_ids(exposure_sentence_dict)
	# print('got here')
	not_exposure_obo_id_set, not_exposure_obo_id_sent_count = gather_all_obo_ids(not_exposure_sentence_dict)
	# raise Exception('hold')

	print('unique exposure obo_ids:', len(exposure_obo_id_set))
	print('unique not exposure obo ids:', len(not_exposure_obo_id_set))
	all_obo_ids = exposure_obo_id_set.union(not_exposure_obo_id_set)
	print('all unique obo_ids:', len(all_obo_ids))
	##obo id list to check for enrichment with!
	other_obo_ids = all_obo_ids - obo_id_list_set
	print('other unique obo ids:', len(other_obo_ids)) #2708 (2 subtracted)




	## enrichment over the obo_ids
	obo_id_enrichment_df = pd.DataFrame(columns=['OBO_ID', 'OBO_LABEL', 'ENRICHMENT_P_VALUE', 'TOTAL_POPULATION', 'TOTAL_SUCCESSES', 'TOTAL_%s' %(exposure_name.upper()), 'TOTAL_SUCCESSES_IN_%s' %(exposure_name.upper())], dtype=object)

	for obo_id in other_obo_ids:
		## N = total number of successes in population - all sentences with the obo concept
		## x = total number of successes in ignorance
		if exposure_obo_id_sent_count.get(obo_id) and not_exposure_obo_id_sent_count.get(obo_id):
			N = exposure_obo_id_sent_count[obo_id][0] + not_exposure_obo_id_sent_count[obo_id][0]
			x = exposure_obo_id_sent_count[obo_id][0]
			obo_id_label = exposure_obo_id_sent_count[obo_id][1]
		elif exposure_obo_id_sent_count.get(obo_id):
			N = exposure_obo_id_sent_count[obo_id][0]
			x = exposure_obo_id_sent_count[obo_id][0]
			obo_id_label = exposure_obo_id_sent_count[obo_id][1]
		else:
			N = not_exposure_obo_id_sent_count[obo_id][0]
			x = 0
			obo_id_label = not_exposure_obo_id_sent_count[obo_id][1]


		obo_id_pval = hypergeom_pval(x, M, n, N)
		# if obo_id_pval < 0.05:
		# 	print(obo_id, obo_id_pval)

		# raise Exception('hold')

		obo_id_enrichment_df = obo_id_enrichment_df.append({'OBO_ID': obo_id, 'OBO_LABEL': obo_id_label, 'ENRICHMENT_P_VALUE': obo_id_pval, 'TOTAL_POPULATION': M, 'TOTAL_SUCCESSES': N, 'TOTAL_%s' %(exposure_name.upper()): n, 'TOTAL_SUCCESSES_IN_%s' %(exposure_name.upper()): x}, ignore_index=True)

		##output the sentences if the p value is less than 0.05 so significant
		if obo_id_pval < 0.05:
			exposure_sentence_df.loc[exposure_obo_id_sent_count[obo_id][2]].to_csv('%s%s_%s_%.3f.txt' % (args.output_path, '%s_SENTENCE_OBO_ID_ENRICHMENT' %(exposure_name.upper()), obo_id, obo_id_pval), sep='\t')

			specific_exposure_article_counts_df = get_article_counts(exposure_sentence_df.loc[exposure_obo_id_sent_count[obo_id][2]])
			specific_exposure_article_counts_df.to_csv('%s%s_%s_%.3f.txt' % (args.output_path, '%s_ARTICLE_COUNTS_OBO_ID' %(exposure_name.upper()), obo_id, obo_id_pval), sep='\t')

			try:
				not_exposure_sentence_df.loc[not_exposure_obo_id_sent_count[obo_id][2]].to_csv('%s%s_%s_%.3f.txt' % (args.output_path, 'NOT_%s_SENTENCE_OBO_ID_ENRICHMENT' %(exposure_name.upper()), obo_id, obo_id_pval), sep='\t')

				specific_not_exposure_article_counts_df = get_article_counts(not_exposure_sentence_df.loc[not_exposure_obo_id_sent_count[obo_id][2]])
				specific_not_exposure_article_counts_df.to_csv(
					'%s%s_%s_%.3f.txt' % (args.output_path, 'NOT_%s_ARTICLE_COUNTS_OBO_ID' %(exposure_name.upper()), obo_id, obo_id_pval), sep='\t')

				combined_specific_exposure_article_counts_df = pd.merge(specific_exposure_article_counts_df,specific_not_exposure_article_counts_df, how='outer', on=['ARTICLE', 'ARTICLE DATE']).fillna(0)
				combined_specific_exposure_article_counts_df.to_csv('%s%s_%s_%.3f.txt' % (args.output_path, 'ALL_%s_ARTICLE_COUNTS_OBO_ID' %(exposure_name.upper()), obo_id, obo_id_pval), sep='\t')

			except KeyError:
				with open('%s%s_%s_%.3f.txt' %(args.output_path, 'NOT_%s_SENTENCE_OBO_ID_ENRICHMENT' %(exposure_name.upper()), obo_id, obo_id_pval), 'w+') as not_exposure_empty_file:
					not_exposure_empty_file.write('NO SENTENCES')

				specific_exposure_article_counts_df.to_csv('%s%s_%s_%.3f.txt' % (args.output_path, 'ALL_%s_ARTICLE_COUNTS_OBO_ID' % (exposure_name.upper()), obo_id, obo_id_pval), sep='\t')


		else:
			pass

	# obo_id_enrichment_df.sort_values(by=['ENRICHMENT_P_VALUE'])
	# print(obo_id_enrichment_df)
	obo_id_enrichment_df = obo_id_enrichment_df.sort_values(by=['ENRICHMENT_P_VALUE'])


	##multiple test correction p-values - https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html
	obo_id_pval_sorted_list = obo_id_enrichment_df['ENRICHMENT_P_VALUE']
	bonferroni_correction_info = sm.stats.multipletests(obo_id_pval_sorted_list, alpha=0.05, method='bonferroni', is_sorted=True)
	# print(bonferroni_corretion_info)
	# print(bonferroni_corretion_info[0][:20])
	# print(bonferroni_corretion_info[1][:20])
	print('Bonferroni alphacBonf:', bonferroni_correction_info[-1])
	obo_id_enrichment_df['BONFERRONI_CRRECTION_P_VALUE'] = bonferroni_correction_info[1]
	obo_id_enrichment_df['BONFERRONI_CRRECTION_P_VALUE_REJECT'] = bonferroni_correction_info[0]

	##benjamini-hochberg one
	bh_correction_info = sm.stats.multipletests(obo_id_pval_sorted_list, alpha=0.05, method='fdr_bh', is_sorted=True)
	# print(bh_correction_info)
	print('Benjamini/Hochberg alphacBonf:', bh_correction_info[-1])
	obo_id_enrichment_df['BH_CRRECTION_P_VALUE'] = bh_correction_info[1]
	obo_id_enrichment_df['BH_CRRECTION_P_VALUE_REJECT'] = bh_correction_info[0]

	##output the enrichment dataframe
	obo_id_enrichment_df.to_csv('%s%s.txt' % (args.output_path, '0_%s_SENTENCE_OBO_ID_ENRICHMENT_P_VALUES' %(exposure_name.upper())),
								sep='\t')



	##word enrichment analysis if there is a list of words
	if args.word_enrichment_list:

		word_enrichment_df = pd.DataFrame(columns=['WORD', 'ENRICHMENT_P_VALUE', 'TOTAL_POPULATION', 'TOTAL_SUCCESSES', 'TOTAL_%s' %(exposure_name.upper()), 'TOTAL_SUCCESSES_IN_%s' %(exposure_name.upper())], dtype=object)

		word_enrichment_list = ast.literal_eval(args.word_enrichment_list)
		print(word_enrichment_list)

		for word in word_enrichment_list:
			##TODO: can make this more efficient if we need to by gathering all words at once
			exposure_word_sentence_count, exposure_sent_num_list = get_word_sentence_count(word, exposure_sentence_dict)
			not_exposure_word_sentence_count, not_exposure_sent_num_list = get_word_sentence_count(word, not_exposure_sentence_dict)

			N = exposure_word_sentence_count + not_exposure_word_sentence_count
			x = exposure_word_sentence_count

			word_pval = hypergeom_pval(x, M, n, N)
			# print(word, word_pval)

			word_enrichment_df = word_enrichment_df.append({'WORD': word, 'ENRICHMENT_P_VALUE': word_pval, 'TOTAL_POPULATION': M,'TOTAL_SUCCESSES': N, 'TOTAL_%s' %(exposure_name.upper()): n, 'TOTAL_SUCCESSES_IN_%s' %(exposure_name.upper()): x}, ignore_index=True)

			##output the sentences if the p value is less than 0.05 so significant
			if word_pval < 0.05:
				exposure_sentence_df.loc[exposure_sent_num_list].to_csv(
					'%s%s_%s_%.3f.txt' % (args.output_path, '%s_SENTENCE_WORD_ENRICHMENT' %(exposure_name.upper()), word, word_pval),
					sep='\t')

				specific_exposure_article_counts_df1 = get_article_counts(exposure_sentence_df.loc[exposure_sent_num_list])
				specific_exposure_article_counts_df1.to_csv('%s%s_%s_%.3f.txt' % (args.output_path, '%s_ARTICLE_COUNTS_WORD' % (exposure_name.upper()), word, word_pval), sep='\t')


				not_exposure_sentence_df.loc[not_exposure_sent_num_list].to_csv(
					'%s%s_%s_%.3f.txt' % (args.output_path, 'NOT_%s_SENTENCE_WORD_ENRICHMENT' %(exposure_name.upper()), word, word_pval),
					sep='\t')

				specific_not_exposure_article_counts_df1 = get_article_counts(
					not_exposure_sentence_df.loc[not_exposure_sent_num_list])
				specific_not_exposure_article_counts_df1.to_csv(
					'%s%s_%s_%.3f.txt' % (
					args.output_path, 'NOT_%s_ARTICLE_COUNTS_WORD' % (exposure_name.upper()), word, word_pval),
					sep='\t')
			else:
				pass

		word_enrichment_df = word_enrichment_df.sort_values(by=['ENRICHMENT_P_VALUE'])
		# print(word_enrichment_df)

		##multiple test correction p-values
		word_pval_sorted_list = word_enrichment_df['ENRICHMENT_P_VALUE']
		word_bonferroni_correction_info = sm.stats.multipletests(word_pval_sorted_list, alpha=0.05, method='bonferroni', is_sorted=True)
		print('Bonferroni alphacBonf:', word_bonferroni_correction_info[-1])
		word_enrichment_df['BONFERRONI_CRRECTION_P_VALUE'] = word_bonferroni_correction_info[1]
		word_enrichment_df['BONFERRONI_CRRECTION_P_VALUE_REJECT'] = word_bonferroni_correction_info[0]

		##benjamini-hochberg one
		word_bh_correction_info = sm.stats.multipletests(word_pval_sorted_list, alpha=0.05, method='fdr_bh', is_sorted=True)

		# print(word_bh_correction_info)
		# print(len(word_bh_correction_info[0]), len(word_bh_correction_info[1]))

		print('Benjamini/Hochberg alphacBonf:', word_bh_correction_info[-1])
		word_enrichment_df['BH_CRRECTION_P_VALUE'] = word_bh_correction_info[1]
		word_enrichment_df['BH_CRRECTION_P_VALUE_REJECT'] = word_bh_correction_info[0]


		word_enrichment_df.to_csv('%s%s.txt' % (args.output_path, '0_%s_SENTENCE_WORD_ENRICHMENT_P_VALUES' %(exposure_name.upper())), sep='\t')

	else:
		pass

	if args.ignorance_categories_list:
		ignorance_categories_list = args.ignorance_categories_list.split(',')
		print('Ignorance category enrichment list:', ignorance_categories_list)

		ignorance_category_enrichment_df = pd.DataFrame(columns=['IGNORANCE_CATEGORY', 'ENRICHMENT_P_VALUE', 'TOTAL_POPULATION', 'TOTAL_SUCCESSES','TOTAL_%s' % (exposure_name.upper()), 'TOTAL_SUCCESSES_IN_%s' % (exposure_name.upper())], dtype=object)

		##gather all ignorance category enrichment information
		exposure_ignorance_category_sent_count = get_ignorance_category_sentence_count(ignorance_categories_list, exposure_sentence_dict)

		not_exposure_ignorance_category_sent_count = get_ignorance_category_sentence_count(ignorance_categories_list, not_exposure_sentence_dict)

		for ig_cat in ignorance_categories_list:
			## N = total number of successes in population - all sentences with the ignorance category
			## x = total number of successes in ignorance
			if exposure_ignorance_category_sent_count.get(ig_cat) and not_exposure_ignorance_category_sent_count.get(ig_cat):
				N = exposure_ignorance_category_sent_count[ig_cat][0] + not_exposure_ignorance_category_sent_count[ig_cat][0]
				x = exposure_ignorance_category_sent_count[ig_cat][0]

			elif exposure_ignorance_category_sent_count.get(ig_cat):
				N = exposure_ignorance_category_sent_count[ig_cat][0]
				x = exposure_ignorance_category_sent_count[ig_cat][0]

			else:
				N = not_exposure_ignorance_category_sent_count[ig_cat][0]
				x = 0


			ignorance_category_pval = hypergeom_pval(x, M, n, N)

			ignorance_category_enrichment_df = ignorance_category_enrichment_df.append(
				{'IGNORANCE_CATEGORY': ig_cat, 'ENRICHMENT_P_VALUE': ignorance_category_pval, 'TOTAL_POPULATION': M,
				 'TOTAL_SUCCESSES': N, 'TOTAL_%s' % (exposure_name.upper()): n,
				 'TOTAL_SUCCESSES_IN_%s' % (exposure_name.upper()): x}, ignore_index=True)

			##output the sentences if the p value is less than 0.05 so significant
			if ignorance_category_pval < 0.05:
				exposure_sentence_df.loc[exposure_ignorance_category_sent_count[ig_cat][1]].to_csv('%s%s_%s_%.3f.txt' % (args.output_path, '%s_SENTENCE_INGNORANCE_CATEGORY_ENRICHMENT' % (exposure_name.upper()), ig_cat, ignorance_category_pval), sep='\t')

				specific_exposure_article_counts_df2 = get_article_counts(exposure_sentence_df.loc[exposure_ignorance_category_sent_count[ig_cat][1]])
				specific_exposure_article_counts_df2.to_csv('%s%s_%s_%.3f.txt' % (
				args.output_path, '%s_ARTICLE_COUNTS_ IGNORANCE_CATEGORY' % (exposure_name.upper()), ig_cat, ignorance_category_pval), sep='\t')

				try:
					not_exposure_sentence_df.loc[exposure_ignorance_category_sent_count[ig_cat][1]].to_csv('%s%s_%s_%.3f.txt' % (args.output_path, 'NOT_%s_SENTENCE_IGNORANCE_CATEGORY_ENRICHMENT' % (exposure_name.upper()), ig_cat, ignorance_category_pval), sep='\t')

					specific_not_exposure_article_counts_df2 = get_article_counts(not_exposure_sentence_df.loc[exposure_ignorance_category_sent_count[ig_cat][1]])
					specific_not_exposure_article_counts_df2.to_csv('%s%s_%s_%.3f.txt' % (args.output_path, 'NOT_%s_ARTICLE_COUNTS_IGNOANCE_CATEGORY' % (exposure_name.upper()), ig_cat, ignorance_category_pval), sep='\t')

				except KeyError:
					with open('%s%s_%s_%.3f.txt' % (args.output_path, 'NOT_%s_SENTENCE_IGNORANCE_CATEGORY_ENRICHMENT' % (exposure_name.upper()), ig_cat, ignorance_category_pval), 'w+') as not_exposure_empty_file:
						not_exposure_empty_file.write('NO SENTENCES')


			else:
				pass


		ignorance_category_enrichment_df = ignorance_category_enrichment_df.sort_values(by=['ENRICHMENT_P_VALUE'])

		##multiple test correction p-values - https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html
		ignorance_category_pval_sorted_list = ignorance_category_enrichment_df['ENRICHMENT_P_VALUE']
		bonferroni_correction_info = sm.stats.multipletests(ignorance_category_pval_sorted_list, alpha=0.05, method='bonferroni',
															is_sorted=True)
		# print(bonferroni_corretion_info)
		# print(bonferroni_corretion_info[0][:20])
		# print(bonferroni_corretion_info[1][:20])
		print('Bonferroni alphacBonf:', bonferroni_correction_info[-1])
		ignorance_category_enrichment_df['BONFERRONI_CRRECTION_P_VALUE'] = bonferroni_correction_info[1]
		ignorance_category_enrichment_df['BONFERRONI_CRRECTION_P_VALUE_REJECT'] = bonferroni_correction_info[0]

		##benjamini-hochberg one
		bh_correction_info = sm.stats.multipletests(ignorance_category_pval_sorted_list, alpha=0.05, method='fdr_bh', is_sorted=True)
		# print(bh_correction_info)
		print('Benjamini/Hochberg alphacBonf:', bh_correction_info[-1])
		ignorance_category_enrichment_df['BH_CRRECTION_P_VALUE'] = bh_correction_info[1]
		ignorance_category_enrichment_df['BH_CRRECTION_P_VALUE_REJECT'] = bh_correction_info[0]

		##output the enrichment dataframe
		ignorance_category_enrichment_df.to_csv(
			'%s%s.txt' % (args.output_path, '0_%s_SENTENCE_IGNORANCE_CATEGORY_ENRICHMENT_P_VALUES' % (exposure_name.upper())),
			sep='\t')

	else:
		pass

	print("--- %s seconds ---" % (time.time() - start_time))





