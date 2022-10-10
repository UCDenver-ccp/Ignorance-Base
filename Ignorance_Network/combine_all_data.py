import os
import nltk
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import pickle
import ast



def collect_all_lcs(all_lcs_path):
    all_lcs_dict = {}  # lc -> [ignorance_type]
    all_ignorance_types = []
    # if excluded_ignorance_types:
    # print('PROGRESS: excluded files include ', excluded_ignorance_types)


    ##get rid of the it to exclude using regex
    # create all_lcs_dict: lc -> [regex, ignorance_type]
    with open('%s' % all_lcs_path, 'r') as all_lcs_file:
        next(all_lcs_file)
        for line in all_lcs_file:
            lc, regex, it = line.strip('\n').split('\t')
            all_ignorance_types += [it]
            if all_lcs_dict.get(lc):
                print('multiple ignorance types for lexical cue', lc, it)
                all_lcs_dict[lc] += [it]

            else:
                all_lcs_dict[lc] = [it]
    # print('PROGRESS: all ignorance types include:', set(all_ignorance_types))

    ##add ontology concepts that were changed or updated previously
    # if corpus.upper == 'IGNORANCE':
    all_lcs_dict['urgent_call_to_action'] = [
        'IMPORTANT_CONSIDERATION']  # switched name of urgent_call_to_action category to important consideration
    all_lcs_dict['than'] = ['ALTERNATIVE_OPTIONS_CONTROVERSY']  # from ontology of ignorance 2/11/20
    all_lcs_dict['alternative_options'] = [
        'ALTERNATIVE_OPTIONS_CONTROVERSY']  # combined alternative_options and controversy category together
    all_lcs_dict['is'] = ['EXPLICIT_QUESTION']  # TODO: we got rid of this and I don't love this!
    all_lcs_dict['epistemics'] = ['EPISTEMICS']  # the broadest category - empty annotations

    return all_lcs_dict, list(set(all_ignorance_types))



def collect_all_unique_OBOs(unique_obos_path, ontologies):
    unique_OBO_dict = {} #obo_id.lower() -> OBO
    for ont in ontologies:
        with open('%s%s_%s' %(unique_obos_path, ont, 'unique_ids.txt'), 'r+') as unique_obo_file:
            next(unique_obo_file)
            next(unique_obo_file)
            file_start = False
            for line in unique_obo_file:
                if line.startswith('UNIQUE OBO IDS'):
                    file_start = True
                    continue
                elif file_start:
                    obo_id = line.strip('\n')
                    if unique_OBO_dict.get(obo_id):
                        print(obo_id)
                        print(unique_OBO_dict[obo_id])
                        print(ont)
                        raise Exception('ERROR: Issue with unique obo ids not being unique')
                    else:
                        unique_OBO_dict['%s_%s' %(ont, obo_id)] = ont
                else:
                    raise Exception('ERROR: Issue with finding the beginning of the unique id files!')

    return unique_OBO_dict







def collect_sentence_data(sentence_file_path, included_articles):
    article_dicts = {} # article -> (sentence_dict, mention_ID_dict)


    for root, directories, filenames in os.walk(sentence_file_path):
        for filename in sorted(filenames):
            if filename.endswith('sentence_info.txt') and (included_articles.lower() == 'all' or filename.split('.nxml.gz')[0] in included_articles):
                with open(sentence_file_path+filename,'r+') as sentence_file:
                    next(sentence_file)
                    sentence_dict = {} #dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)
                    for line in sentence_file:
                        pmc_nxml_gz, sent_num, sent_text_list, sent_span = line.strip('\n').split('\t')
                        sent_span_list = [int(a) for a in ast.literal_eval(sent_span)]
                        sent_text_list = ast.literal_eval(sent_text_list)
                        sentence_dict['%s_%s' %(filename.split('.nxml')[0], sent_num)] = [[sent_span_list[0]], [sent_span_list[1]], sent_text_list, '%s_%s' %(filename.split('.nxml')[0], sent_num), None, sent_num] #change class label to subject_scope once we know that it is a statement of ignorance meaning it has lexical cues!

                    ##set the sentence dict with the article dict
                    article_dicts[filename.split('.nxml.gz')[0]] = [sentence_dict, None]
                    # print(len(sentence_dict))

    return article_dicts



