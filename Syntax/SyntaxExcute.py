# -*- coding: utf-8 -*-
import os
from pygraphviz import *

currentToken = 0       # 当前指向的词的编号
syntax = []
result = []     # 存储的数据类型为[当前结点，父节点，label，辅助判断]
error = []
cnt_association = 0
cnt_reference = 0
cnt_splitter = 0
cnt_match = 0
input1 = []

# 常量
THREAD = 'Thread(thread identifier end identifier ;)'
FEATURE1 = 'feature(none ;)'
FEATURE2 = 'feature(identifier :)'
PORTSPEC = 'port_spec(;)'
PORTTYPE1 = 'port_type(data port)'
PORTTYPE2 = 'port_type(event data port)'
PORTTYPE3 = 'port_type(event port)'
PARAMETER = 'Parameter(parameter ;)'
IOTYPE1 = 'IOtype(in out)'
IOTYPE2 = 'IOtype(out)'
IOTYPE3 = 'IOtype(in)'
FLOWSPEC1 = 'flow_spec(none ;)'
FLOWSPEC2 = 'flow_spec(indetifier : flow)'
FLOWSOURCESPEC = 'flow_source_spec(source identifier ;)'
FLOWSINKSPEC = 'flow_sink_spec(sink identifier ;)'
FLOWPATHSPEC = 'flow_path_spec(path identifier -> identifier ;)'
ASSOCIATION1 = '(none)'
ASSOCIATION2 = '(identifier access decimal)'
SPLITTER1 = '(=>)'
SPLITTER2 = '(+=>)'
REFERENCE = '(identifier)'

def debug(num):
    print(num)
    print(syntax[currentToken][0])
    os.system('pause')

def excute(input2):
    global currentToken
    global syntax
    global result
    global error
    result = []
    error = []
    currentToken = 0
    syntax = input2
    ans = thread()
    print(str(ans))
    return ans

def match_key_spec(word):
    global currentToken
    global syntax
    global result
    global error
    global input1
    if word == syntax[currentToken][0]:
        currentToken += 1
        return True
    else:
        error.append("The '" + syntax[currentToken][0] + "' is not what we wanted in line " + str(syntax[currentToken][1]) + '!')
        return False

#  [ { { association } } ] 
def match_association(father):
    global currentToken
    global syntax
    global result
    global cnt_match
    cnt_match = cnt_match + 1
    CONSTMATCH = '{ }'+'('+str(cnt_match)+')'
    #debug(4444)
    if syntax[currentToken][0] == '{' and syntax[currentToken+1][0] == 'identifier':
        #debug(5555)
        if not match_key_spec('{'):
            return False
        while True:
            if not association(CONSTMATCH):
                return False
            #debug(1212)
            if syntax[currentToken][0] == '}':
                break
        if match_key_spec('}'):
            #debug(1313)
            result.append([CONSTMATCH, father, '{ }', 0])
            return True
        else:
            return False
    return True

def thread():
    global result
    global input1
    #result.append([THREAD, THREAD, THREAD, 0])

    if not match_key_spec('thread'): 
        return False
    if not match_key_spec('identifier'):
        return False
        
    if match_key_spec('features'):
        result.append(['features', THREAD, 'features',0])
        #debug(111)
        if not feature('features'):
            return False
            
    if match_key_spec('flows'):
        #debug(1111)
        #a23 = flow_spec()
        result.append(['flows', THREAD, 'flows', 0])
        if not flow_spec('flows'):
            return False
            
    if match_key_spec('properties'):
        result.append(['properties ;', THREAD, 'properties ;',0])
        if not association('properties ;'):
            return False
        if syntax[currentToken][0] == ';':
            match_key_spec(';')
        else:
            error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
            return False
                
    if not match_key_spec('end'):
        return False
    if not match_key_spec('identifier'):
        return False
    if syntax[currentToken][0] == ';':
        match_key_spec(';')
    else:
        error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
        return False
    return True

