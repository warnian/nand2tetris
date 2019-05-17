#codewriter.py 
#codewriter for VM translator module, nand2tetris project 7 and project 8
#spec found in book chapter 7.3.3 and found below

'''
API:

Constructor
takes Output file name, opes output file and gets ready to write into it
prepares internal variables to be used

setFileName
take fileName (string) argument, outputs informs code writer that translation of a new VM file has started

writeArithmetic  //project 7
takes commandType (current line) of type (string) and writes the assembly code for the given command if it is an arithemetic command

writePushPop //project 7
takes commandType(C_PUSH or C_POP) segment (eg constant temp etc) and index(int) of e and write the the assembly code for the given command of type C_PUSH and C_POP

close() 
closes output file being written

need to implement MEMORY ACCESS COMMANDS:

push.segment i
pop.segment i

constant only has push (ie add to main stack)
constant pushop  in assembly is:
eg push constant 1
is:
//push constant 1
@1
D=A //sets value D reg equal to @ value ie 1
@SP //locates current stack position
A=M //sets memory in SP = address ie *sp
M=D //pushes D reg into memory of *SP

@SP //again gets SP address
M=M+1 //increments value inside SP

Add functionality which prints a statement of what you are translating for example:

//push constant 2     <-------------
machine code here


UNDER CONSTRUCTION

//Project 8 Spec:

writeInit
Takes no arguments returns nothing
writes assembly code that effects the VM initialization ie bootstrap code, must place this at beginning of output file

writeLabel
takes a label string 
writes assembly code that effects the lable command

writeGoto
takes a label string
wties assembly code that effect the goto command

writeIf 
takes a label string
writes assembly code that effects the if-goto command

writeCall
takes functionName (string) and numArgs(int)
writes assembly code that effects the call command

writeReturn
takes no arguments
writes assembly code that effects the return command

writeFunction
takes functionName(string) and numLocals(int) 
writes assembly code that effects the function command


'''

