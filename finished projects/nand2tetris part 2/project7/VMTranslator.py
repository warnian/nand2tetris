#VM Main

'''main file for VM translator
    uses ParserVM and CodeWriter
'''
import os
import sys
from ParserVM import ParserVM
from CodeWriter import CodeWriter

def VMTranslator():
    inputfile=str(sys.argv[1])
    parser=ParserVM(inputfile)
    coder=CodeWriter(inputfile)
    coder.setFileName(inputfile)
    count=0
    while count< len(parser.linelist): 
        parser.advance()
        
        if parser.commandType()=='C_ARITHMETIC':
            
            coder.writeArithmetic(parser.arg1())
            count+=1
        elif parser.commandType()=='C_PUSH' :
            
            coder.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())
            count+=1
        elif parser.commandType()== 'C_POP':
            
            coder.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())
            count+=1
    coder.close()
VMTranslator()
        





