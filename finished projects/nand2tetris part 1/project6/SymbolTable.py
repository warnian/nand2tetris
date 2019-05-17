#symbol table for assembler
#spec in chapter 6.3.4, reserved symbols in 6.2.3
class SymbolTable():
#reserved system symbols dictionary first=label second=address    
    reserved_symbols = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4
        ,'R0':0,'R1':1,'R2':2,'R3':3,'R4':4,'R5':5,'R6':6
        ,'R7':7,'R8':8,'R9':9,'R10':10,'R11':11,'R12':12
        ,'R13':13,'R14':14,'R15':15,'SCREEN':16384,'KBD':24576}
    
    def __init__(self):
        self.symbol_dict={}
        self.symbol_dict.update(self.reserved_symbols)
    
    def addEntry(self,symbol,address): #adds entry pari symbol:address to dict
        self.symbol_dict.update({symbol:address})
        
    def contains(self,symbol): 
        if symbol in self.symbol_dict:
            return True
        else:
            return False
    
    def GetAddress(self,symbol):
        return self.symbol_dict[symbol]
    def PrintSymbolTable(self):
        print(self.symbol_dict)
    

