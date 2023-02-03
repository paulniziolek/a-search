from maze import MazeArray, Cell
from collections import deque
import random

def create_maze(m=8, n=8, isRandom=False):
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
            pos = (random.randrange(m), random.randrange(n))
        elif len(args)==2:
            pos = (args[0], args[1])
        else:
            raise Exception(f"{len(args)} arguments given but only 0 or 2 accepted.")
        return maze.world[pos[0]][pos[1]]

    # a node is valid when it is inside the grid and hasn't been visited
    def is_valid(node: Cell | tuple) -> bool:
        if isinstance(node, Cell):
            return 0 <= node.x < n and 0 <= node.y < m and node not in visited
        elif isinstance(node, tuple):
            return 0 <= node[0] < n and 0 <= node[1] < m and maze.world[node[0]][node[1]] not in visited

    # fills neighbors with valid maze Cells
    def get_valid_neighbors(cell: Cell) -> list[Cell]:
        invalidated_neighbors = cell.get_neighbors()
        for i in range(len(invalidated_neighbors)): # technically equal to range(4)
            if is_valid(invalidated_neighbors[i]):
                invalidated_neighbors[i] = maze.world[invalidated_neighbors[i][0]][invalidated_neighbors[i][1]]
        return list(filter(lambda x: isinstance(x, Cell), invalidated_neighbors)) # returns the list of validated neighbors
        

    # SUB METHODS END ---------------------------------------------------------------------------

    # adding in start position
    start = check_args(args)
    visited.add(start)
    stack: list[Cell] = [start]
    

    while stack:
        cell = stack.pop()
        visited.add(cell)
        neighbors = get_valid_neighbors(cell)
        random.shuffle(neighbors)

        # logic here
        if len(neighbors)==1:
            maze.remove_wall(cell, neighbors[-1])
        elif len(neighbors)>1:
            for i in range(len(neighbors[:-1])):
                #remove = random.getrandbits(1)
                remove = 1
                if remove==1:
                    maze.remove_wall(cell, neighbors[i])
            maze.remove_wall(cell, neighbors[-1])
        else:
            print(cell)
        
        stack.extend(neighbors)
        for i in neighbors:
            visited.add(i)
        #print(maze)
    


    print(len(visited))

 
myworld = create_maze()
print(myworld)
dfs(myworld)
print(myworld)