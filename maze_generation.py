from maze import MazeArray
from collections import deque
import random

def create_maze(m=20, n=20, isRandom=False):
    if isRandom:
        m = random.randrange(m+1)
        n = random.randrange(n+1)
    return MazeArray(m, n)



def dfs(maze):
    

    pass
    
    

myworld = create_maze()
print(myworld)