def collect_bionlp_annotations(bionlp_file_path, included_articles, all_lcs_dict, all_ignorance_types, article_dicts, obos):
    # article_dicts = {}  # article -> (subject_scope_dict, mention_ID_dict)
    for root, directories, filenames in os.walk(bionlp_file_path):
        for filename in sorted(filenames):
            print(filename)
            if filename.endswith('.bionlp') and (included_articles.lower() == 'all' or filename.split('.bionlp')[0].replace('BEST_', '').replace('GS_','') in included_articles):
                ##bionlp file to parse through
                # print(filename)

                ##find the
                with open(bionlp_file_path+filename, 'r') as bionlp_file:

                    mention_ID_dict = {}  # dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)

                    ##loop over all bionlp files for annotation information
                    for line in bionlp_file:
                        # print(line)
                        line_info = line.strip('\n').split('\t')
                        t_num = line_info[0]
                        text = line_info[2].rstrip('...').lstrip('...').rstrip(' ').lstrip(' ')
                        if text.startswith('...') or text.endswith('...'):
                            raise Exception('ERROR: Issue with preprocessing text to get rid of starting and trailing ...')
                        else:
                            pass

                        start_list = []
                        end_list = []
                        if ';' in line_info[1]:
                            indices_list = []
                            disc_info = line_info[1].split(';')
                            for j, d in enumerate(disc_info):
                                if j == 0:
                                    ignorance_category, s1, e1 = d.split(' ')
                                    # indices1 = (s1,e1)
                                    indices_list += [(int(s1), int(e1))]
                                    start_list += [int(s1)]
                                    end_list += [int(e1)]

                                else:
                                    # print(d)
                                    if d:
                                        s, e = d.split(' ')
                                        indices_list += [(int(s), int(e))]
                                        start_list += [int(s)]
                                        end_list += [int(e)]
                                    else:
                                        pass

                        else:
                            ignorance_category, text_start, text_end = line_info[1].split(' ')
                            indices_list = [(int(text_start), int(text_end))]
                            start_list += [int(text_start)]
                            end_list += [int(text_end)]


                        if obos:
                            ont_lc = ignorance_category
                            ignorance_category = None
                            for obo in all_ignorance_types:
                                if all_lcs_dict.get('%s_%s' %(obo, ont_lc)):
                                    ignorance_category = all_lcs_dict['%s_%s' %(obo, ont_lc)]
                                    break
                                else:
                                    pass
                            if ignorance_category == None:
                                raise Exception('ERROR: did not find the correct obo category for the obo_id')
                            else:
                                pass

                        else:
                            # print(text.lower().replace(' ... ', '...').replace(' ', '_'))
                            ##lexical cue in the all_lcs_dict (taxonomy)
                            # if 'PMC2022638' in filename and text.lower() == 'future work':
                            #     print(text, all_lcs_dict.get(text.lower().replace(' ... ', '...').replace(' ', '_')))
                            #     print(ignorance_category)
                            #     raise Exception('hold')
                            possible_lc = text.lower().replace(' ... ', '...').replace(' ', '_')
                            # if possible_lc.startswith('...'):
                            #     print(text)
                            #     print(possible_lc)
                            #     raise Exception('ERROR: Issue with ')
                            # elif possible_lc.endswith('...'):
                            #     print(text)
                            #     print(possible_lc)
                            #     raise Exception('hold - end')
                            if all_lcs_dict.get(possible_lc):

                                ##canonical ignorance category so we take the lexical cue
                                if ignorance_category.lower() == all_lcs_dict[possible_lc][0].lower():
                                    ont_lc = possible_lc
                                ##non-canonical ignorance category so we take the canonical ignorance category
                                else:
                                    ont_lc = all_lcs_dict[possible_lc][0].lower()
                                    # print(ont_lc)
                                    # raise Exception('hold1')
                            elif all_lcs_dict.get('0_%s' %(possible_lc)):
                                if ignorance_category.lower() == all_lcs_dict['0_%s' %(possible_lc)][0].lower():
                                    ont_lc = '%s' %(possible_lc)
                                else:
                                    ont_lc = all_lcs_dict['0_%s' %(possible_lc)][0]
                                    # print(ont_lc)
                                    # raise Exception('hold2')

                            elif possible_lc in all_ignorance_types:
                                ont_lc = possible_lc
                            else:
                                ont_lc = ignorance_category.lower()
                            # print(ont_lc)
                            # raise Exception('hold')

                        if mention_ID_dict.get('%s_%s' %(filename.split('.bionlp')[0].replace('BEST_', '').replace('GS_',''), t_num)):
                            print(filename.split('.bionlp')[0].replace('BEST_', '').replace('GS_',''), t_num)
                            print(mention_ID_dict['%s_%s' %(filename.split('.bionlp')[0].replace('BEST_', '').replace('GS_',''), t_num)])
                            raise Exception('ERROR: Issue with duplicate mention ID number for ignorance bionlp files')
                        else:
                            pass

                        mention_ID_dict['%s_%s' %(filename.split('.bionlp')[0].replace('BEST_', '').replace('GS_',''), t_num)] = [start_list, end_list, text, ont_lc, ignorance_category, None]
                        # print(mention_ID_dict['%s_%s' %(filename.split('.bionlp')[0].replace('BEST_', '').replace('GS_',''), t_num)])



                    ##article -> (subject_scope_dict, mention_ID_dict)
                    # print(len(mention_ID_dict))
                    if article_dicts.get(filename.split('.bionlp')[0].replace('BEST_', '').replace('GS_','')):
                        article_dicts[filename.split('.bionlp')[0].replace('BEST_', '').replace('GS_','')][1] = mention_ID_dict
                    else:
                        raise Exception('ERROR: Issue with missing article file - most likely a naming problem!')

    return article_dicts


