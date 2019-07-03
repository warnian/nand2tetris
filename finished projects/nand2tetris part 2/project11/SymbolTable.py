#SymbolTable for compiler in project 11 of nand2tetris
#spec found in 11.3.3 of the book
#provides a symbol table for classes, symbol table has a scope for each class 
'''
API:
    Constructor
        no args, no return, Creates a new empty symbol table
    
    startSubroutine
        no args, no return, starts a new subroutine
    
    Define
        takes args: name (string), type (String), kind (STATIC, FIELD, ARG, VAR)
            returns nothing
        Defines a new identifier of a given name, type, and kind and assigns its a running index.
        STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.
    
    VarCount 
        takes arg: kind(STATIC, FIELD, ARG, or VAR)
        returns an int
        returns the number of variable of the given kind already defined in the current scope
    
    KindOf
        takes arg: name (string) 
        return (STATIC, FIELD, ARG, VAR, NONE) 
        returns the kind of named identifier in the current scope.
        if the identifier is unknown in the current scope returns NONE
    
    TypeOf
        takes arg: name (string) 
        returns String
        returns the type of the name identifier in the current scope

    IndexOf
        takes arg: name (string)
        returns int
        returns the index assigned to the named identifier

    EXAMPLE OF A CLASS SCOPE SYMBOL TABLE:
    ---------------------------------------------
    |      NAME       -    TYPE   -   KIND   - # |
    |   nAccounts           int      static    0 |
    |  bankCommission       int      static    1
    |      id               int      field     0 
    |     owner           String     field     1
    |    balance            int      field     2 
    ---------------------------------------------

    EXAMPLE OF A METHOD SCOPE SYMBOL TABLE:

      ---------------------------------------------
    |      NAME       -      TYPE        -     KIND     - # |
    |      this           BankAccount       argument      0 |
    |      sum               int            argument      1
    |      from            BankAccount      argument      2 
    |     when                Date          argument      3
    |      i                 int             var          0
    |      j                 int             var          1
    |      due               Date            var          2
    ---------------------------------------------

'''
import os
from JackTokenizer import JackTokenizer

class SymbolTable():

    def __init__(self):
        self.ClassSymbolTable={} #class symbol table
        self.SubSymbolTable={} #subroutine symbol table
        self.static_index=0
        self.field_index=0
        self.arg_index=0
        self.var_index=0

    def startSubroutine(self):
        self.SubSymbolTable.clear()
        self.arg_index=0
        self.var_index=0
        
    #adds stuff to symbol table
    def define(self,name,typing,kind):
        
        if 'static' in kind or 'field' in kind: #class scope add to class table
            if kind=='static':
                self.ClassSymbolTable.update({name:[typing,kind,self.static_index]})
                self.static_index+=1
            elif kind=='field':
                self.ClassSymbolTable.update({name:[typing,kind,self.field_index]})
                self.field_index+=1
        elif 'argument' in kind or 'var' in kind: #subroutine scope add to subroutine table
            if kind=='argument':
                self.SubSymbolTable.update({name:[typing,kind,self.arg_index]})
                self.arg_index+=1
            if kind=='var':
                
                self.SubSymbolTable.update({name:[typing,kind,self.var_index]})
                self.var_index+=1
    def varCount(self,kind):
        if kind=='static':
            return self.static_index
        elif kind=='field':
            return self.field_index
        elif kind=='argument':
            return self.arg_index
        elif kind=='var':
            return self.var_index
    
    def kindOf(self,name):
        if name in self.ClassSymbolTable:
            return self.ClassSymbolTable[name][1]
        elif name in self.SubSymbolTable:
            return self.SubSymbolTable[name][1]
        else:
            return 'NONE'
    
    def typeOf(self,name):
        if name in self.ClassSymbolTable:
            return self.ClassSymbolTable[name][0]
        elif name in self.SubSymbolTable:
            return self.SubSymbolTable[name][0]
        else:
            pass
            #raise Exception(LookupError('symbolTable.typeOf lookup error'))
    def indexOf(self,name):
        if name in self.ClassSymbolTable:
            return self.ClassSymbolTable[name][2]
        elif name in self.SubSymbolTable:
            return self.SubSymbolTable[name][2]
        else:
            #raise Exception(LookupError('symbolTable.indexOf lookup error'))
            pass
    def debug(self):
        print('Class Symbol Table: ')
        for key in self.ClassSymbolTable:
            print(key)
            print(self.ClassSymbolTable[key])
        print('Subroutine Symbol Table: ')
        for key in self.SubSymbolTable:
            print(key)
            print(self.SubSymbolTable[key])
