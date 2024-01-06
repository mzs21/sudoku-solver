class Board:
    def __init__(self, board): 
        # The __init__ method is a special method that allows to instantiate an object to a customized state. When a class implements an __init__ method, __init__ is automatically called upon instantiation

        # `self`` is a reference to the instance of the class. It is a convention to name this parameter self
        
        self.board = board

        # self.board refers to the board attribute of the instance of the class. It's a variable that belongs to the object created from the Board class

    def __str__(self):
        # This method is automatically called when str() function is called on an instance of the class or when you use print() with the object

        # Borders using ASCII art style

        upper_lines = f'\n╔═══{"╤═══"*2}{"╦═══"}{"╤═══"*2}{"╦═══"}{"╤═══"*2}╗\n'
        middle_lines = f'╟───{"┼───"*2}{"╫───"}{"┼───"*2}{"╫───"}{"┼───"*2}╢\n'
        lower_lines = f'╚═══{"╧═══"*2}{"╩═══"}{"╧═══"*2}{"╩═══"}{"╧═══"*2}╝\n'

        board_string = upper_lines 
        # Starting point for building the entire visual representation of the sudoku board
        
        for index, line in enumerate(self.board): # line = content

            # The enumerate() function is a built-in function in Python that takes an iterable (such as a list, tuple, or string) and returns an iterator that produces tuples containing indices and corresponding values from the iterable
            
            row_list = [] # Elements of a single row in the sudoku board

            for square_no, part in enumerate([line[:3], line[3:6], line[6:]], start=1):
                # Split each row in three segments, in order to represent the 3x3 squares properly. start = 1 will start the enumeration from 1

                row_square = '|'.join(str(item) for item in part) # Access all elements and join them as string

                row_list.extend(row_square) # row_list will now have the accessed elements 

                if square_no != 3: # Square number is the last or not, if it's not
                    row_list.append('║') # Append this ASCII character

            row = f'║ {" ".join(row_list)} ║\n' # Joining the elements o row_list with a space

            row_empty = row.replace('0', ' ') # Replacing "0"s with empty string in the row

            board_string += row_empty # Adding the empty rows to the sudoku board

            if index < 8: 
                # Whether the current index of the board is less than 8 or not. The last row of the sudoku board has an index of 8
                
                if index % 3 == 2: 
                # Verifying if the row is the last row inside a 3x3 square. This occurs when index % 3 is equal to 2
                    
                    board_string += f'╠═══{"╪═══"*2}{"╬═══"}{"╪═══"*2}{"╬═══"}{"╪═══"*2}╣\n'
                    # If it is, add the following border style to the board

                else:
                    board_string += middle_lines
                    # Else, add the middle lines to the board
            else:
                board_string += lower_lines
                # If the current index is not less than 8 or the last row, then add the bottom border

        return board_string # Sudoku board

    def find_empty_cell(self):
        for row, contents in enumerate(self.board):
            try:
                col = contents.index(0) 
                # Attempt to find the index of the first occurrence of 0 in the current row and assigning it
                
                return row, col 
                # If 0 is found, the code immediately returns a tuple (row, col) with the row index and column index of the empty cell.
            
            except ValueError: # If 0 is not found, it'll throw the error  
                pass
        
        return None 
        # If the loop completes without finding any empty cells, the method should return None to indicate that the sudoku board is filled

    def valid_in_row(self, row, num): 
        # Method that checks if a given number can be inserted into a specified row of the sudoku board
        # row: Representing the row index
        # num: Representing the number to be checked
        
        return num not in self.board[row]  # If the number is not already present in that row
    
        # If num is not in the row, the expression evaluates to True and it means the number is valid for insertion

        # If num is in the row, the expression evaluates to False and insertion would violate the rules

    def valid_in_col(self, col, num):
        # Method that checks if a number can be inserted in a specified column of the sudoku board by checking if the number is not already present in that column for any row
        # col: Representing the column index
        # num: representing the number to be checked
        
        return all(
            self.board[row][col] != num 
            # Check if a given number is not equal to the number in the specified column of the current row.
            for row in range(9) # From index 0 to 8
        )
    
        # The generator expression all() function checsk if all the elements in the column are different from num
    
    def valid_in_square(self, row, col, num):
        # Method that checks if a number can be inserted in the 3x3 square
        # row: Represents the row index
        # col: Represents the column index
        # num: Represents the number to be checked

        row_start =  (row // 3) * 3 # Calculate the starting row index for the 3x3 block in the board grid
        col_start = (col // 3) * 3 # Calculate the starting column index for the 3x3 block in the board grid

        for row_no in range(row_start, row_start + 3):
            for col_no in range(col_start, col_start + 3):
            # Looping through the eleements in both row and col
                
                if self.board[row_no][col_no] == num:
                # Check if the specified number (num) is already present in the current cell of the 3x3 square
                    return False # The number cannot be inserted into the square
        return True 
        # If the number is not present, it can be inserted into the square without violating the rules of sudoku

    def is_valid(self, empty, num):
        # Method checks if a given number is a valid choice for an empty cell in the sudoku board by validating its compatibility with the row, column, and 3x3 square of the specified empty cell.
        # empty: A tuple representing the row and column indices of an empty cell
        # num: Representing the number to be checked

        row, col = empty # Unpacking empty tuple

        valid_in_row = self.valid_in_row(row, num) 
        # Check if the number is valid for insertion in the specified row 

        valid_in_col = self.valid_in_col(col,num) 
        # Check if the number is valid for insertion in the specified column 

        valid_in_square = self.valid_in_square(row, col, num)
        # Check if the number is valid for insertion in the 3x3 square that contains the specified cell

        return all(
            [valid_in_row, valid_in_col, valid_in_square]
        )
        # This will verify that all the function calls return True
    
    def solver(self):
        # Method that attempts to solve the sudoku in-place, meaning it would modify the existing sudoku board rather than creating a new one

        if (next_empty := self.find_empty_cell()) is None:
        # By using the walrus operator, the assignment and the conditional check can be combined into a single line, making the code more concise and readable.
            
            return True    
            # If there are no empty cells (i.e., next_empty is None), the puzzle is solved. So, return True
        
        else: # Cater the case where there are empty cells and the puzzle is unsolved
            for guess in range(1,10): 
            # If there are empty cells, the loop iterates over numbers from 1 to 9 (inclusive)
                
                if self.is_valid(next_empty, guess):
                # For each number (guess), check if the number is a valid choice for the current empty cell. If the guess is valid, the method updates the sudoku board with the guess by assigning guess to the cell specified by next_empty.

                    row, col = next_empty # Unpacking next_empty tuple

                    self.board[row][col] = guess # Assigning the guess value to the specified cell

                    if self.solver(): # Solving rest of the sudoku and if it's true
                            return True
                
                    self.board[row][col] = 0
                    # If self.solver() returns False, this means the guess led to an unsolvable sudoku. Undo the guess by setting the cell value back to 0
        
        return False # None of the guesses leads to a solution

def solve_sudoku(board): #  function to print and solve the sudoku board
    gameboard = Board(board) # This initializes the sudoku board with the given initial state

    print(f'\nPuzzle to solve:\n{gameboard}')
    if gameboard.solver():
        print('\nSolved puzzle:')
        print(gameboard)
    else:
        print('\nThe provided puzzle is unsolvable.')

    return gameboard

puzzle = [
  [0, 0, 2, 0, 0, 8, 0, 0, 0],
  [0, 0, 0, 0, 0, 3, 7, 6, 2],
  [4, 3, 0, 0, 0, 0, 8, 0, 0],
  [0, 5, 0, 0, 3, 0, 0, 9, 0],
  [0, 4, 0, 0, 0, 0, 0, 2, 6],
  [0, 0, 0, 4, 6, 7, 0, 0, 0],
  [0, 8, 6, 7, 0, 4, 0, 0, 0],
  [0, 0, 0, 5, 1, 9, 0, 0, 8],
  [1, 7, 0, 0, 0, 6, 0, 0, 5]
]

solve_sudoku(puzzle)