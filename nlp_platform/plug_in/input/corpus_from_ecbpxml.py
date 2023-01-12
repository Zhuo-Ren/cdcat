# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import re
from typing import Dict, List, Tuple, Union
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nlp_platform.center.node import Node
    from nlp_platform.center.corpus import Corpus


# 配置logging



class MentionData(object):
    '''
    An helper class for a mid-representation of a mention when reading the corpus.
    '''
    def __init__(self, doc_id, sent_id, tokens_numbers, tokens_str, coref_chain, mention_type='ACT',
                 is_continuous=True, is_singleton=False, score=float(-1)):
        '''

        :param doc_id: the mention's document ID
        :param sent_id: the mention's sentence ID
        :param tokens_numbers: the token IDs in the mention's text span
        :param tokens_str: the mention's string
        :param coref_chain: the mention's gold coreference chain
        :param mention_type: the mention's type, marked with ACT for event mention and with the
        following types for entity mentions: HUM for human participant, NON for non-human participant,
        LOC for location, and TIM for time.
        :param is_continuous: a variable indicates whether the mention span is continuous or not
        :param is_singleton: a variable indicates whether the mention belongs to a singleton  coreference
        cluster ( a cluster which contains only a single mention)
        :param score: a confidence score of the span for being a real mention (this score relates to
        predicted mentions only, and it sets to -1 dealing with gold mentions)
        '''
        self.doc_id = doc_id
        self.sent_id = sent_id
        self.tokens_number = tokens_numbers
        self.tokens_str = tokens_str
        self.mention_type = mention_type
        self.coref_chain = coref_chain
        self.is_continuous = is_continuous
        self.is_singleton = is_singleton
        self.score = score


def read_selected_sentences(file_path: str) -> dict:
    """
    A CSV file is released with ECB+ corpus which list all "selected sentence" (the labeled sentences). This file
    contains the IDs of 1840 sentences which were manually reviewed and checked for correctness. The ECB+ creators
    recommend to use this subset of the dataset.
    the content in this .csv file is like:
        1 10ecbplus 1  \n
        1 10ecbplus 3  \n
        1 11ecbplus 1  .

    This function reads this file (given by param *file_path*), and returns a dictionary contains those sentences IDs.

    example1:
        >>> file_path = r'data\\raw\\ECBplus_coreference_sentences.csv'
        >>> read_selected_sentences(file_path)
        {'1_10ecbplus.xml':[1,3],'1_11ecbplus.xml':[1]}

    :param file_path: path to the CSV file
    :return: a dictionary, where a key is an XML filename (i.e. ECB+ document) and the value is a list contains all
        the sentences IDs that were selected from that XML filename.

    """
    import csv
    xml_to_sent_dict = {}
    with open(file_path, 'rt') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        # reader.next()
        next(reader)
        for line in reader:
            xml_filename = '{}_{}.xml'.format(line[0], line[1])
            sent_id = int(line[2])

            if xml_filename not in xml_to_sent_dict:
                xml_to_sent_dict[xml_filename] = []
            xml_to_sent_dict[xml_filename].append(sent_id)

    return xml_to_sent_dict


def m_tag_to_type(tag: str) -> str:
    """
    example::

        'ACT' = type_to_type_abbr('ACTION_REPORTING')
        'UNK' = type_to_type_abbr('UNKNOWN_INSTANCE_TAG')

    :param tag:  m_tag.
    :return: m_type.
    """
    if tag == 'UNKNOWN_INSTANCE_TAG':
        return 'UNK'
    if 'ACTION' in tag:
        return 'ACT'
    if 'LOC' in tag:
        return 'LOC'
    if 'NON' in tag:
        return 'NON'
    if 'HUMAN' in tag:
        return 'HUM'
    if 'TIME' in tag:
        return 'TIM'
    else:
        print('unknown tag:', tag)


def i_id_to_i_type(i_id: str) -> str:
    '''
    example::
        i_id_to_i_type('ACT150798320') -> 'ACT'

    :param i_id: i_id or anything that like a i_id( e.g. note property in cd r， instance_id
        property in cd tm).
    :return: type
    '''
    if 'ACT' in i_id or 'NEG' in i_id:
        return 'ACT'
    if 'LOC' in i_id:
        return 'LOC'
    if 'NON' in i_id:
        return 'NON'
    if 'HUM' in i_id or 'CON' in i_id:
        return 'HUM'
    if 'TIM' in i_id:
        return 'TIM'
    if 'UNK' in i_id:
        return 'UNK'


def sentencindex_to_bodysentenceindex(doc_id: str, sentenceindex: int, parse_all: bool) -> int:
    '''
    in xml file, a news text = [newsUrl] + [newsTime] + newsBody

    In X_Xecb.xml, news body starts with sentence 0. So sm_bodysentenceindex = sm_sentenceindex.
    A sm_bodysentenceindex is different from sm_sentenceindex in 2 condition:
        - 1st: Only in X_Xecbplus.xml, there is a newsUrl which is the sentence 0. So, newsBody
          starts with sentence 1.
        - 2nd: Only in 9_3ecbplus.xml and 9_4ecbplus.xml, there is a newsTime which is the sentence
          1. So, newsBody starts with sentence 2.
    '''
    bodysentenceindex = sentenceindex
    # 1st condition: there is url sentence.
    if 'plus' in doc_id:
        if int(bodysentenceindex) > 0:
            bodysentenceindex -= 1
    # 2nd condition: there is time sentence.
    if parse_all and (doc_id == '9_3ecbplus' or doc_id == '9_4ecbplus'):
        if bodysentenceindex > 0:
            bodysentenceindex -= 1
    return bodysentenceindex


