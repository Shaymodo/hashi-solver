from multiprocessing import Value
import sys


class PuzzleDigit:                              # Class for each puzzle number that isn't 0
    def __init__(self, num):
        self.full_num = num                     # Initialize the actual number
        self.remaining_num = num                # Initialize the number counting down for each line drawn

    def done(self):                             # Returns True if all the lines drawn for this number
        return self.remaining_num == 0

    def number(self):                           # Returns the int value of the full_num
        return self.full_num

    def add_horizontal(self):
        pass

    def add_vertical(self):
        pass


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
                        print (f"{layout[i][j].number()}", end=" ")
                    print("]")
            else:
                print("Current puzzle is not valid")

        elif choice == 4:                   # Solve current puzzle
            if layout != []:
                solver(layout, num_total)
            else:                           # If layout is empty, puzzle does not exist
                print("No current puzzle")

        elif choice == 5:                   # Quit
            sys.exit()

        else:                               # Error message for invalid input
            print("Not a valid choice")

        print()


def manual_layout_input(width, height):     # Iterates through the 2D array and asks for user input for each value
    layout = []                             # Creates empty row and column arrays
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
                        valid_digit = PuzzleDigit(num)
                        layout_inner.append(valid_digit)        # Adds object with valid digit to the row
                        print("[", end=" ")
                        for k in range (len(layout_inner)):     # Displays row for user to see
                            print (f"{layout_inner[k].number()}", end=" ")
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
    lined_layout = layout
    while not solved:                               # Loops until puzzle is solved
        finished_nums = 0
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                if (layout[i][j].done()):                  # Checks object to see if all lines are drawn
                    finished_nums += 1
                else:
                    print(layout[i][j].done())     #TEMP
                    num = layout[i][j].number()
                    if num == 1:
                        lined_layout = solver_one(lined_layout)
                    elif num == 2:
                        lined_layout = solver_two(lined_layout)
                    elif num == 3:
                        lined_layout = solver_three(lined_layout)
                    elif num == 4:
                        lined_layout = solver_four(lined_layout)
                    elif num == 5:
                        lined_layout = solver_five(lined_layout)
                    elif num == 6:
                        lined_layout = solver_six(lined_layout)
                    elif num == 7:
                        lined_layout = solver_seven(lined_layout)
                    elif num == 8:
                        lined_layout = solver_eight(lined_layout)

        if finished_nums == num_total:
            solved = True                               # Ends the loop

        solved = True                           # TEMPORARY TO PREVENT INFINITE LOOPING
    return

def solver_one(layout):
    pass

def solver_two(layout):
    pass

def solver_three(layout):
    pass

def solver_four(layout):
    pass

def solver_five(layout):
    pass

def solver_six(layout):
    pass

def solver_seven(layout):
    pass

def solver_eight(layout):
    pass

def check_neighbor(layout):
    pass


if __name__ == "__main__":
    main()
