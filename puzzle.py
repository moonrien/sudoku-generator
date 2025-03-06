import numpy as np
import random
import matplotlib.pyplot as plt


grid = np.zeros((9, 9), dtype=int)  #Generate a grid filled with zeros


def is_valid(grid, row, col, num):  #Check if a number can be placed in a given cell
    if num in grid[row, :]:
        return False

    if num in grid[:, col]:
        return False

    start_row = (row // 3) * 3  #Check the 3x3 square
    start_col = (col // 3) * 3
    if num in grid[start_row:start_row+3, start_col:start_col+3]:
        return False

    return True


def generate_solution(grid):  #Recursively generate a fully solved Sudoku board
    for row in range(9):
        for col in range(9):
            if grid[row, col] == 0:
                numbers = random.sample(range(1, 10), 9)  #Try random numbers
                for num in numbers:
                    if is_valid(grid, row, col, num):
                        grid[row, col] = num
                        if generate_solution(grid):
                            return True
                        grid[row, col] = 0
                return False
    return True


def has_unique_solution(grid):  #Check if there is only one solution
    copy_grid = np.copy(grid)
    return count_solutions(copy_grid, 0) == 1


def count_solutions(grid, count):  #Count all possible solutions for the grid
    for row in range(9):
        for col in range(9):
            if grid[row, col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row, col] = num
                        count += count_solutions(grid, count)
                        if count > 1:
                            return count
                        grid[row, col] = 0
                return count
    return count + 1


def generate_puzzle(grid):  #Remove numbers to create a Sudoku puzzle with a unique solution
    cells = [(i, j) for i in range(9) for j in range(9)]
    for row, col in cells:
        temp = grid[row, col]
        grid[row, col] = 0
        if not has_unique_solution(grid):
            grid[row, col] = temp
    return grid


def display_sudoku(grid):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xticks(np.arange(10) - 0.5, minor=False)
    ax.set_yticks(np.arange(10) - 0.5, minor=False)
    ax.grid(which="major", color='black', linestyle='-', linewidth=2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(which='both', bottom=False, left=False)

    for i in range(1, 3):
        ax.axhline(i * 3 - 0.5, color='black', linewidth=4)
        ax.axvline(i * 3 - 0.5, color='black', linewidth=4)
  
    for i in range(9):
        for j in range(9):
            if grid[i, j] != 0:
                ax.text(j, i, str(grid[i, j]), ha='center', va='center', fontsize=14)
    
    plt.gca().invert_yaxis()
    plt.show()


generate_solution(grid)
sudoku_puzzle = generate_puzzle(grid)

print("Here is your Sudoku puzzle:")
display_sudoku(sudoku_puzzle)
