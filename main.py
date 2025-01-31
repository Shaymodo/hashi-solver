from multiprocessing import Value
import sys


class PuzzleDigit:                              # Class for each puzzle number that isn't 0
    def __init__(self, num, location):
        self.full_num = num                     # Initialize the actual number
        self.location = location                # Store where the number is in the layout
        self.remaining_num = num                # Initialize the number counting down for each line drawn
        self.neighbors = []
        self.top_edge = False
        self.bot_edge = False
        self.left_edge = False
        self.right_edge = False

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
        if self.full_num == "-" or self.full_num == "|":            # Return single for lines
            return ("single")
        elif self.full_num == "=" or self.full_num == "d":          # Return single or double for lines
            return ("double")
        return self.full_num

    def set_one_vert_line(self):                # Sets number value to |
        self.full_num = "|"
        self.remaining_num = "|"

    def set_two_vert_line(self):                # Sets number value to d
        self.full_num = "d"
        self.remaining_num = "d"

    def set_one_hori_line(self):                # Sets number value to -
        self.full_num = "-"
        self.remaining_num = "-"

    def set_two_hori_line(self):                # Sets number value to =
        self.full_num = "="
        self.remaining_num = "="

    def get_remaining_num(self):                # Returns the remaining number
        return self.remaining_num

    def remaining_num_decrement(self, dec_val):      # Decreases the remaining amount of lines that can be drawn
        self.remaining_num -= dec_val

    def set_neighbors(self, neighbors):             # Sets neighbors variable to the list passed in
        self.neighbors = neighbors

    def get_neighbors(self):
        return self.neighbors                   # Returns neighbors list


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
                    num = layout[i][j].get_remaining_num()
                    current = layout[i][j].get_location()
                    if num == "-" or num == "=" or num == "|" or num == "dubvert":
                        break
                    if num == 1:
                        layout = solver_one(layout, current)
                    elif num == 2:
                        layout = solver_two(layout, current)
                    elif num == 3:
                        layout = solver_three(layout, current)
                    elif num == 4:
                        layout = solver_four(layout, current)
                    elif num == 5:
                        layout = solver_five(layout, current)
                    elif num == 6:
                        layout = solver_six(layout, current)
                    elif num == 7:
                        layout = solver_seven(layout, current)
                    elif num == 8:
                        layout = solver_eight(layout, current)

        if finished_nums == num_total:
            solved = True                               # Ends the loop

        solved = True                           # TEMPORARY TO PREVENT INFINITE LOOPING
    return layout

def solver_one(layout, location, neighbors = 0):            # Solves if remaining_num is 1
    if neighbors == 0:
        neighbors = modify_neighbors(layout, location)

    neighbor_count = 4 - neighbors.count("none")

    if neighbor_count == 1:                 # If there is only one neighbor, connect it with single line
        target = neighbors[0]
        counter = 1
        while target == "none":
            target = neighbors[counter]
            counter += 1
        connect(layout, location, target, 1)

def solver_two(layout, location, neighbors = 0):            # Solves if remaining_num is 2
    if neighbors == 0:
        neighbors = modify_neighbors(layout, location)

    neighbor_top = (neighbors[0], neighbors[1])
    neighbor_bot = (neighbors[2], neighbors[3])
    neighbor_left = (neighbors[4], neighbors[5])
    neighbor_right = (neighbors[6], neighbors[7])

    neighbor_count = 4 - neighbors.count("none")
    total_remaining = neighbors[0] + neighbors[2] + neighbors[4] + neighbors[6]
    neighbor_nums = [neighbors[0], neighbors[2], neighbors[4], neighbors[6]]
    neighbor_locations = [neighbors[1], neighbors[3], neighbors[5], neighbors[7]]

    if neighbor_count < 4:

        if total_remaining == 2:                # If there are only two available numbers nearby, connect all lines possible
            if neighbor_count == 1:                 # 1 neighbor
                target = "none"
                counter = 0
                while target == "none":
                    target = neighbors[counter]
                    counter += 1
                connect(layout, location, target, 2)

            if neighbor_count == 2:                 # 2 neighbors
                target = "none"
                counter = 0
                while neighbor_count > 0:
                    while target == "none":
                        target = neighbor_locations[counter]
                        counter += 1
                    connect(layout, location, target, 1)
                    neighbor_count -= 1

        elif neighbor_count == 2:               # 2 neighbors with varying numbers
            if neighbor_nums.count(1) == 1:         # 1 and any other number, connect one line to other number
                if neighbor_top[0] in (2,3,4,5,6,7,8): x = neighbor_top[1]
                elif neighbor_bot[0] in (2,3,4,5,6,7,8): x = neighbor_bot[1]
                elif neighbor_left[0] in (2,3,4,5,6,7,8): x = neighbor_left[1]
                elif neighbor_right[0] in (2,3,4,5,6,7,8): x = neighbor_right[1]
                connect(layout, location, x, 1)

            elif neighbor_nums.count(2) == 2:       # 2 and 2, connect one line to each
                target = "none"
                counter = 0
                while neighbor_count > 0:
                    while target == "none":
                        target = neighbor_locations[counter]
                        counter += 1
                    connect(layout, location, target, 1)
                    neighbor_count -= 1

            elif neighbor_nums.count(2) == 1:       # 2 and any number 3 or higher, connect one line to other number
                if neighbor_top[0] in (3,4,5,6,7,8): x = neighbor_top[1]
                elif neighbor_bot[0] in (3,4,5,6,7,8): x = neighbor_bot[1]
                elif neighbor_left[0] in (3,4,5,6,7,8): x = neighbor_left[1]
                elif neighbor_right[0] in (3,4,5,6,7,8): x = neighbor_right[1]
                connect(layout, location, x, 1)

        # 3 neighbors MAY NOT WORK WITH REMAINING NUMS, ADJUST FOR FULL NUM INSTEAD