def read_ecb_plus_doc(selected_sent_list: List[int],
                      doc_name: str,
                      doc_id: str,
                      extracted_tokens: List[str],
                      extracted_mentions: List[Union[None, MentionData]],
                      parse_all: bool,
                      load_singletons: bool) -> List:
    """
    Read xml file of ecb+ corpora, extract t info and sm info, and save it.

    ---------------
     t info
    ---------------
    t info are saved into the text file given by *output_file_obj*.

    - A t will be saved when the following statement is True::

        parse_all or (t_sentenceindex in selected_sent_list)

    - In the file, one line corresponds to one t.
      There is one black line after the end token of a sentence.
      And there are 5 columns:

      - the 1st column: *doc_id* parameter of this function.
      - the 2nd column: t_bodysentenceindex. For detail , see sentencindex_to_bodysentenceindex
      - the 3rd column: t_id.
      - the 4th column: t_text, and if t_text is ' ' or '\t', it will be replaced by a '-'.
      - The 5th column: the id of the i that this t refer to.

        - '-', if this t isn't in a mention( so it do not refer to any i).
        - wd_i_id( For detail, see wd_i_info.), if this t refer to a wd i.
        - cd_i_id( For detail, see cd_i_info.), if this t refer to a cd i.
        - sg_i_id( For detail, see sg_i_info.), if this t refer to a sg i and load singletons;
        - '-', if this t refer to a sg i and do not load singletons;

      example::

            14_5ecb	2	37	being	-
            14_5ecb	2	38	treated	ACT17478359686333015
            14_5ecb	2	39	as	-
            14_5ecb	2	40	potentially	-
            14_5ecb	2	41	suspicious	-
            14_5ecb	2	42	.	-
            14_5ecb	2	43	''	-

            14_6ecb	0	0	Residents	Singleton_HUM_14_14_6ecb
            14_6ecb	0	1	evacuated	Singleton_ACT_15_14_6ecb
            14_6ecb	0	2	from	-
            14_6ecb	0	3	their	INTRA_UNK_33690_14_6ecb
            14_6ecb	0	4	homes	INTRA_UNK_33690_14_6ecb
            14_6ecb	0	5	after	-
            14_6ecb	0	6	a	-
            14_6ecb	0	7	huge	-
            14_6ecb	0	8	fire	ACT17478306085573007

    ---------------
     sm info
    ---------------
    sm info: are saved into parameter *extracted_mentions* which is a shallow copied object.

    - A sm will be saved when the following statement is True::

        parse_all or (sm_sentenceindex in selected_sent_list)

    - sm info is saved as a *src.mention_data.MentionData* objects, which has the following property：

      - doc_id = doc_id
      - cur_t_sentenceindex = cur_sm_bodysentenceindex
      - tokens_numbers = cur_sm_tokenindex
      - tokens_str = cur_sm_string
      - coref_chain = cur_i_id
      - mention_type = cur_sm_type,
      - is_continuous = is_continuous
      - is_singleton = is_singleton
      - score = float(-1)

    :param selected_sent_list:
        A list of the sentenceindex( rather than a bodysentenceindex) of
        'selected sentence'. This parameter is activated only when parse_all=
        False, and then extract info from only those 'selected sentences'.
        e.g. [0, 3]
    :param doc_name:
        Path of the xml file. The xml file should be encoded with utf-8.
        e.g. 'data/raw/ECBplus\\2\\2_10ecbplus.xml' or 'data/raw/ECBplus\\1\\1_10ecb.xml'
    :param doc_id:
        Document ID of the xml file, in form of  {topic id}_{file
        name}{ecb/ecbplus type}).
        e.g. '1_10ecb' or '1_10ecbplus'.
    :param extracted_tokens:
        Each t info, which is represented by a string, is appended to this list.
    :param extracted_mentions:
        Each sm info, which is represented by src.data.mention_data.MentionData
        object, is appended to this list.
    :param parse_all:
        From which sentence to extract information
        True, extract info from all sentences in xml file as in Yang setup;
        False, extract info from only the selected sentences as in Cybulska setup.
            The selected sentences is given by parameter selected_sent_list.
    :param load_singletons:
        A boolean variable indicates whether to read singleton mentions as in
        Cybulska setup or whether to ignore them as in Yang setup.
    """
    ecb_file = open(doc_name, 'r', encoding='UTF-8')

    import xml.etree.ElementTree as ET  # for the parse of xml file.
    tree = ET.parse(ecb_file)
    root = tree.getroot()

    t_info: dict[str, dict[str, str]] = {}
    """
    {t_id: t_info_dict}
        - t_id: id of a t, **All t(selected or not) are included.** The 1st t in whole
          doc has a t_id = 1.

          - Value: 't_id' attr of this t label.
          - Type: str 

        - t_info_dict['t_text']: text of this t.

          - Value: text of this t label, e.g. 'has'.
          - Type: str.

        - t_info_dict['t_sentenceindex']:  index of this sentence, the 1st sentence in
          whole doc is index 0. 

          - Value: 'sentence' attr of this t label, e.g. "3".
          - Type: str.

        - t_info_dict['t_bodysentenceindex']:  index of this sentence, the 1st sentence in
          news body is index 0. For detail about sentenceindex and bodysentenceindex, see
          *sentencindex_to_bodysentenceindex*.

          - Value: calculated by *sentencindex_to_bodysentenceindex(sentencindex)*, e.g. "1"
          - Type: str

        - t_info_dict['t_tokenindex']: index of this t, the 1st t in cur sentence is
          index 0.

          - Value: 'number' attr of this t, e.g. "0".
          - Type: str.

        - t_info_dict['i_id']: id of the corresponding i.

          - wd_i_id( For detail, see wd_i_info.) for a wd i. 
          - cd_i_id( For detail, see cd_i_info.) for a cd i. 
          - sg_i_id( For detail, see sg_i_info.) for a sg i, if load singletons; 
            None, if not load singletons.

        - t_info_dict['i_desc']: description of the corresponding i.

          - wd_i_desc for a wd i. For detail, see wd_i_info.
          - cd_i_desc for a cd i. For detail, see cd_i_info.
          - 'padding' for a sg i, if load singletons; None, if not load singleton.

    """

    sm_info: dict[str, str] = {}
    """
    {sm_id: sm_tag}
        - sm_id: id of a sm. 
          **All(selected and not; sg, wd and cd) sm are included.**

          - Value: 'm_id' attr of this sm label.

        - sm_tag: 

          -Value: tag of this sm label.
    """

    tm_info: dict[str, tuple[str, str]] = {}
    """
    {'tm_id':(tm_desc, i_id_or_tag)}
        - tm_id: id of a tm. **All( selected and not) cd and wd tm are included.**

          - Value: 'm_id' attr of this tm label. 

        - tm_desc: describe of this tm.

          - Value: 'TAG_DESCRIPTOR' attr of the tm label. 

        - i_id_or_tag: info of the corresponding i:
          for a cd tm, we have the i_id of the corresponding i; 
          for a wd tm, we have the i_type of the corresponding i.

          - Value:

            - for CD tm, it is the 'instance_id' attr of this tm label.
            - for WD tm, it is the tag of this tm label.

    """

    mapped_sm_id: [str] = []
    """
    [sm_id]
        - sm_id: id of a sm which refer to a tm. 
          All(seleted and not; CD and WD sm, except SG sm) sm which refer to a tm are
          included.
    """

    sm_id_to_t_id: dict[str, list[str]] = {}
    """
    {sm_id: sm_tidlist}
        - sm_id: id of a sm. **All sm included( selected and not; sg sm(if loaded), wd sm and
          cd sm).**
        - sm_tidlist:[t_id,t_id,...]. t_id is the id of all(in cur doc) the t that
          refer to this sm.
    """

    sm_id_to_i_id: dict[str, str] = {}
    """
    {sm_id: i_id}
        - sm_id: id of a sm. **All sm included( selected or not; cd sm, wd sm and 
          sg sm).**
        - i_id: 

          - a wd_i_id(for detail, see wd_i_info) for a wd i. 
          - a cd_i_id(for detail, see cd_i_info) for a cd i.
          - a sg_i_if(for detail, see sg_i_info) for a sg i, if load_singletons=True.
    """

    wd_i_info: dict[str, tuple[list[str], str]] = {}
    """
    {wd_i_id:(t_id_list, wd_i_desc)}
        - wd_i_id: represented in the form of 'INTRA_{wd_i_type}_{rId}_{docId}'.
            **All wd_i included( selected or not).**

          - wd_i_type: A wd_i has many tm and sm, each of them has a type. wd_i_type
            equals to the type if all the types are same; otherwise, a accordance strategy
            is need:

            - tm_type strategy: set wd_i_type as wd_tm_type without accordance check
            - Barhom2019 strategy: 
              this value is 'UNK' if the type of tm is 'UNKNOWN_INSTANCE_TAG', 
              otherwise, the value equals to the type of the first sm.

          - rId: A wd_i has only one wd_r, rId is the 'r_id' attr of this wd_r
          - docId:

        - t_id_list:[t_id, t_id, ...], t_id of all(in cur doc) the t that refer to this wd_i.
        - wd_i_desc: description string of this wd_i.
          The value equals to 'TAG_DESCRIPTOR' attr of the tm of this wd_i.
    """

    cd_i_info: dict[str, tuple[list[str], str]] = {}
    """
    {'cd_i_id': (cd_i_tidlist, cd_i_desc)}
        - cd_i_id: if the 'instance_id ' attr of corresponding tm and the 'note'
          attr of the corresponding r is equal, cd_i_id is this value. otherwise, a 
          accordance strategy is need:

        - cd_i_tidlist:[t_id, t_id, ...], t_id of all(in cur doc) the t that refer to
          this cd_i.
        - cd_i_desc: description string of this cd_i.
          The value equals to 'TAG_DESCRIPTOR' attr of the tm of this cd_i.
    """

    sg_i_info: dict[str, tuple[list[str], str]] = {}
    """
    **there is no sg_i in ecb+, only when load_singletons=True, we make a sg_i for every
    sg sm.**

    {'sg_i_id': (t_id_list, sg_i_desc)}
        - sg_i_id: in the form of 'Singleton_{sg_i_type}_{sg_sm_id}_{doc_id}'

          - sg_i_type: equals to the type of sg_sm.( A sg_i has only one sg_sm, no 
            accordance check needed)
          - sg_sm_id: id of the sg_sm.( A sg_i has only one sg_sm, no accordance check 
            needed)
          - doc_id: id of the doc

        - t_id_list:[t_id, t_id, ...], t_id of all(in cur doc) the t that refer to
          this sg_i. But it is None because we do not need this, the varable sg_i_tidlist
          here is to keep the same structer as cd_i_info and wd_i_info.
        - sg_i_desc: description string of this cd_i.But it is always 'padding' because
          there is no description for a sg i in ecb+.
    """

    # 1.extract info from <Markables>...</Markables> tag
    """
    iterate through every tag in <Markables>...</Markables>
    there are 4 kinds of conditions: token anchor and 3 kinds of mention: 
        (1)token anchor,
        (2)source mention,
        (3)CD target mention,
        (4)WD target mention:    
    e.g.::
        <Markables>
        (2) <XXX m_id="48" note="byCROMER" >
        (1)     <token_anchor t_id="19"/>
        (1)     <token_anchor t_id="20"/>
            </XXX>
        (3) <TIME_DURATION m_id="52" RELATED_TO="" TAG_DESCRIPTOR="t26_decades" instance_id="TIM18440826675897964" />
        (3) <ACTION_OCCURRENCE m_id="51" RELATED_TO="" TAG_DESCRIPTOR="t26_died" instance_id="ACT18440577880137709" />
        (4) <UNKNOWN_INSTANCE_TAG m_id="17" RELATED_TO="" TAG_DESCRIPTOR="" />"
        (4) <HUMAN_PART_PER m_id="40" RELATED_TO="" TAG_DESCRIPTOR="spokesman" />
        </Markables>
    """
    cur_m_id = ''
    for cur_tag in root.find('Markables').iter():
        if cur_tag.tag == 'Markables':
            continue
        # for condition (1)
        elif cur_tag.tag == 'token_anchor':
            sm_id_to_t_id[cur_m_id].append(cur_tag.attrib['t_id'])
        # for condition (2)(3)(4)
        else:
            cur_m_id = cur_tag.attrib['m_id']
            # for condition (3)(4), it is a tm
            if 'TAG_DESCRIPTOR' in cur_tag.attrib:
                # for condition (3), it is a CD tm
                if 'instance_id' in cur_tag.attrib:
                    tm_info[cur_m_id] = (
                        cur_tag.attrib['TAG_DESCRIPTOR'],
                        cur_tag.attrib['instance_id']
                    )
                # for condition (4), it is a WD tm
                else:
                    tm_info[cur_m_id] = (
                        cur_tag.attrib['TAG_DESCRIPTOR'],
                        cur_tag.tag
                    )
            # for condition (2), it is a source mention
            else:
                sm_id_to_t_id[cur_m_id] = []
                sm_info[cur_m_id] = cur_tag.tag

    # 2.extract info from <Relations><INTRA_DOC_COREF>...</INTRA_DOC_COREF></Relations>
    """
    iterate through every tag in <Markables><INTRA_DOC_COREF>...</INTRA_DOC_COREF></Markables>
    there are 3 kinds of conditions marked as (i1)(i2)(i3)
        <Relations>
        (i1) <INTRA_DOC_COREF r_id="37615" >
        (i2)    <source m_id="24" />
        (i2)    <source m_id="25" />
        (i3)    <target m_id="17" />
             </INTRA_DOC_COREF>
             ...
        </Relations>
    填写了:wd_i_info完成, mapped_sm_id填了wd_sm的部分，sm_id_to_i_id填了wd_sm的部分
    """
    cur_wd_i_id = ''
    cur_wd_i_tidlist = []
    for cur_wd_r in root.find('Relations').findall('INTRA_DOC_COREF'):
        for cur_label in cur_wd_r.iter():
            # for condition (i1), cur r is a WD r
            if cur_label.tag == 'INTRA_DOC_COREF':
                # two strategy for setting the cur_wd_i_type, leave the accordance check for later.
                strategy = 'Barhom2019 strategy'
                if strategy == 'Barhom2019 strategy':
                    cur_wd_tm_tag = tm_info[cur_wd_r.find('target').get('m_id')][1]
                    # this value is 'UNK' if the type of tm is 'UNKNOWN_INSTANCE_TAG'
                    if cur_wd_tm_tag == 'UNKNOWN_INSTANCE_TAG':
                        cur_wd_i_type = m_tag_to_type(cur_wd_tm_tag)
                    # otherwise, the value equals to the type of the first sm.
                    else:
                        cur_1th_wd_sm_tag = sm_info[cur_wd_r.find('source').get('m_id')]
                        cur_1th_wd_sm_type = m_tag_to_type(cur_1th_wd_sm_tag)
                        cur_wd_i_type = cur_1th_wd_sm_type
                    # cid of a WD coref is represented by 'INTRA_tagAttr_rId_docId'
                elif strategy == 'tm_type strategy':
                    # tm_type strategy:
                    # set wd_i_type as wd_tm_type immediately
                    cur_wd_tm_tag = tm_info[cur_wd_r.find('target').get('m_id')][1]
                    cur_wd_tm_type = m_tag_to_type(cur_wd_tm_tag)
                    cur_wd_i_type = cur_wd_tm_type
                elif strategy == '一致性检查':
                    pass  # 检查tm和所有sm的type，如果一致，才作为wd_i_type
                cur_wd_i_id = 'INTRA_{}_{}_{}'.format(cur_wd_i_type, cur_label.attrib['r_id'],
                                                      doc_id)
                wd_i_info[cur_wd_i_id] = ()
            # for condition (i2), it is the sm in cur r
            elif cur_label.tag == 'source':
                cur_wd_i_tidlist += (sm_id_to_t_id[cur_label.attrib['m_id']])
                mapped_sm_id.append(cur_label.attrib['m_id'])
                sm_id_to_i_id[cur_label.attrib['m_id']] = cur_wd_i_id
            # for condition (i3), it is the tm in cur r
            elif cur_label.tag == 'target':
                wd_i_info[cur_wd_i_id] = (cur_wd_i_tidlist, tm_info[cur_label.attrib['m_id']][0])
                # end of iteration of cur relation, clear variable for iteration of the next relation.
                cur_wd_i_tidlist = []

    # 3. extract info from <Relations><CROSS_DOC_COREF>...</CROSS_DOC_COREF></Relations>
    """
    iterate through every tag in <Markables><CROSS_DOC_COREF>...</CROSS_DOC_COREF></Markables>
    there are 3 kinds of conditions marked as (c1)(c2)(c3)
        <Relations>
        (c1) <CROSS_DOC_COREF r_id="37623" note="ACT16235311629112331" >
        (c2)      <source m_id="36" />
        (c2)      <source m_id="37" />
        (c3)      <target m_id="49" />
              </CROSS_DOC_COREF>
        </Relations>
    填写了:cd_i_info完成, mapped_sm_id填了cd_sm的部分，sm_id_to_i_id填了cd_sm的部分
    """
    cur_cd_i_id = ''
    cur_cd_i_tidlist = []
    for cross_doc_coref in root.find('Relations').findall('CROSS_DOC_COREF'):
        for cur_label in cross_doc_coref.iter():
            # for condition (c1), cur r is CD r
            if cur_label.tag == 'CROSS_DOC_COREF':
                # set the cd_i_id as r_note immediately, leave the accordance check for later.
                cur_cd_r_note = cur_label.attrib['note']
                cur_cd_i_id = cur_cd_r_note
                cd_i_info[cur_cd_i_id] = ()
            # for condition (c2), it is the sm in cur r
            elif cur_label.tag == 'source':
                cur_cd_i_tidlist += (sm_id_to_t_id[cur_label.attrib['m_id']])
                mapped_sm_id.append(cur_label.attrib['m_id'])
                sm_id_to_i_id[cur_label.attrib['m_id']] = cur_cd_i_id
            # for condition (c3), it is the tm in cur r
            else:
                cd_i_info[cur_cd_i_id] = (
                    cur_cd_i_tidlist,
                    tm_info[cur_label.attrib['m_id']][0]
                )
                # end of iteration of cur relation, clear variable for iteration of the next relation.
                cur_cd_i_tidlist = []

    # 4. extract info from <token>...</token>
    """
    填写了:t_info基本完成，只是对属于sg_i的token，其i_id和i_desc全为None，没有根据load_singletons做判断。
    """
    for cur_t in root.findall('token'):
        t_info[cur_t.attrib['t_id']] = {
            't_text': cur_t.text,
            't_sentenceindex': cur_t.attrib['sentence'],
            't_tokenindex': cur_t.attrib['number'],
            'i_id': None,
            'i_desc': None
        }
    for cur_cd_i_id in cd_i_info:
        for cur_t_id in cd_i_info[cur_cd_i_id][0]:
            t_info[cur_t_id]['i_id'] = cur_cd_i_id
            t_info[cur_t_id]['i_desc'] = cd_i_info[cur_cd_i_id][1]
    for cur_wd_i_id in wd_i_info:
        for cur_t_id in wd_i_info[cur_wd_i_id][0]:
            t_info[cur_t_id]['i_id'] = cur_wd_i_id
            t_info[cur_t_id]['i_desc'] = wd_i_info[cur_wd_i_id][1]

    # 5. Load singletons if required
    """
    if load_singletons:
        填写了:cd_i_info完成； mapped_sm_id填了cd_sm的部分；
        填写了：sm_id_to_i_id填了sg_sm的部分,支持sm_id_to_i_id填完了；
        填写了：t_info中属于sg_i的token的i_id和i_desc，至此t_info填完了。
    """
    if load_singletons:
        # find the sg sm(singleton source mention is sm that isn't refer to any cd tm or wd tm)
        for mid in sm_id_to_t_id:
            if mid not in mapped_sm_id:
                # sm in sm_id_to_t_id include sg, cd and wd sm.
                # sm in mapped_sm_id include cd and wd sm.
                # so, the sg sm are the difference between them.
                # iterate through every sg sm
                cur_sg_sm_id = mid

                # (1. create instance id for each singleton mention
                cur_sg_sm_tag = sm_info[cur_sg_sm_id]
                cur_sg_sm_type = m_tag_to_type(cur_sg_sm_tag)
                cur_sg_i_type = cur_sg_sm_type  # a sg_i has only one sg_sm, no accordance check needed.
                cur_sg_i_id = 'Singleton_{}_{}_{}'.format(cur_sg_i_type, cur_sg_sm_id, doc_id)
                sg_i_info[cur_sg_i_id] = (sm_id_to_t_id[cur_sg_sm_id], "")
                # (2. updated sm_id_to_i_id
                # this mention is related to the singleton instance, so this mention appears
                # in this singleton coref, so this mention can be listed in sm_id_to_i_id
                sm_id_to_i_id[cur_sg_sm_id] = cur_sg_i_id
                # (3. updated tokens
                # the token of this mention had it rel_id property as None, after this mention
                # is related to the singleton instance, the rel_id property should save the info
                # of the singleton instance.
                unmapped_tids = sm_id_to_t_id[cur_sg_sm_id]
                for cur_t_id in unmapped_tids:
                    if t_info[cur_t_id]['i_id'] is None:
                        t_info[cur_t_id]['i_id'] = cur_sg_i_id
                        t_info[cur_t_id]['i_desc'] = 'padding'

    # 6. sm info is saved into *extracted_mentions*
    for cur_sm_id in sm_id_to_t_id:
        '''
        check if cur mention need to be save.
        if user want to parse all sentences, then process cur mention
        if user want to parse only the selected sentences, and cur mention is
            selected，then process cur mention
        '''
        cur_sm_sentenceindex = int(t_info[
                                       sm_id_to_t_id[cur_sm_id][0]
                                   ]['t_sentenceindex'])
        if not (parse_all or (cur_sm_sentenceindex in selected_sent_list)):
            continue

        # (1
        cur_sm_tag = sm_info[cur_sm_id]
        cur_sm_type = m_tag_to_type(cur_sm_tag)
        cur_sm_is_person = True if cur_sm_tag == "HUMAN_PART_PER" else False

        # (2
        cur_i_id = sm_id_to_i_id[cur_sm_id]
        cur_i_type = i_id_to_i_type(cur_i_id)

        """
        # the 2 types above should be same
        # if cur_sm_type != cur_i_type:
        #     print('err: diff types in same coref: {}'.format(cur_i_id))
        #     print('  type_attr_of_cur_c: {}'.format(cur_i_type))
        #     print('  type_attr_of_cur_m: {}'.format(cur_sm_type))
        """

        # (3
        cur_sm_tokenindex = []  # One sm has some t, t has *number* attr( token index), this is a list of every *number*
        cur_sm_textlist = []
        tids = sm_id_to_t_id[cur_sm_id]
        for cur_t_id in tids:
            cur_t = t_info[cur_t_id]
            if int(cur_t['t_tokenindex']) not in cur_sm_tokenindex:
                cur_sm_tokenindex.append(int(cur_t['t_tokenindex']))
                cur_sm_textlist.append(cur_t['t_text'])  # .encode('ascii', 'ignore')修改了这里
        cur_sm_string = ' '.join(cur_sm_textlist)

        # (4
        cur_sm_bodysentenceindex = sentencindex_to_bodysentenceindex(
            doc_id, cur_sm_sentenceindex, parse_all
        )

        # (5
        is_continuous = True if cur_sm_tokenindex == list(
            range(cur_sm_tokenindex[0], cur_sm_tokenindex[-1] + 1)) else False

        # (6
        is_singleton = True if 'Singleton' in cur_i_id else False

        # create mention obj based on the above info, and add it to extracted_mentions
        mention_obj = MentionData(doc_id,
                                  cur_sm_bodysentenceindex,
                                  cur_sm_tokenindex,
                                  cur_sm_string,
                                  cur_i_id,
                                  cur_sm_type,
                                  is_continuous=is_continuous,
                                  is_singleton=is_singleton,
                                  score=float(-1))
        mention_obj.is_person = cur_sm_is_person
        extracted_mentions.append(mention_obj)

    # 7. t info is saved into text file
    prev_t_bodysentenceindex = None  # bodysentenceindex of previous sentence
    for cur_t_id in t_info:
        # cur_t = t_info[cur_t_id]
        # cur_t_sentenceindex = int(cur_t['t_sentenceindex'])
        #
        # if not parse_all and cur_t_sentenceindex not in selected_sent_list:
        #     continue
        #
        # cur_t_tokenindex = int(cur_t['t_tokenindex'])
        # cur_t_text = cur_t['t_text'] if (cur_t['t_text'] != '' and cur_t['t_text'] != '\t') else '-'
        # cur_t_iid = cur_t['i_id']
        # cur_t_bodysentenceindex = sentencindex_to_bodysentenceindex(
        #     doc_id, cur_t_sentenceindex, parse_all
        # )
        #
        # # write into output file: if go to next sentence, go to next line
        # if prev_t_bodysentenceindex is None or prev_t_bodysentenceindex != cur_t_bodysentenceindex:
        #     extracted_tokens.append("")
        #     prev_t_bodysentenceindex = cur_t_bodysentenceindex
        # # write into output file: token info
        # s = doc_id \
        #     + '\t' + str(cur_t_bodysentenceindex) \
        #     + '\t' + str(cur_t_tokenindex) \
        #     + '\t' + cur_t_text \
        #     + '\t' + (cur_t_iid if cur_t_iid is not None else '-')
        #extracted_tokens.append(s)
        cur_t = t_info[cur_t_id]
        cur_t["bodysentenceindex"] = sentencindex_to_bodysentenceindex(
            doc_id, int(cur_t['t_sentenceindex']), parse_all
        )
        cur_t["doc_id"] = doc_id
        cur_t["t_id"] = cur_t_id
        extracted_tokens.append(cur_t)



