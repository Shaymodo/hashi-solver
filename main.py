from multiprocessing import Value
import sys


class PuzzleDigit:                              # Class for each puzzle number that isn't 0
    def __init__(self, num, location):
        self.full_num = num                     # Initialize the actual number
        self.location = location                # Store where the number is in the layout
        self.remaining_num = num                # Initialize the number counting down for each line drawn
        self.neighbors = []
        self.top_edge
        self.bot_edge
        self.left_edge
        self.right_edge

    def done(self):                             # Returns True if all the lines drawn for this number
        return self.remaining_num == 0

    def get_location(self):                     # Returns a tuple with the row and column of the object in the 2d array
        return self.location

    def set_top_edge(self):
        self.top_edge = True

    def get_top_edge(self):
        return self.top_edge

    def set_bot_edge(self):
        self.bot_edge = True

    def get_bot_edge(self):
        return self.bot_edge

    def set_left_edge(self):
        self.left_edge = True

    def get_left_edge(self):
        return self.left_edge

    def set_right_edge(self):
        self.right_edge = True

    def get_right_edge(self):
        return self.right_edge

    def get_full_num(self):                           # Returns the value of the full_num
        if self.full_num == type(int):                      # Return ints
            return self.full_num
        elif self.full_num == "-" or self.full_num == "|":            # Return single or double for lines
            return ("single")
        return ("double")

    def set_one_vert_line(self):                # Sets number value to |
        pass

    def set_two_vert_line(self):                # Sets number value to d
        pass

    def set_one_hori_line(self):                # Sets number value to -
        pass

    def set_one_hori_line(self):                # Sets number value to =
        pass

    def get_remaining_num(self):                # Returns the remaining number
        return self.remaining_num

    def remaining_num_decrement(self, dec_val):      # Decreases the remaining amount of lines that can be drawn
        self.remaining_num -= dec_val

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def get_neighbors(self):
        return self.neighbors


def main():
    layout = []
    height, width = 0, 0
    flag = 0
    while flag == 0:                         # Loops until they make their choice
        print("Welcome to Hashi Solver! Please select what you would like to do")
        print("1: Manually input puzzle numbers")
        print("2: Use newfangled tech to have the program analyze a picture (Not implemented yet)")
        print("3: View puzzle you have inputted")
        print("4: Solve current puzzle")
        print("5: Quit")
        choice = int(input("Please select an option: "))
        print("\033[H\033[J", end="")       # Clears the screen


        if choice == 1:                     # Manual Entry
            try:
                while height < 4: height = int(input("Please enter the height of the puzzle: "))
                while width < 4: width = int(input("Please enter the width of the puzzle: "))
            except ValueError:
                print("Input a valid integer")
                break
            layout, num_total = manual_layout_input(width, height)
            print("\033[H\033[J", end="")   # Clears the screen

        elif choice == 2:                   # Automatic Entry
            print("This isn't implemented yet, I just told you that")

        elif choice == 3:                   # View current puzzle
            if layout != []:
                for i in range(height):
                    print("[", end=" ")
                    for j in range(width):
                        print (f"{layout[i][j].get_full_num()}", end=" ")
                    print("]")
            else:
                print("Current puzzle is not valid")

        elif choice == 4:                   # Solve current puzzle and display it
            if layout != []:
                solved_layout = solver(layout, num_total)
                for i in range(height):
                    print("[", end=" ")
                    for j in range(width):
                        print (f"{solved_layout[i][j].get_full_num()}", end=" ")
                    print("]")
            else:                           # If layout is empty, puzzle does not exist
                print("No current puzzle")

        elif choice == 5:                   # Quit
            sys.exit()

        else:                               # Error message for invalid input
            print("Not a valid choice")

        print()


