#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import get_morphs_tags as mf

###############################################################################
# 색인어 추출
def get_index_terms( mt_list):
    """ 형태소 분석 결과(형태소-품사 쌍)로부터 색인어를 추출
    색인어는 품사가 일반명사(NNG), 고유명사(NNP), 영어(SL), 숫자(SN), 한자(SH)이어야 함
    동일 어절 내에서 인접하여 결합된 경우도 색인어로 추출해야 함 (복합어)

    mt_list: a list of tuples (morpheme, tag)
    return value: a list of string (색인어 리스트)
    """
    nouns = []
    tag_list = ['NNG', 'NNP', 'SL', 'SN', 'SH']      ## 색인어 품사 list
    morpheme_index_list = []                         ## 색인어에 해당하는 index

    # 색인어에 해당하는 index 모음 리스트 생성
    for i in range(len(mt_list)):
        for tag in tag_list:
            if mt_list[i][1] == tag:
                morpheme_index_list.append(i)

    j = 0
    while(j < len(morpheme_index_list)):
        # 연속되는 명사형태소 개수 세기
        _len = 1
        while(1):
            if(j + _len >= len(morpheme_index_list)):
                break
            if morpheme_index_list[j+_len] == (morpheme_index_list[j]+_len):
                _len += 1
            else:
                break

        complex_word = ''
        for k in range(_len):
            # 단일어 list 추가
            nouns.append(mt_list[morpheme_index_list[j+k]][0])
            complex_word += mt_list[morpheme_index_list[j]+k][0]
        # 복합어 list 추가
        if _len != 1:
            nouns.append(complex_word)
        j += (_len-1)
        j+=1

    return nouns

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    with open( sys.argv[1]) as fin:

        mt_freq = {}
    
        # 2 column format
        for line in fin.readlines():

            segments = line.split('\t')

            if len(segments) < 2:
                continue

            # 형태소, 품사 추출
            # result : list of tuples
            result = mf.get_morphs_tags(segments[1].rstrip())
    
            # 색인어 추출 (명사 및 복합명사 등)
            terms = get_index_terms( result)
        
            # 색인어 출력
            for term in terms:
                print(term)
