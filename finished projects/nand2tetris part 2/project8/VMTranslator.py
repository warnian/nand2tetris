#VM Main

'''main file for VM translator
    uses ParserVM and CodeWriter
    correctly translated all project 7 files
    succesfully translated project 8:
        BasicFunction.vm
        BasicLoop.vm
        FibonacciSeries.vm
'''

import shutil
import os
import sys

from ParserVM import ParserVM
from CodeWriter import CodeWriter

def VMTranslator():
    
    inputArg=str(sys.argv[1])
    directory_flag=False
    if inputArg.endswith('.vm'): #IE single file
        
        inputfile=inputArg
        parser=ParserVM(inputfile)
        coder=CodeWriter(inputfile)
        
    else: #IE directory
        outputfile_name=inputArg+'.asm'
        
        cur_directory=os.getcwd()+'/'+inputArg #creates file path for making a list of file in directory
        directory_flag=True
        
        
        if os.path.exists(cur_directory): # if directory exists, continue
            os.chdir(cur_directory) #make current working directory 
            file_list=os.listdir(cur_directory) #creates list of file in directory
            
            for filename in file_list:
                if filename.endswith('.vm'):
                    parser=ParserVM(filename)
                    coder=CodeWriter(filename)
                    
                    
                    for i in range(len(parser.linelist)): 
                        
                        parser.advance()
                        
                        if parser.commandType()=='C_ARITHMETIC':
                            coder.writeArithmetic(parser.arg1())
                            
                        elif parser.commandType()=='C_PUSH' :
                            coder.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())
                            
                        elif parser.commandType()== 'C_POP':
                            coder.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())

                        elif parser.commandType()=='C_LABEL':
                            coder.writeLabel(parser.arg1())

                        elif parser.commandType()=='C_GOTO':
                        
                            coder.writeGoto(parser.arg1())

                        elif parser.commandType()=='C_IF':
                            coder.writeIf(parser.arg1())

                        elif parser.commandType()=='C_FUNCTION':
                            coder.writeFunction(parser.arg1(),parser.arg2())

                        elif parser.commandType()=='C_CALL':
                            coder.writeCall(parser.arg1(),parser.arg2())

                        elif parser.commandType()=='C_RETURN':
                            coder.writeReturn()
            
                else:
                    continue
            
            #concatonate file together here
            new_list=os.listdir(cur_directory) #contains .asm files (hopefully)
            asm_list=[]
            for entry in new_list:

                if entry.endswith('.asm'):
                    asm_list.append(entry)

            
            #mainLines=[]
            
        else:
            print('Directory not found')
            raise(FileNotFoundError)
    #main code below, only translates one file at a time
    for i in range(len(parser.linelist)): 
        
        parser.advance()
        
        if parser.commandType()=='C_ARITHMETIC':
            coder.writeArithmetic(parser.arg1())
            
        elif parser.commandType()=='C_PUSH' :
            coder.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())
            
        elif parser.commandType()== 'C_POP':
            coder.writePushPop(parser.commandType(),parser.arg1(),parser.arg2())

        elif parser.commandType()=='C_LABEL':
            coder.writeLabel(parser.arg1())

        elif parser.commandType()=='C_GOTO':
           
            coder.writeGoto(parser.arg1())

        elif parser.commandType()=='C_IF':
            coder.writeIf(parser.arg1())

        elif parser.commandType()=='C_FUNCTION':
            coder.writeFunction(parser.arg1(),parser.arg2())

        elif parser.commandType()=='C_CALL':
            coder.writeCall(parser.arg1(),parser.arg2())

        elif parser.commandType()=='C_RETURN':
            coder.writeReturn()
    coder.close()
    
    if directory_flag==True:
        
        with open(outputfile_name,'w') as wfd:
            
            #could not get my IO for writeInit working so here it is manually entered
            wfd.write('@256'+'\n')
            wfd.write('D=A'+'\n')
            wfd.write('A=0'+'\n')
            wfd.write('M=D'+'\n')
            wfd.write('//call Sys.init 0 ''\n')
            wfd.write('@return-address'+'\n')
            wfd.write('D=A'+'\n')
            wfd.write('@SP'+'\n')
            wfd.write('A=M'+'\n')
            wfd.write('M=D'+'\n')
            wfd.write('@SP'+'\n')
            wfd.write('M=M+1'+'\n')
            #push local //copied from STATIC PUSH ABOVE
            wfd.write('//push LCL'+'\n') #writes comments in .asm language telling you command given before assembly code is generated
            wfd.write('@LCL'+'\n') #accesses address of index
            wfd.write('D=M'+'\n') #sets the address  into D reg
            wfd.write('@SP'+'\n') #gets address if index
            wfd.write('A=M'+'\n') #adds base *sp to index value and puts it into D reg
            wfd.write('M=D'+'\n')
            wfd.write('@SP'+'\n') #accesses SP
            wfd.write('M=M+1'+'\n') #incements value of SP by 1
            #push argument 
            wfd.write('//push ARG'+'\n') #writes comments in .asm language telling you command given before assembly code is generated
            wfd.write('@ARG'+'\n') #accesses address of index
            wfd.write('D=M'+'\n') #sets the address  into D reg
            wfd.write('@SP'+'\n') #gets address if index
            wfd.write('A=M'+'\n') #adds base *sp to index value and puts it into D reg
            wfd.write('M=D'+'\n')
            wfd.write('@SP'+'\n') #accesses SP
            wfd.write('M=M+1'+'\n') #incements value of SP by 1
            #push this
            wfd.write('//push THIS'+'\n') #writes comments in .asm language telling you command given before assembly code is generated
            wfd.write('@THIS'+'\n') #accesses address of index
            wfd.write('D=M'+'\n') #sets the address  into D reg
            wfd.write('@SP'+'\n') #gets address if index
            wfd.write('A=M'+'\n') #adds base *sp to index value and puts it into D reg
            wfd.write('M=D'+'\n')
            wfd.write('@SP'+'\n') #accesses SP
            wfd.write('M=M+1'+'\n') #incements value of SP by 1
            #push that
            wfd.write('//push THAT'+'\n') #writes comments in .asm language telling you command given before assembly code is generated
            wfd.write('@THAT'+'\n') #accesses address of index
            wfd.write('D=M'+'\n') #sets the address  into D reg
            wfd.write('@SP'+'\n') #gets address if index
            wfd.write('A=M'+'\n') #adds base *sp to index value and puts it into D reg
            wfd.write('M=D'+'\n')
            wfd.write('@SP'+'\n') #accesses SP
            wfd.write('M=M+1'+'\n') #incements value of SP by 1
            #ARG=SP-numArgs-5
            wfd.write('@SP'+'\n')
            wfd.write('D=M'+'\n')#*sp into D reg
            wfd.write('@0'+'\n')#go to @ num Args reg
            wfd.write('D=D-A'+'\n')#ie SP-numArgs into D
            wfd.write('@5'+'\n')
            wfd.write('D=D-A'+'\n')#ie SP-numArgs-5 into D
            wfd.write('@ARG'+'\n')
            wfd.write('M=D'+'\n')#ARG=SP-numArgs-5
            #LCL=SP
            wfd.write('@SP'+'\n')
            wfd.write('D=M'+'\n')#*sp
            wfd.write('@LCL'+'\n')
            wfd.write('M=D'+'\n')#LCL=SP
            #goto functionName copied from goto
            wfd.write('@Sys.init'+'\n')
            wfd.write('0;JMP'+'\n')
            #(return-address)
            wfd.write('(return-address)'+'\n')
            for f in asm_list:
                print(f)
                if inputArg in f:
                    continue
                
                with open(f,'r') as fd:
                    shutil.copyfileobj(fd, wfd)
            
    


                    
            
        
            

    
VMTranslator()
        





