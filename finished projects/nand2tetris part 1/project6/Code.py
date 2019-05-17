#Code.py translates hack machine language mnemonics into binary Code
# 16 instruction "ixxaccccccdddjjj" 
##dest 
  #  takes mnemonic string and converts to 3 bit dest in 16 bit value dest dest

   # comp
  #  takes mnemonic strings and converts to 7 bit comp value

   # jump takes mnemonic string and converts to 3 bit jump value

class Code(object):

        dest_dict = {None:'000','':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}

        jump_dict = {None:'000','':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}

        comp_dict ={'':'xxxxxxx','0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000','!D':'0001101','!A':'0110001','-D':'0001101',
        '-A':'0110011','D+1':'0011111','A+1':'0110111','D-1':'0001110','A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111','D&A':'0000000','D|A':'0010101',
        'M':'1110000', '!M':'1110001', '-M':'1110011', 'M+1':'1110111','M-1':'1110010','D+M':'1000010','D-M':'1010011','M-D':'1000111','D&M':'1000000', 'D|M':'1010101'}
        #comp_dict contains both a values for simplification
        def __init__(self):
            pass

        def dest_conv(self,code):

            return self.dest_dict[code]
        def comp_conv(self,code):
            
            return self.comp_dict[code]
        def jump_conv(self,code):

            return self.jump_dict[code]
        


