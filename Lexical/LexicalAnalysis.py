#-*- coding: utf-8 -*-
import os
from Excute import solve

def LexicalAnalysis(input_file_path, output_file_path):
    #input_file_path = './input/test2.txt'
    file = open(input_file_path)
    #output_file_path = 'test2_result.txt'
    output = open(output_file_path, 'w+')
    row = 1

    while 1:
        line = file.readline()
        if not line:
            break
    
        result, error = solve(line, row)
        if len(result) == 0 and len(error) == 0:
            row += 1
            continue
        str_result = []
        str_error  = []

        line_num = 'Line ' + str(row) + ':\n'
        str_result.append(line_num)
        str_result.append('    Correct:\n')
        for it in result:
            tmp = ', '.join(it)
            str_result.append('        ['+tmp+']\n')
        for it in str_result:
            output.write(it)
        
        str_error.append('    Error:\n')
        for it in error:
            tmp = ' '.join(it)
            str_error.append('        '+tmp+'\n')
        for it in str_error:
            output.write(it)
        output.write('\n')
        #output.write(str_error)
        #print('result------------------', result)
        #print('error-------------------', error)

        
        #os.system("pause")
        row += 1


    output.close()
    file.close()

if __name__ == '__main__':
    input_file_path1 = './input/test1.txt'
    input_file_path2 = './input/test2.txt'
    input_file_path3 = './input/test3.txt'
    output_file_path1 = 'test1_tokenOut.txt'
    output_file_path2 = 'test2_tokenOut.txt'
    output_file_path3 = 'test3_tokenOut.txt'
    LexicalAnalysis(input_file_path1, output_file_path1)
    LexicalAnalysis(input_file_path2, output_file_path2)
    LexicalAnalysis(input_file_path3, output_file_path3)
