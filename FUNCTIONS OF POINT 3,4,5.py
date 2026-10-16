FUNCTIONS OF POINT 3,4,5

POINT 3: 

surr_cells = self.surrounding_cells(cell)
self.knowledge.append(Sentence(surr_cells,count))




POINT and 4:
def clean_tracked_safes_mines(self,a_cells_group,obj): #Well done
    """
    Find safe and mine cells in the surr_cells
    Return just undefined cells in a set of tuples
    """
    #if there are not cells
    if not a_cells_group: 
        self.knowledge.remove(obj)
        
    #Clean safes
    if safe_intersection := a_cells_group.intersection(self.safes):
        for cell in safe_intersection:
            self.mark_safes(cell)

    #Clean mines
    if mine_intersection:=a_cells_group.intersection(self.mines):
        for cell in mine_intersection:
            self.mark_mines(cell)


#def mines_sentence(self,a_cells_group):
    """
    Find out if a cells group is or is not quite a mines sentence
    Return True or False
    """

Intersection JUST RUNS WITH EQUAL COUNTS

if other.count>sentence.count:
    
elif other.count==sentence.count:
    mark_safe which are not intersection

    Delete current sentence and other sentence

    create intersection sentence with the previous count
elif other.count<sentence.count:
    ""

 

-----------------------------------------------------------------
Make sure sentence is subset of other 

Intersection between them



other.cells-sentence.cells= new surr_cells






