#Parser.py parses machine language code and returns various components; fields and smybols
#Chapter 6.3 from book is where spec comes from
""" parts are:
    init 
        input file returns nothing, prepares file for reading'
    hasMoreCommands
        checks for more commands in input
    advance
        reads next command from input and makes it current command
        should be called only if hasmore commands is true
        
    command type{
        takes command and determines if it is A Command for @xxx where xxx is number or smybol
        C command for dest=comp;jmp
        L command for pseudo command (xxx) eg (LOOP) (END)
        
    symbol{
     returns the symbol or decimal xxx of the current command @xxx 
     only used when a command or l command
    Dest 
        returns dest mnemonic in current c command when c command
        8 possibiliites
    comp
        returns comp mnemonic only when c command
        28 possibilities
    jump
        returns jump mnemonic only when c command
        8 possibilities
    """
import os
import re

class Parser():
    """
    dest_list = ['','M','D','MD','A','AM','AD','AMD']

    jump_list = ['','JGT','JEQ','JGE','JLT','JNE','JLE','JMP']

    comp_list = ['0','1','-1','D','A','!D','!A','-D','-A','D+1','A+1','D-1','A+1','D-1','A-1','D+A','D-A','A-D','D&A','D|A','M','!M','-M','M+1','M-1','D+M','D-M','M-D','D&M','D|M']
    """
    def __init__(self, readfile):
        
        with open(readfile, 'r') as infile:  #reads in file, counts lines
            
            self.lines=infile.readlines()
            self.linelist=[]
        for item in self.lines:       #white space removal
            item=item.strip()
            self.linelist.append(item)
            
        self.command = ''      #initilizes command as blank
        self.line=0     #initilize line count as 0
    def hasMoreCommands(self):
        
        if (self.line) < len(self.linelist):
            return True
        else:
            return False
    def advance(self):
        
        
        if self.hasMoreCommands()==True:
            self.command=self.linelist[self.line]
            self.line+=1

    def commandType(self):
        if '@' in self.command:
            return 'A_COMMAND'
        if '('and')' in self.command:
            return 'L_COMMAND'
        if '=' or ';' in self.command:
            return 'C_COMMAND'
    def symbol(self):
        if (self.commandType()=='A_COMMAND' or self.commandType()=='L_COMMAND'):
          return re.sub('[@()]','',self.command)
    def dest(self):
        if self.commandType()=='C_COMMAND' and '=' in self.command:  #if C command returns anything before '=' ie dest mnemonic
            return self.command.split('=')[0]
    def jump(self):
        if self.commandType()=='C_COMMAND' and ';' in self.command:   #if C command returns anything after ';' ie jump command mnemonic
            return self.command.split(';')[1]
    def comp(self):
        if self.commandType()=='C_COMMAND': #if C Command replaces ';' with '=' and then returns string after first '=' ie comp
            if '=' in self.command:
                temp=self.command.replace(';','=') #doesnt work for command nwith no dest eg D;JGT
                return temp.split('=')[1]
            elif '=' not in self.command:
                return self.command.split(';')[0]






    



    
        



        
        
