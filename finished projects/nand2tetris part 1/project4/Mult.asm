// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
//algorithm is num2+num2 num1-1 Times
@0
    D=A
    @R2
    M=D

(LOOP)
    @R1
    D=M
    @END
    D;JEQ

    @R1
    D=A
    M=M-D

    @R0
    D=M
    @R2
    M=M+D

    @LOOP
    0;JMP

(END)
    @END
    0;JMP
	
	
	
	
	