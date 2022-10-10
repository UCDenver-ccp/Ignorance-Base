import os
import argparse
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import ast
import time
import numpy as np
import sent2vec
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from wordcloud import WordCloud
import multidict as multidict
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
# import seaborn as sns


def read_in_pickle_dict(pickle_dict_filepath):
	with open(pickle_dict_filepath, 'rb') as pickle_dict_file:
		pickle_dict = pickle.load(pickle_dict_file)
		return pickle_dict

#TODO

def biosent2vec_model_embeddings(biosent2vec_model_file, preprocessed_sentence_dict):
	##biosent2vec - https://github.com/ncbi-nlp/BioSentVec#biosentvec
	# sent2vec - https://github.com/epfml/sent2vec#sentence-embeddings
	model = sent2vec.Sent2vecModel()
	model.load_model(biosent2vec_model_file)

	biosent2vec_dict = {} #sent num -> embedding
	for sent_num, sent_text in preprocessed_sentence_dict.items():
		sent_embedding = model.embed_sentence(sent_text)
		biosent2vec_dict[sent_num] = sent_embedding
		# print(type(sent_embedding)) #<class 'numpy.ndarray'>
		# raise Exception('hold')

	return biosent2vec_dict


def display_tsne_plot(biosent2vec_dict, output_path):
	biosent2vec_labels = []
	biosent2vec_values = []
	for key, value in biosent2vec_dict.items():
		biosent2vec_labels += [key]
		biosent2vec_values += [value]
	# print()
	biosent2vec_values = np.concatenate(biosent2vec_values, axis=0)

	tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)

	new_values = tsne_model.fit_transform(biosent2vec_values)

	x = []
	y = []
	for value in new_values:
		x.append(value[0])
		y.append(value[1])

	plt.figure(figsize=(16, 16))
	for i in range(len(x)):
		plt.scatter(x[i], y[i])
		plt.annotate(biosent2vec_labels[i],
					 xy=(x[i], y[i]),
					 xytext=(5, 2),
					 textcoords='offset points',
					 ha='right',
					 va='bottom')
	# plt.show()

	plt.savefig('%s%s.pdf' %(output_path, 'vitamin_D_ignorance_cluster_TSNE'))
	plt.close()


def display_pca_plot(biosent2vec_dict, output_path):
	biosent2vec_labels = []
	biosent2vec_values = []
	for key, value in biosent2vec_dict.items():
		biosent2vec_labels += [key]
		biosent2vec_values += [value]
	# print()
	biosent2vec_values = np.concatenate(biosent2vec_values, axis=0)

	pca_model = PCA(n_components=2, random_state=23, svd_solver='full')

	new_values = pca_model.fit_transform(biosent2vec_values)

	x = []
	y = []
	for value in new_values:
		x.append(value[0])
		y.append(value[1])

	plt.figure(figsize=(16, 16))
	for i in range(len(x)):
		plt.scatter(x[i], y[i])
		plt.annotate(biosent2vec_labels[i],
					 xy=(x[i], y[i]),
					 xytext=(5, 2),
					 textcoords='offset points',
					 ha='right',
					 va='bottom')
	# plt.show()

	plt.savefig('%s%s.pdf' %(output_path, 'vitamin_D_ignorance_cluster_PCA'))
	plt.close()

def kmeans_plot(biosent2vec_dict, output_path, num_clusters, ignorance_sentence_dict, preprocessed_sentence_dict):
	biosent2vec_labels = []
	biosent2vec_values = []
	for key, value in biosent2vec_dict.items():
		biosent2vec_labels += [key]
		biosent2vec_values += [value]
	# print()
	biosent2vec_values = np.concatenate(biosent2vec_values, axis=0)

	kmeans = KMeans(n_clusters=num_clusters, random_state=0)
	new_values = kmeans.fit(biosent2vec_values)
	# print(new_values.labels_[:30])
	cluster_assignments = new_values.labels_
	set_clusters = set(cluster_assignments)

	##output the clusters
	ignorance_sentence_df = pd.DataFrame.from_dict(ignorance_sentence_dict, orient='index',
												   columns=['ARTICLE', 'ARTICLE DATE', 'SENTENCE NUM', 'SENTENCE',
															'IGNORANCE CATEGORIES', 'NUM IGNORANCE CATEGORIES',
															'OBO ID (LABEL)'])
	ignorance_sentence_df['CLUSTER'] = None
	ignorance_sentence_df['PREPROCESSED_SENTENCE']= None
	cluster_assignments_dict = {} #sent_num -> cluster
	for i, c in enumerate(cluster_assignments):
		cluster_assignments_dict[biosent2vec_labels[i]] = c
		ignorance_sentence_df['CLUSTER'][biosent2vec_labels[i]] = c
		ignorance_sentence_df['PREPROCESSED_SENTENCE'][biosent2vec_labels[i]] = [preprocessed_sentence_dict[biosent2vec_labels[i]]]



	return ignorance_sentence_df, set_clusters


