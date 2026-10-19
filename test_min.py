import pytest
from minesweeper import Sentence, MinesweeperAI


def test_mark_mine():
    the_set={1,2,3,5}
    s=Sentence(the_set,3)
    s.mark_mine(2)
    assert s.cells=={1,3,5}
    assert s.count==2

def test_mark_safe_and_known_safes():
    the_set={1,2,3,5}
    s=Sentence(the_set,3)
    s.mark_safe(5) #testing mark_safe and...
    assert s.known_safes() == set() #...mark_safe

ai=MinesweeperAI()
def test_surrounding_cells_square():
    cell=(0,0) #UP LEFT SQUARE
    response=ai.surrounding_cells(cell)
    assert {(0,1),(1,0),(1,1)}==response

    i,j=(0,ai.width-1) #UP RIGHT SQUARE
    response=ai.surrounding_cells((i,j))
    assert {(i,j-1),(i+1,j-1),(i+1,j)}==response

    i,j=(ai.height-1,0) #DOWN LEFT SQUARE
    response=ai.surrounding_cells((i,j))
    assert {(i-1,j),(i-1,j+1),(i,j+1)}==response

    i,j=(ai.height-1,ai.width-1) #DOWN RIGHT SQUARE
    response=ai.surrounding_cells((i,j))
    assert {(i,j-1),(i-1,j-1),(i-1,j)}==response

def test_surrounding_cells_center():
    i=int(round(ai.height/2,0))
    j=int(round(ai.width/2,0))
    #UP LEFT SQUARE
    response=ai.surrounding_cells((i,j))
    assert {(i,j+1),(i,j-1),
            (i-1,j),(i-1,j+1),(i-1,j-1),
            (i+1,j),(i+1,j+1),(i+1,j-1)
            }==response

def test_surrounding_cells_one_side():
    #HARDCODED (8*8) TEST, THEREFORE NO SCALABLE
    i=0
    j=1
    #UP SIDE
    response=ai.surrounding_cells((i,j))
    assert {(0,2),(0,0),(1,0),(1,1),(1,2)}==response

    i=4
    j=7
    #DOWN SIDE
    response=ai.surrounding_cells((i,j))
    assert {(3,7),(3,6),(4,6),(5,6),(5,7)}==response

def test_clean_tracked_safes_mines():
    #testing clean safes
    ai=MinesweeperAI()
    j=Sentence({(1,0),(1,1),(0,1)},1)
    ai.knowledge = [j]#,Sentence({(0,1),(1,1),(1,2)},1)]
    ai.safes = {(1,1)}
    ai.clean_tracked_safes_mines(ai.knowledge[0].cells,ai.knowledge[0])
    assert ai.knowledge[0].cells=={(1,0),(0,1)}

    #testing clean mines
    ai.knowledge = [Sentence({(1,0),(1,1),(0,1)},1)]#,Sentence({(0,1),(1,1),(1,2)},1)]
    ai.mines = {(1,1)}
    ai.clean_tracked_safes_mines(ai.knowledge[0].cells,ai.knowledge[0])
    assert ai.knowledge[0].cells=={(1,0),(0,1)}

    #testing erase the object
    ai.knowledge = [Sentence({},0)]#,]
    ai.clean_tracked_safes_mines(ai.knowledge[0].cells,ai.knowledge[0])
    assert not ai.knowledge == True

def test_entire_mines_sentence():
    ai.knowledge = [Sentence({(1,0),(1,1),(0,1)},3)]
    ai.entire_mines_sentence(ai.knowledge[0])
    assert {(1,0),(1,1),(0,1)} == ai.mines
    assert len(ai.knowledge) == 0

def test_entire_safes_sentence():
    ai.knowledge = [Sentence({(1,0),(1,1),(0,1)},0)]
    ai.entire_safes_sentence(ai.knowledge[0])
    assert {(1,0),(1,1),(0,1)} == ai.safes
    assert len(ai.knowledge) == 0

def test_subset_inferences():
    #Testing: Is the greater sentence's.cell set a subset of the lesser sentence's.cell set?
    ai.knowledge = [Sentence({(1,0),(1,1),(0,1)},1),Sentence({(0,1),(1,1)},1)]#,(1,2)},1)]
    for sentence in ai.knowledge[:]:
        KB_change = ai.subset_inferences(sentence)
        break
    assert KB_change == False

    #Testing: Is the lesser sentence's.cell set a subset of the the greater sentence's.cell set?
    ai.knowledge = [Sentence({(0,1),(1,1)},1),Sentence({(1,0),(1,1),(0,1)},1)]#,(1,2)},1)]
    for sentence in ai.knowledge[:]:
        KB_change = ai.subset_inferences(sentence)
        break
    assert KB_change == True 
    assert ai.knowledge[0].cells== {(0,1),(1,1)} and ai.knowledge[0].count == 1
    assert ai.knowledge[1].cells== {(1,0)} and ai.knowledge[1].count == 0

