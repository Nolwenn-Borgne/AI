import copy
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

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # Any time the number of cells is equal to the count, we know that all of that sentence cells must be mines
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # Any time we have a sentence whose count is 0, we know that all of that sentence's cells must be safe
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # we remove the cell from the sentence and decrease the count because we have found a mine
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # we simply remove the cell from the sentence
        if cell in self.cells:
            self.cells.remove(cell)


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

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
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
        # 1 mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2 mark the cell as safe
        self.mark_safe(cell)

        # 3 add a new sentence to the AI's knowledge base based on the value of 'cell' and 'count'

        #   get the nearby cells and remove cells that are known safes or mines
        nearby_cells = set()

        #   Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update nearby_cells if cell in bounds and not an already done move or a known mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.moves_made and (i, j) not in self.mines:
                        nearby_cells.add((i, j))
                    elif (i, j) in self.mines:
                        # if the cell is a mine, we have to decrease the count
                        count = count - 1

        # create a Sentence and add it to the knowledge base if not already in it
        if nearby_cells != set():
            new_sentence = Sentence(nearby_cells, count)
            if new_sentence not in self.knowledge:
                self.knowledge.append(new_sentence)

        while True:
            new = False

            # 4 mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
            for sentence in self.knowledge:
                known_safes_cells = copy.deepcopy(sentence.known_safes())
                for cell in known_safes_cells:
                    self.mark_safe(cell)
                known_mines_cells = copy.deepcopy(sentence.known_mines())
                for cell in known_mines_cells:
                    self.mark_mine(cell)

            # remove empty sentences
            self.knowledge[:] = (x for x in self.knowledge if len(x.cells) != 0)

            # copy of the knowledge base
            knowledge_copy = list(self.knowledge)

            # 5 add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
            # use the subset method
            for sentence1 in knowledge_copy:
                for sentence2 in knowledge_copy:
                    if sentence1 is sentence2:
                        continue
                    if sentence1.cells.issubset(sentence2.cells):
                        new_sentence = Sentence(
                            sentence2.cells - sentence1.cells,
                            sentence2.count - sentence1.count)
                        self.knowledge.append(new_sentence)
                        new = True

            return new

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # return None if there is no more possible move to do ie if the moves_made and the mines cover all the board
        if (len(self.moves_made) + len(self.mines)) == self.height * self.width:
            return None

        # if there still exists a possible move
        # we choose randomly among cells that have not already been chosen and that are not mines
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                return (i, j)
