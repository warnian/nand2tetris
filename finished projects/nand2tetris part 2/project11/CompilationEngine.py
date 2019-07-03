#CompilationEngine module for projects 10 and 11 in nand2tetris
#recursive top down parser
#implementation found in section 10.3 in book
#THIS IMPLEMENTATION DOES NOT CONTAIN THE XML WRITING VERSION THIS IS THE FINAL COMPILER
'''
API:

Constructor 
    takes and Input Stream and an Output stream as arguments
    creates a new compilation engine with the given input and output 
    the next routine called must be complieClass()

CompileClass
    takes no args
    returns nothing 
    compiles a complete class

CompileClassVarDec
    takes no args
    returns nothing
    Compiles a static declation or a field declaration

CompileSubroutine
    takes no args 
    returns nothing
    Compiles a complete method function or constructor
    
CompileParameterList
    takes no args
    returns nothing
    Compiles a (possible empty) parameter list, not include the enclosing '()'

CompileVarDec
    takes no args
    returns nothing
    compiles a var declaration

compileStatements
    takes no args 
    returns nothing
    compiles a sequence of statements not including the enclosing '{}'

compileDo
    takes no args
    returns nothing
    compiles a do statement

compileLet
    compiles a let statement

compileWhile
    compiles a while statement

compileReturn
    compiles a return statement

compileIf 
    compiles an if statement possible with a trailing else clause

compileExpression
    compiles an expression

compileTerm ***big boy
    compiles a term
    if the current token is an identifier the routine must distinguish between a variable an array and a subroutine call
    needs to look ahead sometimes because of '[','(','.' in the next character
    change the function ie:
    x is fine and runs normally
    x[1] is a list which functions differently
    x(4) x is a function call which functions differently
    x.y is a method call which functions differently

    you have to look ahead in order to distinguish which one it is

compileExpressionList
    compiles a (possible empty) comma separated list of expressions'


'''
#main problem with num_indents function infinite looping
import os
from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine():
    vardeclist=['static','field']
    subroutinelist=['constructor','function','method','void']
    statementList=['let','while','if','return','do','turn']
    op_dict={'+':'add','-':'sub','&':'and','|':'or','<':'lt','>':'gt','=':'eq','~':'not','&amp;':'and','&lt;':'lt','&gt;':'gt'}
    running_index=0
    label_index=0
    while_label_index=0
    if_label_index=0
    def __init__(self,inputfile,writefile):
        self.op_flag1=False
        self.op_flag2=False
        self.is_Array=False
        self.ClassName=''
        self.keyword=''
        self.cur_subroutineName=''
        self.sub_return_type=''
        self.running_index=0
        self.array_name=''

        self.Tokenizer=JackTokenizer(inputfile)
        self.SymbolTable=SymbolTable()
        self.infile=inputfile
        self.VMWriter=VMWriter(inputfile.replace('.jack','.vm'))
        self.outfile=open(writefile,'w+')
        self.compileClass()
        

        
        
    def compileClass(self):#draft finished
        print('Compiling started of '+self.infile)
        self.Tokenizer.advance()#starts it, token = 'class'
        if 'class' in self.Tokenizer.getToken():
            
            self.Tokenizer.advance()#token = classname
            self.ClassName=self.Tokenizer.getStrToken()
            self.Tokenizer.advance()#next token = {
            
            #cleaned up from project 10 put while loop in each respective method
            self.compileClassVarDec()
            self.compileSubroutine()
        
            self.Tokenizer.advance()#next token
        else:
            print('error: NO CLASS TO COMPILE')
    
    def compileClassVarDec(self):#finished untested ######WHILE LOOP NOT TURNING ON
        self.Tokenizer.advance() #adv0ance off { to first token in var dec
       
        while 'static' in self.Tokenizer.getStrToken() or 'field' in self.Tokenizer.getStrToken():
           
            kind=self.Tokenizer.getStrToken() #static or 
            self.Tokenizer.advance()#next token advance to type
            type=self.Tokenizer.getStrToken()
            self.Tokenizer.advance()#next token advance to name
            name=self.Tokenizer.getStrToken()
            self.Tokenizer.advance() #advances to either , or ;
           
            self.SymbolTable.define(name,type,kind)
            
            while ';' not in self.Tokenizer.getToken(): #while you havent reached the end of the line
                self.Tokenizer.advance()#advances to next token which is hopefully a name
                name=self.Tokenizer.getStrToken()
                self.SymbolTable.define(name,type,kind)
                
                self.Tokenizer.advance() #advances to either , or ;
                
            #have reached ;
            self.Tokenizer.advance()#next token
        
    def compileSubroutine(self):#draft finished
        #contains subroutine DEc and subroutine Body
        #something fucked up here
        #return_is_void=False
        while 'constructor' in self.Tokenizer.getStrToken() or 'method' in self.Tokenizer.getStrToken() or 'function' in self.Tokenizer.getStrToken():
            constructor_flag=False
            method_flag=False
            self.SymbolTable.startSubroutine()
            if 'constructor' in self.Tokenizer.getStrToken():
                constructor_flag=True
            if 'method' in self.Tokenizer.getStrToken():
                method_flag=True
            #current token right now should be either constructor, method, or function
            self.Tokenizer.advance() #advances to type of return eg int
            self.sub_return_type=self.Tokenizer.getStrToken()
            self.Tokenizer.advance()#next token advances to subroutine name (should be new if constructor)
            self.cur_subroutineName=self.ClassName+'.'+self.Tokenizer.getStrToken()
            if 'method' in self.Tokenizer.getStrToken():
                self.SymbolTable.define('this',self.sub_return_type,'argument')
            self.Tokenizer.advance()#next token advances to (
            self.compileParameterList()
            #after parameter list finishes token is )
            self.Tokenizer.advance()#next token advances to {
            
            #starts subroutine body
            self.Tokenizer.advance() #advances to start of subroutine body First token there
            #moved while loop below into compileVardec
            #while 'var' in self.Tokenizer.getToken():
            self.compileVarDec()
            
            
            self.VMWriter.writeFunction(self.cur_subroutineName,self.SymbolTable.varCount('var')) #calls function related to parent class, if its a function all good. if its method or constructor more has to happen
            self.if_label_index=0
            if constructor_flag==True:
                self.VMWriter.writePush('constant',self.SymbolTable.varCount('field'))#pushes the constructors fields onto stack for however many fields there are
                self.VMWriter.writeCall('Memory.alloc',1)
                self.VMWriter.writePop('pointer',0)
            elif method_flag==True:
                self.VMWriter.writePush('argument',0)
                self.VMWriter.writePop('pointer',0) #init this
                
            
            
            #compile the rest of subroutine
            self.compileStatements()
            #current token after should be }
            self.Tokenizer.advance() #next statement constructor and method function if not breaks out of while loop
           
    def compileParameterList(self): #draft finished
    
        while ')' not in self.Tokenizer.getToken(): 
            self.Tokenizer.advance() #advance to type of parameter or ) in case of no param
            if ')' not in self.Tokenizer.getStrToken(): #parameter here to parameter stuff
                if ',' not in self.Tokenizer.getStrToken():
                    type=self.Tokenizer.getStrToken()
                    self.Tokenizer.advance()#advances to name
                    name=self.Tokenizer.getStrToken()
                    self.Tokenizer.advance()#advances to either comma or end of list start loop over
                    
                    self.SymbolTable.define(name,type,'argument')
            else:
                return # ')' is token, function is done

        
    def compileVarDec(self): #draft
        
        while 'var' in self.Tokenizer.getToken():
            
            if 'var'in self.Tokenizer.getToken():
                self.Tokenizer.advance()#advances to type
                type=self.Tokenizer.getStrToken()
                self.Tokenizer.advance() #advances to name
                name=self.Tokenizer.getStrToken()
                self.SymbolTable.define(name,type,'var')#appends to symbol table
                self.Tokenizer.advance()#advances to either ,  or ;

                while ';' not in self.Tokenizer.getToken():
                    self.Tokenizer.advance() #advances to name
                    name=self.Tokenizer.getStrToken()
                    self.SymbolTable.define(name,type,'var')
                    self.Tokenizer.advance()#next token advances to either , or ;
                
                self.Tokenizer.advance()#next token var if more vars or done if not
                
    def compileStatements(self): #finished
        
        while  'if' or 'let' or 'while' or 'do' or 'return' in self.Tokenizer.getStrToken():
                    
                    if 'let' in self.Tokenizer.getToken():
                        self.compileLet()
                        
                    elif 'while' in self.Tokenizer.getToken():
                        self.compileWhile()
                        
                    elif 'if' in self.Tokenizer.getToken():
                        self.compileIf()
                    
                    elif 'do' in self.Tokenizer.getToken():
                        self.compileDo()
                    
                    elif 'return' in self.Tokenizer.getToken():
                        
                        self.compileReturn()
                    else:
                        
                        break   
        
    def compileCall(self): #finished untested
        #do without pop temp 0
        #next token to function/method name
        doCallName=self.Tokenizer.getStrToken()
        
        self.Tokenizer.advance()#advances to '.' or '('
        if '.' in self.Tokenizer.getToken():
            if doCallName in self.SymbolTable.SubSymbolTable: #ie method like square.move()
                self.Tokenizer.advance()
                subName=self.Tokenizer.getStrToken()
                self.Tokenizer.advance()#next token '('
                self.Tokenizer.advance()#first expression
                self.compileExpressionList() 
                
                nArgs=self.running_index #running index added whenever expression called in expression list +1 for this
                self.running_index=0 #resets index
                self.VMWriter.writePush(self.SymbolTable.kindOf(doCallName),self.SymbolTable.indexOf(doCallName)) #pushes 'this' of object onto stack
                
                self.VMWriter.writeCall(self.SymbolTable.typeOf(doCallName)+'.'+subName,nArgs)
                return

            else: #ie function like Keyboard.keyPressed() Sys.wait(5) basically same thing except you dont push this on stack
                
                self.Tokenizer.advance()
                subName=self.Tokenizer.getStrToken()
                self.Tokenizer.advance()#next token '('
                self.Tokenizer.advance()
                self.compileExpressionList()
                nArgs=self.running_index #running index added whenever expression called in expression list
                #resets index
                self.running_index=0 
                if doCallName in self.SymbolTable.ClassSymbolTable:
                    self.VMWriter.writePush('this',nArgs-1)
                    self.VMWriter.writeCall(self.SymbolTable.typeOf(doCallName)+'.'+subName,nArgs)
                else:
                    if doCallName=='Keyboard':
                        self.VMWriter.writeCall(doCallName+'.'+subName,nArgs-1)
                    else:
                        self.VMWriter.writeCall(doCallName+'.'+subName,nArgs)

        if '(' in self.Tokenizer.getToken(): #method call like do clear()
            self.Tokenizer.advance()#token is first token in expression list
            self.compileExpressionList()
            nArgs=self.running_index
            self.running_index=0
            self.VMWriter.writePush('pointer',0) #pushes this
            
            self.VMWriter.writeCall(self.ClassName+'.'+doCallName,nArgs) 
        
    def compileDo(self): 
        self.Tokenizer.advance()
        self.compileCall()
        self.Tokenizer.advance()
        self.Tokenizer.advance()
        self.VMWriter.writePop('temp',0)
    #dont think this works for arrays like a[b[c[5]] yet NOT CONFIDENT ON THIS METHOD
    
    def compileLet(self): 
        #current token is let
        #doesnt work for a[i]
        self.Tokenizer.advance()#now token = varname
        varName=self.Tokenizer.getStrToken()
        self.array_name=self.Tokenizer.getStrToken()
        self.Tokenizer.advance() # = or [
        
        if '[' in self.Tokenizer.getStrToken(): #array, see section 11.1.1 Array Handling for help or unit 5.8 video
            self.is_array=True
            self.compileArrayExp() #compile arrary term
            
            
            self.compileExpression()
            self.VMWriter.writePop('temp',0)
            self.VMWriter.writePop('pointer',1)
            self.VMWriter.writePush('temp',0)
            self.VMWriter.writePop('that',0)
            
        else:
            self.Tokenizer.advance()#expression
            
            self.compileExpression() #eg(5*(3+4))
            
            self.VMWriter.writePop(self.SymbolTable.kindOf(varName),self.SymbolTable.indexOf(varName))#pop expression t
        self.Tokenizer.advance()
        if ';' in self.Tokenizer.getStrToken():
            self.Tokenizer.advance()
        
    def compileWhile(self): #draft I might have the labeling wrong or something
        #at start token = while
        whileLabel='WHILE_EXP'+str(self.while_label_index)
        self.VMWriter.writeLabel(whileLabel)
        self.Tokenizer.advance()#advances to (
        self.compileExpression()#writes expression
        self.VMWriter.writeArithmetic('not')
        self.VMWriter.writeIf('WHILE_END'+str(self.while_label_index))
        while_end_index=self.while_label_index
        self.while_label_index+=1
        if '{' in self.Tokenizer.getStrToken():
            self.Tokenizer.advance()
        
        self.compileStatements() #writes statements
        
        self.VMWriter.writeGoto(whileLabel)
        self.VMWriter.writeLabel('WHILE_END'+str(while_end_index))
        
        self.Tokenizer.advance() #advance to after } ie done with this while
        
    def compileReturn(self):#draft
        
        #starts at token = return
        self.Tokenizer.advance()
        if ';' not in self.Tokenizer.getToken():
            self.compileExpression()
            self.Tokenizer.advance()#advance past ;
        else: #placeholder return
            self.VMWriter.writePush('constant',0)
            self.Tokenizer.advance()
        self.VMWriter.writeReturn()
        self.op_flag2=False
        if ';' in self.Tokenizer.getStrToken():
            self.Tokenizer.advance()
        
        
            
    def compileIf(self):#finished sort of the same as while
        #start token = if
        
        ifLabel='IF_TRUE'+str(self.if_label_index)
        
        
        self.compileExpression()
        
        self.VMWriter.writeIf(ifLabel)
        self.VMWriter.writeGoto('IF_FALSE'+str(self.if_label_index))
        self.VMWriter.writeLabel(ifLabel)
        else_index=self.if_label_index
        self.if_label_index+=1
        if '{' in self.Tokenizer.getStrToken():
            self.Tokenizer.advance()
        
        self.compileStatements()
        self.Tokenizer.advance()
        
        
        if 'else' in self.Tokenizer.getToken():
            self.VMWriter.writeGoto('IF_END'+str(else_index))
            self.VMWriter.writeLabel('IF_FALSE'+str(else_index))
            self.Tokenizer.advance() #advances to {
            self.Tokenizer.advance() #advances to statements
            self.compileStatements()
            self.Tokenizer.advance()
            self.VMWriter.writeLabel('IF_END'+str(else_index))
            if '}' in self.Tokenizer.peek():
                self.Tokenizer.advance()
        else: 
            self.VMWriter.writeLabel('IF_FALSE'+str(else_index))
        
        #self.if_label_index
        
        

    def compileExpression(self): #draft
        

        self.compileTerm()
        self.op_flag2=False
        
        self.Tokenizer.advance()
       
        if self.Tokenizer.isOp():
            if '*' in self.Tokenizer.getStrToken():
                
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeCall('Math.multiply',2)
            if '/' in self.Tokenizer.getStrToken():
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeCall('Math.divide',2)
                self.Tokenizer.advance()
                
            if '+' in self.Tokenizer.getStrToken():
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeArithmetic('add')
                self.op_flag2=True
                
            if '&gt' in self.Tokenizer.getStrToken():
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeArithmetic('gt')
                
            if '&amp' in self.Tokenizer.getStrToken():
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeArithmetic('and')
                
            if '|' in self.Tokenizer.getStrToken():
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeArithmetic('or')
            if '&lt' in self.Tokenizer.getStrToken():
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeArithmetic('lt')
            if '=' in self.Tokenizer.getStrToken():
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeArithmetic('eq')
            if '-' in self.Tokenizer.getStrToken():
                self.Tokenizer.advance()
                self.compileTerm()
                self.VMWriter.writeArithmetic('sub')
                
            self.op_flag1=True  
        
        else:
            
            self.op_flag1=False
        ##ie two ops in a row so write this
        
    def compileTerm(self):#unfinished god almighty this thing is gonna kill me
        
        if '[' in self.Tokenizer.peek():
            self.array_name=self.Tokenizer.getStrToken()
            self.Tokenizer.advance() #advances to [
            self.Tokenizer.advance()#advances to inner term
            self.VMWriter.writePush(self.SymbolTable.kindOf(self.Tokenizer.getStrToken()),self.SymbolTable.indexOf(self.Tokenizer.getStrToken()))
            self.VMWriter.writePush(self.SymbolTable.kindOf(self.array_name),self.SymbolTable.indexOf(self.array_name))
            self.Tokenizer.advance()#advances to another term or ]
                
            if ']' not in self.Tokenizer.getStrToken():
                    self.array_name=self.Tokenizer.getStrToken()
                    self.Tokenizer.advance()
                    self.compileTerm()
                    self.VMWriter.writeArithmetic('add')
                    self.VMWriter.writePush('temp',0)
                    self.VMWriter.writePop('pointer',1)
                    self.VMWriter.writePush('temp',0)
                    self.VMWriter.writePop('that',0)
            if ']' in self.Tokenizer.getStrToken():
                    
                    self.VMWriter.writeArithmetic('add')
                    self.VMWriter.writePop('pointer',1)
                    
                    self.VMWriter.writePush('that',0)
                    self.Tokenizer.advance()
            return
            
        if 'integerConstant' in self.Tokenizer.getToken():
            if self.op_flag2==False:
                self.VMWriter.writePush('constant',self.Tokenizer.getStrToken())
            
        elif 'stringConstant' in self.Tokenizer.getToken(): #forums explanation here: http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Project-11-gt-Strings-calling-string-constructor-td4030992.html#a4030993
            string=self.Tokenizer.getToken()
            string=string.replace('<stringConstant> ','')
            string=string.replace(' </stringConstant>','')
            
            self.VMWriter.writePush('constant',len(string))
            self.VMWriter.writeCall('String.new',1)
            for char in string:
                
                self.VMWriter.writePush('constant',ord(char))
                self.VMWriter.writeCall('String.appendChar',2)
            
        elif 'this' in self.Tokenizer.getStrToken():
            self.VMWriter.writePush('pointer',0)
        
        elif 'true' in self.Tokenizer.getStrToken():
            self.VMWriter.writePush('constant', 0)
            self.VMWriter.writeArithmetic('not')
        
        elif 'false' in self.Tokenizer.getStrToken():
            self.VMWriter.writePush('constant',0)

        elif '-' in self.Tokenizer.getToken():
            self.Tokenizer.advance()
            self.compileTerm()
            self.VMWriter.writeArithmetic('neg')
            
        
        elif '~' in self.Tokenizer.getToken():
            self.Tokenizer.advance()
            self.compileTerm()
            self.VMWriter.writeArithmetic('not')
        elif '(' in self.Tokenizer.getToken():
            self.Tokenizer.advance() #advances to expression of off (
            self.compileExpression()
            self.Tokenizer.advance() #advances off of )
            
        elif self.Tokenizer.getStrToken() in self.SymbolTable.SubSymbolTable :
            
                self.VMWriter.writePush(self.SymbolTable.kindOf(self.Tokenizer.getStrToken()),self.SymbolTable.indexOf(self.Tokenizer.getStrToken()))
        elif self.Tokenizer.getStrToken() in self.SymbolTable.ClassSymbolTable:
                if self.op_flag2==False:
                    self.VMWriter.writePush('this',self.SymbolTable.indexOf(self.Tokenizer.getStrToken()))
        if '[' in self.Tokenizer.getStrToken(): #recursion here for multiple arrays of arrays
                
                self.Tokenizer.advance()#advance off of [ and on to val
                self.VMWriter.writePush(self.SymbolTable.kindOf(self.Tokenizer.getStrToken()),self.SymbolTable.indexOf(self.Tokenizer.getStrToken()))
                self.VMWriter.writePush(self.SymbolTable.kindOf(self.array_name),self.SymbolTable.indexOf(self.array_name))
                self.Tokenizer.advance()#advances to another term or ]
                
                if ']' not in self.Tokenizer.getStrToken():
                    self.array_name=self.Tokenizer.getStrToken()
                    self.Tokenizer.advance()
                    self.compileTerm()
                    self.VMWriter.writeArithmetic('add')
                    self.VMWriter.writePush('temp',0)
                    self.VMWriter.writePop('pointer',1)
                    self.VMWriter.writePush('temp',0)
                    self.VMWriter.writePop('that',0)
                if ']' in self.Tokenizer.getStrToken():
                    self.VMWriter.writeArithmetic('add')
                    self.Tokenizer.advance()
                
                
                
                print('1: '+self.Tokenizer.getStrToken()+self.Tokenizer.peek())
        else: #var dec makes it harder come back to later
            #very possible something could be wrong here
            if '.' in self.Tokenizer.peek(): 
                
                self.compileCall()
                
        
            if '(' in self.Tokenizer.peek():
                if self.SymbolTable.kindOf(self.Tokenizer.getStrToken) !='NONE':
                    #self.VMWriter.writePush(self.SymbolTable.kindOf(self.Tokenizer.getStrToken),self.SymbolTable.indexOf(self.Tokenizer.getStrToken))
                    pass
                self.Tokenizer.advance()
                self.Tokenizer.advance()
                self.compileExpression()
                self.Tokenizer.advance()
            
        
    def compileArrayExp(self):
        self.compileTerm()
        self.Tokenizer.advance()

    def compileExpressionList(self): #calls compile expression until ; then say im done
        
        self.running_index=1
        while ';' not in self.Tokenizer.peek() : #and ';' not in self.Tokenizer.getStrToken() :
            if '(' in self.Tokenizer.getStrToken() and ')' in self.Tokenizer.peek():
                return
            if ',' in self.Tokenizer.getToken():
                self.Tokenizer.advance()
                self.running_index+=1
            
            else:
                self.compileExpression()
                
        self.op_flag2=False
        
        
        #token at end is )
   

    def close(self):
        self.outfile.close()