def combine_scopes_and_mentions(article, subject_scope_dict, mention_ID_dict, sentence_output_folder):
    ## mention_ID_dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)
    ## subject_scope_dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)

    ##sort subject_scope_dict by start indices
    sorted_subject_tuples = sorted(subject_scope_dict.items(), key=lambda item: item[1])
    # print(sorted_subject_tuples)
    sorted_subject_scope_dict = {k: v for k, v in sorted_subject_tuples}
    # print(sorted_subject_scope_dict)

    ##sort mention_ID_dict by start indices
    sorted_mentions_tuples = sorted(mention_ID_dict.items(), key=lambda item: item[1])
    # print(sorted_subject_tuples)
    sorted_mention_ID_dict = {k: v for k, v in sorted_mentions_tuples}
    # print(sorted_mention_ID_dict)


    ##dictionary from subject_scope_ID -> [list of mention_IDs in it]
    subject_scope_to_mention_ID_dict = {} #dict from subject_scope_ID -> [list of mention_IDs in it]
    # print(sorted_mention_ID_dict)
    for i, (subject_scope_ID, subject_scope_value) in enumerate(sorted_subject_scope_dict.items()):
        list_mention_IDs = []

        # print(subject_scope_ID, subject_scope_value)
        subject_min_start = min(subject_scope_value[0])
        subject_max_end = max(subject_scope_value[1])
        # print(subject_min_start, subject_max_end)
        for mention_ID, mention_value in sorted_mention_ID_dict.items():
            mention_min_start = min(mention_value[0])
            mention_max_end = max(mention_value[1])

            if subject_min_start <= mention_min_start and mention_max_end <= subject_max_end:
                list_mention_IDs += [mention_ID]
                print(mention_ID)


            else:
                ##we are out of bounds so break!
                # if list_mention_IDs:
                #     subject_scope_to_mention_ID_dict[subject_scope_ID] = list_mention_IDs
                #     for m in list_mention_IDs:
                #         ##pop off the mention ID to have less to iterate through
                #         del sorted_mention_ID_dict[m]
                #         ##update the mention_ID_dict to inlcude the subject_scope_ID it goes to
                #         mention_ID_dict[m][5] = subject_scope_ID


                break
                ##check that all subject scopes have concept mentions!
                # else:
                #     # print(subject_scope_ID, subject_scope_value)
                #     # print(mention_ID_dict)
                #     print(sorted_mention_ID_dict)
                #     raise Exception('ERROR: Issue with a subject scope with no concept mentions!')


        ##the last one doesn't get captured because it won't go to the else statement
        # if i == len(sorted_subject_scope_dict) - 1:
        subject_scope_to_mention_ID_dict[subject_scope_ID] = list_mention_IDs



        if list_mention_IDs:
            ##assign the sentence to a subject scope since it has lexical cues!
            if subject_scope_dict[subject_scope_ID][-2]:
                raise Exception('ERROR: Issue that this always should be none since we do not know the class label')
            else:
                subject_scope_dict[subject_scope_ID][-2] = 'subject_scope'

            ##assign the correct id to the concepts!
            for m in list_mention_IDs:
                del sorted_mention_ID_dict[m]
                mention_ID_dict[m][5] = subject_scope_ID

        ##no concepts in the sentence!
        else:
            print('NO CONCEPT MATCHES!')
            print(subject_scope_ID, subject_scope_value)
            pass
            # print(mention_ID_dict)
            # print(sorted_mention_ID_dict)
            # raise Exception('ERROR: Issue with a subject scope with no concept mentions!')


    ##check that all concept mentions have a subject scope!
    if len(sorted_mention_ID_dict) != 0:
        print(sorted_mention_ID_dict)
        raise Exception('ERROR: Issue with not all concept mentions having a subject scope!')
    else:
        pass

    ##check that all concept mentions are assigned a subject_scope_ID
    for m in mention_ID_dict:
        if mention_ID_dict[m][5] is None:
            print(mention_ID_dict[m])
            raise Exception('ERROR: Issue with assigning all subject_scope_IDs to concept mentions!')
        else:
            pass

    # print(subject_scope_to_mention_ID_dict)
    # print(mention_ID_dict)


    return subject_scope_to_mention_ID_dict, mention_ID_dict, subject_scope_dict