def hierarchical_clustering(biosent2vec_dict, output_path, num_clusters_list):
	biosent2vec_labels = []
	biosent2vec_values = []
	for key, value in biosent2vec_dict.items():
		biosent2vec_labels += [key]
		biosent2vec_values += [value]
	# print()
	biosent2vec_values = np.concatenate(biosent2vec_values, axis=0)

	#computing full tree
	hierarchical_model_full = AgglomerativeClustering(distance_threshold=0, n_clusters=None, compute_full_tree=True, affinity='euclidean', linkage='complete', compute_distances=True).fit(biosent2vec_values)
	print('number of clusters:', hierarchical_model_full.n_clusters_)
	plt.title("Hierarchical Clustering Dendrogram Full")

	plot_dendrogram(hierarchical_model_full)
	plt.savefig('%s%s.pdf' % (output_path, 'vitamin_D_ignorance_cluster_hierarchical_full'))
	plt.clf()
	# plot the top three levels of the dendrogram
	# plot_dendrogram(hierarchical_model_full, truncate_mode="level", p=3)

	for p in num_clusters_list:
		plot_dendrogram(hierarchical_model_full, truncate_mode='level', p=p)
		plt.xlabel("Number of points in node (or index of point if no parenthesis).")
		# plt.show()
		plt.savefig('%s%s_%s.pdf' %(output_path, 'vitamin_D_ignorance_cluster_hierarchical_full', p))

		plt.clf()

	# # cluster trees
	# for num_clusters in num_clusters_list:
	# 	# print(num_clusters, type(num_clusters))
	# 	hierarchical_model = AgglomerativeClustering(n_clusters=int(num_clusters),
	# 													  affinity='euclidean', linkage='complete',
	# 													  compute_distances=True, compute_full_tree=False, distance_threshold=None).fit(biosent2vec_values)
	# 	print('number of clusters:', hierarchical_model.n_clusters_)
	#
	# 	plt.title("Hierarchical Clustering Dendrogram %s" %(num_clusters))
	# 	# plot the top three levels of the dendrogram
	# 	# plot_dendrogram(hierarchical_model_full, truncate_mode="level", p=3)
	# 	plot_dendrogram(hierarchical_model, truncate_mode='level', p=15)
	# 	plt.xlabel("Number of points in node (or index of point if no parenthesis).")
	# 	# plt.show()
	# 	plt.savefig('%s%s_%s_%s.pdf' % (output_path, 'vitamin_D_ignorance_cluster_hierarchical', num_clusters, 'clusters'))
	#
	# 	plt.clf()



def plot_dendrogram(model, **kwargs):
	# Create linkage matrix and then plot the dendrogram

	# create the counts of samples under each node
	counts = np.zeros(model.children_.shape[0])
	n_samples = len(model.labels_)
	for i, merge in enumerate(model.children_):
		current_count = 0
		for child_idx in merge:
			if child_idx < n_samples:
				current_count += 1  # leaf node
			else:
				current_count += counts[child_idx - n_samples]
		counts[i] = current_count

	linkage_matrix = np.column_stack(
		[model.children_, model.distances_, counts]
	).astype(float)

	# Plot the corresponding dendrogram
	dendrogram(linkage_matrix, **kwargs)




##wordcloud and frequencies: https://amueller.github.io/word_cloud/auto_examples/frequency.html
def getFrequencyDictForText(sentence):
	fullTermsDict = multidict.MultiDict()
	tmpDict = {}

	# making dict for counting frequencies
	for text in sentence.split(" "):
		val = tmpDict.get(text, 0)
		tmpDict[text.lower()] = val + 1
	for key in tmpDict:
		fullTermsDict.add(key, tmpDict[key])
	return fullTermsDict

