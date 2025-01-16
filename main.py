from multiprocessing import Value
import sys

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
        print("\033[H\033[J")  # Clears the screen and moves the cursor to the top-left corner


        if choice == 1:                 # Manual Entry
            try:
                while height < 4: height = int(input("Please enter the height of the puzzle: "))
                while width < 4: width = int(input("Please enter the width of the puzzle: "))
            except ValueError:
                print("Input a valid integer")
                print()
                break
            layout = manual_layout_input(width, height)

        elif choice == 2:               # Automatic Entry
            print("This isn't implemented yet, I just told you that")
            print()

        elif choice == 3:               # View current puzzle
            if layout != []:
                for i in range(height):
                    print(layout[i])
                    print()
            else:
                print("Current puzzle is not valid")
                print()

        elif choice == 4:               # Solve current puzzle
            if layout != []:
                solver(layout)
            else:
                print("Current puzzle is not valid")
                print()

        elif choice == 5:               # Quit
            sys.exit()

        else:                           # Error message for invalid input
            print("Not a valid choice")


def manual_layout_input(width, height):     # Iterates through the 2D array and asks for user input for each value
    layout = []           # Creates empty row and column arrays
    for i in range (height):
        layout_inner = []
        print()
        print (f"Row {i+1}")
        for j in range (width):
            while True:
                try:                        # Ensure input is an int
                    val = int(input("Please input the next number 0-8, enter 0 if empty: "))
                    if val < 0 or val > 8:
                        print("Not between 0 and 8, try again")
                    else:
                        layout_inner.append(val)        # Adds valid value to the row
                        print(layout_inner)             # Displays row for user to see
                        break
                except ValueError:
                    print("Your input was not an integer, try again")

        layout.append(layout_inner)                 # Adds each row here
                    
    return layout

def solver(layout):                         # Calls solver helper functions depending on the value of each number in the layout
    solved = False
    while not solved:                               # Loops until puzzle is solved
        for i in range(len(layout)):
            for j in range(len(layout[i])):
                num = layout[i][j]
        solved = True                               # Ends the loop  

    pass

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