def output_by_pmcid(article, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, output_folder):
    sorted_subject_tuples = sorted(subject_scope_dict.items(), key=lambda item: item[1])
    # print(sorted_subject_tuples)
    sorted_subject_scope_dict = {k: v for k, v in sorted_subject_tuples}
    # print(sorted_subject_scope_dict)

    ##sort mention_ID_dict by start indices
    sorted_mentions_tuples = sorted(mention_ID_dict.items(), key=lambda item: item[1])
    # print(sorted_subject_tuples)
    sorted_mention_ID_dict = {k: v for k, v in sorted_mentions_tuples}
    # print(sorted_mention_ID_dict)

    with open('%s%s_all_combined_data.txt' %(output_folder, article), 'w+') as article_all_data_file:
        article_all_data_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
        'PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'IGNORANCE TYPE', 'C_START', 'C_END',
        'CONCEPT_MENTION_ID'))
        for subject_scope_ID, subject_scope_info in sorted_subject_scope_dict.items():
            for i, mention_ID in enumerate(subject_scope_to_mention_ID_dict[subject_scope_ID]):
                mention_info = sorted_mention_ID_dict[mention_ID]
                ignorance_type = mention_info[4].upper()
                ##'PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'C_START', 'C_END', 'CONCEPT_MENTION_ID'
                article_all_data_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (article, subject_scope_ID, subject_scope_info[0], subject_scope_info[1], subject_scope_info[2], mention_info[2], ignorance_type, mention_info[0], mention_info[1], mention_ID))



