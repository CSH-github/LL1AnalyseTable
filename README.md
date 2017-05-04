# LL1AnalyseTable
Transform CLF into LL1 Analyse Table
0. This program is designed for Grammer Top-down analysis.<br/>
   The input CLG should be without loop productions and "ε"<br/>
1. Default use Capital Letters as non-terminal<br/>
   use non-Capital Letters as terminal<br/>
   use char "e" to represent "ε"<br/>
2. Use char "S" to represent Start non-terminal for Getting FOLLOW set
3. The output must have less than 26 non-terminals( for 26 Capital Letters )
4. Please do not add unnecessary blanks
5. Please ensure you use the right form to input productions<br/>
   or you will get the wrong output
6. Example Input:<br/>
    S->TE   <br/>
    E->+TE|e<br/>
    T->FU   <br/>
    U->*FU|e<br/>
    F->(S)|i<br/>
    q       <br/>
