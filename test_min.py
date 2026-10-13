import pytest
from minesweeper import Sentence, MinesweeperAI

the_set={1,2,3,5}
s=Sentence(the_set,3)
def test_mark_mine():
    s.mark_mine(2)
    assert s.cells=={1,3,5}
    assert s.count==2

def test_mark_safe_and_known_safes():
    s.mark_safe(5) #testing mark_safe and...
    assert s.known_safes()=={5} #...mark_safe

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

#def test_surrounding_cells_one_side():

