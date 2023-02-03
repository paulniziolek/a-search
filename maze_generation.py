from maze import MazeArray, Cell
from collections import deque
import random

def create_maze(m=20, n=20, isRandom=False):
    if m < 1 or n < 1:
        raise Exception(f"Invalid Maze Size: {m}x{n}")

    if isRandom:
        m = random.randrange(m)
        n = random.randrange(n)
        
    return MazeArray(m, n)
    
# iterative implementation of DFS
def dfs(maze, *args):

    # SUB METHODS START ------------------------------------------------------------------------
    m, n = maze.m, maze.n
    # checks if starting DFS position has been provided, else, provides random position pos
    def check_args(args: list[int]) -> tuple: 
        if not args:
            pos = (random.randrange(m), random.randrange(n))
        elif len(args)==2:
            pos = (args[0], args[1])
        else:
            raise Exception(f"{len(args)} arguments given but only 0 or 2 accepted.")
        return pos

    # a node is valid when it is inside the grid and hasn't been visited
    def is_valid(node: Cell) -> bool:
        return 0 <= node.x < n and 0 <= node.y < m and node.get_pos() not in visited
    # SUB METHODS END ---------------------------------------------------------------------------
    pos = check_args(args)
    visited = set(pos)
    print(is_valid())
    stack = [pos]
    while stack:
        cell = stack.pop()



        



myworld = create_maze()
print(myworld)


