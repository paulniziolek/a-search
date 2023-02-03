from maze import MazeArray, Cell
from collections import deque
import random

def create_maze(m=4, n=4, isRandom=False):
    if m < 1 or n < 1:
        raise Exception(f"Invalid Maze Size: {m}x{n}")

    if isRandom:
        m = random.randrange(m)
        n = random.randrange(n)
        
    return MazeArray(m, n)
    
# iterative implementation of DFS
def dfs(maze, *args):
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

    # a node is valid when it is inside the grid and hasn't been visited
    def is_valid(node: Cell | tuple) -> bool:
        if isinstance(node, Cell):
            return 0 <= node.x < n and 0 <= node.y < m and node not in visited
        elif isinstance(node, tuple):
            return 0 <= node[0] < n and 0 <= node[1] < m and maze.cell_at((node[0], node[1])) not in visited

    # fills neighbors with valid maze Cells
    def get_valid_neighbors(cell: Cell) -> list[Cell]:
        unverified_neighbors = cell.get_neighbors()
        for i in range(4): # for four possible neighbors
            if is_valid(unverified_neighbors[i]):
                unverified_neighbors[i] = maze.cell_at((unverified_neighbors[i][0], unverified_neighbors[i][1]))
        return list(filter(lambda x: isinstance(x, Cell), unverified_neighbors)) # returns the list of validated neighbors
        

    # SUB METHODS END ---------------------------------------------------------------------------

    # adding in start position
    start = check_args(args)
    visited.add(start)
    stack: list[Cell] = [start]
    cell = start

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

# TESTING
myworld = create_maze()
print(myworld)
dfs(myworld)
print(myworld)

for cell in myworld.world[0]:
    print((cell.x, cell.y))
    print(cell.walls)


