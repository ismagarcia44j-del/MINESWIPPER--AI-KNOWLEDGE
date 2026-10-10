import pytest
from minesweeper import Sentence

def test_mark_mine():
    the_set={1,2,3,4}
    s=Sentence(the_set,3)
    s.mark_mine(2)
    assert s.cells=={1,3,4}
    assert s.count==2
