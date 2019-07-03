#Jack Analyzer module for project 10 and 11 nand2teris
#top level driver thats sets up and invokes other modules (main module)
#implementation found in section 10.3.1

'''
three steps for main file
1. Create a JackTokenizer from the Xxx.jack input file
2. Creat an oututfile called Xxx.xml and prepare it for writing
3. Use the CompilationEngine to compile the input JackTokenizer into the output file
'''
import os
import sys
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

def JackCompiler():
    #debug input6
    #inputArg='Seven'

    #command line input arg
    inputArg=str(sys.argv[1])
    
    if inputArg.endswith('.jack'): #IE single file
        outputfile=inputArg.replace('.jack','.vm')
        inputfile=inputArg
        Compiler=CompilationEngine(inputfile,outputfile)
        Compiler.close()
        
    else: #IE directory
        
        
        cur_directory=os.getcwd()+'/'+inputArg #creates file path for making a list of file in directory
        
        
        
        if os.path.exists(cur_directory): # if directory exists, continue
            os.chdir(cur_directory) #make current working directory 
            file_list=os.listdir(cur_directory) #creates list of file in directory
            
            for filename in file_list:
                if filename.endswith('.jack'):
                    outputfile=filename.replace('.jack','.vm')
                    Compiler=CompilationEngine(filename,outputfile)
                    Compiler.close()
JackCompiler()