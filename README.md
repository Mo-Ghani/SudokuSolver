# SudokuSolver
Sudoku Solver for Sudoku puzzles with a unique solution

TO CREATE A PUZZLE:
  Add puzzles to the text file "p096_sudoku.txt".
  Each puzzle should take up 10 lines. The first line should be the title of the puzzle (e.g. "Grid 01").
  The next 9 lines should contain the 9 rows of the puzzle respectively. Each row contains 9 consecutive characters (1 for each column).
  If a cell is blank, it should take the value 0. Otherwise, it should take it's own value.
  
TO SOLVE THE PUZZLE:
  Run "Solver.py". This will search the puzzle cell by cell, and use logic to deduce as many cell values as possible. If logic is
  insufficient, then a "Guess and Test" algorithm is applied to recursively test possible solutions, until the puzzle is completed.
  At every step, an image of the in-progress grid is saved.
  
TO CREATE A VIDEO OF THE SOLVE:
  Run "videomaker.py". This sews the images saved by "Solver.py" into a single .avi video file. With default framerate settings, the video
  will be roughly 200x slower than real time.
  
The MP4 "Solve" shows the result of 50 puzzles being solved consecutively by this program.
