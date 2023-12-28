#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

_CHO_ = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
_JUNG_ = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
_JONG_ = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ' # index를 1부터 시작해야 함

# 겹자음 : 'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ'
# 겹모음 : 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ'

_JAMO2ENGKEY_ = {  # index 0~18: 자음, 19~39: 모음
 'ㄱ': 'r',
 'ㄲ': 'R',
 'ㄴ': 's',
 'ㄷ': 'e',
 'ㄸ': 'E',
 'ㄹ': 'f',
 'ㅁ': 'a',
 'ㅂ': 'q',
 'ㅃ': 'Q',
 'ㅅ': 't',
 'ㅆ': 'T',
 'ㅇ': 'd',
 'ㅈ': 'w',
 'ㅉ': 'W',
 'ㅊ': 'c',
 'ㅋ': 'z',
 'ㅌ': 'x',
 'ㅍ': 'v',
 'ㅎ': 'g',
 'ㅏ': 'k',
 'ㅐ': 'o',
 'ㅑ': 'i',
 'ㅒ': 'O',
 'ㅓ': 'j',
 'ㅔ': 'p',
 'ㅕ': 'u',
 'ㅖ': 'P',
 'ㅗ': 'h',
 'ㅘ': 'hk',
 'ㅙ': 'ho',
 'ㅚ': 'hl',
 'ㅛ': 'y',
 'ㅜ': 'n',
 'ㅝ': 'nj',
 'ㅞ': 'np',
 'ㅟ': 'nl',
 'ㅠ': 'b',
 'ㅡ': 'm',
 'ㅢ': 'ml',
 'ㅣ': 'l',
 'ㄳ': 'rt',
 'ㄵ': 'sw',
 'ㄶ': 'sg',
 'ㄺ': 'fr',
 'ㄻ': 'fa',
 'ㄼ': 'fq',
 'ㄽ': 'ft',
 'ㄾ': 'fx',
 'ㄿ': 'fv',
 'ㅀ': 'fg',
 'ㅄ': 'qt'
}

def distinguish_jamo(ch): # 자음인지 모음인지 알려주는 함수(영어음절이 아닐 때는 return none)
    # index 0~18: 자음, 19~39: 모음, ch: 알파벳
    if ch in list(_JAMO2ENGKEY_.values()): # 자음/모음
        index = list(_JAMO2ENGKEY_.values()).index(ch)
        if 0 <= index <= 18:
            jamo = 'ja'
        elif 19 <= index <= 39:
            jamo = 'mo'
    else: # 특수문자
        jamo = None
    return jamo

###############################################################################
def is_hangeul_syllable(ch):
    '''한글 음절인지 검사
    '''
    if not isinstance(ch, str):
        return False
    elif len(ch) > 1:
        ch = ch[0]
    
    return 0xAC00 <= ord(ch) <= 0xD7A3

###############################################################################
def compose(cho, jung, jong):
    '''초성, 중성, 종성을 한글 음절로 조합
    cho : 초성
    jung : 중성
    jong : 종성
    return value: 음절
    '''
    if not (0 <= cho <= 18 and 0 <= jung <= 20 and 0 <= jong <= 27):
        return None
    code = (((cho * 21) + jung) * 28) + jong + 0xAC00

    return chr(code)