def manual_layout_input(width, height):         # Iterates through the 2D array and asks for user input for each value
    layout = []                                 # Creates empty row and column arrays
    num_total = 0
    for i in range (height):
        layout_inner = []
        print()
        print (f"Row {i+1}")
        for j in range (width):
            while True:
                try:                            # Ensure input is an int
                    num = int(input("Please input the next number 0-8, enter 0 if empty: "))
                    if num < 0 or num > 8:
                        print("Not between 0 and 8, try again")
                    else:
                        valid_digit = PuzzleDigit(num, (i,j))
                        layout_inner.append(valid_digit)        # Adds object with valid digit to the row
                        print("[", end=" ")
                        for k in range (len(layout_inner)):     # Displays row for user to see
                            print (f"{layout_inner[k].get_full_num()}", end=" ")
                        if num != 0:
                            num_total += 1
                        print("]")
                        break
                except ValueError:
                    print("Your input was not an integer, try again")

        layout.append(layout_inner)                 # Adds each row here
                    
    return layout, num_total

def solver(layout, num_total):                      # Calls solver helper functions depending on the value of each number in the layout
    solved = False
    assign_edges(layout)                            # Assigns each non 0 object edges accordingly
    while not solved:                               # Loops until puzzle is solved
        finished_nums = 0
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if (layout[i][j].done()):                # Checks current object to see if all lines are drawn
                    finished_nums += 1
                else:
                    print(layout[i][j].done())      #TEMP prints nothing for 0's, prints false for each int in array
                    num = layout[i][j].get_full_num()
                    location = layout[i][j].get_location()
                    if num == "-" or num == "=" or num == "|" or num == "dubvert":
                        break
                    if num == 1:
                        layout = solver_one(layout, location)
                    elif num == 2:
                        layout = solver_two(layout, location)
                    elif num == 3:
                        layout = solver_three(layout, location)
                    elif num == 4:
                        layout = solver_four(layout, location)
                    elif num == 5:
                        layout = solver_five(layout, location)
                    elif num == 6:
                        layout = solver_six(layout, location)
                    elif num == 7:
                        layout = solver_seven(layout, location)
                    elif num == 8:
                        layout = solver_eight(layout, location)

        if finished_nums == num_total:
            solved = True                               # Ends the loop

        solved = True                           # TEMPORARY TO PREVENT INFINITE LOOPING
    return layout

def solver_one(layout, location, neighbors = 0):            # Solves if remaining_num is 1
    i,j = location

def solver_two(layout, location, neighbors = 0):            # Solves if remaining_num is 2
    pass

def solver_three(layout, location, neighbors = 0):          # Solves if remaining_num is 3
    pass

def solver_four(layout, location, neighbors = 0):           # Solves if remaining_num is 4
    pass

def solver_five(layout, location, neighbors = 0):           # Solves if remaining_num is 5
    pass

def solver_six(layout, location, neighbors = 0):            # Solves if remaining_num is 6
    pass

def solver_seven(layout, location, neighbors = 0):          # Makes single lines for all directions, checks further
    pass

def solver_eight(layout, location, neighbors = 0):          # Makes double lines for all directions
    pass

def assign_edges(layout):                       # Iterates through layout and 
    for i in range(len(layout)):
        for j in range(len(layout[0])):
            if i == 0 or i == 1: layout[i][j].set_top_edge()
            elif i == len(layout) or i == (len(layout)-1): layout[i][j].set_bot_edge()
            if j == 0 or j == 1: layout[i][j].set_left_edge()  
            elif j == len(layout[0]) or j == (len(layout[0])-1): layout[i][j].set_right_edge()

def check_neighbors(layout, current):           # Gives a list of neighbors with their remaining numbers and locations to the class object
    neighbors = []
    neighbors.append(check_top(layout, current))
    neighbors.append(check_bot(layout, current))
    neighbors.append(check_left(layout, current))
    neighbors.append(check_right(layout, current))
    i, j = current
    layout[i][j].set_neighbors(neighbors)
    return