def cluster_wordclouds(num_clusters, set_clusters, ignorance_sentence_df, specific_obo_id_list, output_path):

	for s in set_clusters:
		df_s = ignorance_sentence_df[ignorance_sentence_df['CLUSTER'] == s]

		##OBO ID CONCEPT INFORMATION
		# print(df_s['OBO ID (LABEL)'])
		obo_id_information_list_all = list(df_s['OBO ID (LABEL)'])

		# print(obo_id_information_list_all)
		obo_id_dict = {} #obo_id to label
		obo_id_occurrence_list = [] #list of all obo_id mentions
		for obo_id_info_list in obo_id_information_list_all:
			for obo_id_info in obo_id_info_list:
				(obo_id, obo_label, obo_start, obo_text) = obo_id_info
				if obo_id in specific_obo_id_list:
					pass
				else:
					if obo_id_dict.get(obo_id.lower()):
						if obo_id_dict[obo_id.lower()] != obo_label:
							raise Exception('ERROR: Issue with different label for the same obo id')
						else:
							obo_id_occurrence_list += [obo_id.lower()]
							pass
					else:
						obo_id_dict[obo_id.lower()] = obo_label
						obo_id_occurrence_list += [obo_id.lower()]

		obo_id_occurrence_sentence = ' '.join(obo_id_occurrence_list)
		fullTermsDict1 = getFrequencyDictForText(obo_id_occurrence_sentence)
		wc1 = WordCloud(background_color="white", max_words=1000)
		wc1.generate_from_frequencies(fullTermsDict1)

		##get the top 10 concepts from the wordcloud
		obo_frequency_dict = wc1.words_  ##seems to be in order of frequency
		with open('%s%s_%s_%s_%s.txt' % (output_path, 'kmeans', num_clusters, 'wordcloud_cluster_obo_concept_frequencies', s),'w+') as obo_freq_file:
			obo_freq_file.write('%s\t%s\t%s\n' % ('OBO_ID', 'OBO_LABEL', 'FREQUENCY'))
			for i, obo in enumerate(obo_frequency_dict.keys()):
				if obo:
					if i < 11:
						freq = obo_frequency_dict[obo]
						obo_freq_file.write('%s\t%s\t%.2f%%\n' % (obo, obo_id_dict[obo], float(freq) * float(100)))
					else:
						break

		# show
		plt.imshow(wc1, interpolation="bilinear")
		plt.axis("off")
		# plt.show()
		plt.savefig('%s%s_%s_%s_%s.pdf' % (output_path, 'kmeans', num_clusters, 'OBO_wordcloud_cluster', s))
		plt.clf()



		# raise Exception('hold')
		##WORD INFORMATION!
		# preprocessed_sentences_list = list(df_s['PREPROCESSED_SENTENCE'])
		# print(preprocessed_sentences_list)
		preprocessed_sentences_list = list(np.concatenate(list(df_s['PREPROCESSED_SENTENCE'])).flat)
		# print(preprocessed_sentences_list)
		# raise Exception('hold')
		preprocessed_sentences = ' '.join(preprocessed_sentences_list)
		fullTermsDict = getFrequencyDictForText(preprocessed_sentences)
		# print(fullTermsDict)
		wc = WordCloud(background_color="white", max_words=1000)
		wc.generate_from_frequencies(fullTermsDict)

		##get the top 10 concepts from the wordcloud
		word_frequency_dict = wc.words_ ##seems to be in order of frequency
		with open('%s%s_%s_%s_%s.txt' %(output_path, 'kmeans', num_clusters, 'wordcloud_cluster_word_frequencies', s), 'w+') as word_freq_file:
			word_freq_file.write('%s\t%s\n' %('WORD', 'FREQUENCY'))
			for i, word in enumerate(word_frequency_dict.keys()):
				if word:
					if i < 11:
						freq = word_frequency_dict[word]
						word_freq_file.write('%s\t%.2f%%\n' %(word, float(freq)*float(100)))
					else:
						break

		# show
		plt.imshow(wc, interpolation="bilinear")
		plt.axis("off")
		# plt.show()
		plt.savefig('%s%s_%s_%s_%s.pdf' %(output_path, 'kmeans', num_clusters, 'wordcloud_cluster', s))
		plt.clf()


def all_article_sentence_count(filename):
	all_article_sentence_count_dict = {} #article -> sentence count
	with open(filename, 'r+') as file:
		next(file)
		for line in file:
			article, sentence_count, word_count = line.strip('\n').split('\t')
			#get rid of .nxml.gz.txt from article
			all_article_sentence_count_dict[article.split('.')[0]] = int(sentence_count)

	return all_article_sentence_count_dict