def test_add_knowledge_inferences_large_play():
    #MINE AT 1,1
    ai = MinesweeperAI()
    #The first movement was (0,1) and it was safe
    ai.add_knowledge((0,1),1)
    assert ai.moves_made == {(0,1)} # POINT 1
    assert ai.safes == {(0,1)} # POINT 2
    assert ai.knowledge[0].cells == {(0,0),(1,0),(1,1),(1,2),(0,2)}
    assert ai.knowledge[0].count == 1
    assert ai.knowledge[0].safes == set()

    #The first movement plus the second movement
    ai.add_knowledge((0,2),1)
    assert ai.moves_made == {(0,1),(0,2)}
    assert ai.safes == {(0,1),(0,2)}
    assert ai.knowledge[0].cells == {(0,0),(1,0),(1,1),(1,2)}
    assert ai.knowledge[0].count == 1
    assert ai.knowledge[1].cells == {(1,1),(1,2),(0,3),(1,3),(0,3)}
    assert ai.knowledge[1].count == 1
    
   #The first and second movement plus the third movement
    ai.add_knowledge((2,1),1)
    assert ai.moves_made == {(0,1),(0,2),(2,1)}
    assert ai.safes == {(0,1),(0,2),(2,1)}
    assert ai.knowledge[0].cells == {(0,0),(1,0),(1,1),(1,2)}
    assert ai.knowledge[0].count == 1
    assert ai.knowledge[1].cells == {(1,1),(1,2),(0,3),(1,3),(0,3)}
    assert ai.knowledge[1].count == 1
    assert ai.knowledge[2].cells == {(1,0),(1,1),(1,2),(2,0),(3,0),(3,1),(3,2),(2,2)}
    assert ai.knowledge[2].count == 1

    #The first, second, third movement plus the fourth movement
    ai.add_knowledge((2,0),1)
    assert ai.moves_made == {(0,1),(0,2),(2,1),(2,0)}
    assert ai.safes == {(0,1),(0,2),(2,1),(2,0),(1,2),(3,2),(2,2)}
    assert ai.knowledge[0].cells == {(0,0),(1,0),(1,1)}
    assert ai.knowledge[0].count == 1
    assert ai.knowledge[1].cells == {(1,1),(1,3),(0,3)}
    assert ai.knowledge[1].count == 1
    assert ai.knowledge[2].cells == {(1,0),(1,1),(3,1),(3,0)} #d
    assert ai.knowledge[2].count == 1

    #The first, second, third,fourth movement plus the fifth movement
    #It doesn't create a sentence already exists
    ai.add_knowledge((1,0),1)
    assert ai.moves_made == {(0,1),(0,2),(2,1),(2,0),(1,0)}
    assert ai.safes == {(0,1),(0,2),(2,1),(2,0),(1,2),(3,2),(2,2),(1,0)}
    assert ai.knowledge[0].cells == {(0,0),(1,1)} 
    assert ai.knowledge[0].count == 1
    assert ai.knowledge[1].cells == {(1,1),(1,3),(0,3)}
    assert ai.knowledge[1].count == 1
    assert ai.knowledge[2].cells == {(1,1),(3,1),(3,0)}
    assert ai.knowledge[2].count == 1

def test_add_knowledge_fast_play():
    #MINE AT 1,0
    ai = MinesweeperAI()

    #The first movement was (1,2) and it is thoroughly safe
    ai.add_knowledge((1,2),0)
    assert ai.moves_made == {(1,2)}
    assert ai.safes == {(1,2),(0,1),(0,2),(0,3),(1,1),(2,1),(2,2),(2,3),(1,3)}
    assert len(ai.knowledge) == 0

    #The second movement is (0,0) and it was safe
    ai.add_knowledge((0,0),1)
    assert ai.moves_made == {(1,2),(0,0)}
    assert ai.safes == {(1,2),(0,1),(0,2),(0,3),(1,1),(2,1),(2,2),(2,3),(1,3),(0,0)}
    assert ai.mines == {(1,0)}
    assert len(ai.knowledge) == 0

def test_make_safe_move():
    ai = MinesweeperAI()
    
    #The first movement was (1,2) and it is thoroughly safe
    ai.add_knowledge((1,2),0)
    assert ai.moves_made == {(1,2)}
    assert ai.safes == {(1,2),(0,1),(0,2),(0,3),(1,1),(2,1),(2,2),(2,3),(1,3)}
    assert len(ai.knowledge) == 0

    #The second movement is (0,0) and it was safe
    ai.add_knowledge((0,0),1)
    assert ai.moves_made == {(1,2),(0,0)}
    assert ai.safes == {(1,2),(0,1),(0,2),(0,3),(1,1),(2,1),(2,2),(2,3),(1,3),(0,0)}
    assert ai.mines == {(1,0)}
    assert len(ai.knowledge) == 0

    #TESTING MAKE_SAFE_MOVE
    assert ai.make_safe_move() in {(0,1),(0,2),(0,3),(1,1),(2,1),(2,2),(2,3),(1,3)}
    assert ai.make_safe_move() != {(1,0)}
    assert len(ai.make_safe_move()) == 2

def test_make_random_move():
    ai = MinesweeperAI()
    
    #The first movement was (1,2) and it is thoroughly safe
    ai.add_knowledge((1,2),0)
    assert ai.moves_made == {(1,2)}
    assert ai.safes == {(1,2),(0,1),(0,2),(0,3),(1,1),(2,1),(2,2),(2,3),(1,3)}
    assert len(ai.knowledge) == 0

    #The second movement is (0,0) and it was safe
    ai.add_knowledge((0,0),1)
    assert ai.moves_made == {(1,2),(0,0)}
    assert ai.safes == {(1,2),(0,1),(0,2),(0,3),(1,1),(2,1),(2,2),(2,3),(1,3),(0,0)}
    assert ai.mines == {(1,0)}
    assert len(ai.knowledge) == 0

    #TESTING MAKE_RANDOM_MOVE
    assert ai.make_random_move() not in ai.moves_made
    assert ai.make_random_move() != {(1,0)}
    assert len(ai.make_random_move()) == 2