def obj_dict(obj):
    return obj.__dict__


def save_split_mentions_to_json(split_name: str, mentions_list: List[MentionData]):
    '''
    This function gets  a mentions list of a specific split and saves its mentions in a JSON files.
    Note that event and entity mentions are saved in separate files.
    :param split_name: the split name, e.g. Train, Dev, Test
    :param mentions_list: the split's extracted mentions list
    '''

    # 区分event mention和entity mention
    event_mentions = []
    entity_mentions = []
    for mention_obj in mentions_list:
        mention_type = mention_obj.mention_type
        if 'ACT' in mention_type or 'NEG' in mention_type:
            event_mentions.append(mention_obj)
        else:
            entity_mentions.append(mention_obj)

    # 存储event mentions
    event_mentions

    # 存储entity mentions
    entity_mentions


def read_corpora(
        file_to_selected_sentence: dict,
        parse_all: bool,
        load_singletons: bool,
        corpus_path: str
) -> List:
    """
    read ecb+ corpora and extract info with given config.

    :param file_to_selected_sentence: This parameter is effective only when parse_all=False, and this
        parameter shows which sentence in a xml file will be extracted.
        e.g. {'1_10ecbplus.xml':[1,3],'1_11ecbplus.xml':[1]}
    :param parse_all: a boolean variable indicates whether to read all the ECB+ corpus as in
        Yang setup or whether to filter the sentences according to a selected sentences list
        as in Cybulska setup.
    :param load_singletons:  boolean variable indicates whether to read singleton mentions as in Cybulska setup or whether to ignore them as in Yang setup.
    :param corpus_path: Path to ecb+ corpus.
    """
    # 1. topic_list
    topic_str_list = os.listdir(corpus_path)  # ['1', '10', '11', ...]
    topic_list = [int(d) for d in topic_str_list]  # [1, 10, 11, ...]
    """topic list, e.g. [1, 10, 11, ...]"""

    # 2. split train/dec/test topic
    dev_topics = [2, 5, 12, 18, 21, 23, 34, 35]
    train_topics = [i for i in range(1, 36) if
                    i not in dev_topics]  # train topics 1-35 , test topics 36-45
    test_topics = list(set(topic_list) - set(train_topics) - set(dev_topics))
    print('train_topics:', train_topics)
    print('dev_topics:', dev_topics)
    print('test_topics:', test_topics)

    # 3. split train/dec/test file
    # classify all the ecb/ecb+ docs into train/dev/test set in sorted order.
    """
    The sort is like::
        1_10ecb, 1_11ecb, 1_12ecb, 1_13ecb, 1_14ecb, 1_15ecb, 1_17ecb, 1_18ecb, 1_19ecb, 1_1ecb, 1_2ecb, 1_3ecb, 1_4ecb, 1_5ecb, 1_6ecb, 1_7ecb, 1_8ecb, 1_9ecb, 
        3_1ecb, 3_2ecb, 3_3ecb, 3_4ecb, 3_5ecb, 3_6ecb, 3_7ecb, 3_8ecb, 3_9ecb, 
        4_10ecb, 4_11ecb, 4_12ecb, 4_13ecb, 4_14ecb, 4_1ecb, 4_2ecb, 4_3ecb, 4_4ecb, 4_5ecb, 4_6ecb, 4_7ecb, 4_8ecb, 4_9ecb, 
        ...
    可见这排序是失败的，1_1ecb排在1_19ecb后边，这叫什么事？
    """
    train_ecb_files_sorted = []
    r""" [([0, 3], 'data/raw/ECBplus\\1\\1_10ecb.xml', '1_10ecb'), ...] """
    dev_ecb_files_sorted = []
    r""" [([0], 'data/raw/ECBplus\\2\\2_11ecb.xml', '2_11ecb'), ...] """
    test_ecb_files_sorted = []
    r""" [([0, 1], 'data/raw/ECBplus\\36\\36_1ecb.xml', '36_1ecb'), ...] """
    train_ecb_plus_files_sorted = []
    r""" [([1, 3], 'data/raw/ECBplus\\1\\1_10ecbplus.xml', '1_10ecbplus'), ...] """
    dev_ecb_plus_files_sorted = []
    r""" [([1, 3, 4], 'data/raw/ECBplus\\2\\2_10ecbplus.xml', '2_10ecbplus'), ...] """
    test_ecb_plus_files_sorted = []
    r"""[([1, 11], 'data/raw/ECBplus\\36\\36_10ecbplus.xml', '36_10ecbplus'), ...] """
    # traverse the topics, and fill the above list
    for topic in sorted(topic_list):
        topic_id = str(topic)
        file_list = os.listdir(os.path.join(corpus_path, topic_id))
        """['1_10ecb.xml', '1_10ecbplus.xml', '1_11ecb.xml', ... ]"""
        # classify the file_list into ecb_file_list and ecb_plus_file_list
        ecb_file_list = []
        ecb_plus_file_list = []
        for file_name in file_list:
            if 'plus' in file_name:
                ecb_plus_file_list.append(file_name)
            else:
                ecb_file_list.append(file_name)
        # sort the two file_list
        ecb_file_list = sorted(ecb_file_list)  # 没卵用，sorted完后还跟之前一毛一样
        ecb_plus_file_list = sorted(ecb_plus_file_list)
        # traverse the ecb docs in cur topic, add info to train/test/dev_ecb_files_sorted list
        for ecb_file in ecb_file_list:
            # if user want to parse all sentences, then process cur doc
            # if user want to parse only the selected sentences, and cur doc includes at
            #   least 1 selected sentence, then process cur doc
            if parse_all or (ecb_file in file_to_selected_sentence):
                # get the relative path of xml file of cur doc
                xml_file_path = os.path.join(os.path.join(corpus_path, topic_id),
                                             ecb_file)
                # get the selected sentence id in cur doc
                if parse_all:
                    selected_sentences = None
                else:
                    selected_sentences = file_to_selected_sentence[ecb_file]
                # classify cur doc into train/dev/test
                if topic in train_topics:
                    train_ecb_files_sorted.append((selected_sentences, xml_file_path,
                                                   ecb_file.replace('.xml', '')))
                elif topic in dev_topics:
                    dev_ecb_files_sorted.append((selected_sentences, xml_file_path,
                                                 ecb_file.replace('.xml', '')))
                else:
                    test_ecb_files_sorted.append((selected_sentences, xml_file_path,
                                                  ecb_file.replace('.xml', '')))
        # traverse the ecb+ docs in cur topic, add info to train/test/dev_ecb_plus_files_sorted list
        for ecb_file in ecb_plus_file_list:
            if parse_all or ecb_file in file_to_selected_sentence:
                xml_file_path = os.path.join(os.path.join(corpus_path, topic_id), ecb_file)
                if parse_all:
                    selected_sentences = None
                else:
                    selected_sentences = file_to_selected_sentence[ecb_file]
                if topic in train_topics:
                    train_ecb_plus_files_sorted.append((selected_sentences,
                                                        xml_file_path,
                                                        ecb_file.replace('.xml', '')))
                elif topic in dev_topics:
                    dev_ecb_plus_files_sorted.append((selected_sentences,
                                                      xml_file_path, ecb_file.replace('.xml', '')))
                else:
                    test_ecb_plus_files_sorted.append(
                        (selected_sentences, xml_file_path, ecb_file.replace('.xml', '')))
    # combine the above list
    train_files = train_ecb_files_sorted + train_ecb_plus_files_sorted
    r""" [([0, 3], 'data\\raw\\ECBplus\\1\\1_10ecb.xml', '1_10ecb'), ...] """
    dev_files = dev_ecb_files_sorted + dev_ecb_plus_files_sorted
    r""" [([0], 'data/raw/ECBplus\\2\\2_11ecb.xml', '2_11ecb'), ...] """
    test_files = test_ecb_files_sorted + test_ecb_plus_files_sorted
    r""" [([0, 1], 'data/raw/ECBplus\\36\\36_1ecb.xml', '36_1ecb'), ...] """

    # 4. extract train/dec/test mention/token info
    train_extracted_mentions: List[MentionData] = []
    """
    A sm **in train split** will be saved when the following statement is True::
        parse_all or (sm_sentenceindex in selected_sent_list)

    sm info is saved as a src.data.mention_data.MentionData objects, which has the following property：

    - doc_id = doc_id
    - cur_t_sentenceindex = cur_sm_bodysentenceindex
    - tokens_numbers = cur_sm_tokenindex
    - tokens_str = cur_sm_string
    - coref_chain = cur_i_id
    - mention_type = cur_sm_type,
    - is_continuous = is_continuous
    - is_singleton = is_singleton
    - score = float(-1)
    """
    dev_extracted_mentions: List[MentionData] = []
    """
    A sm **in dev split** will be saved when the following statement is True::
        parse_all or (sm_sentenceindex in selected_sent_list)

    sm info is saved as a src.data.mention_data.MentionData objects, which has the following property：

    - doc_id = doc_id
    - cur_t_sentenceindex = cur_sm_bodysentenceindex
    - tokens_numbers = cur_sm_tokenindex
    - tokens_str = cur_sm_string
    - coref_chain = cur_i_id
    - mention_type = cur_sm_type,
    - is_continuous = is_continuous
    - is_singleton = is_singleton
    - score = float(-1)
    """
    test_extracted_mentions: List[MentionData] = []
    """
    A sm **in test split** will be saved when the following statement is True::
        parse_all or (sm_sentenceindex in selected_sent_list)

    sm info is saved as a src.data.mention_data.MentionData objects, which has the following property：

    - doc_id = doc_id
    - cur_t_sentenceindex = cur_sm_bodysentenceindex
    - tokens_numbers = cur_sm_tokenindex
    - tokens_str = cur_sm_string
    - coref_chain = cur_i_id
    - mention_type = cur_sm_type,
    - is_continuous = is_continuous
    - is_singleton = is_singleton
    - score = float(-1)
    """
    train_extract_tokens = []
    """
    This list includes all tokens (selected or not) in train set.
    Each element corresponds to a token.
    There is a "" element between 2 sentence.
    e.g.::
        [
            '', 
            '1_10ecb\t0\t0\tPerennial\t-', 
            '1_10ecb\t0\t1\tparty\t-', 
            '1_10ecb\t0\t2\tgirl\t-', 
            ...
            '1_10ecb\t0\t16\t.\t-', 
            '', 
            '1_10ecb\t3\t0\tA\t-', 
            '1_10ecb\t3\t1\tfriend\tSingleton_HUM_29_1_10ecb',
            ...
        ]  
    """
    dev_extracted_tokens = []
    """
    This list includes all tokens (selected or not) in dev set.
    Each element corresponds to a token.
    There is a "" element between 2 sentence.
    e.g.::
        [
            '', 
            '1_10ecb\t0\t0\tPerennial\t-', 
            '1_10ecb\t0\t1\tparty\t-', 
            '1_10ecb\t0\t2\tgirl\t-', 
            ...
            '1_10ecb\t0\t16\t.\t-', 
            '', 
            '1_10ecb\t3\t0\tA\t-', 
            '1_10ecb\t3\t1\tfriend\tSingleton_HUM_29_1_10ecb',
            ...
        ]  
    """
    test_extracted_tokens = []
    """
    This list includes all tokens (selected or not) in test set.
    Each element corresponds to a token.
    There is a "" element between 2 sentence.
    e.g.::
        [
            '', 
            '1_10ecb\t0\t0\tPerennial\t-', 
            '1_10ecb\t0\t1\tparty\t-', 
            '1_10ecb\t0\t2\tgirl\t-', 
            ...
            '1_10ecb\t0\t16\t.\t-', 
            '', 
            '1_10ecb\t3\t0\tA\t-', 
            '1_10ecb\t3\t1\tfriend\tSingleton_HUM_29_1_10ecb',
            ...
        ]  
    """

    # extract mention and token info.
    for file in train_files:
        read_ecb_plus_doc(file[0], file[1], file[2], train_extract_tokens, train_extracted_mentions, parse_all, load_singletons)
    for file in dev_files:
        read_ecb_plus_doc(file[0], file[1], file[2], dev_extracted_tokens, dev_extracted_mentions, parse_all, load_singletons)
    for file in test_files:
        read_ecb_plus_doc(file[0], file[1], file[2], test_extracted_tokens, test_extracted_mentions, parse_all, load_singletons)

    # save token info
    all_tokens = train_extract_tokens + dev_extracted_tokens + test_extracted_tokens
    token_tree = {}
    for cur_token in all_tokens:
        doc_id = cur_token["doc_id"]
        topic_id = re.match("^[0-9]*", doc_id).group()
        if topic_id not in token_tree:
            token_tree[topic_id] = {}
        if doc_id not in token_tree[topic_id]:
            token_tree[topic_id][doc_id] = {}
        sentence_id = int(cur_token["t_sentenceindex"])
        if sentence_id not in token_tree[topic_id][doc_id]:
            token_tree[topic_id][doc_id][sentence_id] = {}
        token_id = int(cur_token["t_tokenindex"])  ##
        token_text = cur_token["t_text"]
        if token_id not in token_tree[topic_id][doc_id][sentence_id]:
            token_tree[topic_id][doc_id][sentence_id][token_id] = {}
        token_tree[topic_id][doc_id][sentence_id][token_id]["token_text"] = token_text
        token_tree[topic_id][doc_id][sentence_id][token_id]["token_len"] = len(token_text)
    for topic_id in token_tree.keys():
        for doc_id in token_tree[topic_id].keys():
            for sentence_id in token_tree[topic_id][doc_id].keys():
                cur_sentence = token_tree[topic_id][doc_id][sentence_id]
                t_id_list = cur_sentence.keys()
                t_id_list = sorted(t_id_list)
                last = -1
                for t_id in t_id_list:
                    cur_token = cur_sentence[t_id]
                    cur_token["sentence_level_index"] = [
                        last+1,  # 第一个1是空格，第二个1是开头
                        last+1+cur_token["token_len"]
                    ]
                    last = last+1+cur_token["token_len"]

    # mention info is saved in json file.i.e. ECB_Train/Dev/Test_Event/Entity_gold_mentions.json
    all_mentions = train_extracted_mentions + dev_extracted_mentions + test_extracted_mentions

    #
    return [token_tree, all_mentions]


