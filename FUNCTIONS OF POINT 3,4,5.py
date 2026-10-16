FUNCTIONS OF POINT 3,4,5

POINT 3: 

surr_cells = self.surrounding_cells(cell)
self.knowledge.append(Sentence(surr_cells,count))




POINT and 4:
def clean_tracked_safes_mines(self,a_cells_group): #Well done
    """
    Find safe and mine cells in the surr_cells
    Return just undefined cells in a set of tuples
    """
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