def solver_three(layout, location, neighbors = 0):          # Solver if remaining_num is 3
    if neighbors == 0:
        neighbors = modify_neighbors(layout, location)

    neighbor_top = (neighbors[0], neighbors[1])
    neighbor_bot = (neighbors[2], neighbors[3])
    neighbor_left = (neighbors[4], neighbors[5])
    neighbor_right = (neighbors[6], neighbors[7])

    neighbor_count = 4 - neighbors.count("none")
    total_remaining = neighbors[0] + neighbors[2] + neighbors[4] + neighbors[6]
    neighbor_nums = [neighbors[0], neighbors[2], neighbors[4], neighbors[6]]
    neighbor_locations = [neighbors[1], neighbors[3], neighbors[5], neighbors[7]]

    if neighbor_count < 4:
        pass

    # 2 neighbors  -  draw single line to each neighbor, then call solver_one

    # 3 neighbors   -   1, 1, any  -   1, 2, any


def solver_four(layout, location, neighbors = 0):           # Solver if remaining_num is 4
    if neighbors == 0:
        neighbors = modify_neighbors(layout, location)

def solver_five(layout, location, neighbors = 0):           # Solver if remaining_num is 5
    if neighbors == 0:
        neighbors = modify_neighbors(layout, location)

    # 3 neighbors  -  single line for each neighbor, then call solver_two
    # 4 neighbors  -  1, 1, any, any draw two single lines call solver_three  -  1, 2, 2, any draw single line to any call solver_four

def solver_six(layout, location, neighbors = 0):            # Solver if remaining_num is 6
    neighbors = modify_neighbors(layout, location)

    # 3 neighbors  -  double line for each neighbor
    # 4 neighbors  -  1, any, any, any draw single line to 1 call solver_five  -  2, 2, 2, any draw single line to any call solver_five

def solver_seven(layout, location, neighbors = 0):          # Makes single lines for all directions, then calls solver_three
    neighbors = modify_neighbors(layout, location)

    connect(layout, location, neighbors[1], 1)
    connect(layout, location, neighbors[3], 1)
    connect(layout, location, neighbors[5], 1)
    connect(layout, location, neighbors[7], 1)

    solver_three(layout, location, neighbors)

def solver_eight(layout, location, neighbors = 0):          # Makes double lines for all directions
    neighbors = modify_neighbors(layout, location)

    connect(layout, location, neighbors[1], 2)
    connect(layout, location, neighbors[3], 2)
    connect(layout, location, neighbors[5], 2)
    connect(layout, location, neighbors[7], 2)

def assign_edges(layout):                       # Iterates through layout and sets edges
    for i in range(len(layout)):
        for j in range(len(layout[0])):
            if i == 0 or i == 1: layout[i][j].set_top_edge()
            elif i == len(layout) or i == (len(layout)-1): layout[i][j].set_bot_edge()
            if j == 0 or j == 1: layout[i][j].set_left_edge()  
            elif j == len(layout[0]) or j == (len(layout[0])-1): layout[i][j].set_right_edge()

def modify_neighbors(layout, current):           # Gives a list of neighbors with their remaining numbers and locations to the class object
    neighbors = []
    l, k = 0                        # cannot unpack non-iterable int object -------------------------------------------------------------------------------------------------------
    l, k = check_top(layout, current)
    neighbors.append(l)
    neighbors.append(k)
    l, k = check_bot(layout, current)
    neighbors.append(l)
    neighbors.append(k)
    l, k = check_left(layout, current)
    neighbors.append(l)
    neighbors.append(k)
    l, k = check_right(layout, current)
    neighbors.append(l)
    neighbors.append(k)
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
        return (0,"none")         # Returns none if no neighbors were found

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
        return (0,"none")         # Returns none if no neighbors were found

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
        return (0,"none")         # Returns none if no neighbors were found

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
        return (0,"none")         # Returns none if no neighbors were found

def connect(layout, current, target, amount):               # Connects current location and target location with either 1 or 2 lines
    i,j = current
    x,y = target

    if i == x:                              # If the rows are the same, draws a horizontal line
        if j > y:
            big = j
            small = y
        else:
            big = y
            small = j

        if amount == 1:                     # Single line
            for k in range(big-small):
                layout[i][k+small+1].set_one_hori_line()
            layout[i][j].remaining_num_decrement(1)
            layout[x][y].remaining_num_decrement(1)
        else:                               # Double line
            for k in range(big-small):
                layout[i][k+small+1].set_two_hori_line()
            layout[i][j].remaining_num_decrement(2)
            layout[x][y].remaining_num_decrement(2)

    elif j == y:                            # If the columns are the same, draws a vertical line
        if i > x:
            big = i
            small = x
        else:
            big = x
            small = i
            
        if amount == 1:                     # Single line
            for k in range(big-small):
                layout[k+small+1][j].set_one_vert_line()
            layout[i][j].remaining_num_decrement(1)
            layout[x][y].remaining_num_decrement(1)
        else:                               # Double line
            for k in range(big-small):
                layout[k+small+1][j].set_two_vert_line()
            layout[i][j].remaining_num_decrement(2)
            layout[x][y].remaining_num_decrement(2)

    else:                                   # Error message if rows or columns are not the same
        print("The rows or columns do not line up")

    return

if __name__ == "__main__":
    main()