# 最后的问题：port_type和Parameter的区分 -- 已解决
def feature(father):
    #debug(222)
    global currentToken
    global syntax
    global result
    global error
    
    if syntax[currentToken][0] == 'none' and syntax[currentToken+1][0] == ';':
        if not match_key_spec('none'):
            return False
        if syntax[currentToken][0] == ';':
            match_key_spec(';')
        else:
            error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
            return False
        result.append([FEATURE1, father, FEATURE1, 1])     # 第1种feature情况
        return True
    
    if syntax[currentToken][0] == 'identifier' and syntax[currentToken+1][0] == ':':
        if not match_key_spec('identifier'):
            return False
        if not match_key_spec(':'):
            return False
        result.append([FEATURE2, father, FEATURE2, 2])
    else:
        error.append("The '" + syntax[currentToken][0] + "' is not what we wanted in line " + syntax[currentToken][1] + "!")
        return False

    if not io_type(FEATURE2):
        return False
    tmp = 0
    for it in result:
        if it[1] == FEATURE2:
            tmp = it[3]
            break
    
    if syntax[currentToken][0] == 'parameter':
        #result.append([FEATURE2, father, 2])      # 第2种feature情况
        if tmp == 1:
            return parameter(IOTYPE1)
        elif tmp == 2:
            return parameter(IOTYPE2)
        elif tmp == 3:
            return parameter(IOTYPE3)
    elif syntax[currentToken][0] == 'event' or syntax[currentToken][0] == 'data':
        #result.append([FEATURE2, father, 3])      # 第3种feature情况
        if tmp == 1:
            return port_spec(IOTYPE1)
        elif tmp == 2:
            return port_spec(IOTYPE2)
        elif tmp == 3:
            return port_spec(IOTYPE3)  
    else:
        return False

def port_spec(father):
    global result
    result.append([PORTSPEC, father, PORTSPEC, 0])
    #debug(555)
    if not port_type(PORTSPEC):
        #print('error')
        return False
    if not match_association(PORTSPEC):
        return False
    #debug(777)
    if syntax[currentToken][0] == ';':
        match_key_spec(';')
    else:
        error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
        return False
    return True 

def port_type(father):
    global currentToken
    global syntax
    global result
    
    if syntax[currentToken][0] == 'data' and syntax[currentToken+1][0] == 'port':
        if not match_key_spec('data'):
            return False
        if not match_key_spec('port'):
            return False
        result.append([PORTTYPE1, father, PORTTYPE1, 1])       # 第1种情况
        if syntax[currentToken][0] == 'identifier':
            if not reference(PORTTYPE1):
                return False
        return True
    elif syntax[currentToken][0] == 'event' and syntax[currentToken+1][0] == 'data' and syntax[currentToken+2][0] == 'port':
        if not match_key_spec('event'):
            return False
        if not match_key_spec('data'):
            return False
        if not match_key_spec('port'):
            return False
        result.append([PORTTYPE2, father, PORTTYPE2, 2])       # 第2种情况
        if syntax[currentToken][0] == 'identifier':
            if not reference(PORTTYPE2):
                return False
        return True
    elif syntax[currentToken][0] == 'event' and syntax[currentToken+1][0] == 'port':
        if not match_key_spec('event'):
            return False
        if not match_key_spec('port'):
            return False
        result.append([PORTTYPE3, father, PORTTYPE3, 3])       # 第3种情况
        return True
    else:
        return False

def parameter(father):
    global result
    result.append([PARAMETER, father, PARAMETER, 0])
    if not match_key_spec('parameter'):
        return False
    if syntax[currentToken][0] == 'identifier':
            if not reference(PARAMETER):
                return False 
    if not match_association(PARAMETER):
        return False
    #debug(1414)
    if syntax[currentToken][0] == ';':
        match_key_spec(';')
    else:
        error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
        return False
    return True

def io_type(father):
    global currentToken
    global syntax
    global result
    
    #debug(23333)
    if syntax[currentToken][0] == 'in' and syntax[currentToken+1][0] == 'out':
        if not match_key_spec('in'):
            return False
        if not match_key_spec('out'):
            return False
        #debug(23334)
        result.append([IOTYPE1, father, IOTYPE1, 1])    # 第1种情况
        return True
    elif syntax[currentToken][0] == 'out':
        if not match_key_spec('out'):
            return False
        result.append([IOTYPE2, father, IOTYPE2, 2])    # 第2种情况
        return True
    elif syntax[currentToken][0] == 'in':
        if not match_key_spec('in'):
            return False
        result.append([IOTYPE3, father, IOTYPE3, 3])    # 第3种情况
        return True
    else:
        return False

