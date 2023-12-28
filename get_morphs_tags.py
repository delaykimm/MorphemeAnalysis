#!/usr/bin/env python3
# coding: utf-8

import sys

def get_morphs_tags(tagged):
    tagged_list = tagged.split("+")
    result = []
    for tags in tagged_list:
        ## 외교+통상부 => 외교/NNG++/SW+통상부/NNG => ['외교/NNG', , '/SW','통상부/NNG'] 일 때
        ## ['외교/NNG', '/SW', '통상부/NNG'] -> ['외교/NNG', '+/SW', '통상부/NNG']
        if tags == '':
            del tags
            continue

        if tags[0:3]=='/SW':  ## +/SW case 예외 처리('++')
            tags = '+'+ tags

        ## tags =='외교/NNG' -> tags_split == ['외교', 'NNG']
        #### 치약/마모제 => 치약/NNG+//SP+마모제/NNG => ['치약/NNG', '//SP', '마모제/NNG']
        #### tags == '//SP' -> tags_split == ['', '', 'SP'] -> tags_split == ['/', 'SP']
        tag_split = tags.split("/")

        if tag_split[0]=='': ## //SP case 예외 처리
            tag_split[0] = '/'
            del tag_split[1]

        morph = tag_split[0]
        tag = tag_split[1]
        comp = (morph,tag)  # tuple 생성
        result.append(comp)

    return result

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as fin:

        for line in fin.readlines():

            # 2 column format
            segments = line.split('\t')

            if len(segments) < 2: 
                continue

            # result : list of tuples (morpheme, tag)
            # "결과/NNG+는/JX" : [('결과', 'NNG'), ('는', 'JX')]
            result = get_morphs_tags(segments[1].rstrip())
        
            for morph, tag in result:
                print(morph, tag, sep='\t')
