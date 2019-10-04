'''
Project 1 - CS157

Author: Arthur Tran
Date: 10-3-2019

As for what I would be counting as the basic operation, I think that counting the method 'canGoInLocation' as the basic operation
is a good idea. However within this method/function, there are multiple checks and a for loop going through each spot in the 
cooresponding location in the grid. So theoretically, if we were to count the basic operation as each comparison, the number
would be significantly higher.
'''

from copy import deepcopy 
import time
import os

basicOperations = 0 # holds how many basic operations are being performed

# Function: loadGrid
# Description: Given a filename, loads the puzzle into a matrix with each index of the list holding a row/line.
# Parameters: filename - the filename containing the puzzle and words
# Returns: a list containing each row of the puzzle in list format
def loadGrid(filename):
    grid = []

    for line in open(filename):
        if '.' in line or '*' in line: # checks whether or not the line is part of the puzzle
            grid.append(list(line.strip())) # converts the line into a list of chars and appends the list into the grid list

    return grid

# Function: printGrid
# Description: Helper method for printing the matrix in a good looking format
# Parameters: grid - the matrix containing the grid/puzzle
# Returns: none
def printGrid(grid):
    for line in grid:
        print(''.join(line))

# Function: getWords
# Description: Given a filename, extracts the words at the bottom of the file into a list.
# Parameters: filename - the filename containing the puzzle and words
# Returns: a list containing all the words at the bottom of the file
def getWords(filename):
    words = []

    for line in open(filename):
        if not ('*' in line or '.' in line): # checks that the line isn't part of the puzzle
            words.append(line.strip()) # ensures that there is no whitespace or newline at the end of the word
    
    return words

# Function: fillWord
# Description: Given a word and a location, fills in the spaces in the cooresponding grid with the letters of the word
#              Ex: ..***... -> ..cat...
# Parameters: grid - the grid/matrix that the word goes into
#             word - the word to be implanted into the grid/matrix
#             location - the location on the grid that the word is to be put into
# Returns: a copy of the grid with the word added to it
def fillWord(grid, word, location):
    newGrid = deepcopy(grid) # Python passes lists by reference so this ensures that the original grid/matrix isn't changed

    for i in range(len(word)):
        if location[3]: # verticle
            newGrid[location[0] + i][location[1]] = word[i]
        else:
            newGrid[location[0]][location[1] + i] = word[i]

    return newGrid

# Function: getWordLocations
# Description: Given the grid/matrix containing the puzzle, this function looks for every possible place that a word could go and 
#              stores it into a list of tuples with this format: [(row, col, length, isHorizontal)]
# Parameters: grid - the grid/matrix that contains the empty puzzle
# Returns: a list of tuples 
def getWordLocations(grid):
    locations = [] # holds a list of tuples that contain (row, col, length, isHorizontal) of each word space
    
    # finds all the possible horizontal word locations
    length = 0 # current length of the word location
    coordinateX = 0 
    coordinateY = 0

    for x, line in enumerate(grid): # for every row
        length = 0
        for y, char in enumerate(line): # for every column
            if char == '*':
                # if the length is 0 so far, this means that this is the start of a word location
                if length == 0: 
                    coordinateX = x
                    coordinateY = y
                length += 1

            if char == '.':
                # if there is a '.' and the length is > 1, this means that this is the end of a word location
                if length > 1:
                    locations.append((coordinateX, coordinateY, length, False)) # adds the word location to the list
                length = 0

        if length > 1: # adds the final word location to the list when it reaches the end of the line
            locations.append((coordinateX, coordinateY, length, False))

    # finds all the possible verticle word locations
    for i in range(len(grid[0])): # for every column
        length = 0
        for j in range(len(grid)): # for every row
            if grid[j][i] == '*':
                # if the length is 0 so far, this means that this is the start of a word location
                if length == 0:
                    coordinateX = j
                    coordinateY = i
                length += 1

            if grid[j][i] == '.':
                # if there is a '.' and the length is > 1, this means that this is the end of a word location
                if length > 1:
                    locations.append((coordinateX, coordinateY, length, True)) # adds the word location to the list
                length = 0
            
        if length > 1: # adds the final word location to the list when it reaches the bottom of the column
            locations.append((coordinateX, coordinateY, length, True))

    return locations