def sort_by_ontology(article, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, it_output_dict):
    ###dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)
    for subject_scope_ID, subject_scope_info in subject_scope_dict.items():
        for i, mention_ID in enumerate(subject_scope_to_mention_ID_dict[subject_scope_ID]):
            mention_info = mention_ID_dict[mention_ID]
            ignorance_type = mention_info[4]
            ##get file to output data to:
            it_output_file = it_output_dict[ignorance_type.upper()]
            ##'PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'C_START', 'C_END', 'CONCEPT_MENTION_ID'
            # if i == 0:
            it_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(article, subject_scope_ID, subject_scope_info[0], subject_scope_info[1], subject_scope_info[2], mention_info[2], mention_info[0], mention_info[1], mention_ID))
            # else:
            #     it_output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
            #     '', '', '', '', '', mention_info[2], mention_info[0], mention_info[1], mention_ID))


def output_count_ignorance_type(ignorance_type_occurence_list, it_count, article, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, it_occurence_output_dict):
    ##TODO: issue with only taking the first concept that appears in it. potentially missing other concepts because we list the sentence each time there is a concept.

    sorted_subject_tuples = sorted(subject_scope_dict.items(), key=lambda item: item[1])
    # print(sorted_subject_tuples)
    sorted_subject_scope_dict = {k: v for k, v in sorted_subject_tuples}
    # print(sorted_subject_scope_dict)

    ##sort mention_ID_dict by start indices
    sorted_mentions_tuples = sorted(mention_ID_dict.items(), key=lambda item: item[1])
    # print(sorted_subject_tuples)
    sorted_mention_ID_dict = {k: v for k, v in sorted_mentions_tuples}
    # print(sorted_mention_ID_dict)

    current_it_count = []
    for it in ignorance_type_occurence_list:
        current_it_count += [0]

    for subject_scope_ID, subject_scope_info in sorted_subject_scope_dict.items():
        for i, mention_ID in enumerate(subject_scope_to_mention_ID_dict[subject_scope_ID]):
            mention_info = sorted_mention_ID_dict[mention_ID]
            ignorance_type = mention_info[4].upper()
            ##'PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'C_START', 'C_END', 'CONCEPT_MENTION_ID'
            if ignorance_type.lower() in ignorance_type_occurence_list and current_it_count[ignorance_type_occurence_list.index(ignorance_type.lower())] < it_count:
                it_occurence_file = it_occurence_output_dict[ignorance_type.upper()]
                it_occurence_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (article, subject_scope_ID, subject_scope_info[0], subject_scope_info[1], subject_scope_info[2],mention_info[2], ignorance_type, mention_info[0], mention_info[1], mention_ID))

                current_it_count[ignorance_type_occurence_list.index(ignorance_type.lower())] += 1

                # raise Exception('hold')


            else:
                pass



def get_article_dates(articles, meta_data_article_file_path, output_path):
    with open('%sPMCID_date_info.txt' %(output_path), 'w+') as output_file:
        output_file.write('%s\t%s\n' %('PMCID', 'DATE (MM/YYYY)'))

        for article in articles:
            with open('%s%s.nxml.gz.txt.gz.meta' %(meta_data_article_file_path, article), 'r+') as meta_data_file:
                for line in meta_data_file:
                    if line.startswith('YEAR_PUBLISHED'):
                        year = int(line.replace('\n', '').split('=')[-1])
                    elif line.startswith('MONTH_PUBLISHED'):
                        month = line.replace('\n', '').split('=')[-1]
                        if len(month) == 1:
                            month = int('%s%s'%('0', month))
                    else:
                        pass
                output_file.write('%s\t%s/%s\n' %(article, month, year))







