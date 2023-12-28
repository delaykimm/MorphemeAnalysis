#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import get_morphs_tags as mf
import get_index_terms as term
import pickle

###############################################################################
def indexing_tagged(indexing, sentences, filename):
    """ 형태소 분석 파일로부터 색인 정보를 생성 (역색인, 문장)
    indexing : 역색인 dictionary (key : index term, value : set of sentences)
    sentences : 색인된 문장 리스트
    filename : 형태소 분석 파일
    """
    sentence_index = 10000 * int(filename[2:4])
    with open(filename) as fin:
        sentence = ''
        for line in fin.readlines():

            # 2 column format
            segments = line.split('\t')
            segments[0] = segments[0].rstrip() # 형태소

            if len(segments) < 2:  # 하나의 문장이 끝남
                sentence = sentence[:-1]  # 마지막에 추가된 space 제거
                if sentence !='':
                    sentences.append(sentence)  # 색인된 문장 리스트에 추가
                    sentence_index += 1
                sentence= '' # 문장 리셋
                continue

            sentence += segments[0]  # 분석된 형태소들을 하나의 문장으로 연결
            sentence += ' '

            # 형태소, 품사 추출
            # result : list of tuples
            result = mf.get_morphs_tags(segments[1].rstrip())

            # 색인어 추출 (명사 및 복합명사 등)
            terms = term.get_index_terms(result)

            # 역색인 리스트 만들기
            for word in terms:
                if word not in indexing.keys():  # dict에 색인어 없을 때 index 집합 추가
                    indexing[word] = set([sentence_index])
                else:
                    indexing[word].add(sentence_index)  # 기존 색인어 존재, index만 집합 추가
    fin.close()
    return 0

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    inverted_indexing = {}
    sentences = []
    
    for filename in sys.argv[1:]:
        indexing_tagged( inverted_indexing, sentences, filename)

    with open("index.pickle","wb") as fout:
        pickle.dump((inverted_indexing, sentences), fout)