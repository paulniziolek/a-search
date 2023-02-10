from maze_generation import create_maze, dfs, create_position
from maze import MazeArray, Cell
import heapq
from collections import deque
from functools import lru_cache

def a_star(maze: MazeArray, start: Cell, end: Cell):
    m, n = maze.m, maze.n

    # manhattan distance heuristic from node to end
    @lru_cache()
    def heuristic(node: Cell) -> int:
        return abs(node.x-end.x)+abs(node.y-end.y)
    
    # a cell is valid when it is inside the grid
    def is_valid(cell: Cell | tuple) -> bool:
        if isinstance(cell, Cell):
            return 0 <= cell.x < n and 0 <= cell.y < m
        elif isinstance(cell, tuple):
            return 0 <= cell[0] < n and 0 <= cell[1] < m and maze.cell_at((cell[0], cell[1]))

    # fills neighbors with valid maze Cells
    # a neighbor is valid when it is inside the grid, directly next to its origin cell, and does not have a wall between its origin cell. 
    @lru_cache()
    def get_valid_neighbors(cell: Cell) -> list[Cell]:
        unverified_neighbors = cell.get_neighbors()
        for i in range(4): # four possible neighbors
            if is_valid(unverified_neighbors[i]):
                unverified_neighbors[i] = maze.cell_at((unverified_neighbors[i][0], unverified_neighbors[i][1]))
        unverified_neighbors = list(filter(lambda x: isinstance(x, Cell), unverified_neighbors))
        unverified_neighbors = list(filter(lambda x: not maze.wall_exists(x, cell), unverified_neighbors))
        #print(f"neighbors of {cell} are {unverified_neighbors}") # debugging neighbors
        return unverified_neighbors # returns the list of validated neighbors

    # A* Algorithm logic follows:
    closed_list = {} # hashmap with key=cell, and val=smallest f(n)
    path = {} # hashmap with key=currNode and val=prevNode, for pathing
    open_list: list[tuple(int, Cell)] = [(heuristic(start), start)] # will store cells in the open_list heap by tuple (h(n), n)
    open_list_set = set() # bruh
    heapq.heapify(open_list)

    while open_list:
        fn, node= heapq.heappop(open_list) # fn holds the evaluation result of node. to get g(n), you can subtract fn - heuristic(node).
        if node==end:
            break

        neighbors = get_valid_neighbors(node)
        # g(new n) = fn-heuristic(n)+1, AND h(new n) = heuristic(new n). 
        neighbors = list(map(lambda x: (fn-heuristic(node)+1+heuristic(x), x), neighbors)) # returns list of (f(new n), new n)

        closed_list[node] = fn

        # updating neighbors with closed/open lists
        for fN, neighbor in neighbors:
            if neighbor in closed_list:
                continue
            if neighbor not in open_list_set:
                open_list_set.add(neighbor)
                heapq.heappush(open_list, (fN, neighbor))
                path[neighbor] = node
        """
        # debugging
        print("open list:")
        print(open_list)
        print(closed_list)
        print(path)
        """
    print(f"Total expanded nodes (Closed List): {len(closed_list)}")
    print(f"Total visited nodes (Open List): {len(open_list)}")

    # creating path as list
    ptr: Cell = end
    realpath: list[Cell] = [ptr]
    while ptr != start:
        realpath.append(path[ptr])
        ptr = path[ptr]
    realpath.reverse()
    return realpath



