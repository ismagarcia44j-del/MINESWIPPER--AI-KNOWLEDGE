AFTER CREATE A NEW SENTENCE,
BASED ON THE CURRENT KB, INFERENCE WHICH 
ADDITIONAL CELLS ARE SAFE 

    IF SENTENCE.COUNT=0 
        VERIFY WHICH CELL OF SENTENCE DOESN'T HAS A STATUS AND
        MARK AS SAFE*

AFTER CREATE A NEW SENTENCE,
BASED ON THE CURRENT KB, INFERENCE WHICH 
ADDITIONAL CELLS ARE MINES 

    if len(self.cells) minus (the quantity of self.cells that are in safe cells) is equal to count
        mark_mine(each mine cell)

TAKE ALL SENTENCES
{A,B,H*}=1
{G*,A,B,C,I*}=1
{H*,B,C}=1

DELETE SAFES
{A,B}=1 
{A,B,C}=1
{B,C}=1

CREATE A SET OF ALL UNDETERMINED CELLS UNTIL NOW
{A,B,C,D,E}=2

KB 
1st G
FINALLY {A,B,H}=1
SAFE SET ->G
2nd H 
before_kb_len=LEN(KB)
*partial canceled {A,B,H}=1 by point 2!!!
{A,B}=1
*created and partial canceled {G,A,B,C,I}=1 by iterating in safe cells looking for safe coincidence with the current sentence by point 3!!!
{A,B,C,I}=1
KB_change=True

while KB_change==True:
KB_change = False
*partial canceled {A,B,C,I}=1 by ->
    for sentence in self.knowledge[:]:
        if sentence:
            clean_tracked_safes_mines(self,sentence.cells,sentence)
            break
        elif sentence.count == len(sentence.cells) and sentence.count>0:
            for cell in sentence.cells.copy():#MARK AS MINE EACH ONE
                self.mark_mine(cell)
            self.knowledge.remove(sentence) #DELETE THE ENTIRE OBJECT
            KB_change=True
            break
        elif sentence.count == len(sentence.cells) and sentence.count==0:
            for cell in sentence.cells.copy():#MARK AS SAFE EACH ONE
                self.mark_safe(cell)
            self.knowledge.remove(sentence) #DELETE THE ENTIRE OBJECT
            KB_change=True
            break

        for other in self.knowledge[:]: #LOOKING FOR SUBSETS 
            if sentence.issubset(other):
                if not other is sentence:
                    cells_change = other.cells-sentence.cells
                    count_change = other.count-sentence.count
                    other.cells = cells_change
                    other.count = count_change
                    KB_change=True
                    break
        break 
                #ONCE MODIFIED ONE SENTENCE OF THE ORIGINAL
                #WE NEED TO START ONE MORE TIME THE FORMER ITERATION
                #FROM SCRATCH
    


                        








FINALLY {A,B}=1
SAFE SET ->G,H,C,I

3rd F
{A,B}=1
*created and partial canceled {A,B,C,D,E}=2 by point 3
{A,B,D,E}=2
*partial canceled {A,B,D,E}=1 by point 4
{D,E}=1
FINALLY {A,B}=1 , {D,E}=1
SAFE SET ->G,H,C,I

4th I
{A,B}=1 , {D,E}=1
*created and partial canceled {H,B,C}=1 by point 3
*{B}=1 canceled by point 4
MINE SET=B 
POINT 5!!! repeat point 4!!! until there are not more new sentences to add

FINALLY {D,E}=1
MINE SET=B 
SAFE SET -> G,H,C,I,A







3rd I 
{A,B,H}=1
{G*,A,B,C,I*}=1
{A,B,C,I*}=1
{A,B}=1
{H,B,C}=1
{A,B,C}=1
{B,C}=1
4TH F 
{A,B,H}=1
{G*,A,B,C,I*}=1
{A,B,C,I*}=1
{A,B}=1
{H,B,C}=1
{A,B,C}=1
{B,C}=1
{A,B,C,D,E}=2








    


    














    1. all Mines #DELETE THOSE CELLS FROM EVERY SENTENCE
    2. all Safes #OPEN NEW SAFE CELLS
    3. all Made movements 
    3. all Senteces #IT