from maze import MazeArray, Cell
from collections import deque
import random

def create_maze(m=20, n=20, isRandom=False, hasWalls=True):
    if m < 1 or n < 1:
        raise Exception(f"Invalid Maze Size: {m}x{n}")

    if isRandom:
        m = random.randrange(1,m+1)
        n = random.randrange(1,n+1)
        
    return MazeArray(m, n, hasWalls)
    
# iterative implementation of DFS
def dfs(maze: MazeArray, *args):
    # initializing variables
    m, n = maze.m, maze.n
    visited: set(Cell) = set()

    # SUB METHODS START ------------------------------------------------------------------------
    # checks if starting DFS position has been provided, else, provides random position pos
    def check_args(args: list[int]) -> Cell: 
        if not args:
            pos = (random.randrange(n), random.randrange(m))
        elif len(args)==2:
            pos = (args[0], args[1])
        else:
            raise Exception(f"{len(args)} arguments given but only 0 or 2 accepted.")
        return maze.cell_at((pos[0], pos[1]))

    # a cell is valid when it is inside the grid and hasn't been visited
    def is_valid(cell: Cell | tuple) -> bool:
        if isinstance(cell, Cell):
            return 0 <= cell.x < n and 0 <= cell.y < m and cell not in visited
        elif isinstance(cell, tuple):
            return 0 <= cell[0] < n and 0 <= cell[1] < m and maze.cell_at((cell[0], cell[1])) not in visited

    # fills neighbors with valid maze Cells
    def get_valid_neighbors(cell: Cell) -> list[Cell]:
        unverified_neighbors = cell.get_neighbors()
        for i in range(4): # for four possible neighbors
            if is_valid(unverified_neighbors[i]):
                unverified_neighbors[i] = maze.cell_at((unverified_neighbors[i][0], unverified_neighbors[i][1]))
        return list(filter(lambda x: isinstance(x, Cell), unverified_neighbors)) # returns the list of validated neighbors
        
    # SUB METHODS END ---------------------------------------------------------------------------
    # adding in start position
    cell = check_args(args)
    visited.add(cell)
    stack: list[Cell] = [cell]

    while stack:
        visited.add(cell)
        neighbors = get_valid_neighbors(cell)
        if not neighbors:
            cell = stack.pop()
            continue
        nextCell = random.choice(neighbors)
        maze.remove_wall(cell, nextCell)
        stack.append(cell)
        cell = nextCell

def create_position(maze: MazeArray) -> Cell:
    return maze.cell_at((random.randrange(maze.n), random.randrange(maze.m)))