def flow_spec(father):
    global result
    
    if syntax[currentToken][0] == 'none':    
        if not match_key_spec('none'):
            return False
        if syntax[currentToken][0] == ';':
            match_key_spec(';')
        else:
            error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
            return False
        result.append([FLOWSPEC1, father, FLOWSPEC1, 1])      # 第1种情况
        return True

    if not match_key_spec('identifier'):
        return False
    if not match_key_spec(':'):
        return False
    if not match_key_spec('flow'):
        return False

    result.append([FLOWSPEC2, father, FLOWSPEC2, 4])
    #debug(2222)
    if syntax[currentToken][0] == 'source':
        #result.append(['flow_spec', father, 2])      # 第2种情况
        if not flow_source_spec(FLOWSPEC2):
            return False
    elif syntax[currentToken][0] == 'sink':
        #result.append(['flow_spec', father, 3])      # 第3种情况
        if not flow_sink_spec(FLOWSPEC2):
            return False
    elif syntax[currentToken][0] == 'path':
        #result.append(['flow_spec', father, 4])      # 第4种情况
        if not flow_path_spec(FLOWSPEC2):
            return False    
    return True

def flow_source_spec(father):
    global result
    result.append([FLOWSOURCESPEC, father, FLOWSOURCESPEC, 0])
    if not match_key_spec('source'):
        return False
    if not match_key_spec('identifier'):
        return False
        #debug(3333)
    if not match_association(FLOWSOURCESPEC):
        return False
    if syntax[currentToken][0] == ';':
        match_key_spec(';')
    else:
        error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
        return False
    return True

def flow_sink_spec(father):
    global result
    result.append([FLOWSINKSPEC, father, FLOWSINKSPEC, 0])
    if not match_key_spec('sink'):
        return False
    if not match_key_spec('identifier'):
        return False
    if not match_association(FLOWSINKSPEC):
        return False
    if syntax[currentToken][0] == ';':
        match_key_spec(';')
    else:
        error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
        return False
    return True

def flow_path_spec(father):
    global result
    result.append([FLOWPATHSPEC, father, FLOWPATHSPEC, 0])
    if not match_key_spec('path'):
        return False
    if not match_key_spec('identifier'):
        return False
    if not match_key_spec('->'):
        return False
    if not match_key_spec('identifier'):
        return False
    if syntax[currentToken][0] == ';':
        match_key_spec(';')
    else:
        error.append("A ';' is wanted in line " + str(syntax[currentToken][1]) + '!')
        return False
    return True

def association(father):
    global currentToken
    global syntax
    global result
    global cnt_association
    cnt_association += 1
    CONSTNUM = '('+str(cnt_association)+')'
    CONSTASSOCIATION = 'association'+CONSTNUM+ASSOCIATION2

    if syntax[currentToken][0] == 'none':
        result.append(['association'+CONSTNUM+ASSOCIATION1, father, 'association'+ASSOCIATION1, 1])       # 第1种情况
        return match_key_spec('none')
    
    if syntax[currentToken+1][0] == '::':
        if not match_key_spec('identifier'):
            return False
        if not match_key_spec('::'):
            return False
        result.append(['identifier ::'+CONSTNUM, CONSTASSOCIATION, 'identifier ::', 0])
    #debug(6666)
    if syntax[currentToken][0] == 'identifier':
        if not match_key_spec('identifier'):
            return False
        result.append([CONSTASSOCIATION, father, 'association'+ASSOCIATION2, 2])       # 第2种情况
        #debug(7777)
        if not splitter(CONSTASSOCIATION):
            return False
        #debug(8888)
        if syntax[currentToken][0] == 'constant':
            if not match_key_spec('constant'):
                return False
            result.append(['constant'+CONSTNUM, CONSTASSOCIATION, 'constant', 0])
        #debug(9999)
        if not match_key_spec('access'):
            return False
        
        if match_key_spec('decimal'):
            #debug(1010)
            return True
        else:
            return False   
    else:
        return False
    
