// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
//algorithm is R0+R0 R1-1 Times
@R0
D=M
@i
M=D //sets i = R0

@R1 
D=M
@count
M=D //sets count = R1

@R2
D=M
@sum
M=D //sets sum=R2

(LOOP)
	@count
	D=M
	@STOP
	D;JEQ //if count=0 goto stop
	@i
	D=M //calls R0
	@sum
	M=M+D //adds r0 to sum
	
	@count
	M=M-1 //decreases count by 1
	@LOOP
	0;JMP
(STOP)
	@sum
	D=M
	@R2
	M=D  //sets R2 = Sum
	
(END)
	@END
	0;JMP
	
	
	
	
	