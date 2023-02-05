from maze import MazeArray, Cell
from collections import deque
from typing import Generator, List, Optional, Set, Tuple
import random

random.seed(0)

def create_maze(m=20, n=20, isRandom=False, hasWalls=True):
    if m < 1 or n < 1:
        raise Exception(f"Invalid Maze Size: {m}x{n}")

    if isRandom:
        m = random.randrange(1,m+1)
        n = random.randrange(1,n+1)
        
    return MazeArray(m, n, hasWalls)
    
# iterative implementation of DFS
def dfs(maze: MazeArray, x: Optional[int] = None, y: Optional[int] = None):
    # initializing variables
    m, n = maze.m, maze.n
    visited: Set[Tuple[int, int]] = set()

    # SUB METHODS START ------------------------------------------------------------------------
    # checks if starting DFS position has been provided, else, provides random position pos
    def check_args(x: Optional[int], y: Optional[int]) -> Cell: 
        if (x == None) != (y == None):
            raise Exception(f"x and y must be both None or both not None; received {x} and {y}.")
        x, y = random.randrange(n) if x is None else x, random.randrange(m) if y is None else y
        return maze.world[x][y]

    # a position is valid when it is inside the grid and hasn't been visited
    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < n and 0 <= y < m and (x, y) not in visited

    # fills neighbors with valid maze Cells
    def get_valid_neighbors(cell: Cell) -> Generator[Cell, None, None]:
        for dx, dy in ((0,-1), (0,1), (-1, 0), (1, 0)):  # for four possible neighbors
            if is_valid(cell.x + dx, cell.y + dy):
                yield maze.world[cell.x + dx][cell.y + dy]
        
    # SUB METHODS END ---------------------------------------------------------------------------
    # adding in start position
    cell = check_args(x, y)
    cell.blocked = False
    visited.add((cell.x, cell.y))
    stack: List[Cell] = [cell]
    iters = 0
    while stack:
        # print(stack)
        neighbors = tuple(get_valid_neighbors(stack[-1]))
        if not neighbors:
            stack.pop()
            continue
        next_cell = random.choice(neighbors)
        visited.add((next_cell.x, next_cell.y))
        next_cell.blocked = random.uniform(0, 1) < 0.3
        stack.append(next_cell)
        iters += 1
        # if iters == 6:
        #     exit(0)

def rand_position(maze: MazeArray, unallowed: Optional[Cell] = None) -> Cell:
    x, y = random.randrange(maze.n), random.randrange(maze.m)
    while maze.world[x][y].blocked or maze.world[x][y] == unallowed:
        x, y = random.randrange(maze.n), random.randrange(maze.m)
    return maze.world[x][y]
