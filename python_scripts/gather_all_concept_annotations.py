import os
import xml.etree.ElementTree as ET
import pickle



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



def collect_annotations(gold_standard_annotation_path, articles, all_lcs_dict, all_ignorance_types):
    article_dicts = {}  # article -> (subject_scope_dict, mention_ID_dict)

    for root, directories, filenames in os.walk(gold_standard_annotation_path):
        for filename in sorted(filenames):
            if filename.split('.nxml')[0] in articles:
                ##annotation files to parse through
                # print(filename)

                with open(gold_standard_annotation_path+filename, 'r') as annotation_file:
                    tree = ET.parse(annotation_file)
                    root = tree.getroot()
                    mention_ID_dict = {}  # dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)
                    subject_scope_dict = {} #dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)

                    ##loop over all annotations
                    for annotation in root.iter('annotation'):
                        annotation_id = annotation.attrib['id']
                        # print('annotation id', annotation_id)
                        start_list = []
                        end_list = []
                        spanned_text = ''
                        empty_annotation = False  # empty annotations or subject_scopes for right now to do binary
                        ##loop over all annotation information
                        for child in annotation:
                            if child.tag == 'class':
                                ont_lc = child.attrib['id']
                                # print('ont_lc', ont_lc)

                                ##concept annotations
                                if ont_lc: #and ont_lc != 'subject_scope':

                                    ##subject scope
                                    if ont_lc.upper() == 'SUBJECT_SCOPE':
                                        it = ont_lc.upper()

                                    # ##binary ignorance
                                    # it = 'ignorance'  # ignorance type category
                                    elif ont_lc.replace('0_', '').upper() in all_ignorance_types:
                                        it = ont_lc.replace('0_', '')
                                        # if ont_lc == ontology.replace('/', '_'):
                                        #     it = ont_lc.replace('0_', '')
                                        # else:
                                        #     ##get rid of annotations that are not the correct ontology
                                        #     empty_annotation = True
                                    elif all_lcs_dict.get(ont_lc.replace('0_', '').lower()):

                                        ##TODO: taking the first ignorance type
                                        it = all_lcs_dict[ont_lc.replace('0_', '').lower()][0]
                                        # if all_lcs_dict[ont_lc.replace('0_', '').lower()][0].lower() == ontology.replace('/', '_').lower():
                                        #     it = all_lcs_dict[ont_lc.replace('0_', '').lower()][0]
                                        # else:
                                        #     ##get rid of annotations that are not to the correct ontology
                                        #     empty_annotation = True

                                    elif 'PMC5706533.nxml.gz.txt' in filename and ont_lc == 'studies':
                                        it = 'PROBLEM_COMPLICATION'  # the ont_lc is actually "insufficient"
                                        # if ontology.replace('/', '_').lower() == 'problem_complication':
                                        #     it = 'PROBLEM_COMPLICATION'  # the ont_lc is actually "insufficient"
                                        # else:
                                        #     empty_annotation = True

                                    else:
                                        ##old types from the initial ontology
                                        if ont_lc.lower() in ['black_box_topic', 'components', 'environment', 'risk',
                                                              'sex', 'age', 'distinction_between_things', 'sr_partner',
                                                              'life_span', 'new_scope', 'mobilization', 'duration',
                                                              'establishes', 'time_points', 'gender', 'regulation',
                                                              'molecular_nature', 'options/specific_hypotheses',
                                                              'magnitude/amount/size', 'body_location', 'pathway',
                                                              'sr_partner_1', 'abilities', 'start_time',
                                                              'reproducibility', 'comparison', 'etiology']:
                                            empty_annotation = True
                                        else:
                                            print('filename', filename)
                                            print('ont_lc', ont_lc)
                                            raise Exception('ERROR: MISSING LEXICAL CUES AND IGNORANCE TYPE PAIRS!')
                                ##subject_scope annotations
                                else:
                                    empty_annotation = True

                            elif child.tag == 'span':
                                ##empty annotation - delete
                                if not child.text:
                                    # print(child)
                                    empty_annotation = True
                                    # raise Exception('ERROR WITH EMPTY ANNOTATION')
                                else:
                                    span_start = int(child.attrib['start'])  # int
                                    span_end = int(child.attrib['end'])  # int
                                    start_list += [span_start]
                                    end_list += [span_end]
                                    if spanned_text:
                                        # discontinuous spans
                                        spanned_text += ' ... %s' % child.text  # str #this is how disjoint cues are in the CRAFT stuff
                                    else:
                                        spanned_text += '%s' % child.text  # str

                            else:
                                print('got here weirdly')
                                raise Exception('ERROR WITH READING IN THE ANNOTATION FILES!')
                                pass

                            if empty_annotation:
                                continue
                            else:
                                # not an empty annotation - should be no duplicates because gold standard
                                ##fill the dictionary with the info
                                # ensure there are spans!
                                if start_list and end_list:
                                    ## dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)
                                    # if excluded_ignorance_types:
                                    #     # don't want to include the annotation id if it is in the excluded ignorance types
                                    #     # print(all_lcs_dict[ont_lc])
                                    #     if all_lcs_dict.get(ont_lc) and len(
                                    #             set(excluded_ignorance_types) & set(all_lcs_dict[ont_lc])) > 0:
                                    #         # print('got here:', ont_lc, all_lcs_dict[ont_lc])
                                    #         pass
                                    #     elif ont_lc.upper() in excluded_ignorance_types:
                                    #         # print('here also:', ont_lc)
                                    #         pass
                                    #     else:
                                    #         mention_ID_dict[annotation_id] = [start_list, end_list, spanned_text,
                                    #                                           ont_lc, it, None]

                                    # else:
                                    # mention_ID_dict[annotation_id] = [start_list, end_list, spanned_text, ont_lc,
                                    #                                       it, None]
                                    # print(mention_ID_dict[annotation_id])

                                    if it == 'SUBJECT_SCOPE':
                                        subject_scope_dict[annotation_id] = [start_list, end_list, spanned_text, ont_lc, it, None]
                                    else:
                                        mention_ID_dict[annotation_id] = [start_list, end_list, spanned_text, ont_lc, it, None]
                                else:
                                    continue

                    ##article -> (subject_scope_dict, mention_ID_dict)
                    article_dicts[filename.split('.nxml')[0]] = (subject_scope_dict, mention_ID_dict)

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

        print(subject_scope_ID, subject_scope_value)
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
            for m in list_mention_IDs:
                del sorted_mention_ID_dict[m]
                mention_ID_dict[m][5] = subject_scope_ID

        else:
            print(subject_scope_ID, subject_scope_value)
            # print(mention_ID_dict)
            print(sorted_mention_ID_dict)
            raise Exception('ERROR: Issue with a subject scope with no concept mentions!')


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