###############################################################################
# input: 음절
# return: 초, 중, 종성
def decompose(syll):
    '''한글 음절을 초성, 중성, 종성으로 분해
    syll : 한글 음절
    return value : tuple of integers (초성, 중성, 종성)
    '''
    if not is_hangeul_syllable(syll):
        return (None, None, None)
    
    uindex = ord(syll) - 0xAC00

    jong = uindex % 28
    jung = ((uindex - jong) // 28) % 21
    cho = ((uindex - jong) // 28) // 21

    return (cho, jung,jong)

###############################################################################
def str2jamo(str):
    '''문자열을 자모 문자열로 변환 ex. ('닭고기' -> 'ㄷㅏㄺㄱㅗㄱㅣ')
    '''
    jamo = []
    for ch in str:
        if is_hangeul_syllable(ch):
            cho, jung, jong = decompose(ch)
            jamo.append( _CHO_[cho])
            jamo.append( _JUNG_[jung])
            if jong != 0:
                jamo.append( _JONG_[jong-1])
        else:
            jamo.append(ch)
    return ''.join(jamo)

# 자모 문자열을 키입력 문자열로 변환 ('ㄷㅏㄺㄱㅗㄱㅣ' -> 'ekfrrhrl')
def jamo2engkey(jamo_str):
    engkey = []
    for jamo in jamo_str:
        if jamo not in list(_JAMO2ENGKEY_.keys()):  # 한글이 아닐 때 그대로 입력받음
            engkey.append(jamo)
        else:
            engkey.append(_JAMO2ENGKEY_[jamo])  ## 'ㄷ' -> 'e'
    return ''.join(engkey)

# 키입력 문자열을 자모 문자열로 변환 ('ekfrrhrl' -> 'ㄷㅏㄹㄱㄱㅗㄱㅣ')
def engkey2jamo(engkey):
    jamo_str = []
    for eng in engkey:
        if not eng in list(_JAMO2ENGKEY_.values()): # 숫자/특수문자일 때 그대로 입력받음
            jamo_str.append(eng)
        else:
            index = list(_JAMO2ENGKEY_.values()).index(eng)
            jamo_str.append(list(_JAMO2ENGKEY_.keys())[index])
    return ''.join(jamo_str)

# 음절 조합 default 설정값
cho = 19  # out of index
jung = 21
jong = 0  # 받침이 없는 경우

def make_start_state():  # start 상태로 만드는 함수
    global cho,jung,jong
    cho = 19
    jung = 21
    jong = 0

def check_start():  # start 상태인지 확인하는 함수
    if cho == 19 and jung ==21 and jong == 0:
        return True
    else:
        return False
def cho_setting(ch): # 초성 설정해주는 함수
    index = list(_JAMO2ENGKEY_.values()).index(ch)
    hangeul = list(_JAMO2ENGKEY_.keys())[index]
    _cho = _CHO_.index(hangeul)
    return _cho

def jung_setting(ch): # 중성 설정해주는 함수
    index = list(_JAMO2ENGKEY_.values()).index(ch)
    hangeul = list(_JAMO2ENGKEY_.keys())[index]
    _jung = _JUNG_.index(hangeul)
    return _jung

def jong_setting(ch): # 종성 설정해주는 함수
    index = list(_JAMO2ENGKEY_.values()).index(ch)
    hangeul = list(_JAMO2ENGKEY_.keys())[index]
    _jong = _JONG_.index(hangeul) +1
    return _jong

# 자모 문자열을 음절열로 변환 ('ㄷㅏㄹㄱㄱㅗㄱㅣ' -> '닭고기')
def jamo2syllable(jamo_str): # 자모 문자열 -> 키문자열 -> 음절열
    syll_str = []  # default 음절열
    global cho, jung, jong
    engkey = jamo2engkey(jamo_str) # 'ㄷㅏㄹㄱㄱㅗㄱㅣ' -> 'ekfrrhrl'
    i = 0
    while(i < len(engkey)):
        if check_start() == True: # 시작상태일 때
            if engkey[i] not in list(_JAMO2ENGKEY_.values()): # 특수문자일 때 그대로 출력
                syll_str.append(engkey[i])
            elif distinguish_jamo(engkey[i])== 'mo':  # 모음일 때... 모은 케이스 처리 후에도 시작 상태 유지
                try: # in the index :: 뒤에 문자가 존재할 때
                    if (distinguish_jamo(engkey[i+1]) == None) or (distinguish_jamo(engkey[i+1]) == 'ja'): # (모음+자음/특수문자)일 때 모음 출력
                        index = list(_JAMO2ENGKEY_.values()).index(engkey[i])
                        syll_str.append(list(_JAMO2ENGKEY_.keys())[index])
                    else: # (모음+모음)일 때
                        mo2 = engkey[i]+engkey[i+1]
                        if mo2 in list(_JAMO2ENGKEY_.values()):  # 겹모음일 때 겹모음 출력
                            index = list(_JAMO2ENGKEY_.values()).index(mo2)
                            syll_str.append(list(_JAMO2ENGKEY_.keys())[index])
                            i += 1 # 모음 2개를 한 번에 처리했으므로
                        else:                                    # 겹모음이 아닐 때 앞모음만 출력
                            index = list(_JAMO2ENGKEY_.values()).index(engkey[i])
                            syll_str.append(list(_JAMO2ENGKEY_.keys())[index])
                except IndexError: # out of index :: 뒤에 문자가 존재하지 않을 때 모음 그대로 출력
                    index = list(_JAMO2ENGKEY_.values()).index(engkey[i])
                    syll_str.append(list(_JAMO2ENGKEY_.keys())[index])

            elif distinguish_jamo(engkey[i])== 'ja': # 자음일 때
                try: # in the index :: 뒤에 문자가 존재할 때
                    if distinguish_jamo(engkey[i+1]) == None: # (자음+특수문자)일 때 자음 그대로 출력 => 시작상태 유지
                        index = list(_JAMO2ENGKEY_.values()).index(engkey[i])
                        syll_str.append(list(_JAMO2ENGKEY_.keys())[index])
                    elif distinguish_jamo(engkey[i+1]) == 'ja': # (자음+자음)일 때 => 시작상태유지
                        ja2 = engkey[i]+engkey[i+1]
                        if ja2 not in list(_JAMO2ENGKEY_.values()):  # 겹자음이 아니면 앞자음만 출력
                            index = list(_JAMO2ENGKEY_.values()).index(engkey[i])
                            syll_str.append(list(_JAMO2ENGKEY_.keys())[index])
                        else: # 겹자음일 가능성이 존재
                            try: # 뒤에 문자 존재
                                if (distinguish_jamo(engkey[i+2])==None) or (distinguish_jamo(engkey[i+2])=='ja'): # (자음+자음+자음/특수문자) => 겹자음 출력
                                    index = list(_JAMO2ENGKEY_.values()).index(ja2)
                                    syll_str.append(list(_JAMO2ENGKEY_.keys())[index])
                                    i += 1  # 자음 2개를 한 번에 처리했으므로
                                elif distinguish_jamo(engkey[i+2])=='mo': #(자음+자음+모음) => (단자음+초성+중성)
                                    index = list(_JAMO2ENGKEY_.values()).index(engkey[i])
                                    syll_str.append(list(_JAMO2ENGKEY_.keys())[index])
                            except IndexError: # 뒤에 아무 문자도 없음. 겹자음 출력
                                index = list(_JAMO2ENGKEY_.values()).index(ja2)
                                syll_str.append(list(_JAMO2ENGKEY_.keys())[index])
                                i += 1  # 자음 2개를 한 번에 처리했으므로

                    else: # (자음+모음)일 때 => 시작 상태가 파괴된다 # 자음이 초성이 된다 # 모음이 중성이 되지만 겹모음/단모음일지 뒤에 확인필수.
                        cho = cho_setting(engkey[i])
                except IndexError: # out of index :: 뒤에 문자가 존재하지 않을 때 자음 그대로 출력
                    index = list(_JAMO2ENGKEY_.values()).index(engkey[i])
                    syll_str.append(list(_JAMO2ENGKEY_.keys())[index])

        else: # check_start == False : 시작상태가 아닐 때(초성만 설정되어있음)(초성이 설정되어 있을 때, 그 다음은 모음 밖에 올 수 없음)
            try: # in the index 뒤에 문자가 존재할때
                if distinguish_jamo(engkey[i+1])==None: # 모음+특수문자 : (초성+중성) 출력
                    jung = jung_setting(engkey[i])  # 중성 설정
                    syll = compose(cho, jung, jong)  # 음절 변환
                    syll_str.append(syll)  # 변환된 음절 추가
                elif distinguish_jamo(engkey[i+1])=='ja': # (모음+자음)일 때
                    if engkey[i+1] in ['E', 'Q', 'W']: # 뒤에 오는 자음이 ㄸ, ㅃ, ㅉ 중에 하나일 때
                        jung = jung_setting(engkey[i])  # 중성 설정
                        syll= compose(cho,jung,jong)   # 음절 변환
                        syll_str.append(syll)  # 변환된 음절 추가
                    else: # ㄸ,ㅃ,ㅉ가 아닐 때
                        try: # in the index
                            if distinguish_jamo(engkey[i+2]) == None: #(모음+자음+특수문자)
                                jung = jung_setting(engkey[i])  # 중성 설정
                                jong = jong_setting(engkey[i+1])  # 종성 설정
                                syll = compose(cho, jung, jong)  # 음절 변환
                                syll_str.append(syll)  # 변환된 음절 추가
                                i += 1  # 모음+자음 2개 동시 처리
                            elif distinguish_jamo(engkey[i+2]) == 'mo': #(모음+자음+모음)
                                jung = jung_setting(engkey[i])  # 중성 설정
                                syll = compose(cho, jung, jong)  # 음절 변환
                                syll_str.append(syll)  # 변환된 음절 추가
                            elif distinguish_jamo(engkey[i+2]) == 'ja': #(모음+자음+자음)
                                ja2 = engkey[i+1]+engkey[i+2]
                                if ja2 not in list(_JAMO2ENGKEY_.values()): # 겹자음X
                                    jung = jung_setting(engkey[i])  # 중성 설정
                                    jong = jong_setting(engkey[i + 1])  # 종성 설정
                                    syll = compose(cho, jung, jong)  # 음절 변환
                                    syll_str.append(syll)  # 변환된 음절 추가
                                    i += 1  # 모음+자음 2개 동시 처리
                                else: # 겹자음이 가능한 경우
                                    try:
                                        if (distinguish_jamo(engkey[i+3]) == None) or (distinguish_jamo(engkey[i+3]) == 'ja'): # (모음+자음+자음+자음/특수문자)
                                            jung = jung_setting(engkey[i])  # 중성 설정
                                            jong = jong_setting(ja2) # 종성 설정(겹자음)
                                            syll = compose(cho, jung, jong)  # 음절 변환
                                            syll_str.append(syll)  # 변환된 음절 추가
                                            i += 2  # 모음+겹자음 3개 동시 처리
                                        else: #(모음+자음+자음+모음) => 겹자음X
                                            jung = jung_setting(engkey[i])  # 중성 설정
                                            jong = jong_setting(engkey[i + 1])  # 종성 설정(단자음)
                                            syll = compose(cho, jung, jong)  # 음절 변환
                                            syll_str.append(syll)  # 변환된 음절 추가
                                            i += 1  # 모음+단자음 2개 동시 처리

                                    except IndexError: # (모음+자음+자음+끝)
                                        jung = jung_setting(engkey[i])  # 중성 설정
                                        jong = jong_setting(ja2)  # 종성 설정(겹자음)
                                        syll = compose(cho, jung, jong)  # 음절 변환
                                        syll_str.append(syll)  # 변환된 음절 추가
                                        i += 2  # 모음+겹자음 3개 동시 처리
                        except IndexError: # out of index
                            jung = jung_setting(engkey[i])  # 중성 설정
                            jong = jong_setting(engkey[i + 1]) # 종성 설정
                            syll = compose(cho, jung, jong)  # 음절 변환
                            syll_str.append(syll)  # 변환된 음절 추가
                            i +=1 # 모음+자음 동시 처리
                elif distinguish_jamo(engkey[i+1])=='mo': # (모음+모음)일 때
                    mo2 = engkey[i]+engkey[i+1]
                    if mo2 not in list(_JAMO2ENGKEY_.values()) : # 겹모음X
                        jung = jung_setting(engkey[i])  # 중성: 단모음 설정
                        syll = compose(cho,jung,jong)
                        syll_str.append(syll)
                    else: # 겹모음O
                        jung = jung_setting(mo2)  # 중성 : 겹모음 설정
                        try:
                            if (distinguish_jamo(engkey[i+2])==None) or (distinguish_jamo(engkey[i+2])=='mo'): #(초성+겹모음+모음/특수문자)
                                syll = compose(cho, jung, jong)  # 음절 변환
                                syll_str.append(syll)  # 변환된 음절 추가
                                i += 1  # 겹모음 처리
                            elif distinguish_jamo(engkey[i+2])=='ja': #(초성+겹모음+자음)
                                if engkey[i + 2] in ['E', 'Q', 'W']:  # 뒤에 오는 자음이 ㄸ, ㅃ, ㅉ 중에 하나일 때
                                    syll = compose(cho, jung, jong)  # 음절 변환
                                    syll_str.append(syll)  # 변환된 음절 추가
                                    i +=1 # 겹모음 처리
                                else:  # ㄸ,ㅃ,ㅉ가 아닐 때
                                    try:  # in the index
                                        if distinguish_jamo(engkey[i + 3]) == None:  # (겹모음+자음+특수문자)
                                            jong = jong_setting(engkey[i + 2])  # 종성 설정
                                            syll = compose(cho, jung, jong)  # 음절 변환
                                            syll_str.append(syll)  # 변환된 음절 추가
                                            i += 2  # 겹모음+자음 3개 동시 처리
                                        elif distinguish_jamo(engkey[i + 3]) == 'mo':  # (겹모음+자음+모음)
                                            syll = compose(cho, jung, jong)  # 음절 변환
                                            syll_str.append(syll)  # 변환된 음절 추가
                                            i+=1 # 겹모음 동시 처리
                                        elif distinguish_jamo(engkey[i + 3]) == 'ja':  # (겹모음+자음+자음)
                                            ja2 = engkey[i + 2] + engkey[i + 3]
                                            if ja2 not in list(_JAMO2ENGKEY_.values()):  # 겹자음X
                                                jong = jong_setting(engkey[i + 2])  # 종성 설정
                                                syll = compose(cho, jung, jong)  # 음절 변환
                                                syll_str.append(syll)  # 변환된 음절 추가
                                                i += 2  # 겹모음+자음 3개 동시 처리
                                            else:  # 겹자음이 가능한 경우
                                                try:
                                                    if (distinguish_jamo(engkey[i + 4]) == None) or (distinguish_jamo(engkey[i + 4]) == 'ja'):  # (겹모음+자음+자음+자음/특수문자)
                                                        jong = jong_setting(ja2)  # 종성 설정(겹자음)
                                                        syll = compose(cho, jung, jong)  # 음절 변환
                                                        syll_str.append(syll)  # 변환된 음절 추가
                                                        i += 3  # 겹모음+겹자음 4개 동시 처리
                                                    else:  # (겹모음+자음+자음+모음) => 겹자음X
                                                        jong = jong_setting(engkey[i + 2])  # 종성 설정(단자음)
                                                        syll = compose(cho, jung, jong)  # 음절 변환
                                                        syll_str.append(syll)  # 변환된 음절 추가
                                                        i += 2  # 겹모음+단자음 3개 동시 처리
                                                except IndexError:  # (겹모음+자음+자음+끝)
                                                    jong = jong_setting(ja2)  # 종성 설정(겹자음)
                                                    syll = compose(cho, jung, jong)  # 음절 변환
                                                    syll_str.append(syll)  # 변환된 음절 추가
                                                    i += 3  # 겹모음+겹자음 4개 동시 처리
                                    except IndexError:  # out of index
                                        jong = jong_setting(engkey[i + 2])  # 종성 설정
                                        syll = compose(cho, jung, jong)  # 음절 변환
                                        syll_str.append(syll)  # 변환된 음절 추가
                                        i += 2  # 겹모음+자음 3개 동시 처리

                        except IndexError: # (초성+겹모음+끝)
                            syll = compose(cho, jung, jong)  # 음절 변환
                            syll_str.append(syll)  # 변환된 음절 추가
                            i += 1  # 겹모음 처리

            except IndexError: # out of index # 뒤에 문자가 존재하지 않을 때
                jung = jung_setting(engkey[i])  # 중성 설정
                syll = compose(cho, jung,jong)    # 음절 변환
                syll_str.append(syll)             # 변환된 음절 추가

            make_start_state()                # 시작 상태로 만들기
        i+=1

    return ''.join(syll_str)

###############################################################################
if __name__ == "__main__":
    
    i = 0
    line = sys.stdin.readline()

    while line:
        line = line.rstrip()
        i += 1
        print('[%06d:0]\t%s' %(i, line)) # 원문
    
        # 문자열을 자모 문자열로 변환 ('닭고기' -> 'ㄷㅏㄺㄱㅗㄱㅣ')
        jamo_str = str2jamo(line)
        print('[%06d:1]\t%s' %(i, jamo_str)) # 자모 문자열

        # 자모 문자열을 키입력 문자열로 변환 ('ㄷㅏㄺㄱㅗㄱㅣ' -> 'ekfrrhrl')
        key_str = jamo2engkey(jamo_str)
        print('[%06d:2]\t%s' %(i, key_str)) # 키입력 문자열
        
        # 키입력 문자열을 자모 문자열로 변환 ('ekfrrhrl' -> 'ㄷㅏㄹㄱㄱㅗㄱㅣ')
        jamo_str = engkey2jamo(key_str)
        print('[%06d:3]\t%s' %(i, jamo_str)) # 자모 문자열

        # 자모 문자열을 음절열로 변환 ('ㄷㅏㄹㄱㄱㅗㄱㅣ' -> '닭고기')
        syllables = jamo2syllable(jamo_str)
        print('[%06d:4]\t%s' %(i, syllables)) # 음절열

        line = sys.stdin.readline()