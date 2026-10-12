import pytest
from minesweeper import Sentence

the_set={1,2,3,5}
s=Sentence(the_set,3)
def test_mark_mine():
    s.mark_mine(2)
    assert s.cells=={1,3,5}
    assert s.count==2

def test_mark_safe_and_known_safes():
    s.mark_safe(5) #testing mark_safe and...
    assert s.known_safes()=={5} #...mark_safe