# Function: canGoInLocation
# Description: Given a word and a location, checks if the word will fit in there
# Parameters: grid - the grid/matrix that the word would be put into
#             word - the word to check for placeability
#             location - the location on the grid that the word is supposed to go into
# Returns: True if the word can fit, False otherwise
def canGoInLocation(grid, word, location):
    for i in range(len(word)):
        if location[3]: # verticle
            # checks if each spot is empty ('*') or is the same letter as the word
            if grid[location[0] + i][location[1]] != word[i] and grid[location[0] + i][location[1]] != '*':
                return False
        else:
            # checks if each spot is empty ('*') or is the same letter as the word
            if grid[location[0]][location[1] + i] != word[i] and grid[location[0]][location[1] + i] != '*':
                return False

    return len(word) == location[2] # makes sure the word is the right length

# Function: solve
# Description: Utilizes depth-first-search to solve the puzzle if there is a solution.
# Parameters: grid - the current grid/matrix
#             words - the list of words
#             wordLocations - the list of all possible word locations
#             solutions - a list holding the finished board solutions
# Returns: none
def solve(grid, words, wordLocations, solutions):
    if len(words) == 0: # board is solved
        solutions.append(grid) # adds solution into the list of solutions
        return

    else:
        location = wordLocations[0] # picks a starting word location to start the tree

        for word in words:
            # debugPrint(grid, words, wordLocations, word, location)

            if canGoInLocation(grid, word, location): # if there is a word that fits the location
                global basicOperations
                basicOperations += 1

                tempWords = words[:] # creates a copy of the word list
                tempWords.remove(word) # removes the word that's going to be inserted into the board

                # solve the board with the newly added word and a smaller list of words and word locations
                solve(fillWord(grid, word, location), tempWords, wordLocations[1:], solutions) 

        return

# Function: debugPrint
# Description: Helper function to help visualize the call stack. Prints out the current grid, the current word, the location,
#              the list of words, and the list of word locations.
# Parameters: grid - the current grid
#             words - the list of words
#             wordLocations - the list of word locations
#             word - the current word being checked
#             location - the current location being checked
# Returns: none
def debugPrint(grid, words, wordLocations, word, location):
    printGrid(grid)
    print(word, end = " ")
    print(location)
    print(words, end = " ")
    print(wordLocations)

def main():
    # Loops until the user terminates the program with Ctrl+C (Windows)
    while True:
        global basicOperations
        basicOperations = 0

        puzzle = "puzzles/"

        # lists every possible puzzle in the folder puzzles
        allPuzzles = os.listdir("puzzles")
        print(allPuzzles)

        usrInput = input("Which puzzle do you want to run?: ")

        # loops until the user enters a valid puzzle
        while not (usrInput in allPuzzles):
            usrInput = input("Sorry that is not a valid puzzle. Enter another: ")

        puzzle += usrInput # appends the filename to the folder name constructing the full pathname

        #sets up the variables for solving the puzzle
        words = getWords(puzzle)
        grid = loadGrid(puzzle)
        wordLocations = getWordLocations(grid)
        solutions = []

        startTime = time.time() # holds the current time since epoch to be used to see how much time has passed 

        solve(grid, words, wordLocations, solutions)

        endTime = time.time() # holds the current time since epoch to be used to see how much time has passed 

        if len(solutions) == 0: print("There were no solutions to this puzzle\n")
        else:
            for solNumber, solution in enumerate(solutions):
                print("Solution %d" % (solNumber + 1))
                printGrid(solution)
                print("")

        print("This puzzle took %f seconds to solve" % (endTime - startTime), "with %s basic operations\n" % basicOperations)

if __name__ == "__main__":
    main()