def check_top(layout, current):         # Checks top neighbors
    i,j = current
    temp = i
    if not layout[i][j].get_top_edge():         # If the object is not in the top 2 edges, checks for vertical neighbors
        while temp > -1:
            if layout[temp][j].get_full_num() == 0: temp -= 1       # If the number of the object is 0 it keeps going
            else:
                if layout[temp][j].get_full_num() == "single":      # Already has a single line
                    temp -= 1
                    while layout[temp][j].get_full_num() == "single":       # Loops until the value is no longer a line
                        temp -= 1
                    return (layout[temp][j].get_remaining_num(), layout[temp][j].get_location())    # Adds remaining num and location of neighbor above current location to neighbors list
                elif layout[temp][j].get_remaining_num() == 0:        # Non valid neighbor
                    break 
                else:
                    return (layout[temp][j].get_remaining_num(), layout[temp][j].get_location())    # Adds remaining num and location of neighbor above current location to neighbors list
        return ("none")         # Returns none if no neighbors were found

def check_bot(layout, current):         # Checks bottom neighbors
    i,j = current
    temp = i
    height = len(layout)
    if not layout[i][j].get_bot_edge():         # If the object is not in the bot 2 edges, checks for vertical neighbors
        while temp < height:
            if layout[temp][j].get_full_num() == 0: temp += 1       # If the number of the object is 0 it keeps going
            else:
                if layout[temp][j].get_full_num() == "single":      # Already has a single line
                    temp += 1
                    while layout[temp][j].get_full_num() == "single":       # Loops until the value is no longer a line
                        temp += 1
                    return (layout[temp][j].get_remaining_num(), layout[temp][j].get_location())    # Adds remaining num and location of neighbor above current location to neighbors list
                elif layout[temp][j].get_remaining_num() == 0:        # Non valid neighbor
                    break 
                else:
                    return (layout[temp][j].get_remaining_num(), layout[temp][j].get_location())    # Adds remaining num and location of neighbor above current location to neighbors list
        return ("none")         # Returns none if no neighbors were found

def check_left(layout, current):        # Checks left neighbors
    i,j = current
    temp = j
    if not layout[i][j].get_left_edge():         # If the object is not in the left 2 edges, checks for horizontal neighbors
        while temp > -1:
            if layout[i][temp].get_full_num() == 0: temp -= 1       # If the number of the object is 0 it keeps going
            else:
                if layout[i][temp].get_full_num() == "single":      # Already has a single line
                    temp -= 1
                    while layout[i][temp].get_full_num() == "single":       # Loops until the value is no longer a line
                        temp -= 1
                    return (layout[i][temp].get_remaining_num(), layout[i][temp].get_location())    # Adds remaining num and location of neighbor left of current location to neighbors list
                elif layout[i][temp].get_remaining_num() == 0:        # Non valid neighbor
                    break 
                else:
                    return (layout[i][temp].get_remaining_num(), layout[i][temp].get_location())    # Adds remaining num and location of neighbor left of current location to neighbors list
        return ("none")         # Returns none if no neighbors were found

def check_right(layout, current):         # Checks right neighbors
    i,j = current
    temp = i
    width = len(layout[0])
    if not layout[i][j].get_bot_edge():         # If the object is not in the bot 2 edges, checks for vertical neighbors
        while temp < width:
            if layout[i][temp].get_full_num() == 0: temp += 1       # If the number of the object is 0 it keeps going
            else:
                if layout[i][temp].get_full_num() == "single":      # Already has a single line
                    temp += 1
                    while layout[i][temp].get_full_num() == "single":       # Loops until the value is no longer a line
                        temp += 1
                    return (layout[i][temp].get_remaining_num(), layout[i][temp].get_location())    # Adds remaining num and location of neighbor above current location to neighbors list
                elif layout[i][temp].get_remaining_num() == 0:        # Non valid neighbor
                    break 
                else:
                    return (layout[i][temp].get_remaining_num(), layout[i][temp].get_location())    # Adds remaining num and location of neighbor above current location to neighbors list
        return ("none")         # Returns none if no neighbors were found

def connect(layout, current, target, amount):               # Connects current location and target location with either 1 or 2 lines
    
    # code to swap each 0 in between with lines
    # MAKE SURE TO TEST IF THERE IS ALREADY A SINGLE LINE THAT BECOMES A DOUBLE LINE

    return

if __name__ == "__main__":
    main()
