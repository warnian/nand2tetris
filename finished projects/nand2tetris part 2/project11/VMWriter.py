#VMWriter Module for project 11 in nand2tetris
#spec found in 11.3.4 of book 
#writes VM code

'''
API:

Constructor
    takes a filename for arg
    returns nothing
    creates a new file and prepares it for writing

writePush
    takes a segment name (CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP)
    takes an Index (int)
    returns nothing
    writes a VM Push command

writePop
    takes a segment name (CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP)
    takes an index(int)
    returns nothing
    writes a VM pop command

writeArithmetic
    takes a command (ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT)
    returns nothing
    writes a VM Arithmetic command

writeLabel
    takes a label (string) 
    returns nothing
    writes a VM label command

writeGoto
    takes a label(string)
    returns nothing
    writes a VM goto command
    
writeIf
    takes a label
    returns nothing
    writes a VM If-goto command

writeCall 
    takes a name(string)
    takes nArgs (int) 
    returns nothing
    writes a VM call command

writeFunction
    takes a name(string)
    takes nLocals (int)
    writes a VM function command

writeReturn 
    takes no args
    returns nothing
    Writes a VM return command

close
    closes the output file

'''
#Looks good but have to do everything else to see
class VMWriter():

    def __init__(self,outfile):
        self.writeFile=open(outfile,'w+')

    
    def writePush(self, Segment, Index):
        if Segment=='var':
            self.writeFile.write('push '+'local'+' '+str(Index)+'\n')
            return
        if Segment=='field':
            self.writeFile.write('push '+'this'+' '+str(Index)+'\n')
            return
        else:
            self.writeFile.write('push '+Segment+' '+str(Index)+'\n')
            
    def writePop(self, Segment, Index):
        if 'var' in Segment:
            self.writeFile.write('pop '+'local'+' '+str(Index)+'\n')
            return
        elif 'field' in Segment:
            self.writeFile.write('pop '+'this'+' '+str(Index)+'\n')
            return
        else:
            self.writeFile.write('pop '+Segment+' '+str(Index)+'\n')
            
            
    def writeArithmetic(self, command):
        self.writeFile.write(command+'\n')
    
    def writeLabel(self, label):
        self.writeFile.write('label '+label+'\n')

    def writeGoto(self,label):
        self.writeFile.write('goto '+label+'\n')

    def writeIf(self,label):
        self.writeFile.write('if-goto '+label+'\n')

    def writeCall(self, name, nArgs):
        self.writeFile.write('call '+name+' '+str(nArgs)+'\n')
    
    def writeFunction(self, name, nLocals):
        self.writeFile.write('function '+name+' '+str(nLocals)+'\n')
    
    def writeReturn(self):
        self.writeFile.write('return'+'\n')
    def writeDebugFlag(self):
        self.writeFile.write('DEBUG'+'\n')
    def close(self):
        self.writeFile.close()

        