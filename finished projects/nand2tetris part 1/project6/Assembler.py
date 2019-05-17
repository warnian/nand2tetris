#THE ALMIGHTY ASSEMBLER COMETH
'''
imports Code.py 
        Parser.py
        SymbolTable.py
0 error handling
whitespace handling in parser.py
'''
import re
import os
from Code import Code
from Parser import Parser
from SymbolTable import SymbolTable

class Assembler():
    NewSymbolAdd=16
    def __init__(self,readfile):
    
        self.readfile=readfile
        self.writefile=readfile.replace('.asm','.hack')#creates new output file named the same as input file but with .hack extension
         
        self.symboltable = SymbolTable()           #populates symbol table
        
    def FirstPass(self):    #grabs (xxx) symbols and notes them in symbol tables with the correct address
        
        firstPassParser=Parser(self.readfile)
        firstPassAddress=0
        while firstPassParser.hasMoreCommands():

            firstPassParser.advance()

            if (firstPassParser.commandType()=='A_COMMAND' or firstPassParser.commandType()=='C_COMMAND'):

                firstPassAddress+=1

            elif firstPassParser.commandType()=='L_COMMAND':
                print(firstPassParser.command)
                self.symboltable.addEntry(firstPassParser.symbol(),firstPassAddress)
        
    def SecondPass(self):

        secondPassParser=Parser(self.readfile)
        outfile=open(self.writefile,'w+')
        code=Code()

        while secondPassParser.hasMoreCommands():
            
            secondPassParser.advance()
            if secondPassParser.commandType()=='A_COMMAND':
                
                if secondPassParser.symbol().isdigit():
                    
                    writeline='0'+('{0:b}'.format(int(secondPassParser.symbol())).zfill(15))
                    outfile.write(writeline+'\n')
                elif self.symboltable.contains(secondPassParser.symbol()): # if symbol is in table write binary to file
                    writeline='0'+'{0:b}'.format(self.symboltable.GetAddress(secondPassParser.symbol())).zfill(15) #makes writeline with 0 (a instruction)+15 bit address of symbol
                    outfile.write(writeline+'\n')
                    
                else: #if symbol is not in table add to table then write to file in binary
                    
                    self.symboltable.addEntry(secondPassParser.symbol(),self.NewSymbolAdd)
                    self.NewSymbolAdd+=1
                    writeline2='0'+'{0:b}'.format(self.symboltable.GetAddress(secondPassParser.symbol())).zfill(15)
                    outfile.write(writeline2+'\n')

            if secondPassParser.commandType()=='C_COMMAND':
                writelineC='111'+code.comp_conv(secondPassParser.comp())+code.dest_conv(secondPassParser.dest())+code.jump_conv(secondPassParser.jump())
                outfile.write(writelineC+'\n')
            '''
            if secondPassParser.commandType()=='L_COMMAND':
                 if self.symboltable.contains(secondPassParser.symbol()):
                    writeline=writeline='0'+('{0:b}'.format(self.symboltable.GetAddress(secondPassParser.symbol())).zfill(15))
                else:
                    continue
                 '''
        
            
        outfile.close()
        
    
def main():
        file_name=input('input file name to be compiled: ')
        assemble=Assembler(file_name)
        print('started...')
        assemble.FirstPass()
        assemble.SecondPass()
        
        print('finished...')
        
main()




                
        





        

        


