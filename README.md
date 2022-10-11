# Ignorance-Base
The ignorance-base combines biomedical concept classifiers and ignorance classifiers in order to understand the state of our scientific ignorance through two new exploration methods: (1) exploration of the ignorance-base by topic (exploration by topic) and (2) exploration of the ignorance-base by experimental results (exploration by experimental results).

Exploration by topic is called just EXPLORATION in our file system. Exploration by experimental results is called GENE_LIST_ENRICHMENT.

Clone this repository to create the ignorance-base from scratch or add more articles. 

If you do not want to do it from scratch, a full ignorance-base can be found in Ignorance_Network/ALL_DATA_GRAPHS/0_FULL_IGNORANCE_MULTIGRAPH_03_23_22_ALL_SENTENCES_DICT.pkl.zip (you will need to unzip it). There is other supporting information in the file as well.


Our ignorance-base contains 1,643 articles with 91 having gold standard ignorance annotations (prefix GS) and 1,552 run automatically for ignorance identification. All 1,643 articles have automatic classification for the biomedical concepts to ten OBOs from CRAFT.

A lot of our work was run on a supercomputer, FIJI, out of boulder to save time, space, and computing resources. There are two different environments we used and these can be found in Automated_Data_Corpus/Anaconda_Environments_for_FIJI/. Use the general_environment unless you are runnning BioBERT or OpenNMT, then use the other one.



## Automated Data Corpus: The first step to creating the ignorance-base is to automatically run the classifiers over all of your articles in a text format.

0. We are working in the Automated_Data_Corpus/ folder.

1. Place all articles of interest in the Articles/ folder. There are already the 1,552 not gold standard ones there. All articles must be in txt format and have the suffix .nxml.gz.txt

2. Ignorance Classification Process:
	a. 





## All Data Corpus

## Ignorance-Network
