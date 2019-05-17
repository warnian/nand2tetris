#Code.py translates hack machine language mnemonics into binary Code
# 16 instruction "ixxaccccccdddjjj" 
##dest 
  #  takes mnemonic string and converts to 3 bit dest in 16 bit value dest dest

   # comp
  #  takes mnemonic strings and converts to 7 bit comp value

   # jump takes mnemonic string and converts to 3 bit jump value

class Code(object):

      dest_dict = {'':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}

        jump_dict = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}

        comp_dict ={'0':'101010','1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101','!A':'110001','-D':'001101',
        '-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110','A-1':'110010','D+A':'000010','D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101'}
    def __init__(self):

     code=self.code

    def dest(code):
        if self in dest_dict:
            return dest_dict[key]