def create_bubble_plots(ignorance_sentence_dict, not_ignorance_sentence_dict, ignorance_categories, scale, all_article_sentence_count_dict, output_path):

	##raw numbers dataframe: X - article, Y is ignorance category
	column_names = ['ARTICLE', 'ARTICLE_DATE', 'IGNORANCE_CATEGORY', 'BUBBLE_SIZE'] #sort by article date
	raw_bubble_plot_df = pd.DataFrame(columns=column_names, dtype=object)
	not_igorance_row = 'NOT_IGNORANCE'
	# ignorance_categories += [not_igorance_row]

	#loop through the ignorance dictionary and the not ignorance one and add accordingly
	for sent_num in ignorance_sentence_dict.keys():
		article, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info = ignorance_sentence_dict[sent_num]
		sorted_sentence_lc = ast.literal_eval("%s" %(sorted_sentence_lc))
		sentence_lc_set = set([i[0].lower() for i in sorted_sentence_lc]) #all lowercase
		# print(article_date)

		# print(ignorance_sentence_dict[sent_num])
		# raise Exception('hold')
		for ig_cat in sentence_lc_set:
			# print(ig_cat)
			if ig_cat not in ignorance_categories:
				print(ig_cat)
				raise Exception('ERROR: Issue with missing ignorance categories potentially')
			else:
				pass


			if raw_bubble_plot_df.loc[(raw_bubble_plot_df['ARTICLE'] == '%s (%s)' %(article, article_date.split('/')[-1])) & (raw_bubble_plot_df['IGNORANCE_CATEGORY'] == ig_cat)].empty:
				# article_date = datetime.strptime(article_date, '%m/%Y')
				# print('got here')

				raw_bubble_plot_df = raw_bubble_plot_df.append({'ARTICLE': '%s (%s)' %(article, article_date.split('/')[-1]), 'ARTICLE_DATE': article_date, 'IGNORANCE_CATEGORY':ig_cat, 'BUBBLE_SIZE': 1.0}, ignore_index=True)

				# # print(raw_bubble_plot_df)

			else:
				raw_bubble_plot_df.loc[(raw_bubble_plot_df['ARTICLE'] == '%s (%s)' %(article, article_date.split('/')[-1])) & (raw_bubble_plot_df['IGNORANCE_CATEGORY'] == ig_cat), 'BUBBLE_SIZE'] += 1.0


	# loop through the not ignorance dictionary
	for sent_num in not_ignorance_sentence_dict.keys():
		article, article_date, sent_num, sentence_output_text, sorted_sentence_lc, num_lc, sorted_sentence_obo_info = not_ignorance_sentence_dict[sent_num]

		if raw_bubble_plot_df.loc[(raw_bubble_plot_df['ARTICLE'] == '%s (%s)' %(article, article_date.split('/')[-1])) & (raw_bubble_plot_df['IGNORANCE_CATEGORY'] == not_igorance_row)].empty:
			# article_date = datetime.strptime(article_date, '%m/%Y')
			# print('got here')
			raw_bubble_plot_df = raw_bubble_plot_df.append({'ARTICLE': '%s (%s)' %(article, article_date.split('/')[-1]), 'ARTICLE_DATE': article_date, 'IGNORANCE_CATEGORY': not_igorance_row, 'BUBBLE_SIZE': 1.0}, ignore_index=True)
		# print(raw_bubble_plot_df)

		else:
			# print('got here')
			raw_bubble_plot_df.loc[(raw_bubble_plot_df['ARTICLE'] == '%s (%s)' %(article, article_date.split('/')[-1])) & (raw_bubble_plot_df['IGNORANCE_CATEGORY'] == not_igorance_row), 'BUBBLE_SIZE'] += 1.0



	##check if duplicate rows:
	duplicate = raw_bubble_plot_df[raw_bubble_plot_df.duplicated(['ARTICLE', 'IGNORANCE_CATEGORY'])]
	if duplicate.empty:
		pass
	else:
		print(duplicate)
		raise Exception('ERROR: Issue with duplicates via article and ignorance category')

	# print(raw_bubble_plot_df)

	##SORT DF BY DATE and ignorance category custom order
	df_mapping = pd.DataFrame({'ignorance_category_order': ignorance_categories,})
	# print(df_mapping)
	sort_mapping = df_mapping.reset_index().set_index('ignorance_category_order')
	# print(sort_mapping)
	raw_bubble_plot_df['ig_num'] = raw_bubble_plot_df['IGNORANCE_CATEGORY'].map(sort_mapping['index'])

	# print(type(raw_bubble_plot_df.ARTICLE_DATE[0]))
	raw_bubble_plot_df['ARTICLE_DATE'] = pd.to_datetime(raw_bubble_plot_df['ARTICLE_DATE'])
	# print(type(raw_bubble_plot_df.ARTICLE_DATE[0]))

	sorted_raw_bubble_plot_df_all = raw_bubble_plot_df.sort_values(by=['ARTICLE_DATE','ig_num'], ascending=[True, True])
	# sorted_raw_bubble_plot_df_all = raw_bubble_plot_df.sort_values(by=['ARTICLE_DATE', 'IGNORANCE_CATEGORY'],ascending=[True, False])
	# print(sorted_raw_bubble_plot_df_all)



	##output the raw data
	sorted_raw_bubble_plot_df = sorted_raw_bubble_plot_df_all[['ARTICLE', 'ig_num', 'BUBBLE_SIZE']]
	# print(sorted_raw_bubble_plot_df)

	# print(sorted_raw_bubble_plot_df)
	sorted_raw_bubble_plot_df['BUBBLE_SIZE'] *= 10
	scatter0 = plt.scatter(x="ARTICLE", y="ig_num", s="BUBBLE_SIZE", data=sorted_raw_bubble_plot_df)
	plt.grid()
	# plt.xticks(rotation=90)
	scatter0.axes.get_xaxis().set_ticks([])
	plt.yticks([ignorance_categories.index(i) for i in ignorance_categories], ignorance_categories)
	plt.xlabel('Articles (sorted by year: %s - %s)' % (sorted_raw_bubble_plot_df_all.iloc[0]['ARTICLE_DATE'].year, sorted_raw_bubble_plot_df_all.iloc[-1]['ARTICLE_DATE'].year), size=16)
	plt.ylabel('Ignorance Category', size=16)
	plt.title('BUBBLE PLOT (RAW DATA) FOR %s' %(output_path.split('/')[-1]), size=18)
	handles, labels = scatter0.legend_elements(prop="sizes", alpha=1.0)
	legend3 = plt.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5), title="Total (*10)")
	# plt.margins(.1)
	plt.savefig('%s%s.pdf' %(output_path, 'bubble_plot_raw_data'), bbox_inches='tight', pad_inches=1)
	plt.clf()






	##article scale
	if scale.lower() =='article':
		if not all_article_sentence_count_dict:
			raise Exception('ERROR: Issue with needing the all article sentence count information')
		else:
			pass

		##scale by sentences in the article to get percents
		sorted_raw_bubble_plot_df_all['ARTICLE_SCALE_PERCENTS'] = sorted_raw_bubble_plot_df_all.apply(lambda row: row.BUBBLE_SIZE / float(all_article_sentence_count_dict[row.ARTICLE.split(' ')[0]]), axis=1)

		# sorted_raw_bubble_plot_df_all['ARTICLE_SCALE_PERCENTS_SIZE'] = sorted_raw_bubble_plot_df_all.apply(
		# 	lambda row: '0-25%%' if row.BUBBLE_SIZE < 0.26 else '26-50%%' if 0.25 < row.BUBBLE_SIZE < 0.51 else '51-75%%' if 0.51 < row.BUBBLE_SIZE < 0.76 else '76-100%%', axis=1)

		article_scaled_sorted_raw_bubble_plot_df = sorted_raw_bubble_plot_df_all[['ARTICLE', 'ig_num', 'ARTICLE_SCALE_PERCENTS']]#, 'ARTICLE_SCALE_PERCENTS_SIZE']]

		# print(article_scaled_sorted_raw_bubble_plot_df)
		article_scaled_sorted_raw_bubble_plot_df['ARTICLE_SCALE_PERCENTS'] *= 100
		scatter = plt.scatter(x="ARTICLE", y="ig_num", s="ARTICLE_SCALE_PERCENTS", data=article_scaled_sorted_raw_bubble_plot_df)
		plt.grid()
		# plt.xticks(rotation=90)
		scatter.axes.get_xaxis().set_ticks([])
		plt.yticks([ignorance_categories.index(i) for i in ignorance_categories], ignorance_categories)
		plt.xlabel('Articles (sorted by year: %s - %s)' %(sorted_raw_bubble_plot_df_all.iloc[0]['ARTICLE_DATE'].year, sorted_raw_bubble_plot_df_all.iloc[-1]['ARTICLE_DATE'].year), size=16)
		plt.ylabel('Ignorance Category', size=16)
		plt.title('BUBBLE PLOT (ARTICLE SCALED - total sentences) FOR %s' % (output_path.split('/')[-1]), size=18)
		handles, labels = scatter.legend_elements(prop="sizes", alpha=1.0)
		legend2 = plt.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5), title="Percent")

		# plt.margins(.1)
		plt.savefig('%s%s.pdf' % (output_path, 'bubble_plot_article_scaled'), bbox_inches='tight', pad_inches=1)
		plt.clf()




	##ignorance category scale
	elif scale.lower() == 'ignorance_category':
		# print(sorted_raw_bubble_plot_df)
		ignorance_category_sums_df = sorted_raw_bubble_plot_df_all.groupby('IGNORANCE_CATEGORY')['BUBBLE_SIZE'].sum()
		# print(ignorance_category_sums_df)
		sorted_raw_bubble_plot_df_all['IGNORANCE_CATEGORY_SCALE_PERCENTS'] = sorted_raw_bubble_plot_df_all.apply(lambda row: row.BUBBLE_SIZE / ignorance_category_sums_df.loc[row.IGNORANCE_CATEGORY], axis=1)

		ignorance_category_scaled_sorted_raw_bubble_plot_df = sorted_raw_bubble_plot_df_all[['ARTICLE', 'ig_num', 'IGNORANCE_CATEGORY_SCALE_PERCENTS']]

		# print(ignorance_category_scaled_sorted_raw_bubble_plot_df)
		ignorance_category_scaled_sorted_raw_bubble_plot_df['IGNORANCE_CATEGORY_SCALE_PERCENTS'] *= 100
		scatter1 = plt.scatter(x="ARTICLE", y="ig_num", s="IGNORANCE_CATEGORY_SCALE_PERCENTS", data=ignorance_category_scaled_sorted_raw_bubble_plot_df)
		plt.grid()
		# plt.xticks(rotation=90)
		scatter1.axes.get_xaxis().set_ticks([])
		plt.yticks([ignorance_categories.index(i) for i in ignorance_categories], ignorance_categories)
		plt.xlabel('Articles (sorted by year: %s - %s)' % (sorted_raw_bubble_plot_df_all.iloc[0]['ARTICLE_DATE'].year, sorted_raw_bubble_plot_df_all.iloc[-1]['ARTICLE_DATE'].year), size=16)
		plt.ylabel('Ignorance Category', size=16)
		plt.title('BUBBLE PLOT (IGNORANCE CATEGORY SCALED) FOR %s' % (output_path.split('/')[-1]), size=18)
		handles, labels = scatter1.legend_elements(prop="sizes", alpha=1.0)
		legend3 = plt.legend(handles, labels, loc='center left', bbox_to_anchor=(1, 0.5), title="Percent")
		# plt.margins(.1)
		plt.savefig('%s%s.pdf' % (output_path, 'bubble_plot_ignorance_category_scaled'), bbox_inches='tight', pad_inches=1)
		plt.clf()



	else:
		raise Exception('ERROR: Must put in the scale options: article or ignorance_category or add more options to code')

	# print(sorted_raw_bubble_plot_df_all)
	# raise Exception('hold')

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-processed_sentences', type=str, help='the file path to the ignorance preprocessed sentence .pkl file or folder path ending in /')
	parser.add_argument('--processed_sentences_ext', type=str, help='the extension for the files if given a folder for processed sentences, default None', default=None)
	parser.add_argument('-not_processed_sentences', type=str,
						help='the file path to the not ignorance preprocessed sentence .pkl file or folder path ending in /')
	parser.add_argument('--not_processed_sentences_ext', type=str,
						help='the extension for the files if given a folder for not processed sentences, default None',
						default=None)
	parser.add_argument('-biosent2vec_model_file', type=str, help='the file path to the biosent2vec model file')
	parser.add_argument('-kmeans_num_clusters', type=str, help='a string of a list of numbers for clustering delimited by , with no spaces')
	parser.add_argument('-ignorance_sentence_dict_file', type=str, help='the file path to the ignorance sentence dict pkl file')
	parser.add_argument('--ignorance_sentence_dict_file_ext', type=str, help='the extension for the files if given a folder for ignorance_sentence_dict_file, default None', default=None)
	parser.add_argument('-not_ignorance_sentence_dict_file', type=str, help='the file path to the not ignorance sentence dict pkl file')
	parser.add_argument('--not_ignorance_sentence_dict_file_ext', type=str,
						help='the extension for the files if given a folder for not_ignorance_sentence_dict_file, default None',
						default=None)
	parser.add_argument('-all_article_summary_file_path', type=str, help='the file path to the all article file summary with sentence counts by article')
	parser.add_argument('--obo_id_list', type=str, help='the obo ids used to gather these sentences delimited with , no spaces, default None', default=None)
	parser.add_argument('-ignorance_categories', type=str, help='a list of ignorance categories delimited with , no spaces')
	parser.add_argument('-output_path', type=str, help='the output file path for the results')
	args = parser.parse_args()



	start_time = time.time()
	if args.ignorance_categories.lower() == 'no_ignorance':
		ignorance_categories = []
	else:
		ignorance_categories = args.ignorance_categories.lower().split(',')
		not_igorance_row = 'NOT_IGNORANCE'
		ignorance_categories += [not_igorance_row]


	if args.obo_id_list and args.obo_id_list.lower() != 'none' and args.obo_id_list.lower() != 'false':
		obo_id_list = args.obo_id_list.split(',')
	else:
		obo_id_list = []



	##read in the pickle dict file
	if str(args.processed_sentences).endswith('.pkl') and str(args.ignorance_sentence_dict_file).endswith('.pkl'):
		sentence_files_dict = {'': [args.processed_sentences, args.ignorance_sentence_dict_file]}

		# processed_sentences_files_list = [args.processed_sentences]
		# ignorance_sentence_dict_file_list = [args.ignorance_sentence_dict_file]
	elif str(args.processed_sentences).endswith('/') and str(args.ignorance_sentence_dict_file).endswith('/'):
		sentence_files_dict = {} #obo_id to files
		##ignorance and preprocessed in the same folder based on workflow
		for root, directories, filenames in os.walk(args.processed_sentences):
			for filename in sorted(filenames):
				if filename.endswith(args.processed_sentences_ext) and 'NOT' not in filename:
					obo_id = filename.split('_%s' %(args.processed_sentences_ext))[0]
					# print(obo_id)
					if sentence_files_dict.get(obo_id):
						sentence_files_dict[obo_id][0] = args.processed_sentences + filename
					else:
						sentence_files_dict[obo_id] = [args.processed_sentences + filename, '']
				elif filename.endswith(args.ignorance_sentence_dict_file_ext) and 'NOT' not in filename:
					obo_id = filename.split('_%s' %(args.ignorance_sentence_dict_file_ext))[0]
					# print(obo_id)
					if sentence_files_dict.get(obo_id):
						sentence_files_dict[obo_id][1] = args.ignorance_sentence_dict_file + filename
					else:
						sentence_files_dict[obo_id] = ['', args.ignorance_sentence_dict_file + filename]
				else:
					pass
	else:
		raise Exception('ERROR: either provide single files for processed_sentences and ignorance_sentence_dict_file or both need to be folders with ext information')

	##read in the pickle dict file
	if str(args.not_processed_sentences).endswith('.pkl') and str(args.not_ignorance_sentence_dict_file).endswith('.pkl'):
		not_sentence_files_dict = {'': [args.not_processed_sentences, args.not_ignorance_sentence_dict_file]}

	# processed_sentences_files_list = [args.processed_sentences]
	# ignorance_sentence_dict_file_list = [args.ignorance_sentence_dict_file]
	elif str(args.not_processed_sentences).endswith('/') and str(args.not_ignorance_sentence_dict_file).endswith('/'):
		not_sentence_files_dict = {}  # obo_id to files
		##ignorance and preprocessed in the same folder based on workflow
		for root, directories, filenames in os.walk(args.not_processed_sentences):
			for filename in sorted(filenames):
				if filename.endswith(args.not_processed_sentences_ext):
					obo_id = filename.split('_%s' % (args.not_processed_sentences_ext))[0]
					# print(obo_id)
					if not_sentence_files_dict.get(obo_id):
						not_sentence_files_dict[obo_id][0] = args.not_processed_sentences + filename
					else:
						not_sentence_files_dict[obo_id] = [args.not_processed_sentences + filename, '']
				elif filename.endswith(args.not_ignorance_sentence_dict_file_ext):
					obo_id = filename.split('_%s' % (args.not_ignorance_sentence_dict_file_ext))[0]
					# print(obo_id)
					if not_sentence_files_dict.get(obo_id):
						not_sentence_files_dict[obo_id][1] = args.not_ignorance_sentence_dict_file + filename
					else:
						not_sentence_files_dict[obo_id] = ['', args.not_ignorance_sentence_dict_file + filename]
				else:
					pass
	else:
		raise Exception(
			'ERROR: either provide single files for not processed_sentences and not ignorance_sentence_dict_file or both need to be folders with ext information')





	##TODO!!
	# # print(sentence_files_dict.keys())
	for obo_id in sentence_files_dict.keys():

		print(obo_id)
		preprocessed_sentence_dict_file, ignorance_sentence_dict_file = sentence_files_dict[obo_id]
		preprocessed_sentence_dict = read_in_pickle_dict(preprocessed_sentence_dict_file) #sentence_num -> preprocessed sentence text
		print(len(preprocessed_sentence_dict.keys())) ###8688 sentences
		ignorance_sentence_dict = read_in_pickle_dict(ignorance_sentence_dict_file)
	#
		##assign output information
		if obo_id:
			output_path = args.output_path + obo_id + '_'
			specific_obo_id_list = obo_id_list + [obo_id]

		else:
			output_path = args.output_path
			specific_obo_id_list = obo_id_list

		if ignorance_categories:
			pass
		else:
			output_path = '%s%s_' %(output_path, 'no_ignorance')

		##not information also
		if args.not_ignorance_sentence_dict_file:
			not_preprocessed_sentence_dict_file, not_ignorance_sentence_dict_file = not_sentence_files_dict[obo_id] ##TODO: this could error?!
			not_preprocessed_sentence_dict = read_in_pickle_dict(not_preprocessed_sentence_dict_file)  # sentence_num -> preprocessed sentence text
			# print(len(not_preprocessed_sentence_dict.keys()))  ###8688 sentences
			not_ignorance_sentence_dict = read_in_pickle_dict(not_ignorance_sentence_dict_file)


			if ignorance_categories:
				##bubble plots only if we have both pieces of info

				##bubble plot scaled by article
				#get all article summary - dict from article to sentence count
				all_article_sentence_count_dict = all_article_sentence_count(args.all_article_summary_file_path)

				create_bubble_plots(ignorance_sentence_dict, not_ignorance_sentence_dict, ignorance_categories, 'article', all_article_sentence_count_dict, output_path)

				##bubble plot scaled by category
				create_bubble_plots(ignorance_sentence_dict, not_ignorance_sentence_dict, ignorance_categories, 'ignorance_category', None, output_path)

			##TODO: combine ignorance and not and preprocessed and not
			else:
				##merge the two dictionaries
				if set(ignorance_sentence_dict.keys()).intersection(set(not_ignorance_sentence_dict.keys())):
					print(set(ignorance_sentence_dict.keys()).intersection(set(not_ignorance_sentence_dict.keys())))
					raise Exception('ERROR: Issue with overlapping sets for ignorance and not!')
				else:
					pass

				if set(preprocessed_sentence_dict.keys()).intersection(set(not_preprocessed_sentence_dict.keys())):
					print(set(preprocessed_sentence_dict.keys()).intersection(set(not_preprocessed_sentence_dict.keys())))
					raise Exception('ERROR: Issue with overlapping sets for ignorance preprocessed and not!')
				else:
					pass


				ignorance_sentence_dict.update(not_ignorance_sentence_dict)
				preprocessed_sentence_dict.update(not_preprocessed_sentence_dict)


		else:
			pass

		# raise Exception('hold')

		##TODO: ALL THE OTHER VISUALIZATIONS
		# ##biosent2vec embedding dictionary
		biosent2vec_dict = biosent2vec_model_embeddings(args.biosent2vec_model_file, preprocessed_sentence_dict)

		if len(biosent2vec_dict.keys()) != len(preprocessed_sentence_dict.keys()):
			print(len(biosent2vec_dict.keys()), len(preprocessed_sentence_dict.keys()))
			raise Exception('ERROR: Issue with creating embeddings for each preprocessed sentence')
		else:
			pass
		#

		#
		#plot the embeddings using TSNE
		display_tsne_plot(biosent2vec_dict, output_path)

		#plot the embeddings with PCA
		display_pca_plot(biosent2vec_dict, output_path)
		#
		##kmeans
		kmeans_num_clusters = args.kmeans_num_clusters.split(',')
		for n in kmeans_num_clusters:
			ignorance_sentence_df, set_clusters = kmeans_plot(biosent2vec_dict, output_path, int(n), ignorance_sentence_dict, preprocessed_sentence_dict)

			ignorance_sentence_df.to_csv('%s%s_%s.txt' %(output_path,'IGNORANCE_SENTENCE_CLUSTERS_KMEANS', n), sep='\t')

			##TODO: add frequency output of words to be able to provide list of key terms per cluster
			# print('word cloud')
			##get the top 10 concepts from the wordcloud
			if args.ignorance_categories.lower() == 'no_ignorance':
				specific_obo_id_list = [o.replace('no_ignorance_', '') for o in specific_obo_id_list]
			else:
				pass

			cluster_wordclouds(n, set_clusters, ignorance_sentence_df, specific_obo_id_list, output_path)
		#
		#
		#
		#
		##hierarchical clustering
		int_kmeans_num_clusters = [int(k) for k in kmeans_num_clusters]
		hierarchical_clustering(biosent2vec_dict, output_path, int_kmeans_num_clusters)

	print("--- %s seconds ---" % (time.time() - start_time))
