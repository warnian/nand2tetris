#ParserVM.py
#parser for vm for nand2tetris project 7 and 8
#Spec found in book in chapter 7.3.3
'''
API:

Constructor 
Takes input file and prepares it for parsing
Init command as blank ==''

hasMoreCommands 
Returns boolean of value of morelines in the file
ie true for if more lines false if no more lines

advance
Reads the next command from input and makes it current command
called only if hasMoreCommands() == True

commandType
returns the type of the VM command C_Arithmetic is returned for all aritmetic/logic commands
return values:
-------------- PROJECT 7 PARTS BELOW
C_ARITHMETIC
C_PUSH
C_POP
-------------- PROJECT 8 PARTS BELOW
C_LABEL
C_GOTO
C_IF
C_FUNCTION
C_RETURN
C_CALL
--------------

arg1
Returns the first argument of the current command in the case of C_ARITHEMETIC the command itself is returned
(add, sub etc.)
EG for push constant 1 returns push constant
should not be called if current command is C_RETURN

arg2
returns the second argument of the current command is C_PUSH, C_POP, C_FUNCTION OR C_CALL
s=

Re using material from project 6 for assembly translator
'''
import re
import os
from CodeWriter import CodeWriter
class ParserVM():
    
    C_ARITHMETIC_LIST = ['add','sub','neg','eq','gt','lt','and','or','not']

    def __init__(self,readfile):

        #init variables
        
        self.linelist=[]
        self.command=''
        self.cur_line=0
        with open(readfile) as infile:
            for line in infile:
                line=line.split('//',1)[0] #removes comments
                line=line.strip()     #removes trailing and leading whitespace
                line=' '.join(re.split('\s+',line)) #removes duplicate white space
                if line!='':
                    self.linelist.append(line)  #only appends non empty lines
                    
        

    def hasMoreCommands(self):
        
        if (self.cur_line) < len(self.linelist): #if current line is less then length of line list keep going
            return True
        else:
            return False

    def advance(self):
        if self.hasMoreCommands()==True:
            self.command=self.linelist[self.cur_line] #grabs current line
            self.cur_line+=1 #advance current line by 1
    
    def commandType(self):
        #Project 7 below
        
        if 'push' in self.command:
            return 'C_PUSH'
        if 'pop' in self.command:
            return 'C_POP'
        if 'label' in self.command:
            return 'C_LABEL'
        if 'goto'in self.command and 'if' not in self.command:
            return 'C_GOTO'
        if 'if' in self.command and 'goto' in self.command:
            return 'C_IF'
        if 'function' in self.command:
            return 'C_FUNCTION'
        if 'call' in self.command:
            return 'C_CALL'
        if 'return' in self.command:
            return 'C_RETURN'
        else:
        
            for val in self.C_ARITHMETIC_LIST:
                if val in self.command:
                    
                    return 'C_ARITHMETIC'
                
    def arg1(self):
        
        if self.commandType()=='C_ARITHMETIC': #something wrong here not triggering arithmetic
            return self.command
            
        else: #ie push pop etc.
            temp=self.command.split(' ') #possible error for future commands (works for push pop in project 7)
            return temp[1]
         
    def arg2(self): 
        # only call if there is a second arg 
        if self.commandType()=='C_PUSH' or 'C_POP' or 'C_FUNCTION' or 'C_CALL':
            try:
                temp=int(self.command.split(' ')[2]) #gets second value of op EG for push constant 2 -----> 2  #turns into integer as shown in spec
                return temp
            except:
                pass
        elif self.commandType()!='C_PUSH' or 'C_POP' or 'C_FUNCTION' or 'C_CALL':
            return 'arg2 error: wrong commandtype'
    
            
        


            

        


