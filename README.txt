Project 1 - Arthur Tran

Algorithm Description:
    This is more or less an implementation of Depth-First-Search. First the function takes the first location in the list of 
    possible locations. Then it would loop through all the words calling the function again with a smaller list of words and 
    possible locations and fills the board in with the word if it fits the location. This is repeated until a solution is found 
    (list of words is empty). It'll append the solved board to a list of solutions and backtrack to find another solution.

    1. If the list of words is empty, add the current board to list of solutions
    2. Take the first location from list of available locations
    3. Check every word from the list of words and see if it fits the location
    4. If it fits, insert the word into the board and go back to number 1 with a smaller list of words and locations

Pseudocode:
    solve(board[][], words[0..n-1], possibleLocations[0..n-1], solutions[0..])
        if length of words is 0:
            add board to solutions

        currentLocation <- possibleLocations[0]

        for i <- 0 to n - 1 do
            if words[i] fits in currentLocation
                solve(board, words[0..n-2], possibleLocations[1..n-1], solutions)

Recurrence Relation:
    S(n) = n * S(n - 1) + 1
         = n * [n * S(n - 2) + 1] + 1             = n^2 * S(n - 2) + n + 1
         = n^2 * [n * S(n - 3) + 1] + n + 1       = n^3 * S(n - 3) + n^2 + n + 1
         = n^3 * [n * S(n - 4) + 1] + n^2 + n + 1 = n^4 * S(n - 4) + n^3 + n^2 + n + 1

    S(n) = n^(i - 1) * S(n - i) + n^((i - 1)!) + 1

Time Complexity:
    S(n) = n^(i - 1) * S(n - i) + n^((i - 1)!)
    S(0) = 0
    let i = n

    S(n) = n^(n - 1) * S(n - n) + n^((n - 1)!) + 1
         = n^(n - 1) * 0 + n^((n - 1)!) + 1
         = n^((n - 1)!) + 1

    Big-Theta(n^((n - 1)!))