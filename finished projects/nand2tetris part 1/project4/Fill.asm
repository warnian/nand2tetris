// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

//if keyboad = 0 white otherwise black
//8192 total number of pixels on screen

@SCREEN
D=A
@pixel  //starts at first pixel
M=D

@8192 //total number of pixels
D=A
@SCREEN
D=D+A

@lastpixel
M=D  //sets last pixel to variable

(LOOP) //checks keyboard value
	
	@KBD
	D=M
	@DISPLAYWHITE
	D;JEQ
	@DISPLAYBLACK
	0;JMP

(DISPLAYBLACK)
	@pixel
	A=M
	M=-1
	@END
	0;JMP
(DISPLAYWHITE)
	@pixel
	A=M
	M=0
	@END

(END)
	@pixel
	D=M+1
	M=D //counts pixel pointer up one
	@lastpixel
	D=D-M
	@LOOP
	D;JNE
	@SCREEN
	D=A
	@pixel
	M=D
	@LOOP
	0;JMP