def splitter(father):
    global syntax
    global currentToken
    global result
    global cnt_splitter
    cnt_splitter += 1
    CONSTNUM = '('+str(cnt_splitter)+')'
    
    if syntax[currentToken][0] == '=>':
        result.append(['splitter'+CONSTNUM+SPLITTER1, father, 'splitter'+SPLITTER1, 1])      # 第1种情况
        return match_key_spec('=>')
    elif syntax[currentToken][0] == '+=>':
        result.append(['splitter'+CONSTNUM+SPLITTER2, father, 'splitter'+SPLITTER2, 2])      # 第2种情况
        return match_key_spec('+=>')
        

def reference(father):
    global syntax
    global currentToken
    global result
    global cnt_reference
    cnt_reference += 1
    CONSTNUM = '('+str(cnt_reference)+')'

    result.append(['reference'+CONSTNUM+REFERENCE, father, 'reference'+REFERENCE, 0])
    if syntax[currentToken+1][0] == '::':
        CONSTQ = "'"
        while True:
            if syntax[currentToken][0] == 'identifier' and syntax[currentToken+1][0] == '::':
                if not match_key_spec('identifier'):
                    return False
                if not match_key_spec('::'):
                    return False
                result.append(['identifier :: '+CONSTQ, 'reference'+CONSTNUM+REFERENCE, 'identifier :: ', 0])
            else:
                break
            CONSTQ = CONSTQ + "'"
    if match_key_spec('identifier'):
        return True
    else:
        return False

def draw(result, name):
    g = AGraph(ranksep = '0.7')
    for it in result[:]:
        if not it[0] in g:
            g.add_node(it[0], label = it[2])
    #g.add_node()
    for it in result[:]:
        g.add_edge(it[1], it[0])
    g.node_attr['shape'] = 'box'
    g.edge_attr['color'] = 'red'
    g.node_attr['fontsize'] = 16
    g.layout(prog='dot')
    g.draw(name)

def launch(input_file_path, output_file_path):
    global currentToken
    global syntax
    global result
    global error
    global input1

    file = open(input_file_path)
    output = open(output_file_path, 'w+')
    #input1 = []     # 存储[type, word]
    input2 = []     # 存储words
    cnt = 1
    flag = False    # 判断词法错误
    while True:
        line = file.readline()
        #print (line)
        line = line.strip('\n')
        if not line:
            break
        if flag:
            if line != '$':
                #flag = False
                continue
        
        #print(line)
        if line == '$':
            #print(input2)
            if error:       # 有词法错误，输出到错误文件中
                #print (error)
                output.write('False\n')
                output.write(error[0] + '\n')
                os.system('pause')
            if not flag:    # 如果没有词法错误，则进行语法分析
                ans = excute(input2)
                output.write(str(ans) + '\n')
                #print(result)
                
                name = 'Thread' + str(cnt) + '.jpg'
                if error:       # 如果存在语法错误，输出错误到错误文档中
                    output.write(error[0] + '\n')
                else:
                    draw(result, name)
                cnt += 1
                os.system('pause')
            input1 = []
            input2 = []
            error = []
            flag = False
            cnt_association = 0
            cnt_reference = 0
            cnt_splitter = 0
            cnt_match = 0
            continue
            #break
        line = line.split(',')
        if line[0] == 'error':
            error.append('There is a lexical error(\'' + line[1] + '\') in line ' + str(line[2]) + '!')
            flag = True
            continue
        #input1.append(line[2])      # 用于存储行号
        input2.append([line[0], line[2]])      # 用于存储词法分析后的结果和行号
    
    output.close()
    file.close()

if __name__ == '__main__':
    input_file_path1 = 'test1_tokenOut.txt'
    input_file_path3 = 'test3_tokenOut.txt'
    output_file_path1 = 'test1_syntaxOut.txt'
    output_file_path3 = 'test3_syntaxOut.txt'

    launch(input_file_path1, output_file_path1)
    launch(input_file_path3, output_file_path3)