class CodeWriter():
    C_ARITHMETIC_LIST = ['add','sub','neg','eq','gt','lt','and','or','not']
    seg_base_addr = {'argument':2,'local':1,'this':3,'that':4,'static':16,'pointer':3,'temp':5}
    loop_number=0
    cur_ret_loop=0
    def __init__(self,readfile): #creates outfile and opens it

        self.outfilename=readfile.replace('.vm','.asm')  
        self.writefile=open(self.outfilename,'w+')
        self.loop_number=0
    
    def setFileName(self,filename):
        print('Translation of '+filename+' has started...')

    def writeArithmetic(self,command):
        if command=='add':
            self.writefile.write('//add'+'\n')
            self.writefile.write('@SP'+'\n')#accesses current sp
            self.writefile.write('M=M-1'+'\n')#decrements by 1 to get current value 2
            self.writefile.write('A=M'+'\n') #sets address to value in SP M
            self.writefile.write('D=M'+'\n') #sets D register equals value in new address ie value 2
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M-1'+'\n')#decremnts by 1 to get current value 1
            self.writefile.write('A=M'+'\n')#sets addres to value in SP M ie *sp
            self.writefile.write('D=D+M'+'\n')#sums value in D
            self.writefile.write('M=D'+'\n') #writes new sum to memory
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M+1'+'\n') #increments SP by 1
        elif command=='sub':
            self.writefile.write('//sub'+'\n')
            self.writefile.write('@SP'+'\n')#accesses current sp
            self.writefile.write('M=M-1'+'\n')#decrements by 1 to get current value 2
            self.writefile.write('A=M'+'\n') #sets address to value in SP M
            self.writefile.write('D=M'+'\n') #sets D register equals value in new address ie value 2
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M-1'+'\n')#decremnts by 1 to get current value 1
            self.writefile.write('A=M'+'\n')#sets addres to value in SP M ie *sp
            self.writefile.write('D=M-D'+'\n')#difference of value in D
            self.writefile.write('M=D'+'\n') #writes new sum to memory
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M+1'+'\n') #increments SP by 1
        elif command=='neg':
            self.writefile.write('//neg'+'\n')
            self.writefile.write('@SP'+'\n')#accesses current sp
            self.writefile.write('M=M-1'+'\n')#decrements by 1 to get current value 
            self.writefile.write('A=M'+'\n') #sets address to value in SP M
            self.writefile.write('M=-M'+'\n') #sets M value in *sp = -M
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M+1'+'\n') #increments SP by 1
        elif command=='eq':    #have to use jump functions
            self.writefile.write('//eq'+'\n')
            self.writefile.write('@SP'+'\n')#access SP
            self.writefile.write('AM=M-1'+'\n') #decrement SP and *SP by 1
            self.writefile.write('D=M'+'\n') #put *sp into memory'
            self.writefile.write('A=A-1'+'\n') #get second value
            self.writefile.write('D=M-D'+'\n') #subtact values to be used in conditional
            self.writefile.write('@!EQ'+str(self.loop_number)+'\n')
            self.writefile.write('D;JEQ'+'\n')
            self.writefile.write('@SP'+'\n')
            self.writefile.write('A=M-1'+'\n')
            self.writefile.write('M=0'+'\n')
            self.writefile.write('@CONTINUE'+str(self.loop_number)+'\n')
            self.writefile.write('0;JMP'+'\n')
            self.writefile.write('(!EQ'+str(self.loop_number)+')'+'\n')
            self.writefile.write('@SP'+'\n')
            self.writefile.write('A=M-1'+'\n')
            self.writefile.write('M=-1'+'\n')
            self.writefile.write('(CONTINUE'+str(self.loop_number)+')'+'\n')#continues with program 
            self.loop_number+=1
        elif command=='gt':    #have to use jump functions
            self.writefile.write('@SP'+'\n')#access SP
            self.writefile.write('AM=M-1'+'\n') #decrement SP and *SP by 1
            self.writefile.write('D=M'+'\n') #put *sp into memory'
            self.writefile.write('A=A-1'+'\n') #get second value
            self.writefile.write('D=M-D'+'\n') #subtact values to be used in conditional
            self.writefile.write('@!GT'+str(self.loop_number)+'\n')
            self.writefile.write('D;JGT'+'\n')
            self.writefile.write('@SP'+'\n')
            self.writefile.write('A=M-1'+'\n')
            self.writefile.write('M=0'+'\n')
            self.writefile.write('@CONTINUE'+str(self.loop_number)+'\n')
            self.writefile.write('0;JMP'+'\n')
            self.writefile.write('(!GT'+str(self.loop_number)+')'+'\n')
            self.writefile.write('@SP'+'\n')
            self.writefile.write('A=M-1'+'\n')
            self.writefile.write('M=-1'+'\n')
            self.writefile.write('(CONTINUE'+str(self.loop_number)+')'+'\n')#continues with program 
            self.loop_number+=1
        elif command=='lt':   #have to use jump functions
            self.writefile.write('@SP'+'\n')#access SP
            self.writefile.write('AM=M-1'+'\n') #decrement SP and *SP by 1
            self.writefile.write('D=M'+'\n') #put *sp into memory'
            self.writefile.write('A=A-1'+'\n') #get second value
            self.writefile.write('D=M-D'+'\n') #subtact values to be used in conditional
            self.writefile.write('@!LT'+str(self.loop_number)+'\n')
            self.writefile.write('D;JLT'+'\n')
            self.writefile.write('@SP'+'\n')
            self.writefile.write('A=M-1'+'\n')
            self.writefile.write('M=0'+'\n')
            self.writefile.write('@CONTINUE'+str(self.loop_number)+'\n')
            self.writefile.write('0;JMP'+'\n')
            self.writefile.write('(!LT'+str(self.loop_number)+')'+'\n')
            self.writefile.write('@SP'+'\n')
            self.writefile.write('A=M-1'+'\n')
            self.writefile.write('M=-1'+'\n')
            self.writefile.write('(CONTINUE'+str(self.loop_number)+')'+'\n')#continues with program 
            self.loop_number+=1
        elif command=='and':
            self.writefile.write('//and'+'\n')
            self.writefile.write('@SP'+'\n')#accesses current sp
            self.writefile.write('M=M-1'+'\n')#decrements by 1 to get current value 2
            self.writefile.write('A=M'+'\n') #sets address to value in SP M
            self.writefile.write('D=M'+'\n') #sets D register equals value in new address ie value 2
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M-1'+'\n')#decremnts by 1 to get current value 1
            self.writefile.write('A=M'+'\n')#sets addres to value in SP M ie *sp
            self.writefile.write('D=D&M'+'\n')#difference of value in D
            self.writefile.write('M=D'+'\n') #writes new sum to memory
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M+1'+'\n') #increments SP by 1
        elif command=='or':
            self.writefile.write('//or'+'\n')
            self.writefile.write('@SP'+'\n')#accesses current sp
            self.writefile.write('M=M-1'+'\n')#decrements by 1 to get current value 2
            self.writefile.write('A=M'+'\n') #sets address to value in SP M
            self.writefile.write('D=M'+'\n') #sets D register equals value in new address ie value 2
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M-1'+'\n')#decremnts by 1 to get current value 1
            self.writefile.write('A=M'+'\n')#sets addres to value in SP M ie *sp
            self.writefile.write('D=D|M'+'\n')#D register equals D or M
            self.writefile.write('M=D'+'\n') #writes new sum to memory
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M+1'+'\n') #increments SP by 1
        elif command=='not':
            self.writefile.write('//not'+'\n')
            self.writefile.write('@SP'+'\n')#accesses current sp
            self.writefile.write('M=M-1'+'\n')#decrements by 1 to get current value 
            self.writefile.write('A=M'+'\n') #sets address to value in SP M ie *sp
            self.writefile.write('M=!M'+'\n') # sets memory at address *sp to not m
            self.writefile.write('@SP'+'\n') #back to SP
            self.writefile.write('M=M+1'+'\n') #increments SP by 1

    def writePushPop(self,command,segment,index):
        file_name_no_ext=self.outfilename.replace('.asm','')
        
        if command=='C_PUSH': 
            
            
            if 'constant' in segment:
                self.writefile.write('//push '+segment+' '+str(index)+'\n') #writes comments in .asm language telling you command given before assembly code is generated
                self.writefile.write('@'+str(index)+'\n') #grabs address = index
                self.writefile.write('D=A'+'\n')#sets value of D reg to address value
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('A=M'+'\n') #sets value of address = M in sp ie *sp
                self.writefile.write('M=D'+'\n') #sets memory in stack pointer to D
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('M=M+1'+'\n') #incements value of SP by 1
            elif segment=='static':
                self.writefile.write('//push '+segment+' '+str(index)+'\n') #writes comments in .asm language telling you command given before assembly code is generated
                self.writefile.write('@'+file_name_no_ext+'.'+str(index)+'\n') #accesses address of index
                self.writefile.write('D=M'+'\n') #sets the address  into D reg
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('A=M'+'\n') #set address to value in M ie *sp
                self.writefile.write('M=D'+'\n') #sets value in D reg(@index) into memory
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('M=M+1'+'\n') #incements value of SP by 1
            elif 'pointer' in segment:
                self.writefile.write('//push '+segment+' '+str(index)+'\n')
                self.writefile.write('@'+str(self.seg_base_addr[segment])+'\n') #accesses address of index
                self.writefile.write('D=A'+'\n') #sets the address  into D reg
                self.writefile.write('@'+str(index)+'\n') #gets address if index
                self.writefile.write('A=D+A'+'\n') 
                self.writefile.write('D=M'+'\n')
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('A=M'+'\n') #set address to value in M ie *sp
                self.writefile.write('M=D'+'\n') #sets value in D reg(@index) into memory
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('M=M+1'+'\n') #incements value of SP by 1

            elif segment=='temp':
                self.writefile.write('//push '+segment+' '+str(index)+'\n') #writes comments in .asm language telling you command given before assembly code is generated
                self.writefile.write('@'+str(self.seg_base_addr[segment])+'\n') #accesses address of index
                self.writefile.write('D=A'+'\n') #sets the address  into D reg
                self.writefile.write('@'+str(index)+'\n') #gets address if index
                self.writefile.write('A=D+A'+'\n') #adds base *sp to index value and puts it into D reg
                self.writefile.write('D=M'+'\n')
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('A=M'+'\n') #set address to value in M ie *sp
                self.writefile.write('M=D'+'\n') #sets value in D reg from line 222 into memory
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('M=M+1'+'\n') 
            else: #@*segment+i
                self.writefile.write('//push '+segment+' '+str(index)+'\n') #writes comments in .asm language telling you command given before assembly code is generated
                self.writefile.write('@'+str(self.seg_base_addr[segment])+'\n') #accesses address of index
                self.writefile.write('D=M'+'\n') #sets the address  into D reg
                self.writefile.write('@'+str(index)+'\n') #gets address if index
                self.writefile.write('A=D+A'+'\n') #adds base *sp to index value and puts it into D reg
                self.writefile.write('D=M'+'\n')
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('A=M'+'\n') #set address to value in M ie *sp
                self.writefile.write('M=D'+'\n') #sets value in D reg from line 222 into memory
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('M=M+1'+'\n') #incements value of SP by 1
        if command=='C_POP':
            
            if segment =='pointer':
                self.writefile.write('//pop '+segment+' '+str(index)+'\n') #write comments in .asm language telling you command before assembly code is written
                self.writefile.write('@'+str(self.seg_base_addr[segment])+'\n') #accesses base address of segment
                self.writefile.write('D=A'+'\n') #sets the address of @lineabove  into D reg
                self.writefile.write('@'+str(index)+'\n') #gets address of index
                self.writefile.write('D=D+A'+'\n') #puts top value of address into D ie *segment 
                self.writefile.write('@R13'+'\n')#acceses general ram
                self.writefile.write('M=D'+'\n')#writes D (address of seg pointer) to R5
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('AM=M-1'+'\n') #set address to value in M-1 ie *sp-1 Also decrements stack pointer by 1
                self.writefile.write('D=M'+'\n') #sets D reg equal to memory value of *sp
                self.writefile.write('@R13'+'\n') #back to general ram
                self.writefile.write('A=M'+'\n') #*R5
                self.writefile.write('M=D'+'\n') #Pop value to segment pointer
            
            if segment=='static':
                #correct DO NO TOUCH 
                self.writefile.write('//pop '+segment+' '+str(index)+'\n') #write comments in .asm language telling you command before assembly code is written
                self.writefile.write('@'+file_name_no_ext+'.'+str(index)+'\n') #accesses address of index
                self.writefile.write('D=A'+'\n')
                self.writefile.write('@R13'+'\n')#acceses temp ram
                self.writefile.write('M=D'+'\n')#writes D (address of seg pointer) to R5
                self.writefile.write('@SP'+'\n') #accesses SP
                self.writefile.write('AM=M-1'+'\n') #set address to value in M-1 ie *sp-1 Also decrements stack pointer by 1
                self.writefile.write('D=M'+'\n') #sets D reg equal to memory value of *sp
                self.writefile.write('@R13'+'\n') #back to R5
                self.writefile.write('A=M'+'\n') #*R5
                self.writefile.write('M=D'+'\n') #Pop value to segment pointer
            if segment=='temp':
                self.writefile.write('//pop '+segment+' '+str(index)+'\n')
                self.writefile.write('@'+str(self.seg_base_addr[segment])+'\n')
                self.writefile.write('D=A'+'\n')
                self.writefile.write('@'+str(index)+'\n')
                self.writefile.write('D=D+A'+'\n') #adds base address pointer plus index
                self.writefile.write('@R13'+'\n') #accesses general purpose ram
                self.writefile.write('M=D'+'\n') #stores base address pointer plus index in R13
                self.writefile.write('@SP'+'\n')
                self.writefile.write('AM=M-1'+'\n')
                self.writefile.write('D=M'+'\n')
                self.writefile.write('@R13'+'\n')
                self.writefile.write('A=M'+'\n')
                self.writefile.write('M=D'+'\n')
            elif 'pointer' not in segment and 'static' not in segment:
                
                self.writefile.write('//pop '+segment+' '+str(index)+'\n')
                self.writefile.write('@'+str(self.seg_base_addr[segment])+'\n')
                self.writefile.write('D=M'+'\n')
                self.writefile.write('@'+str(index)+'\n')
                self.writefile.write('D=D+A'+'\n') #adds base address pointer plus index
                self.writefile.write('@R13'+'\n') #accesses general purpose ram
                self.writefile.write('M=D'+'\n') #stores base address pointer plus index in R13
                self.writefile.write('@SP'+'\n')
                self.writefile.write('AM=M-1'+'\n')
                self.writefile.write('D=M'+'\n')
                self.writefile.write('@R13'+'\n')
                self.writefile.write('A=M'+'\n')
                self.writefile.write('M=D'+'\n')
    def writeInit(self):
        self.writefile.write('@256'+'\n')
        self.writefile.write('D=A'+'\n')
        self.writefile.write('A=0'+'\n')
        self.writefile.write('M=D'+'\n')
        self.writeCall('Sys.init',0)
        print('init happened')
    def writeLabel(self,label):
        self.writefile.write('('+str(label)+')'+'\n')
        
    def writeGoto(self,label):
        self.writefile.write('@'+str(label)+'\n')#@label
        self.writefile.write('0;JMP'+'\n')#jump to @label unconditionally
        
    def writeIf(self, label):
        self.writefile.write('//if-goto '+str(label)+'\n')
        self.writefile.write('@SP'+'\n')#accesses sp
        self.writefile.write('M=M-1'+'\n') #*sp-1 =M
        self.writefile.write('A=M'+'\n')#A=*sp
        self.writefile.write('D=M'+'\n')#puts memoery of *sp into D reg
        self.writefile.write('A=A-1'+'\n')#decrements *sp
        self.writefile.write('@'+label+'\n')#@label
        self.writefile.write('D;JNE'+'\n')#if D not equal to 0 value jump
    def writeCall(self,functionName,numArgs):#complex op basically manually translate vm commands from figure 8.5 chapter 8 in the book
        #push return-address
        self.writefile.write('//call '+str(functionName)+' '+str(numArgs)+'\n')
        self.writefile.write('@return-address'+str(self.loop_number)+'\n')
        self.writefile.write('D=A'+'\n')
        self.writefile.write('@SP'+'\n')
        self.writefile.write('A=M'+'\n')
        self.writefile.write('M=D'+'\n')
        self.writefile.write('@SP'+'\n')
        self.writefile.write('M=M+1'+'\n')
        #push local //copied from STATIC PUSH ABOVE
        self.writefile.write('//push LCL'+'\n') #writes comments in .asm language telling you command given before assembly code is generated
        self.writefile.write('@LCL'+'\n') #accesses address of index
        self.writefile.write('D=M'+'\n') #sets the address  into D reg
        self.writefile.write('@SP'+'\n') #gets address if index
        self.writefile.write('A=M'+'\n') #adds base *sp to index value and puts it into D reg
        self.writefile.write('M=D'+'\n')
        self.writefile.write('@SP'+'\n') #accesses SP
        self.writefile.write('M=M+1'+'\n') #incements value of SP by 1
        #push argument 
        self.writefile.write('//push ARG'+'\n') #writes comments in .asm language telling you command given before assembly code is generated
        self.writefile.write('@ARG'+'\n') #accesses address of index
        self.writefile.write('D=M'+'\n') #sets the address  into D reg
        self.writefile.write('@SP'+'\n') #gets address if index
        self.writefile.write('A=M'+'\n') #adds base *sp to index value and puts it into D reg
        self.writefile.write('M=D'+'\n')
        self.writefile.write('@SP'+'\n') #accesses SP
        self.writefile.write('M=M+1'+'\n') #incements value of SP by 1
        #push this
        self.writefile.write('//push THIS'+'\n') #writes comments in .asm language telling you command given before assembly code is generated
        self.writefile.write('@THIS'+'\n') #accesses address of index
        self.writefile.write('D=M'+'\n') #sets the address  into D reg
        self.writefile.write('@SP'+'\n') #gets address if index
        self.writefile.write('A=M'+'\n') #adds base *sp to index value and puts it into D reg
        self.writefile.write('M=D'+'\n')
        self.writefile.write('@SP'+'\n') #accesses SP
        self.writefile.write('M=M+1'+'\n') #incements value of SP by 1
        #push that
        self.writefile.write('//push THAT'+'\n') #writes comments in .asm language telling you command given before assembly code is generated
        self.writefile.write('@THAT'+'\n') #accesses address of index
        self.writefile.write('D=M'+'\n') #sets the address  into D reg
        self.writefile.write('@SP'+'\n') #gets address if index
        self.writefile.write('A=M'+'\n') #adds base *sp to index value and puts it into D reg
        self.writefile.write('M=D'+'\n')
        self.writefile.write('@SP'+'\n') #accesses SP
        self.writefile.write('M=M+1'+'\n') #incements value of SP by 1
        #ARG=SP-numArgs-5
        self.writefile.write('@SP'+'\n')
        self.writefile.write('D=M'+'\n')#*sp into D reg
        self.writefile.write('@'+str(numArgs)+'\n')#go to @ num Args reg
        self.writefile.write('D=D-A'+'\n')#ie SP-numArgs into D
        self.writefile.write('@5'+'\n')
        self.writefile.write('D=D-A'+'\n')#ie SP-numArgs-5 into D
        self.writefile.write('@ARG'+'\n')
        self.writefile.write('M=D'+'\n')#ARG=SP-numArgs-5
        #LCL=SP
        self.writefile.write('@SP'+'\n')
        self.writefile.write('D=M'+'\n')#*sp
        self.writefile.write('@LCL'+'\n')
        self.writefile.write('M=D'+'\n')#LCL=SP
        #goto functionName copied from goto
        self.writefile.write('@'+str(functionName)+'\n')
        self.writefile.write('0;JMP'+'\n')
        #(return-address)
        self.writefile.write('(return-address'+str(self.loop_number)+')'+'\n')
        self.loop_number+=1
    def writeReturn(self):#see comment on writeCall above, similar process
        #FRAME=LCL
        self.writefile.write('//Return'+'\n')
        self.writefile.write('@LCL'+'\n')
        self.writefile.write('D=M'+'\n')
        self.writefile.write('@FRAME'+'\n')
        self.writefile.write('M=D'+'\n')#stores value of LCL in @Frame
        #RET=*(FRAME-5)
        self.writefile.write('@5'+'\n')
        self.writefile.write('D=A'+'\n')
        self.writefile.write('@FRAME'+'\n')
        self.writefile.write('D=M-D'+'\n')#D=FRAME-5
        self.writefile.write('A=D'+'\n')
        self.writefile.write('D=M'+'\n')#D=*(FRAME-5)
        self.writefile.write('@RET'+'\n')
        self.writefile.write('M=D'+'\n')# #RET=*(FRAME-5)
        #*ARG =pop() ?? = pop *ARG ??
        self.writefile.write('//pop argument 0'+'\n')
        self.writefile.write('@ARG'+'\n')
        self.writefile.write('D=M'+'\n')
        self.writefile.write('@0'+'\n')
        self.writefile.write('D=D+A'+'\n') #adds base address pointer plus index
        self.writefile.write('@R15'+'\n') #accesses general purpose ram
        self.writefile.write('M=D'+'\n') #stores base address pointer plus index in R13
        self.writefile.write('@SP'+'\n')
        self.writefile.write('AM=M-1'+'\n')
        self.writefile.write('D=M'+'\n')
        self.writefile.write('@R15'+'\n')
        self.writefile.write('A=M'+'\n')
        self.writefile.write('M=D'+'\n')#writes D reg (ie stack value) to Memory a la pop()
        #SP=ARG+1
        self.writefile.write('@ARG'+'\n')
        self.writefile.write('D=M+1'+'\n')#ie ARG+1
        self.writefile.write('@SP'+'\n')
        self.writefile.write('M=D'+'\n') #SP=ARG+1
        #THAT=*(FRAME-1)
        self.writefile.write('@1'+'\n')
        self.writefile.write('D=A'+'\n')
        self.writefile.write('@FRAME'+'\n')
        self.writefile.write('D=M-D'+'\n')#D=FRAME-1
        self.writefile.write('A=D'+'\n')
        self.writefile.write('D=M'+'\n')#D=*(FRAME-1)
        self.writefile.write('@4'+'\n')
        self.writefile.write('M=D'+'\n')# #THAT=*(FRAME-1)
        #THIS=*(FRAME-2)
        self.writefile.write('@ARG'+'\n')
        self.writefile.write('D=A'+'\n')
        self.writefile.write('@FRAME'+'\n')
        self.writefile.write('D=M-D'+'\n')#D=FRAME-2
        self.writefile.write('A=D'+'\n')
        self.writefile.write('D=M'+'\n')#D=*(FRAME-2)
        self.writefile.write('@3'+'\n')
        self.writefile.write('M=D'+'\n')# #THIS=*(FRAME-2)
        #ARG=*(FRAME-3)
        self.writefile.write('@3'+'\n')
        self.writefile.write('D=A'+'\n')
        self.writefile.write('@FRAME'+'\n')
        self.writefile.write('D=M-D'+'\n')#D=FRAME-3
        self.writefile.write('A=D'+'\n')
        self.writefile.write('D=M'+'\n')#D=*(FRAME-3)
        self.writefile.write('@ARG'+'\n')
        self.writefile.write('M=D'+'\n')# #ARG=*(FRAME-3)
        #LCL=*(FRAME-4)
        self.writefile.write('@4'+'\n')
        self.writefile.write('D=A'+'\n')
        self.writefile.write('@FRAME'+'\n')
        self.writefile.write('D=M-D'+'\n')#D=FRAME-4
        self.writefile.write('A=D'+'\n')#A=*(FRAME-4)
        self.writefile.write('D=M'+'\n')#D=*(FRAME-4)
        self.writefile.write('@LCL'+'\n')
        self.writefile.write('M=D'+'\n')# #THAT=*(FRAME-4)
        #goto RET
        self.writefile.write('@RET'+'\n')
        self.writefile.write('A=M'+'\n') #go to value stored in @ RET ie *RET or return address
        self.writefile.write('0;JMP'+'\n')
    
    def writeFunction(self,functionName,numLocals):
        
        self.writefile.write('//function '+str(functionName)+' '+str(numLocals)+'\n')#header for debug
        self.writefile.write('('+str(functionName)+')'+'\n')
        #start of push constant 0 numLocals times
        for i in range(numLocals):
            ##push constant 0 i numlocal times
            self.writefile.write('@0'+'\n') #grabs address = 0
            self.writefile.write('D=A'+'\n')#sets value of D reg to address value
            self.writefile.write('@SP'+'\n') #accesses SP
            self.writefile.write('A=M'+'\n') #sets value of address = M in sp ie *sp
            self.writefile.write('M=D'+'\n') #sets memory in stack pointer to D
            self.writefile.write('@SP'+'\n') #accesses SP
            self.writefile.write('M=M+1'+'\n') #incements value of SP by 1
            

    def close(self): #closes file
        self.writefile.close()





        
        
        