def output_count_ignorance_type(ignorance_type_first_list, it_count, article, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, it_first_output_dict):
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
    for it in ignorance_type_first_list:
        current_it_count += [0]

    for subject_scope_ID, subject_scope_info in sorted_subject_scope_dict.items():
        for i, mention_ID in enumerate(subject_scope_to_mention_ID_dict[subject_scope_ID]):
            mention_info = sorted_mention_ID_dict[mention_ID]
            ignorance_type = mention_info[4].upper()
            ##'PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'C_START', 'C_END', 'CONCEPT_MENTION_ID'
            if ignorance_type.upper() in ignorance_type_first_list and current_it_count[ignorance_type_first_list.index(ignorance_type.upper())] < it_count:
                it_first_file = it_first_output_dict[ignorance_type.upper()]
                it_first_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (article, subject_scope_ID, subject_scope_info[0], subject_scope_info[1], subject_scope_info[2],mention_info[2], ignorance_type, mention_info[0], mention_info[1], mention_ID))

                current_it_count[ignorance_type_first_list.index(ignorance_type.upper())] += 1


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
    ##gold standard annotions v1 path
    gold_standard_annotation_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Annotations/'

    current_ignorance_types = ['ALTERNATIVE_OPTIONS_CONTROVERSY', 'ANOMALY_CURIOUS_FINDING', 'DIFFICULT_TASK', 'EXPLICIT_QUESTION', 'FULL_UNKNOWN', 'FUTURE_PREDICTION', 'FUTURE_WORK', 'IMPORTANT_CONSIDERATION', 'INCOMPLETE_EVIDENCE', 'PROBABLE_UNDERSTANDING', 'PROBLEM_COMPLICATION', 'QUESTION_ANSWERED_BY_THIS_WORK', 'SUPERFICIAL_RELATIONSHIP']

    ignorance_type_first_list = ['QUESTION_ANSWERED_BY_THIS_WORK']
    it_count = 1 #first occurrence


    ##gold standard v1 with training updated
    articles = ['PMC1247630','PMC1474522','PMC1533075','PMC1626394','PMC2009866','PMC2265032','PMC2396486','PMC2516588','PMC2672462','PMC2874300','PMC2885310','PMC2889879','PMC2898025','PMC2999828','PMC3205727','PMC3272870','PMC3279448','PMC3313761','PMC3342123','PMC3348565','PMC3373750','PMC3400371','PMC3427250','PMC3513049','PMC3679768','PMC3800883','PMC3914197','PMC3915248','PMC3933411','PMC4122855','PMC4304064','PMC4311629','PMC4352710','PMC4377896','PMC4428817','PMC4500436','PMC4564405','PMC4653409','PMC4653418','PMC4683322','PMC4859539','PMC4897523','PMC4954778','PMC4992225','PMC5030620','PMC5143410','PMC5187359','PMC5273824','PMC5501061','PMC5540678','PMC5685050','PMC5812027','PMC6000839','PMC6011374','PMC6022422','PMC6029118','PMC6033232','PMC6039335','PMC6054603','PMC6056931']

    all_lcs_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/0_Gold_Standard_Annotation/Ontologies/Ontology_Of_Ignorance_all_cues_2020-08-25.txt'

    output_folder = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/3_Ignorance_Base/Ignorance-Base/Output_Folders/'
    sentence_folder = 'PMCID_Sentence_Files/'

    sentence_output_folder = output_folder + sentence_folder

    all_combined_data = '0_all_combined'

    dictionary_folder = 'dictionary_files/'

    dictionary_output_folder = output_folder + dictionary_folder

    meta_data_article_file_path = '/Users/MaylaB/Dropbox/Documents/0_Thesis_stuff-Larry_Sonia/1_First_Full_Annotation_Task_9_13_19/document_collection_pre_natal/' #PMC6011374.nxml.gz.txt.gz.meta



    ##collect all lcs:
    all_lcs_dict, all_ignorance_types = collect_all_lcs(all_lcs_path)
    print(all_ignorance_types) ##all upper case

    article_dicts = collect_annotations(gold_standard_annotation_path, articles, all_lcs_dict, all_ignorance_types)



    ##setup ontology separating files for all scopes files
    it_output_dict = {} #it -> output file
    for it in current_ignorance_types:
        #dict: mention_ID -> (start_list, end_list, spanned_text, mention_class_ID, class_label, sentence_number)
        it_all_data = open('%s%s/%s_all_data.txt' %(sentence_output_folder, it.lower(), it,), 'w+')
        it_all_data.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %('PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'C_START', 'C_END', 'CONCEPT_MENTION_ID'))

        it_output_dict[it] = it_all_data

    ##setup ignorance type first occurrence output file
    it_first_output_dict = {} #it -> output file
    for it in current_ignorance_types:
        it_first_file = open('%s%s/%s_all_data_first_occurrence.txt' % (sentence_output_folder, it.lower(), it.upper()),'w+')
        it_first_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
            'PMCID', 'SUBJECT_SCOPE_ID', 'S_START', 'S_END', 'SUBJECT_SCOPE', 'CONCEPT', 'IGNORANCE TYPE',
            'C_START', 'C_END', 'CONCEPT_MENTION_ID'))

        it_first_output_dict[it.upper()] = it_first_file


    # print(article_dicts.keys())
    for i, a in enumerate(articles):
        # if i == 2:
        print('article', a)
        subject_scope_dict, mention_ID_dict = article_dicts[a]

        print(len(subject_scope_dict.keys()), len(mention_ID_dict.keys()))
        # print(subject_scope_dict)
        # print(mention_ID_dict)
        print('combine scopes:')
        subject_scope_to_mention_ID_dict, mention_ID_dict, subject_scope_dict = combine_scopes_and_mentions(a, subject_scope_dict, mention_ID_dict, sentence_output_folder)

        ##dump all dictionary files:
        dump_filenames = ['subject_scope_info', 'concept_mention_info', 'subject_scope_to_concept_mention_info']
        dump_dicts = [subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict]
        for j, f in enumerate(dump_filenames):
            output = open('%s%s_%s.pkl'  %(dictionary_output_folder, a, f), 'wb')
            pickle.dump(dump_dicts[j], output)
            output.close()

        ##output the subject_scopes per pmcid
        output_by_pmcid(a, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, sentence_output_folder+all_combined_data+'/')

        ##sort by ontology
        sort_by_ontology(a, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, it_output_dict)

        ##output the first occurrence of an ignorance type of choice
        output_count_ignorance_type(current_ignorance_types, it_count, a, subject_scope_dict, mention_ID_dict, subject_scope_to_mention_ID_dict, it_first_output_dict)

        # else:
        #     pass


        ##get dates for all articles
        get_article_dates(articles, meta_data_article_file_path, output_folder)