if __name__=='__main__':
    # ##gold standard annotions v1 path
    # gold_standard_annotation_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Annotations/'
    #
    # current_ignorance_types = ['ALTERNATIVE_OPTIONS_CONTROVERSY', 'ANOMALY_CURIOUS_FINDING', 'DIFFICULT_TASK', 'EXPLICIT_QUESTION', 'FULL_UNKNOWN', 'FUTURE_PREDICTION', 'FUTURE_WORK', 'IMPORTANT_CONSIDERATION', 'INCOMPLETE_EVIDENCE', 'PROBABLE_UNDERSTANDING', 'PROBLEM_COMPLICATION', 'QUESTION_ANSWERED_BY_THIS_WORK', 'SUPERFICIAL_RELATIONSHIP']
    #
    # ignorance_type_first_list = ['QUESTION_ANSWERED_BY_THIS_WORK']
    # it_count = 1 #first occurrence
    #
    #
    # ##gold standard v1 with training updated
    # articles = ['PMC1247630','PMC1474522','PMC1533075','PMC1626394','PMC2009866','PMC2265032','PMC2396486','PMC2516588','PMC2672462','PMC2874300','PMC2885310','PMC2889879','PMC2898025','PMC2999828','PMC3205727','PMC3272870','PMC3279448','PMC3313761','PMC3342123','PMC3348565','PMC3373750','PMC3400371','PMC3427250','PMC3513049','PMC3679768','PMC3800883','PMC3914197','PMC3915248','PMC3933411','PMC4122855','PMC4304064','PMC4311629','PMC4352710','PMC4377896','PMC4428817','PMC4500436','PMC4564405','PMC4653409','PMC4653418','PMC4683322','PMC4859539','PMC4897523','PMC4954778','PMC4992225','PMC5030620','PMC5143410','PMC5187359','PMC5273824','PMC5501061','PMC5540678','PMC5685050','PMC5812027','PMC6000839','PMC6011374','PMC6022422','PMC6029118','PMC6033232','PMC6039335','PMC6054603','PMC6056931']
    #
    # all_lcs_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Ontologies/Ontology_Of_Ignorance_all_cues_2020-08-25.txt'
    #
    # output_folder = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/3_Ignorance_Base/Ignorance-Base/Output_Folders/'
    # sentence_folder = 'PMCID_Sentence_Files/'
    #
    # sentence_output_folder = output_folder + sentence_folder
    #
    # all_combined_data = '0_all_combined'
    #
    # dictionary_folder = 'dictionary_files/'
    #
    # dictionary_output_folder = output_folder + dictionary_folder
    #
    # meta_data_article_file_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/1_First_Full_Annotation_Task_9_13_19/document_collection_pre_natal/' #PMC6011374.nxml.gz.txt.gz.meta

    parser = argparse.ArgumentParser()

    parser.add_argument('-all_lcs_path', type=str, help='the file path to the current lexical cue list')
    parser.add_argument('-included_articles', type=str, help='list of all articles delimited with , with no spaces or defaults to all', default='all')
    parser.add_argument('-ignorance_ontologies', type=str, help='a list of all the ignorance ontologies delimited with , no spaces')
    parser.add_argument('-sentence_file_path', type=str, help='the file path to the pmcid sentence files')
    parser.add_argument('-bionlp_file_path', type=str, help='file path to the ignorance bionlp files')
    parser.add_argument('-sentence_output_folder', type=str, help='path to sentence output folder')
    parser.add_argument('-all_combined_data', type=str, help='a file within the sentences for all the combined sentence data output')
    parser.add_argument('-dictionary_output_folder', type=str, help='path to dictionary  output folder')
    parser.add_argument('-it_occurence_count', type=int, help='an integer that defines the number of occurences you want to explore for each ignorance type, default is 1', default=1)
    parser.add_argument('-output_folder', type=str, help='the file path to the general output folder')
    parser.add_argument('-meta_data_article_file_path', type=str, help='file path to the article metadata for the all corpus data')
    parser.add_argument('--obo_ontologies', type=str, help='a list of the obo ontologies delimited with a , no spaces - optional')
    parser.add_argument('--unique_obos_path', type=str, help='the file path to the unique obo files')
    args = parser.parse_args()



    ##collect all lcs:
    all_lcs_dict, all_taxonomy_ignorance_types = collect_all_lcs(args.all_lcs_path)
    # print(all_ignorance_types) ##all upper case


    ##COLLECT ALL THE ARTICLE IGNORANCE ANNOTATION INFORMATION
    if args.included_articles.lower() == 'all':
        included_articles = 'all'
    else:
        included_articles = args.included_articles.split(',')

    article_dicts = collect_sentence_data(args.sentence_file_path, included_articles)


    if args.obo_ontologies:
        # print('got here')
        current_ignorance_types = args.obo_ontologies.split(',')
        print(current_ignorance_types)
        unique_OBO_dict = collect_all_unique_OBOs(args.unique_obos_path, current_ignorance_types)
        article_dicts = collect_bionlp_annotations(args.bionlp_file_path, included_articles, unique_OBO_dict, current_ignorance_types, article_dicts, True)
        # raise Exception('hold')
    else:
        current_ignorance_types = args.ignorance_ontologies.split(',')
        article_dicts = collect_bionlp_annotations(args.bionlp_file_path, included_articles, all_lcs_dict, current_ignorance_types, article_dicts, False)
        print(len(article_dicts))




    ##setup ontology separating files for all scopes files
    it_output_dict = {} #it -> output file
    it_occurence_output_dict = {}  # it -> output file
    for it in current_ignorance_types:
        #dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)
        it_all_data = open('%s%s/%s_all_data.txt' %(args.sentence_output_folder, it.lower(), it.upper()), 'w+')
        it_all_data.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %('PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'C_START', 'C_END', 'CONCEPT_MENTION_ID'))

        it_output_dict[it.upper()] = it_all_data

    # ##setup ignorance type first occurrence output file
    # it_first_output_dict = {} #it -> output file
    # for it in current_ignorance_types:
        it_occurence_file = open('%s%s/%s_all_data_%s_occurrence.txt' % (args.sentence_output_folder, it.lower(), it.upper(), args.it_occurence_count),'w+')
        it_occurence_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
            'PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'IGNORANCE TYPE',
            'C_START', 'C_END', 'CONCEPT_MENTION_ID'))

        it_occurence_output_dict[it.upper()] = it_occurence_file


    ##all of the articles we care about to loop over
    if included_articles.lower() == 'all':
        articles_list = article_dicts.keys()
    else:
        articles_list = included_articles


    # print(article_dicts.keys())
    for i, a in enumerate(articles_list):
        # if i == 2:
        print('article', a)
        subject_scope_dict, mention_ID_dict = article_dicts[a]

        print(len(subject_scope_dict.keys()), len(mention_ID_dict.keys()))
        # print(subject_scope_dict)
        # print(mention_ID_dict)
        print('combine scopes:')
        subject_scope_to_mention_ID_dict, mention_ID_dict, subject_scope_dict = combine_scopes_and_mentions(a, subject_scope_dict, mention_ID_dict, args.sentence_output_folder)

        ##dump all dictionary files:
        dump_filenames = ['subject_scope_info', 'concept_mention_info', 'subject_scope_to_concept_mention_info']
        dump_dicts = [subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict]
        for j, f in enumerate(dump_filenames):
            output = open('%s%s_%s.pkl' %(args.dictionary_output_folder, a, f), 'wb')
            pickle.dump(dump_dicts[j], output)
            output.close()

        ##output the subject_scopes per pmcid
        output_by_pmcid(a, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, args.sentence_output_folder+args.all_combined_data)

        ##sort by ontology
        sort_by_ontology(a, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, it_output_dict)

        ##output the first occurrence of an ignorance type of choice
        output_count_ignorance_type(current_ignorance_types, args.it_occurence_count, a, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, it_occurence_output_dict)

        # else:
        #     pass


        ##get dates for all articles
        get_article_dates(articles_list, args.meta_data_article_file_path, args.output_folder)
