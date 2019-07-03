project 11 readme

overall completed. Could be reimplemented for better system of looking ahead in characters to determine what the compiler needs to do. A better implementation instead of having a function which looks ahead, would be to have a static pointer which can be added or substracted to to keep the current position of which token you are looking at. 

This would be a more consistent and workable system. 

 I started to run into problems with certain edge cases and either had to make specific exceptions or rework the system.  I implemented certain extensions where this happened as rewriting the entire logic would be troublesome. The main problem I had was double writing certain pop variables after calling an expression list with an arithmetic symbol being in the expression. It would write the expression correctly but before advancing the tokenizer, write the last command after the arithmetic. If you advance it within the expression list it would put the tokenizer in the wrong place causing a sort of waterfall effect of problems. The only way I found in isolation to fix this problem on a systemic scale was to rewrite the entire code to function around this change as I would have to then change the tokenizer system so I decided to implement solutions for the edge cases on a case by case basis. This could (and I assume would) bite me if this system was deployed in a more rigorous industrial setting. 
 
 Very challenging project but satisfying to get working.

#succesfully compiles:
Seven: #completed
    Main
ConvertTobin: #completed
    Main
Square:
    Main
    Square
    SquareGame
Average:
    #problem with stopping at /s in string #fixed 11:13 am 6/13

    #problem handling a[i] let getting hung up on a[i]