# ################上边的主要改编自Barhom2019##############
# ################下边的是新代码##########################
def info_from_ecbpxml(
        ecbp_path: str = r"data\raw\ECBplus",
        csv_path: str = r"data\raw\ECBplus_coreference_sentences.csv"):
    file_to_selected_sentence = read_selected_sentences(csv_path)
    [token_tree, all_mentions] = read_corpora(
        file_to_selected_sentence=file_to_selected_sentence,
        parse_all=False, load_singletons=True, corpus_path=ecbp_path)
    return [token_tree, all_mentions]


def corpus_from_ecbpxml(
        ecbp_path: str = r"data\raw\ECBplus",
        csv_path: str = r"data\raw\ECBplus_coreference_sentences.csv"
) -> Corpus:
    """
    读取ecb+语料库，生成Corpus对象。

    ecb+语料库中涉及离散指称。
    例如“turn it off”中的“turn off”被标注为一个mention。
    但是Corpus对象暂时还不支持（主要是Raw.__getitem__不支持）。
    所以在把ecb+语料存到Corpus对象时，进行了简化。
    即对离散指称，只保留其第一个连续部分，即“turn”。

    本方法涉及后缀转换，例如ecb+中的1_ecb.xml对应1_ecb.raw.txt。

    :param ecbp_path: ecb+语料根文件夹路径。
    :param csv_path: ecb+语料中ECBplus_coreference_sentences.csv文件的路径。
    :return: 基于ecb+语料库构建的Corpus obj。
    """
    from nlp_platform.center.raw import Raw
    from nlp_platform.center.node import Node
    from nlp_platform.center.nodepool import NodePool
    from nlp_platform.center.instance import Instance
    from nlp_platform.center.instancepool import InstancePool
    from nlp_platform.center.corpus import Corpus
    #
    [token_tree, mention_list] = info_from_ecbpxml(ecbp_path=ecbp_path, csv_path=csv_path)
    # 对每个token，基于句级index，生成文档级index
    for topic_id in token_tree.keys():
        for doc_id in token_tree[topic_id].keys():
            last = -1
            for sentence_id in token_tree[topic_id][doc_id].keys():
                cur_sentence = token_tree[topic_id][doc_id][sentence_id]
                for t_id in cur_sentence.keys():
                    cur_token = cur_sentence[t_id]
                    cur_token["doc_level_index"] = [
                        last+1,  # 第一个1是空格，第二个1是开头
                        last+1+cur_token["token_len"]
                    ]
                    last = last+1+cur_token["token_len"]
                    del cur_token
                del t_id
                del cur_sentence
            del sentence_id
            del last
        del doc_id
    del topic_id
    # 生成corpus
    c = Corpus()
    # 生成raw
    raw = {}
    for topic_id in token_tree.keys():
        if topic_id not in raw:
            raw[topic_id] = {}
        for doc_id in token_tree[topic_id].keys():
            doc_id_raw_txt = doc_id + ".raw.txt"
            if doc_id not in raw[topic_id]:
                raw[topic_id][doc_id_raw_txt] = ""
            doc_text = []
            for sentence_id in token_tree[topic_id][doc_id].keys():
                cur_sentence = token_tree[topic_id][doc_id][sentence_id]
                cur_sentence_tokens = []
                for t_id in cur_sentence.keys():
                    cur_token = cur_sentence[t_id]
                    cur_sentence_tokens.append(cur_token["token_text"])
                    del cur_token
                    del t_id
                doc_text.append(" ".join(cur_sentence_tokens))
                del cur_sentence, cur_sentence_tokens
                del sentence_id
            raw[topic_id][doc_id_raw_txt] = "\n".join(doc_text)
            del doc_text
            del doc_id, doc_id_raw_txt
        del topic_id
    raw = Raw(raw)
    c.raw = raw
    # 生成node（mention）
    node_list = []
    for cur_mention in mention_list:
        # mention的topic_id
        topic_id = re.match("^[0-9]*", cur_mention.doc_id).group()
        # mention的doc_id
        doc_id = cur_mention.doc_id
        # mention的sentence_index
        if doc_id[-4:] == "plus":
            sentence_index = cur_mention.sent_id + 1
        else:
            sentence_index = cur_mention.sent_id
        # mention的index_str
        token_id_list = cur_mention.tokens_number
        token_id_group = []
        i = 0
        while True:
            if i >= len(token_id_list):
                break
            # find start
            start = token_id_list[i]
            # find end
            while True:
                if i+1 >= len(token_id_list):
                    break
                elif (token_id_list[i]+1 != token_id_list[i+1]):
                    break
                i += 1
            end = token_id_list[i]
            token_id_group.append([start, end])
            i += 1
            del start, end
        del i
        token_index_str = []
        for cur_group in token_id_group:
            start = token_tree[topic_id][doc_id][sentence_index][cur_group[0]]['doc_level_index'][0]
            end = token_tree[topic_id][doc_id][sentence_index][cur_group[1]]['doc_level_index'][1]
            token_index_str.append(f"{start}-{end}")
            del start, end
        token_index_str = ";".join(token_index_str)
        del token_id_group, token_id_list, cur_group
        if ";" in token_index_str:  # 简化离散指称（就是对3-5;7-8仅保留第一个组3-5）
            token_index_str = re.match("^[^;]*(?=;)", token_index_str).group()
        # node
        n_id = f"n:{topic_id}/{doc_id+'.raw.txt'}:{token_index_str}"
        cur_node = Node(info={"id": n_id})
        if raw[n_id] != cur_mention.tokens_str:
            pass  # value error是因为n_id支持了离散指称，但是node.__get_item__()还不支持。
        c.np.add(cur_node)
        del topic_id, doc_id, sentence_index, cur_node, token_index_str
        # instance
        if cur_mention.coref_chain[:9] != "Singleton":
            cur_instance = Instance(info={"id": "i:"+cur_mention.coref_chain}, pool=c.ip)
            t = list(cur_instance["mentions"]["value"])  # Relation Label的value是ReportList类型，此类型不支持修改。所以这里先给搞成一般List。
            t.append(n_id)
            cur_instance["mentions"]["value"] = t
            del cur_instance
        del cur_mention, n_id
    return c

