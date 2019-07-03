#JackTokenizer module for project 10 and 11 in nand2tetris
#acts as toeknizer for compiler, separates lines of code into symbols
#implementation in section 10.3.2 of book
# removes all comment and white space from the input stream and breaks it into jack language tokemns as specified by the jack grammar

'''
API:

Constructor 
    takes input file as arg
    has not return
    opens the input file and gets ready to tokenize it

hasMoreTokens
    takes no args
    returns boolean if there are more tokens to proces

advance
    takes no args
    has no returns
    Gets the next token from the input and makes it the current token
    should only be called if hasMoreTokens()=True
    initially sets no token

tokenType
    takes no args
    returns: KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
    returns the type of the certain token

keyWord
    takes no args
    returns: CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN, CHAR, VOID,
                VAR, STATIC, FIELD, LET, DO, IF, ELSE, WHILE, RETURN, TRUE, FALSE,
                 NULL, THIS
    returns the keyword which is the current token.
        should be called only when tokenType()=Keyword

symbol 
    takes no args
    returns the character which is the current token
    should only be called when tokenType() is SYMBOL

identifier 
    takes no args
    returns a String
    returns the identifer which is the current token
    should be called only when tokenType() is IDENTIFIER

intVal 
    takes no args
    returns the integer value of the current token 
    should be called only when tokenType() is INT_CONST

stringVal
    takes no args
    returns the string value of the current token
    should only be called when tokenType() is STRING_CONST

'''
#start
import os
import re
class JackTokenizer():
    keywordTokens=['class','constructor','return','function','method','field','static','var','int','char'
                ,'boolean','void','true','false','null','this','let','do','if','else','while']
    symbolTokens=['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
    operators=['+','-','*','/','&','|','<','>','=','~','&amp;','&lt;','&gt;']
    def __init__(self,readfile):
        self.outfilename=readfile.replace('.jack','T.xml')
        self.token=''
        self.cur_line=''
        self.linelist=[]
        self.tokenlist=[]
        self.string_flag=False
        self.token_index=0
        #reads in file while removing whitespace and comments, taken from previous VMTranslator project08
        #currently does not handle multiline /*
        
        with open(readfile) as infile:
            for line in infile:
                line=line.split('//',1)[0] #removes comments
                line=line.split('/*',1)[0] #removes first line of /*
                line=line.split('*       ',1)[0]
                line=line.split('*/',1)[0]
                line=line.strip()     #removes trailing and leading whitespace
                line=' '.join(re.split('\s+',line)) #removes duplicate white space
                if line!='':
                    if not line.startswith('*'):
                        self.linelist.append(line)  #only appends non empty lines
        
        #now we have linelist with all of the lines in it wiht no white space and no empty
        #have to parse it now to identify individual tokens, probably not the most efficient algorithm rougly O(a*b*c)
        for element in self.linelist:
            for character in element: #marches through each character in element
                #gets string token, once it sees a " it appends everything in between that and next " and continues IE skips characters until next "
                if character=='"':
                    #if we are in a string continue (ie skips character) also sets string flag equal to false and waits for next "
                    if self.string_flag==True:
                        self.string_flag=False
                        continue
                    self.string_flag=True
                    self.tokenlist.append('<stringConstant> '+element.split('"',2)[1]+' </stringConstant>')
                #if we are in a string skips those characters  
                if self.string_flag==True:
                    continue       

                #gets the rest of non symbol non string tokens 
                elif character not in self.symbolTokens:
                    
                    #general method for getting token
                    if character !=' ':
                        self.token+=character #builds up tokens as long as no space and no symbol
                    #end of token push to tokenlist
                    elif character == ' ':
                        if self.token!='':
                            if self.tokenType()=='KEYWORD':
                               
                                self.tokenlist.append('<keyword> '+self.token+' </keyword>')
                                self.token=''
                            elif self.tokenType()=='INT_CONST':
                                self.tokenlist.append('<integerConstant> '+self.token+' </integerConstant>')
                                self.token=''
                            
                            else:
                                self.tokenlist.append('<identifier> '+self.token+' </identifier>')
                                self.token=''
                            

                #gets symbol tokens
                if character in self.symbolTokens:
                        if self.token!='':
                            if self.token in self.keywordTokens:
                                
                                    self.tokenlist.append('<keyword> '+self.token+' </keyword>')
                                    self.token=''
                            else:
                                if self.tokenType()=='INT_CONST':
                                    self.tokenlist.append('<integerConstant> '+self.token+' </integerConstant>')
                                    self.token=''
                                else:
                                    self.tokenlist.append('<identifier> '+self.token+' </identifier>')
                                    self.token=''
                        if character=='>':
                            self.tokenlist.append('<symbol> '+'&gt;'+' </symbol>')  
                        elif character=='<':
                            self.tokenlist.append('<symbol> '+'&lt;'+' </symbol>')  
                        elif character=='&':
                            self.tokenlist.append('<symbol> '+'&amp;'+' </symbol>')  
                        else:
                            self.tokenlist.append('<symbol> '+character+' </symbol>')        

        #writes tokentlist to file for debug
        with open (self.outfilename,'w') as outfile:
            outfile.write('<tokens>'+'\n')
            for element in self.tokenlist:
                
                outfile.write(element+'\n')
            outfile.write('</tokens>')

    
    def hasMoreTokens(self):
        if (self.token_index) < len(self.tokenlist): 
            return True
        else:
            return False

    def advance(self):
        # I think according to the lectures Professor Schocken intended for my method above of creating a token list to be inside here. 
        # I did it in the init but the overall effect is the same, it just makes my init more complicated and simplies this
        
        if self.hasMoreTokens()==True:
            self.token=self.tokenlist[self.token_index]
            self.token_index+=1
            
    
    
    
    def tokenType(self):
        if self.token in self.keywordTokens:
            return 'KEYWORD'
        elif self.token in self.symbolTokens:
            return 'SYMBOL'
        elif (self.token).isdigit():
            return 'INT_CONST'
        elif '"' in self.token:
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'
    
    def keyWord(self):
        if self.tokenType()=='KEYWORD':
            return self.token.upper()
    
    def symbol(self):
        if self.tokenType()=='SYMBOL':
            return(self.token)
    
    def identifier(self):
        if self.tokenType()=='IDENTIFIER':
            return(self.token)
    
    def intVal(self):
        if self.tokenType()=='INT_CONST':
            return(self.token)
    
    def stringval(self):
        if self.tokenType()=='STRING_CONST':
            
            return (self.token)
    
    def getToken(self):
        
        return self.token
    def getStrToken(self):
        return self.token.split(' ',2)[1]
    def isOp(self):
        newToken=self.token.split(' ',2)[1]
        
        for element in self.operators:
            if element in newToken:
                return True
        else:
            return False
    def peek(self):
        peek_index=self.token_index
        try:
            peek=self.tokenlist[peek_index]
        except:
            peek=''
        return peek
    def peek_back(self):
        b_peek_index=self.token_index-1
        try:
            b_peek=self.tokenlist[b_peek_index]
        except:
            b_peek=''
        return b_peek
    def double_peek(self):
        d_peek_index=self.token_index+1
        try:
            d_peek=self.tokenlist[d_peek_index]
        except:
            d_peek=''
        return d_peek
    def printDebug(self):
        print('hello')
        
        print(self.tokenlist)
    