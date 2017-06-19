#-*- coding: utf-8 -*-

import re
import os

TRUE = 1
FALSE = 0

def solve(line, row):
    result = []
    words = []
    st = 0
    ed = 0
        
    #print(line)
    length = len(line)
    if line[length-1] != '\n':
        line = line + '\n'
    for i in range(len(line)):
        # 处理先变量后符号（向words中添加变量）
        if not(line[i] == ' ' or line[i] == '\n' or line[i] == '\t' or line[i] == '\r' or\
        line[i] == '=' or line[i] == '+' or line[i] == ';' or line[i] == ':' or\
        line[i] == '{' or line[i] == '}' or line[i] == '-') and\
        (line[i+1] == ' ' or line[i+1] == '\n' or line[i+1] == '\t' or line[i+1] == '\r' or\
        line[i+1] == '=' or line[i+1] == '+' or line[i+1] == ';' or line[i+1] == ':' or\
        line[i+1] == '{' or line[i+1] == '}' or line[i+1] == '-'):
            ed = i + 1
            words.append(line[st:ed])
            st = ed
        # 单独处理;
        elif line[i] == ';' or line[i] == '{' or line[i] == '}':
            words.append(line[i])
            st = i + 1
            ed = i + 1
        # 处理先符号后变量（向words中添加符号）
        elif (line[i] == '>' or line[i] == ':') and\
        (identifier_letter(line[i+1]) == TRUE or digit(line[i+1]) == TRUE or \
        line[i+1] == ' ' or line[i+1] == '\n' or line[i+1] == '\t' or line[i+1] == '\r'):
            ed = i + 1
            words.append(line[st:ed])
            st = ed
        
        elif st == ed and (line[i] == ' ' or line[i] == '\n' or line[i] == '\t' or line[i] == '\r'):
            st += 1
            ed += 1

        else:
            ed += 1
    
    #print(words)
    #os.system("pause")
    # 检测
    for w_it in words:
        # 判断数字
        if digit(w_it[0]) == TRUE or ((w_it[0] == '+' or w_it[0] == '-') and digit(w_it[1]) == TRUE) or w_it[0] == '.':
            if decimal(w_it) == TRUE:
                result.append(['decimal', w_it])
            else:
                result.append(['error', w_it])
        # 判断id和keyword
        elif identifier_letter(w_it[0]) == TRUE or underline(w_it[0]) == TRUE:
            if identifier(w_it) == TRUE:
                if keywords(w_it) == TRUE:
                    result.append([w_it, w_it]) 
                else:
                    result.append(['identifier', w_it])
            else:
                result.append(['error', w_it])
        # 判断特殊符号
        else:
            if specialSymbol(w_it) == TRUE:
                result.append([w_it, w_it])
            else:
                result.append(['error', w_it])
    
    return result

def identifier(words):
    cnt = 0
    if identifier_letter(words[cnt]) == FALSE:
        return FALSE
    else:
        cnt += 1
    flag = FALSE
    if underline(words[cnt]):
        cnt += 1
    
    if cnt == len(words):
        return TRUE
    elif letter_or_digit(words[cnt]) == TRUE:
        cnt += 1
        for it in words[cnt : ]:
            if flag == TRUE:
                if letter_or_digit(it) == TRUE:
                    cnt += 1
                    flag = FALSE
            elif underline(it) == TRUE:
                cnt += 1
                flag = TRUE
            elif letter_or_digit(it) == TRUE:
                cnt += 1           
            else:
                break
        if cnt == len(words):
            return TRUE       
    else:
        return FALSE      

def decimal(words):         # 判断是否为浮点数，是TRUE，否FALSE
    if sign(words[0]) == TRUE:
        istart = 1
    elif digit(words[0]) == TRUE:
        istart = 0
    else:
        return FALSE
    #print('istart------',istart)
    
    if words.find('.') == -1:
        return FALSE
    dotNum = words.index('.')

    #print('dotNum------',dotNum)
    
    t_words = words[istart : dotNum]
    if numeral(t_words) == FALSE:
        return FALSE
    t_words = words[dotNum+1 : ]
    if numeral(t_words) == FALSE:
        return FALSE

    return TRUE    


def sign(word):                 # +-为TRUE否则为FALSE
    if word == '-' or word == '+':
        return TRUE
    else:#
        return FALSE

def numeral(words):             # 检查某个字符串是否是纯数字
    for it in words:
        if words == '':
            #print("REEOR: words are empty!")
            return FALSE
        elif digit(it) == FALSE:
            #print("REEOR: words are not a number!")
            return FALSE
    return TRUE

def letter_or_digit(word):      # 数字或字母TRUE
    if word.isdigit() == TRUE or word.isalpha() == TRUE: 
        return TRUE
    else:
        return FALSE

def identifier_letter(word):     # 判断是否字母
    if word.isalpha():
        return TRUE
    else:
        return FALSE

def digit(word):     # 判断是否数字
    if word.isdigit():
        return TRUE
    else:
        return FALSE

def underline(word):        # 检查下划线
    if word != '_':
        return FALSE
    else:
        return TRUE

def dot(word):              # 检查小数点
    if word != '.':
        return FALSE
    else:
        return TRUE

def specialSymbol(words):         # 检查8个专用符号=>  +=>  ;  :  ::  {  }  ->
    if words == '=>' or words == '+=>' or words == ';' or words == ':' or\
       words == '::' or words == '{' or words == '}' or words == '->':
        return TRUE
    else:
        return FALSE

def keywords(words):
    if words == 'thread' or words == 'features' or words == 'flows' or words == 'properties' or\
       words == 'end' or words == 'none' or words == 'in' or words == 'out' or\
       words == 'data' or words == 'port' or words == 'event' or words == 'parameter' or\
       words == 'flow' or words == 'source' or words == 'sink' or words == 'path' or\
       words == 'constant' or words == 'access':
        return TRUE
    else:
        return FALSE

if __name__ == '__main__':
    #print(decimal('50'))
    result = solve('end Thread6;', 1)