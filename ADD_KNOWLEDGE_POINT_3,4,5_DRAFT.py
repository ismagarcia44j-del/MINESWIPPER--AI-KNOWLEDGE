KB 
1st G ------------------
FINALLY {A,B,H}=1
SAFE SET ->G

2nd H ------------------
before_kb_len=LEN(KB)
*partial canceled {A,B,H}=1 by point 2!!!
{A,B}=1
*created and partial canceled {G,A,B,C,I}=1 by iterating in safe cells looking for safe coincidence with the current sentence by point 3!!!
{A,B,C,I}=1

*partial canceled {A,B,C,I}=1 by ->
FINALLY {A,B}=1
SAFE SET ->G,H,C,I

3rd F ------------------
{A,B}=1
*created and partial canceled {A,B,C,D,E}=2 by point 3
{A,B,D,E}=2
*partial canceled {A,B,D,E}=1 by point 4
{D,E}=1
FINALLY {A,B}=1 , {D,E}=1
SAFE SET ->G,H,C,I

4th I ------------------
{A,B}=1 , {D,E}=1
*created and partial canceled {H,B,C}=1 by point 3
*{B}=1 canceled by point 4
MINE SET=B 
POINT 5!!! repeat point 4!!! until there are not more new sentences to add

FINALLY {D,E}=1
MINE SET=B 
SAFE SET -> G,H,C,I,A




