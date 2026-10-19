import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if self.cells and self.count == len(self.cells):
            return set(self.cells)
        return set()

    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #Delete the mine cell
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            #Sustracts one to the count
        self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #Delete the safe cell
        if cell in self.cells:
            self.cells.remove(cell)
        self.safes.add(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):#DONE BY D
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):#DONE BY D
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        #1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        #2) mark the cell as safe and updates any sentences that 
            # contain the cell as well. [ALREADY Developed and tested deeply]
        self.mark_safe(cell)
            #I NEED TO UPDATE any sentences that contain the cell as well
            #Make inferences and one more time update the knowledgebase

        #3) add a new sentence to the AI’s knowledge base to indicate that count of the cell’s neighbors are mines. 
            #Be sure to only include cells whose state is still undetermined in the sentence.
        surr_cells=self.surrounding_cells(cell)
        self.knowledge.append(Sentence(surr_cells,count))

        

        #4) mark any additional cells as safe or as mines if it can be concluded
            #    based on the AI's knowledge base and #5 add any new sentences to the AI's knowledge base
               #    if they can be inferred from existing knowledge

        KB_change=True

        while KB_change==True:
            KB_change = False

            for sentence in self.knowledge[:]:
                if KB_change := self.clean_tracked_safes_mines(sentence.cells,sentence):
                    break
                elif sentence.count == len(sentence.cells) and sentence.count>0:
                    self.entire_mines_sentence(sentence)
                    KB_change=True
                    break
                elif sentence.cells and (sentence.count==0):
                    self.entire_safes_sentence(sentence)
                    KB_change=True
                    break
                elif KB_change := self.subset_inferences(sentence):#LOOKING FOR SUBSETS
                    break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        """1 Sustract  mines from self.moves_made.
           2 Sustract  intersection of (self.moves_made from self.safes) from self.safes"""
        if len(self.safes) > len (self.moves_made):
            inferenced_safes = list( self.safes - self.moves_made.intersection(self.safes) )
            return random.choice(inferenced_safes)
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        the_grid = self.yields_grid()

        not_selected = the_grid - self.moves_made
        availability = list(not_selected - self.mines)
        return random.choice(availability)
        
    def surrounding_cells(self,cell):
        """
        Returns the surrounding cells (set of tuples) of 
        the cell already clicked
        """
        around_cells=set()
        i,j = cell

        row_before = False
        row_after = False
        col_left = False
        col_right = False
        
        if i-1 >= 0:
            row_before= True
        if i+1 <= self.height-1:
            row_after = True
        if j-1 >= 0:
            col_left = True
        if j+1 <= self.width-1:
            col_right = True
    
        #ANALYZING ROWS
        if row_before: #IS THERE A ROW BEFORE?
            #UP CELL
            around_cells.add((i-1,j))
            if col_left: #IS THERE A LEFT COLUMN?
                #LEFT UP SQUARE
                around_cells.add((i-1,j-1))
            if col_right: #IS THERE A RIGHT COLUMN?
                #RIGHT UP SQUARE
                around_cells.add((i-1,j+1))
    
        if row_after: #IS THERE A ROW AFTER?
            #DOWN CELL
            around_cells.add((i+1,j))
            if col_left: #IS THERE A LEFT COLUMN?
                #LEFT DOWN SQUARE
                around_cells.add((i+1,j-1))
            if col_right: #IS THERE A RIGHT COLUMN?
                #RIGHT DOWN SQUARE
                around_cells.add((i+1,j+1))
    
        #ANALYZING COLUMNS
        if col_left:
            around_cells.add((i,j-1))
        if col_right:
            around_cells.add((i,j+1))

        return around_cells

    def clean_tracked_safes_mines(self,a_cells_group,obj): #Already tested
        """
        Mark safe and mines cells based on the tracking lists and
        remove a sentence in case of the are not more cells.
        """
        if a_cells_group:   
            #Clean safes
            if safe_intersection := a_cells_group.intersection(self.safes):
                for cell in safe_intersection:
                    self.mark_safe(cell)
                return True
            #Clean mines
            elif mine_intersection:=a_cells_group.intersection(self.mines):
                for cell in mine_intersection:
                    self.mark_mine(cell)
                return True
        else:
            self.knowledge.remove(obj)
            return True

    def entire_mines_sentence(self,sentence_obj):
        """
        It looks for a sentence that it is 
        completely undentified mines made. 
        Once it mark as mine delete the entire sentence object"""
        
        for cell in sentence_obj.cells.copy():#MARK AS MINE EACH ONE
            self.mark_mine(cell)
        self.knowledge.remove(sentence_obj) #DELETE THE ENTIRE OBJECT

    def entire_safes_sentence(self,sentence_obj):
        """
        It looks for a sentence that it is 
        completely undentified safes made. 
        Once it mark as mine delete the entire sentence object"""

        for cell in sentence_obj.cells.copy():#MARK AS SAFE EACH ONE
            self.mark_safe(cell)
        self.knowledge.remove(sentence_obj) #DELETE THE ENTIRE OBJECT

    def subset_inferences(self,copy_sentence):
        """
        It looks for a subset, if there is, so make the corresponding
        inferences between those and immediately after the changes 
        ends the loop with return.
        
        It returns True if it make changes, otherwise False"""
        for other in self.knowledge[:]: #LOOKING FOR SUBSETS 
            if copy_sentence.cells.issubset(other.cells):
                if not other is copy_sentence:
                    cells_change = other.cells - copy_sentence.cells
                    count_change = other.count - copy_sentence.count
                    other.cells = cells_change
                    other.count = count_change
                    return True
        return False

    def yields_grid(self):
        the_grid = set()
        for i in range(self.height):
            for j in range(self.width):
                the_grid.add((i,j))
        return the_grid
